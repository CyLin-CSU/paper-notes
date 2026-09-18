# -*- coding: utf-8 -*-
"""把 Zotero 导出的 CSL JSON 转成笔记骨架。

用法：python zotero_import.py imports/xxx.json [slug]
"""
import datetime
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DOCS = ROOT / "docs"


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    data = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    item = data[0] if isinstance(data, list) else data
    title = item.get("title", "Untitled")
    authors = [a.get("family", a.get("literal", "?")) for a in item.get("author", [])]
    year = (item.get("issued", {}).get("date-parts") or [[""]])[0][0] or ""
    venue = item.get("container-title", "") or item.get("publisher", "")
    arxiv = ""
    for u in item.get("URL", ""), :
        if "arxiv" in str(u):
            arxiv = u
    d = datetime.date.today()
    slug = sys.argv[2] if len(sys.argv) > 2 else f"{authors[0].lower() if authors else 'anon'}{d.year}"
    month_dir = DOCS / "papers" / d.strftime("%Y-%m")
    month_dir.mkdir(parents=True, exist_ok=True)
    out = month_dir / f"{d.strftime('%m%d')}-{slug}.md"
    fm = (
        "---\n"
        f'title: "{title}"\n'
        f"date: {d.isoformat()}\n"
        f"authors: [{', '.join(authors)}]\n"
        f'venue: "{venue}"\n'
        f"year: {year}\n"
        "tags: []\n"
        'status: "粗读"\n'
        "rating:\n"
        f'arxiv: "{arxiv}"\n'
        'code: ""\n'
        'one-liner: ""\n'
        "---\n\n"
        f"# {title}\n\n> **{venue} {year}**\n\n## 问题定位\n\n## 方法\n\n## 架构图\n\n"
        "![架构图](../../assets/待补充.png)\n\n## 创新点\n\n## 流程\n\n"
        "## 实验与结果\n\n## 与其他论文的关系\n\n## 个人思考\n\n## 自问自答\n"
    )
    out.write_text(fm.encode().decode("unicode_escape"), encoding="utf-8")
    print(f"[+] {out}")
    print(f"[i] nav 登记：      - {d.strftime('%m%d')} · {title}: papers/{d.strftime('%Y-%m')}/{out.name}")


if __name__ == "__main__":
    main()
