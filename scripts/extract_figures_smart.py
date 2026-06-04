#!/usr/bin/env python3
"""
paper-anatomist Smart Figure Extractor
Maps extracted images to paper figure numbers by detecting "Figure N" text on pages.
Renders vector-only figures (no embedded raster) as high-res PNGs.

Usage:
    python extract_figures_smart.py <input_pdf> --output-dir <dir> [--dpi 200]
"""

import argparse, re, sys, os
from pathlib import Path

try:
    import fitz
except ImportError:
    print("需要安装 pymupdf: pip install pymupdf")
    sys.exit(1)


def detect_figure_numbers(page_text: str) -> list[int]:
    """Find figure numbers mentioned on this page."""
    nums = set()
    for m in re.finditer(r'(?:Fig\.?\s*|Figure\s+)(\d+)', page_text, re.IGNORECASE):
        nums.add(int(m.group(1)))
    return sorted(nums)


def extract_figures_smart(pdf_path: Path, output_dir: Path, dpi: int = 200) -> dict:
    """Extract and map figures to paper numbers. Returns mapping dict."""
    output_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(str(pdf_path))
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    mapping = {}

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        fig_nums = detect_figure_numbers(text)

        if not fig_nums:
            continue

        # Get all images on this page
        image_list = page.get_images(full=True)
        large_images = []
        for img_info in image_list:
            try:
                bi = doc.extract_image(img_info[0])
            except Exception:
                continue
            size_kb = len(bi["image"]) / 1024
            w, h = bi.get("width", 0), bi.get("height", 0)
            if size_kb > 30 and w > 100 and h > 100:  # Filter icons
                large_images.append({"xref": img_info[0], "ext": bi.get("ext", "png"),
                                     "width": w, "height": h, "size_kb": size_kb,
                                     "image_bytes": bi["image"]})

        # For each figure number on this page, assign an image
        for idx, fnum in enumerate(fig_nums):
            if idx < len(large_images):
                # Use extracted raster image
                img = large_images[idx]
                ext = img["ext"]
                fname = f"fig{fnum:02d}.{ext}"
                with open(output_dir / fname, "wb") as f:
                    f.write(img["image_bytes"])
                mapping[fnum] = {"filename": fname, "page": page_num + 1,
                                 "source": "extracted", "width": img["width"],
                                 "height": img["height"], "size_kb": round(img["size_kb"], 1)}
            else:
                # No raster image — render page as fallback
                fname = f"fig{fnum:02d}.png"
                pix = page.get_pixmap(matrix=mat)
                pix.save(str(output_dir / fname))
                size_kb = os.path.getsize(output_dir / fname) / 1024
                mapping[fnum] = {"filename": fname, "page": page_num + 1,
                                 "source": "rendered (vector)", "size_kb": round(size_kb, 1)}

    doc.close()

    # Sort by figure number
    return dict(sorted(mapping.items()))


def main():
    parser = argparse.ArgumentParser(description="Smart figure extractor with paper-number mapping")
    parser.add_argument("input_pdf", help="Input PDF path")
    parser.add_argument("--output-dir", "-d", default="figures", help="Output directory")
    parser.add_argument("--dpi", type=int, default=200, help="Render DPI for vector figures (default: 200)")
    args = parser.parse_args()

    pdf_path = Path(args.input_pdf)
    if not pdf_path.exists():
        print(f"Error: {args.input_pdf} not found")
        sys.exit(1)

    output_dir = Path(args.output_dir)
    print(f"📄 {pdf_path.name}")
    print(f"🔍 Mapping figures...")

    mapping = extract_figures_smart(pdf_path, output_dir, args.dpi)

    print(f"\n📊 Mapped {len(mapping)} figures:")
    total_kb = 0
    for fnum, info in mapping.items():
        src = info["source"]
        print(f"  Fig {fnum:2d}: {info['filename']:<20} P.{info['page']:<3} {info['size_kb']:>6.0f} KB  [{src}]")
        total_kb += info["size_kb"]

    print(f"\n  Total: {total_kb:.0f} KB | Dir: {output_dir}")

    # Print markdown template
    print("\n--- MD Template ---")
    for fnum, info in mapping.items():
        print(f"### Figure {fnum} | 图{fnum}")
        print(f"![Figure {fnum}](figures/{info['filename']})")
        print(f"- **基本信息:** ...")
        print(f"- **主要结论:** ...")
        print(f"- **原文结论句:** 🟣 \"...\" (P.{info['page']})")
        print(f"- **我的批注:** ")
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
