# -*- coding: utf-8 -*-
"""审计全站被 Markdown 撕碎的公式（em 损坏 / 游离 LaTeX 碎片）。"""
import pathlib
import re

site = pathlib.Path(__file__).resolve().parent / "site"
em_pat = re.compile(r"<em _[^>]*>")
frag_pat = re.compile(r"\\(?:mathrm|underbrace|sqrt|mathcal|frac|left|right|ell|times)[^<]{0,30}")

problems = 0
for f in sorted(site.rglob("index.html")):
    t = f.read_text(encoding="utf-8")
    # 移除 arithmatex 节点后再找游离碎片
    stripped = re.sub(r'<(?:span|div) class="arithmatex">.*?</(?:span|div)>', "", t, flags=re.S)
    mangled = em_pat.findall(t)
    frags = frag_pat.findall(stripped)
    if mangled or frags:
        problems += 1
        print(f"[X] {f.relative_to(site)}")
        for x in mangled[:3]:
            print("     em 损坏:", x)
        for x in frags[:4]:
            print("     游离碎片:", x)
print("问题页面数:", problems)
