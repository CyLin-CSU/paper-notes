# -*- coding: utf-8 -*-
"""逐行审计：列出每一行含数学符号/公式痕迹的内容，供逐行定性。"""
import pathlib
import re

DOCS = pathlib.Path(r"C:\Users\ChengyeLin.LINOUP-XIAOXIN1\Desktop\work\paper-notes\docs")
SITE = pathlib.Path(r"C:\Users\ChengyeLin.LINOUP-XIAOXIN1\Desktop\work\paper-notes\site")

# 数学痕迹字符集（宽特征）
MATH_CHARS = "∈ℝ∑Π∫‖ℓ≤≥⊕⊗→←⌊⌋⟨⟩λφαβθδσςẐŜ×−–^\\("
# 排除明显的非数学行（标题装饰、链接箭头用 → 是导航语义，单独标注）
in_block = False
block_lang = ""

print("=" * 80)
print("A. 源 md 逐行扫描（行号 | 类型判定 | 内容）")
print("=" * 80)
for f in sorted(DOCS.rglob("*.md")):
    lines = f.read_text(encoding="utf-8").splitlines()
    in_code = False
    for ln, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue  # mermaid/普通代码块里的内容跳过
        has_math = any(c in line for c in MATH_CHARS) or re.search(r"\{\\", line) or re.search(r"\\\(|\\\[", line)
        in_backtick = re.search(r"`[^`]+`", line) and any(
            c in re.search(r"`[^`]+`", line).group(0) for c in "∈ℝ∑Π‖ℓ^≤"
        )
        if not has_math:
            continue
        if in_backtick:
            kind = "❓反引号数学（需判断）"
        elif re.search(r"\\\(|\\\[", line):
            kind = "✅真LaTeX"
        elif re.search(r"\{\\|\^[0-9a-z{]", line):
            kind = "❓裸上标/花括号"
        else:
            kind = "⭕unicode文本（可接受）"
        print(f"{f.name}:{ln} [{kind}] {line.strip()[:110]}")

print()
print("=" * 80)
print("B. 构建产物：arithmatex 节点外的原始 \\( \\[ 残留")
print("=" * 80)
n = 0
for f in sorted(SITE.rglob("index.html")):
    t = f.read_text(encoding="utf-8")
    stripped = re.sub(r'<(?:span|div) class="arithmatex">.*?</(?:span|div)>', "", t, flags=re.S)
    stripped = re.sub(r"<script.*?</script>", "", stripped, flags=re.S)
    for m in re.finditer(r"\\\(|\\\[", stripped):
        n += 1
        print(f"[X] {f.relative_to(SITE)}: ...{stripped[max(0,m.start()-60):m.start()+40]}...")
print(f"残留计数: {n}")

print()
print("=" * 80)
print("C. 构建产物：被 Markdown 撕碎的公式痕迹")
print("=" * 80)
bad = 0
for f in sorted(SITE.rglob("index.html")):
    t = f.read_text(encoding="utf-8")
    stripped = re.sub(r'<(?:span|div) class="arithmatex">.*?</(?:span|div)>', "", t, flags=re.S)
    for m in re.finditer(r"\\(?:mathrm|underbrace|sqrt|mathcal|frac|left|ell|times)", stripped):
        bad += 1
        print(f"[X] {f.relative_to(SITE)}: {stripped[max(0,m.start()-50):m.start()+40]}")
print(f"撕碎计数: {bad}")
