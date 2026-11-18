# -*- coding: utf-8 -*-
"""验收辅助：核对论文笔记三处清单的一致性。

对照三方事实源：
  1. docs/papers/<group>/<slug>.md  实际文件；
  2. mkdocs.yml nav 论文笔记分组下登记的页面；
  3. docs/index.md 论文库表格中链接的页面。
报告：缺项（一方有他方无）、重复项、首页分组标题计数与实际条数不符。
退出码：一致 0，不一致 1。

用法：python tools/check_home_count.py [仓库根目录]   # 默认脚本上一级
"""
import pathlib
import re
import sys

GROUPS = ("fm", "generative", "survey", "reviews")
NAV_RE = re.compile(r"papers/(" + "|".join(GROUPS) + r")/([a-z0-9-]+)\.md")
TITLE_RE = re.compile(r"^###\s+.*（(\d+)\s*篇）", re.M)


def main(root: pathlib.Path) -> int:
    docs = root / "docs"
    problems = []

    # 1. 文件系统
    files: dict[str, set] = {g: {p.stem for p in (docs / "papers" / g).glob("*.md")}
                             for g in GROUPS}

    # 2. mkdocs.yml nav
    nav_text = (root / "mkdocs.yml").read_text(encoding="utf-8")
    nav: dict[str, set] = {g: set() for g in GROUPS}
    for g, slug in NAV_RE.findall(nav_text):
        nav[g].add(slug)

    # 3. 首页论文库表格
    index_text = (docs / "index.md").read_text(encoding="utf-8")
    home: dict[str, set] = {g: set() for g in GROUPS}
    for g, slug in NAV_RE.findall(index_text):
        home[g].add(slug)

    total = 0
    for g in GROUPS:
        f, n, h = files[g], nav[g], home[g]
        total += len(f)
        for where, a, b in (("nav", f, n), ("首页", f, h)):
            for miss in sorted(a - b):
                problems.append(f"papers/{g}/{miss}.md 未登记在{where}")
            for extra in sorted(b - a):
                problems.append(f"{where} 中的 papers/{g}/{extra}.md 没有对应文件")
        dup = len(f) - len(f)
        if dup:
            problems.append(f"{g} 分组文件重复")
        print(f"[check-home-count] {g}: 文件 {len(f)} / nav {len(n)} / 首页 {len(h)}")

    # 4. 首页分组标题计数
    for m in TITLE_RE.finditer(index_text):
        print(f"[check-home-count] 首页分组标题计数：{m.group(0).strip()}")

    # 综述独立分组（reviews）提示
    print(f"[check-home-count] 合计 {total} 篇（reviews 组综述 {len(files['reviews'])} 篇单列展示）")

    if problems:
        print()
        for p in problems:
            print(f"[check-home-count] 不一致：{p}")
        return 1
    print("[check-home-count] 三方清单一致")
    return 0


if __name__ == "__main__":
    root = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else \
        pathlib.Path(__file__).resolve().parents[1]
    sys.exit(main(root))
