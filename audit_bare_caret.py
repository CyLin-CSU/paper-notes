# -*- coding: utf-8 -*-
"""最终判定：LaTeX 定界符之外的裸 ^{ 检查（原始字符串版）。"""
import pathlib
import re

docs = pathlib.Path(r"C:\Users\ChengyeLin.LINOUP-XIAOXIN1\Desktop\work\paper-notes\docs")
inline = re.compile(r"\\\(.{0,300}?\\\)")
display = re.compile(r"\\\[(.{0,600}?)\\\]")

bare = 0
for f in sorted(docs.rglob("*.md")):
    if f.name == "abbreviations.md":
        continue
    for ln, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        stripped = inline.sub("", line)
        stripped = display.sub("", stripped)
        if "^{" in stripped:
            bare += 1
            print(f"[X] {f.name}:{ln}: {stripped.strip()[:100]}")
print("LaTeX 之外的裸 ^{ 计数:", bare)
