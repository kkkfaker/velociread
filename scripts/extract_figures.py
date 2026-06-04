#!/usr/bin/env python3
"""
paper-anatomist PDF Figure Extractor
从 PDF 中提取内嵌图片，按页码范围过滤，自动命名。

Usage:
    python extract_figures.py <input_pdf> [--output-dir <dir>] [--min-size-kb <kb>] [--prefix <prefix>]

输出文件名格式: {prefix}_fig{序号}.{ext}
"""

import argparse
import sys
from pathlib import Path

try:
    import fitz
except ImportError:
    print("错误: 需要安装 pymupdf。运行: pip install pymupdf")
    sys.exit(1)


def extract_figures(
    pdf_path: Path,
    output_dir: Path,
    prefix: str = "Figure",
    min_size_kb: int = 30,
    pages: list[int] | None = None,
) -> list[dict]:
    """
    Extract embedded images from PDF.

    Args:
        pdf_path: Path to PDF file
        output_dir: Directory to save extracted images
        prefix: Filename prefix for saved images
        min_size_kb: Minimum file size in KB to keep (filters small icons/logos)
        pages: Specific pages to extract from (None = all pages)

    Returns:
        List of dicts with keys: filename, page, width, height, size_kb
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf_path))
    extracted = []
    img_counter = 0
    skipped_small = 0

    for page_num in range(len(doc)):
        if pages and page_num not in [p - 1 for p in pages]:
            continue

        page = doc[page_num]
        image_list = page.get_images(full=True)

        for img_idx, img_info in enumerate(image_list):
            xref = img_info[0]
            try:
                base_image = doc.extract_image(xref)
            except Exception as e:
                print(f"  ⚠ 无法提取图片 xref={xref} (P.{page_num+1}): {e}")
                continue

            image_bytes = base_image["image"]
            size_kb = len(image_bytes) / 1024
            width = base_image.get("width", 0)
            height = base_image.get("height", 0)
            ext = base_image.get("ext", "png")

            # Filter: skip small images (icons, logos)
            if size_kb < min_size_kb:
                skipped_small += 1
                continue

            # Filter: skip very small images (< 100px in both dimensions)
            if width < 100 and height < 100:
                skipped_small += 1
                continue

            img_counter += 1
            filename = f"{prefix}_fig{img_counter:02d}.{ext}"
            filepath = output_dir / filename

            with open(filepath, "wb") as f:
                f.write(image_bytes)

            extracted.append({
                "filename": filename,
                "filepath": str(filepath),
                "page": page_num + 1,
                "width": width,
                "height": height,
                "size_kb": round(size_kb, 1),
                "ext": ext,
            })

    doc.close()

    if skipped_small:
        print(f"  ℹ  {skipped_small} 张小图片已过滤（< {min_size_kb}KB）")

    return extracted


def print_summary(extracted: list[dict], output_dir: Path) -> None:
    """Print a summary of extracted figures."""
    if not extracted:
        print("  ⚠ 未提取到图片（检查 min_size_kb 阈值或 PDF 是否为扫描版）")
        return

    print(f"\n📊 提取结果 ({len(extracted)} 张):")
    print(f"{'文件名':<30} {'页码':<6} {'尺寸':<15} {'大小':<10}")
    print("-" * 61)

    for img in extracted:
        dims = f"{img['width']}×{img['height']}"
        size = f"{img['size_kb']}KB"
        print(f"{img['filename']:<30} P.{img['page']:<4}  {dims:<15} {size:<10}")

    total_size = sum(img["size_kb"] for img in extracted)
    print(f"\n  总计: {total_size:.0f} KB | 目录: {output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="小绿鲸精读 PDF 图表提取器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python extract_figures.py paper.pdf --output-dir figures/ --prefix Chen2025
  python extract_figures.py paper.pdf --min-size-kb 50 --pages 3-10
        """,
    )
    parser.add_argument("input_pdf", help="输入 PDF 文件路径")
    parser.add_argument("--output-dir", "-d", default="figures", help="输出目录 (默认: figures/)")
    parser.add_argument(
        "--prefix", "-p", default="Figure", help="文件名前缀，如 Author2025 (默认: Figure)"
    )
    parser.add_argument(
        "--min-size-kb", "-m", type=int, default=30, help="最小图片尺寸 (KB) (默认: 30)"
    )
    parser.add_argument(
        "--pages", "-r",
        help="只提取指定页码，如 '1-5' 或 '3,7,10' (默认: 全部)",
    )

    args = parser.parse_args()

    input_path = Path(args.input_pdf)
    if not input_path.exists():
        print(f"错误: 找不到文件 {args.input_pdf}")
        sys.exit(1)

    output_dir = Path(args.output_dir)

    # Parse pages argument
    page_list = None
    if args.pages:
        page_list = []
        for part in args.pages.split(","):
            part = part.strip()
            if "-" in part:
                start, end = part.split("-", 1)
                page_list.extend(range(int(start), int(end) + 1))
            else:
                page_list.append(int(part))

    print(f"📄 打开 PDF: {input_path}")
    print(f"🔍 提取图片 (最小 {args.min_size_kb}KB)...")

    extracted = extract_figures(
        pdf_path=input_path,
        output_dir=output_dir,
        prefix=args.prefix,
        min_size_kb=args.min_size_kb,
        pages=page_list,
    )

    print_summary(extracted, output_dir)

    if extracted:
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
