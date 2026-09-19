# -*- coding: utf-8 -*-
"""LaTeX 公式静态审计：源 md 配对 + 构建产物节点完整性。"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
SITE = ROOT / "site"

print("=== 1. 源 md 定界符配对 ===")
issues = 0
for f in (ROOT / "docs").rglob("*.md"):
    t = f.read_text(encoding="utf-8")
    n_open = t.count(r"\(")
    n_close = t.count(r"\)")
    n_dopen = t.count(r"\[")
    n_dclose = t.count(r"\]")
    if n_open != n_close or n_dopen != n_dclose:
        issues += 1
        print(f"[X] {f.name}: \\(={n_open} \\)={n_close} \\[={n_dopen} \\]={n_dclose}")
print("（无 [X] = 全部配对）")

print("=== 2. 构建产物 arithmatex 节点完整性 ===")
bad = 0
total = 0
for f in SITE.rglob("index.html"):
    t = f.read_text(encoding="utf-8")
    for s in re.findall(r'<span class="arithmatex">(.*?)</span>', t, re.S):
        total += 1
        if s.count(r"\(") != s.count(r"\)") or len(s) < 10:
            bad += 1
            print(f"[X] span {f.relative_to(SITE)}: {s[:70]!r}")
    for s in re.findall(r'<div class="arithmatex">(.*?)</div>', t, re.S):
        total += 1
        if s.count(r"\[") != s.count(r"\]") or len(s) < 10:
            bad += 1
            print(f"[X] div {f.relative_to(SITE)}: {s[:70]!r}")
print(f"节点总数 {total}，损坏 {bad}")

print("=== 3. 反引号伪公式残留 ===")
n = 0
for f in (ROOT / "docs").rglob("*.md"):
    t = f.read_text(encoding="utf-8")
    for m in re.finditer(r"`[^`\n]*(?:\^|\\\(|\[|∈)[^`\n]*`", t):
        n += 1
        print(f"[?] {f.name}: {m.group(0)[:70]}")
print(f"残留 {n}")
