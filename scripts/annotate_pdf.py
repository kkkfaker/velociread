#!/usr/bin/env python3
"""
paper-anatomist PDF Annotation Engine
基于 pymupdf 的 PDF 批注叠加工具，支持高亮、便签批注和层级书签。

Usage:
    python annotate_pdf.py <input_pdf> <annotations.json> [--output <output_pdf>]

annotations.json format:
{
    "highlights": [
        {"page": 2, "text": "sentence to highlight", "color": "red", "label": "核心观点"}
    ],
    "sticky_notes": [
        {"page": 3, "x": 100, "y": 200, "content": "术语: OER → 析氧反应", "color": "yellow"}
    ],
    "toc": [
        [1, "Introduction", 3],
        [2, "Results", 5]
    ]
}

Colors: red=(1,0,0), blue=(0,0,1), green=(0,0.6,0), yellow=(1,1,0)
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import fitz
except ImportError:
    print("错误: 需要安装 pymupdf。运行: pip install pymupdf")
    sys.exit(1)


COLOR_MAP = {
    "red": (1.0, 0.55, 0.55),
    "blue": (0.55, 0.65, 1.0),
    "green": (0.4, 0.8, 0.5),
    "purple": (0.55, 0.4, 0.9),
    "yellow": (1.0, 1.0, 0.55),
    "orange": (1.0, 0.75, 0.5),
}


def _normalize_text(text: str) -> str:
    """Normalize text for fuzzy matching: fix ligatures, collapse whitespace, strip special chars."""
    import unicodedata
    # Fix common PDF ligatures
    ligatures = {
        'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬀ': 'ff', 'ﬃ': 'ffi', 'ﬄ': 'ffl',
        '–': '-', '—': '--', '‘': "'", '’': "'",
        '“': '"', '”': '"', ' ': ' ', '­': '',
    }
    for old, new in ligatures.items():
        text = text.replace(old, new)
    # Collapse whitespace
    text = ' '.join(text.split())
    return text


def _search_page_fuzzy(page, text: str):
    """Multi-strategy text search on a PDF page. Returns quads or None."""
    # Strategy 1: exact match
    quads = page.search_for(text)
    if quads:
        return quads

    # Strategy 2: normalize and search
    norm = _normalize_text(text)
    quads = page.search_for(norm)
    if quads:
        return quads

    # Strategy 3: search with first meaningful sentence (up to 120 chars)
    for cutoff in [120, 90, 60]:
        short = norm[:cutoff].rsplit(' ', 1)[0]  # cut at word boundary
        quads = page.search_for(short)
        if quads:
            return quads

    # Strategy 4: search for most distinctive 4-5 word phrase
    words = norm.split()
    if len(words) >= 6:
        # Try middle portion (often most distinctive)
        mid_start = len(words) // 4
        for phrase_len in [5, 4, 3]:
            phrase = ' '.join(words[mid_start:mid_start + phrase_len])
            quads = page.search_for(phrase)
            if quads:
                return quads

    # Strategy 5: try regex with flexible whitespace
    import re
    regex = r'\s+'.join(re.escape(w) for w in norm.split()[:6])
    try:
        quads = page.search_for(regex, regex=True)
        if quads:
            return quads
    except Exception:
        pass

    return None


def add_highlights(doc: fitz.Document, highlights: list[dict]) -> int:
    """Add highlight annotations to the PDF. Returns count of highlights added.

    Uses multi-strategy fuzzy matching to maximize hit rate (target: 90%+).
    """
    count = 0
    skipped = 0

    for item in highlights:
        page_num = item["page"] - 1
        if page_num < 0 or page_num >= len(doc):
            print(f"  ⚠ 跳过: 页码 {item['page']} 超出范围")
            skipped += 1
            continue

        page = doc[page_num]
        text = item["text"]
        color = COLOR_MAP.get(item.get("color", "red"), COLOR_MAP["red"])

        quads = _search_page_fuzzy(page, text)
        if not quads:
            # Last resort: search adjacent pages (text might be near page boundary)
            found = False
            for adj in [page_num - 1, page_num + 1]:
                if 0 <= adj < len(doc):
                    quads = _search_page_fuzzy(doc[adj], text)
                    if quads:
                        page = doc[adj]
                        found = True
                        print(f"  🔄 在P.{adj+1}找到: \"{text[:40]}...\"")
                        break
            if not found:
                print(f"  ⚠ 未找到: \"{text[:60]}...\" (P.{page_num+1})")
                skipped += 1
                continue

        for quad in quads[:3]:  # max 3 quads to avoid over-highlighting
            annot = page.add_highlight_annot(quad)
            annot.set_colors(stroke=color)
            annot.set_info(title=item.get("label", ""))
            annot.update()
            count += 1

    rate = 100 * count / (count + skipped) if (count + skipped) > 0 else 0
    print(f"  📊 命中率: {count}/{count+skipped} ({rate:.0f}%)")
    return count


def add_sticky_notes(doc: fitz.Document, notes: list[dict]) -> int:
    """Add sticky note annotations to the PDF. Returns count of notes added."""
    count = 0

    for item in notes:
        page_num = item["page"] - 1
        if page_num < 0 or page_num >= len(doc):
            print(f"  ⚠ 跳过: 页码 {item['page']} 超出范围")
            continue

        page = doc[page_num]
        x = item.get("x", 50)
        y = item.get("y", 50)
        content = item.get("content", "")
        color = COLOR_MAP.get(item.get("color", "yellow"), COLOR_MAP["yellow"])

        point = fitz.Point(x, y)
        annot = page.add_text_annot(point, content, icon="Note")
        annot.set_colors(stroke=color)
        annot.set_info(title=item.get("label", ""))
        annot.update()
        count += 1

    return count


def add_figure_notes_from_positions(doc: fitz.Document, figure_notes: list[dict]) -> int:
    """Add sticky notes near figure/table captions.

    Each figure_note entry should have:
    - page: page number (1-indexed)
    - caption_text: text of the figure/table caption to search for
    - content: sticky note content
    - color: optional, default yellow
    """
    count = 0

    for item in figure_notes:
        page_num = item["page"] - 1
        if page_num < 0 or page_num >= len(doc):
            continue

        page = doc[page_num]
        caption = item.get("caption_text", "")

        # Find caption position and place note nearby
        quads = page.search_for(caption[:60])
        if quads:
            # Place note 10pt above the caption
            rect = quads[0]
            point = fitz.Point(rect.x0, rect.y0 - 10)
        else:
            # Fallback: place at default position on the right side
            point = fitz.Point(400, 100)

        content = item.get("content", "")
        color = COLOR_MAP.get(item.get("color", "yellow"), COLOR_MAP["yellow"])

        annot = page.add_text_annot(point, content, icon="Note")
        annot.set_colors(stroke=color)
        annot.update()
        count += 1

    return count


def set_bookmarks(doc: fitz.Document, toc: list) -> bool:
    """Set hierarchical bookmarks (Table of Contents) for the PDF.

    toc format: nested list like [level, "title", page_number]
    Example: [[1, "Introduction", 1], [2, "Background", 1], [1, "Results", 5]]
    """
    try:
        doc.set_toc(toc)
        return True
    except Exception as e:
        print(f"  ⚠ 设置书签失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="小绿鲸精读 PDF 批注引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python annotate_pdf.py paper.pdf annotations.json
  python annotate_pdf.py paper.pdf annotations.json --output paper-annotated.pdf
        """,
    )
    parser.add_argument("input_pdf", help="输入 PDF 文件路径")
    parser.add_argument("annotations", help="批注配置文件 (JSON)")
    parser.add_argument("--output", "-o", help="输出 PDF 路径（默认: {name}-annotated.pdf）")
    parser.add_argument("--dry-run", action="store_true", help="只检查不保存")

    args = parser.parse_args()

    # Validate input
    input_path = Path(args.input_pdf)
    if not input_path.exists():
        print(f"错误: 找不到文件 {args.input_pdf}")
        sys.exit(1)

    # Set output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.parent / f"{input_path.stem}-annotated.pdf"

    # Load annotations
    annot_path = Path(args.annotations)
    if not annot_path.exists():
        print(f"错误: 找不到批注文件 {args.annotations}")
        sys.exit(1)

    with open(annot_path, "r", encoding="utf-8") as f:
        ann_data = json.load(f)

    # Process
    print(f"📄 打开 PDF: {input_path}")
    doc = fitz.open(str(input_path))
    total_pages = len(doc)

    try:
        # 1. Highlights
        highlights = ann_data.get("highlights", [])
        if highlights:
            print(f"🔴 添加高亮 ({len(highlights)} 条)...")
            hl_count = add_highlights(doc, highlights)
            print(f"  ✅ {hl_count} 条高亮已添加")
        else:
            print("🔴 无高亮批注")

        # 2. Sticky notes (general)
        notes = ann_data.get("sticky_notes", [])
        if notes:
            print(f"💛 添加便签批注 ({len(notes)} 条)...")
            sn_count = add_sticky_notes(doc, notes)
            print(f"  ✅ {sn_count} 条便签已添加")
        else:
            print("💛 无便签批注")

        # 3. Figure/table notes
        fig_notes = ann_data.get("figure_notes", [])
        if fig_notes:
            print(f"📊 添加图表批注 ({len(fig_notes)} 条)...")
            fn_count = add_figure_notes_from_positions(doc, fig_notes)
            print(f"  ✅ {fn_count} 条图表批注已添加")
        else:
            print("📊 无图表批注")

        # 4. Bookmarks
        toc = ann_data.get("toc", [])
        if toc:
            print(f"📑 设置层级书签 ({len(toc)} 条)...")
            if set_bookmarks(doc, toc):
                print(f"  ✅ 书签已设置")
        else:
            print("📑 无书签配置")

        # Save
        if not args.dry_run:
            print(f"\n💾 保存至: {output_path}")
            doc.save(str(output_path), incremental=False, deflate=True)
            file_size = output_path.stat().st_size / 1024
            print(f"✅ 完成! 文件大小: {file_size:.1f} KB")
        else:
            print("\n🔍 干跑模式 — 未保存更改")

    finally:
        doc.close()


if __name__ == "__main__":
    main()
