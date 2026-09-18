# -*- coding: utf-8 -*-
"""
论文笔记助手：新增笔记（按月份归档）+ 自动更新首页时间线。

用法（在 paper-notes 目录下，pythonProject1 环境）：
  python new_note.py note <slug> "论文标题"      # 例：python new_note.py note cbramod "CBraMod"
  python new_note.py log "更新说明文字"          # 例：python new_note.py log "新增 CBraMod 精读"

note 子命令会在 docs/papers/YYYY-MM/ 下按当天日期生成模板文件（含架构图占位）；
之后记得在 mkdocs.yml 的 nav 里登记。
log 子命令会在首页时间线插入今天的条目，并自动刷新"最近更新"日期。
"""
import datetime
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DOCS = ROOT / "docs"
INDEX = DOCS / "index.md"

TEMPLATE = '''---
title: "{title}"
date: {today}
authors: []
venue: ""
year: {year}
tags: []
status: "粗读"
rating:
arxiv: ""
code: ""
one-liner: ""
---

# {title}

> **venue 年份**

## 问题定位

## 方法

## 架构图

![架构图占位](../../assets/占位.png)
*把论文架构图放到 docs/assets/ 后替换上面的路径与说明*

## 创新点

## 流程

## 实验与结果

## 与其他论文的关系

| 论文 / 工作 | 关系说明 |
|---|---|

## 个人思考

'''


def today() -> str:
    return datetime.date.today().isoformat()


def cmd_note(slug: str, title: str) -> None:
    d = datetime.date.today()
    month_dir = DOCS / "papers" / d.strftime("%Y-%m")
    month_dir.mkdir(parents=True, exist_ok=True)
    out = month_dir / f"{d.strftime('%m%d')}-{slug}.md"
    if out.exists():
        print(f"[!] 已存在：{out}")
        sys.exit(1)
    out.write_text(TEMPLATE.format(title=title, today=d.isoformat(), year=d.year), encoding="utf-8")
    print(f"[+] 已创建 {out}")
    print(f"[i] 记得在 mkdocs.yml 的 nav 里登记：\n"
          f'      - {d.strftime("%m%d")} · {title}: papers/{d.strftime("%Y-%m")}/{out.name}')


def cmd_log(message: str) -> None:
    text = INDEX.read_text(encoding="utf-8")
    today_str = today()
    entry = f"- **{today_str}** · {message}\n"
    # 插入到样式化时间线 <ul> 的第一条位置
    pattern = r'(<ul class="timeline" markdown>\s*\n)'
    if not re.search(pattern, text):
        print('[!] index.md 中找不到 <ul class="timeline" markdown> 时间线')
        sys.exit(1)
    text = re.sub(pattern, r"\1" + entry + "\n", text, count=1)
    text = re.sub(r"(\*\*最近更新\*\*：)\d{4}-\d{2}-\d{2}", r"\g<1>" + today_str, text)
    INDEX.write_text(text, encoding="utf-8")
    print(f"[+] 时间线已更新：{today_str} · {message}")
    print(f"[+] 最近更新日期已刷新为 {today_str}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "note" and len(sys.argv) >= 4:
        cmd_note(sys.argv[2], sys.argv[3])
    elif cmd == "log" and len(sys.argv) >= 3:
        cmd_log(" ".join(sys.argv[2:]))
    else:
        print(__doc__)
        sys.exit(1)
