# -*- coding: utf-8 -*-
"""从 docs/papers/** front matter 生成 data/papers.json（可再生文件）。

papers.json 是 front matter 的派生物：别名、短摘要等补充信息一律进
front matter，不要手改 papers.json——下次重建会被覆盖。
用法：python tools/build_data.py            # 写 data/papers.json
     python tools/build_data.py --stdout    # 只打印不写
CI 漂移检查：重新生成并与已提交版本逐字节比对，不一致即失败（deploy 工作流）。
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
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # Windows 控制台默认 GBK，--stdout 需 UTF-8
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
