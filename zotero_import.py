# -*- coding: utf-8 -*-
"""Zotero CSL JSON → 论文笔记骨架转换器。

用法：
  python zotero_import.py imports/xxx.json            # 单文件（CSL JSON 数组或单条目）
  python zotero_import.py imports/xxx.json <slug>     # 指定 slug
  python zotero_import.py imports/*.json              # 一次导入多个文件

说明：
  - Zotero 中选中条目 → 右键 → 导出条目 → 格式选 "CSL JSON" 存到 imports/
  - 自动填写 frontmatter（title/authors/venue/year/arxiv/doi），生成与 new_note.py
    相同结构的笔记骨架（含架构图占位与自问自答等全部板块）
  - slug 默认取第一作者姓氏小写+年份（如 yang2023），可在命令行覆盖
"""
import datetime
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DOCS = ROOT / "docs"

TEMPLATE = """---
title: "{title}"
date: {today}
authors: [{authors}]
venue: "{venue}"
year: {year}
tags: []
status: "粗读"
rating:
arxiv: "{arxiv}"
code: ""
doi: "{doi}"
one-liner: ""
---

# {title}

> **{venue} {year}**

## 问题定位

## 方法

## 架构图

![架构图占位](../../assets/待补充.png)
*把论文架构图放到 docs/assets/ 后替换上面的路径与说明*

## 创新点

## 流程

## 实验与结果

## 与其他论文的关系

| 论文 / 工作 | 关系说明 |
|---|---|

## 个人思考

## 自问自答
"""


def parse_item(item: dict) -> dict:
    title = item.get("title", "Untitled").strip()
    authors = []
    for a in item.get("author", []):
        name = a.get("family") or a.get("literal") or a.get("given", "?")
        authors.append(name)
    year = ""
    parts = item.get("issued", {}).get("date-parts") or []
    if parts and parts[0]:
        year = parts[0][0]
    venue = item.get("container-title") or item.get("publisher") or ""
    if isinstance(venue, list):
        venue = venue[0] if venue else ""
    url = item.get("URL", "") or ""
    doi = item.get("DOI", "") or ""
    arxiv = ""
    m = re.search(r"arxiv\.org/(?:abs|pdf)/([0-9.]+)", url)
    if m:
        arxiv = f"https://arxiv.org/abs/{m.group(1)}"
    elif "arXiv" in str(item.get("id", "")):
        arxiv = url
    return dict(title=title, authors=authors, year=year, venue=venue, url=url, doi=doi, arxiv=arxiv)


def import_file(path: pathlib.Path, slug_override: str | None = None) -> pathlib.Path | None:
    raw = path.read_text(encoding="utf-8-sig")
    data = json.loads(raw)
    items = data if isinstance(data, list) else [data]
    d = datetime.date.today()
    month_dir = DOCS / "papers" / d.strftime("%Y-%m")
    month_dir.mkdir(parents=True, exist_ok=True)

    created = []
    for item in items:
        if item.get("type") in {"webpage", "attachment"}:
            continue
        info = parse_item(item)
        if slug_override:
            slug = slug_override
        else:
            first = (info["authors"][0] if info["authors"] else "anon")
            first = re.sub(r"[^a-zA-Z]", "", first).lower() or "anon"
            slug = f"{first}{info['year'] or d.year}"
        out = month_dir / f"{d.strftime('%m%d')}-{slug}.md"
        if out.exists():
            print(f"[!] 已存在，跳过：{out.name}")
            continue
        fm = TEMPLATE.format(
            title=info["title"].replace('"', "'"),
            today=d.isoformat(),
            authors=", ".join(info["authors"]),
            venue=info["venue"].replace('"', "'"),
            year=info["year"],
            arxiv=info["arxiv"],
            doi=info["doi"],
        )
        out.write_text(fm, encoding="utf-8")
        created.append((out, info))
        print(f"[+] 已创建 {out.relative_to(ROOT)}")
        print(f"[i] nav 登记：  {d.strftime('%m%d')} · {info['title'][:40]}: papers/{d.strftime('%Y-%m')}/{out.name}")
    return created


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    slug = None
    args = [a for a in sys.argv[1:]]
    # 最后一个不以 .json 结尾的参数视为 slug
    jsons = [a for a in args if a.lower().endswith(".json")]
    if len(args) > len(jsons):
        slug = [a for a in args if not a.lower().endswith(".json")][0]
    if not jsons:
        print("[!] 未找到 .json 输入文件")
        sys.exit(1)
    for jp in jsons:
        p = pathlib.Path(jp)
        if not p.exists():
            print(f"[!] 文件不存在：{p}")
            continue
        import_file(p, slug)


if __name__ == "__main__":
    main()
