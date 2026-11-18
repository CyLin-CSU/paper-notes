# -*- coding: utf-8 -*-
"""从 docs/papers/** front matter 生成 data/papers.json（31 篇元数据迁移首版）。

用法：python tools/build_data.py            # 写 data/papers.json
     python tools/build_data.py --stdout   # 只打印不写
生成内容为纯机器抽取，不含手工字段；手工补充（别名等）直接编辑 papers.json
时请同时修改本脚本的 HAND_EXTRAS 合并逻辑，避免下次重建丢失。
"""
import json
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
GROUPS = ("fm", "generative", "survey", "reviews")
FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)


def group_type(group: str) -> str:
    return "review" if group == "reviews" else "research"


def load_note(path: pathlib.Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    if not m:
        raise SystemExit(f"[build-data] 未找到 front matter：{path}")
    meta = yaml.safe_load(m.group(1)) or {}
    return {
        "paper_id": path.stem,
        "group": path.parent.name,
        "type": group_type(path.parent.name),
        "title": meta.get("title", ""),
        "authors": meta.get("authors", []) or [],
        "year": int(meta.get("year", 0) or 0),
        "venue": meta.get("venue", ""),
        "doi": (meta.get("doi") or "").strip() or None,
        "arxiv": (meta.get("arxiv") or "").strip() or None,
        "code": (meta.get("code") or "").strip() or None,
        "status": meta.get("status", ""),
        "verified_date": str(meta.get("date", "")),
        "one_liner": meta.get("one-liner", ""),
    }


def main() -> int:
    papers = []
    for group in GROUPS:
        for path in sorted((ROOT / "docs" / "papers" / group).glob("*.md")):
            papers.append(load_note(path))
    out = ROOT / "data" / "papers.json"
    payload = json.dumps(papers, ensure_ascii=False, indent=2) + "\n"
    if "--stdout" in sys.argv:
        sys.stdout.write(payload)
    else:
        out.write_text(payload, encoding="utf-8")
        print(f"[build-data] 已写入 {out.relative_to(ROOT)}（{len(papers)} 篇）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
