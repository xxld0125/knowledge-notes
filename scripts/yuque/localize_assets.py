#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import os
import re
import urllib.parse
import urllib.request
from pathlib import Path


IMG_MD_RE = re.compile(r"!\[[^\]]*\]\((?P<url>[^)]+)\)")
IMG_HTML_RE = re.compile(r"<img\s+[^>]*src=[\"'](?P<url>[^\"']+)[\"'][^>]*>", re.I)


def is_remote_asset(url: str) -> bool:
    u = url.strip()
    if u.startswith("<") and u.endswith(">"):
        u = u[1:-1]
    if not (u.startswith("http://") or u.startswith("https://")):
        return False
    host = urllib.parse.urlparse(u).netloc.lower()
    return any(h in host for h in ("cdn.nlark.com", "yuque.com"))


def safe_filename_from_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    name = Path(parsed.path).name or "asset"
    # strip query-ish
    name = name.split("?")[0].split("#")[0]
    # ensure extension
    if "." not in name:
        name += ".bin"
    # sanitize
    name = re.sub(r"[\\/:*?\"<>|]", "-", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name or "asset.bin"


def download(url: str, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        return
    req = urllib.request.Request(url, headers={"User-Agent": "knowledge-notes-yuque-assets/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    dst.write_bytes(data)


def rewrite_doc(md_path: Path, assets_root: Path) -> int:
    text = md_path.read_text(encoding="utf-8")
    changed = 0

    def handle_url(url: str) -> str | None:
        u = url.strip()
        if u.startswith("<") and u.endswith(">"):
            u = u[1:-1]
        if not is_remote_asset(u):
            return None
        # stable per-url naming to avoid collisions
        h = hashlib.sha1(u.encode("utf-8")).hexdigest()[:10]
        fn = safe_filename_from_url(u)
        dst = assets_root / f"{h}-{fn}"
        try:
            download(u, dst)
        except Exception:
            return None
        rel = os.path.relpath(dst, md_path.parent).replace(os.sep, "/")
        return rel

    def md_repl(m: re.Match[str]) -> str:
        nonlocal changed
        url = m.group("url")
        new_rel = handle_url(url)
        if not new_rel:
            return m.group(0)
        changed += 1
        return m.group(0).replace(url, new_rel)

    def html_repl(m: re.Match[str]) -> str:
        nonlocal changed
        url = m.group("url")
        new_rel = handle_url(url)
        if not new_rel:
            return m.group(0)
        changed += 1
        return m.group(0).replace(url, new_rel)

    new_text = IMG_MD_RE.sub(md_repl, text)
    new_text = IMG_HTML_RE.sub(html_repl, new_text)

    if new_text != text:
        md_path.write_text(new_text, encoding="utf-8")
    return changed


def main() -> None:
    p = argparse.ArgumentParser(description="Download remote Yuque images and rewrite links to relative paths.")
    p.add_argument("--book-dir", required=True, help="知识库目录，如 knowledge-base/面试训练")
    p.add_argument("--assets-dirname", default="assets", help="每个文档目录下的资产目录名")
    args = p.parse_args()

    repo_root = Path(os.environ.get("REPO_ROOT", Path.cwd())).resolve()
    book_dir = (repo_root / args.book_dir).resolve()
    docs_root = book_dir / "docs"

    if not docs_root.exists():
        raise SystemExit(f"Missing docs: {docs_root}")

    total = 0
    for md in sorted(docs_root.rglob("*.md")):
        if md.name == "000_目录.md":
            continue
        assets_root = md.parent / args.assets_dirname / md.stem
        total += rewrite_doc(md, assets_root)

    print(f"rewritten_links={total}")


if __name__ == "__main__":
    main()

