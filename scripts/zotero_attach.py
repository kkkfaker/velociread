#!/usr/bin/env python3
"""
paper-anatomist Zotero Attachment Manager
通过 Zotero 本地 API 或文件系统直接操作，将批注 PDF 和笔记附加到 Zotero 文献条目。

Usage:
    python zotero_attach.py <pdf_or_note_path> --parent-pdf <original.pdf>
    python zotero_attach.py <pdf_or_note_path> --item-key <ZOTERO_ITEM_KEY>
    python zotero_attach.py <annotated.pdf> --parent-pdf <original.pdf> --dry-run

Requirements:
    Zotero 7+ running with local HTTP server (default port 23119)
    or: Access to Zotero storage directory for filesystem fallback
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError


ZOTERO_API_BASE = "http://localhost:23119"
ZOTERO_STORAGE_DIRS = [
    Path.home() / "Zotero" / "storage",
    Path(os.environ.get("APPDATA", "")) / "Zotero" / "Zotero" / "Profiles",
]


def find_zotero_storage() -> Path | None:
    """Find the Zotero storage directory."""
    # Method 1: Check common locations
    for d in ZOTERO_STORAGE_DIRS:
        if d.exists():
            # If it's the Profiles directory, find the active profile
            if "Profiles" in str(d):
                for profile_dir in d.iterdir():
                    if profile_dir.is_dir() and "storage" in os.listdir(profile_dir):
                        return profile_dir / "storage"
            else:
                return d

    # Method 2: Search in user home
    home = Path.home()
    for pattern in ["Zotero/storage", "Zotero/data/storage"]:
        candidate = home / pattern
        if candidate.exists():
            return candidate

    return None


def find_item_key_by_pdf(pdf_path: str, storage_dir: Path) -> str | None:
    """Find Zotero item key by matching PDF filename in storage directory."""
    pdf_name = Path(pdf_path).name

    for item_dir in storage_dir.iterdir():
        if item_dir.is_dir():
            for f in item_dir.iterdir():
                if f.name == pdf_name:
                    return item_dir.name  # Directory name is the item key

    return None


def attach_via_filesystem(source_path: str, item_key: str, storage_dir: Path) -> bool:
    """Copy a file into the Zotero storage directory for the given item key."""
    item_dir = storage_dir / item_key
    if not item_dir.exists():
        print(f"  ⚠ Zotero item 目录不存在: {item_dir}")
        return False

    source = Path(source_path)
    dest = item_dir / source.name

    try:
        shutil.copy2(str(source), str(dest))
        print(f"  ✅ 文件已复制: {dest}")
        return True
    except Exception as e:
        print(f"  ❌ 复制失败: {e}")
        return False


def check_zotero_api() -> bool:
    """Check if Zotero local API is running."""
    try:
        req = Request(f"{ZOTERO_API_BASE}/connector/ping", method="GET")
        urlopen(req, timeout=3)
        return True
    except URLError:
        return False


def attach_via_api(source_path: str, item_key: str) -> bool:
    """Attach a file to a Zotero item via the local API."""
    # Zotero 7 local API for attachment management
    # This is a simplified version; the full API may require more parameters
    source = Path(source_path)
    if not source.exists():
        print(f"  ❌ 源文件不存在: {source_path}")
        return False

    try:
        # Read file content
        with open(source_path, "rb") as f:
            file_data = f.read()

        # POST to Zotero attachment endpoint
        url = f"{ZOTERO_API_BASE}/connector/saveAttachment"
        boundary = "----XiaoLvJingReaderBoundary"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{source.name}"\r\n'
            f"Content-Type: application/pdf\r\n\r\n"
        ).encode("utf-8")
        body += file_data
        body += f"\r\n--{boundary}--\r\n".encode("utf-8")

        req = Request(
            url + f"?itemKey={item_key}",
            data=body,
            method="POST",
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        )
        response = urlopen(req, timeout=30)
        print(f"  ✅ API 响应: {response.status}")
        return True
    except URLError as e:
        print(f"  ⚠ Zotero API 连接失败: {e}")
        return False
    except Exception as e:
        print(f"  ❌ API 附件上传失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="小绿鲸精读 Zotero 附件管理器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 通过原始PDF自动查找Zotero条目并附加
  python zotero_attach.py paper-annotated.pdf --parent-pdf ~/Zotero/storage/ABC123/paper.pdf

  # 通过Zotero item key直接附加
  python zotero_attach.py paper-annotated.pdf --item-key ABC123

  # 同时附加多个文件
  python zotero_attach.py paper-annotated.pdf paper-精读笔记.md --parent-pdf original.pdf

  # 干跑
  python zotero_attach.py paper-annotated.pdf --parent-pdf original.pdf --dry-run
        """,
    )
    parser.add_argument("files", nargs="+", help="要附加的文件路径")
    parser.add_argument("--parent-pdf", help="原始 PDF 路径，用于在 Zotero 中定位条目")
    parser.add_argument("--item-key", help="直接指定 Zotero item key")
    parser.add_argument("--dry-run", action="store_true", help="只检查不执行")
    parser.add_argument("--method", choices=["auto", "api", "filesystem"],
                        default="auto", help="附加方式 (默认: auto)")

    args = parser.parse_args()

    # Validate files
    for fpath in args.files:
        if not Path(fpath).exists():
            print(f"错误: 文件不存在 {fpath}")
            sys.exit(1)

    # Determine item key
    item_key = args.item_key

    if not item_key and args.parent_pdf:
        storage_dir = find_zotero_storage()
        if storage_dir:
            print(f"📂 Zotero 存储目录: {storage_dir}")
            parent_path = Path(args.parent_pdf)
            if parent_path.exists():
                # Check if the parent PDF is already in Zotero storage
                try:
                    item_key = find_item_key_by_pdf(parent_path.name, storage_dir)
                except Exception:
                    pass
                if item_key:
                    print(f"🔑 找到 Zotero item: {item_key}")
                else:
                    # Try matching by parent directory
                    if parent_path.parent.name and len(parent_path.parent.name) == 8:
                        item_key = parent_path.parent.name
                        print(f"🔑 推测 Zotero item: {item_key}")
            else:
                print(f"⚠ 找不到原始 PDF: {args.parent_pdf}")
        else:
            print("⚠ 未找到 Zotero 存储目录")

    if not item_key:
        print("\n❌ 无法确定 Zotero item key。请用 --item-key 直接指定。")
        print("   提示: Zotero 文献条目 → 右键 → Show File → 复制路径")
        print("   路径中的随机文件夹名（如 ABC123）就是 item key。")
        sys.exit(1)

    # Check Zotero API availability
    api_available = check_zotero_api()
    method = args.method
    if method == "auto":
        method = "api" if api_available else "filesystem"

    print(f"\n📎 附加文件到 Zotero item: {item_key}")
    print(f"   方式: {method} {'(Zotero 运行中)' if api_available else '(Zotero 离线)'}")
    if args.dry_run:
        print("   🔍 干跑模式")

    storage_dir = None
    if method == "filesystem":
        storage_dir = find_zotero_storage()
        if not storage_dir:
            print("❌ 无法找到 Zotero 存储目录")
            sys.exit(1)

    success_count = 0
    for fpath in args.files:
        print(f"\n  📄 {Path(fpath).name}")

        if args.dry_run:
            print(f"     → 将附加到 item {item_key}")
            success_count += 1
            continue

        if method == "api":
            ok = attach_via_api(fpath, item_key)
        else:
            assert storage_dir is not None
            ok = attach_via_filesystem(fpath, item_key, storage_dir)

        if ok:
            success_count += 1

    print(f"\n✅ {success_count}/{len(args.files)} 个文件附加成功")

    # If using filesystem method, remind user to sync
    if method == "filesystem" and not args.dry_run:
        print("\n💡 提示: 请在 Zotero 中右键文献 → Sync 以索引新附件。")

    return 0 if success_count == len(args.files) else 1


if __name__ == "__main__":
    sys.exit(main())
