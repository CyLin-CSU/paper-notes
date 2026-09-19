# -*- coding: utf-8 -*-
"""修复 TFM 页被 Markdown 撕碎的总损失公式：移出列表项 + 独立成段。"""
import pathlib

p = pathlib.Path(
    r"C:\Users\ChengyeLin.LINOUP-XIAOXIN1\Desktop\work\paper-notes\docs\papers\2026-09\0918-tfm-tokenizer.md"
)
t = p.read_text(encoding="utf-8")

marker = "- 损失："
i = t.find(marker)
assert i != -1, "找不到损失行"
j = t.find("\n", i)
corrupted = t[i:j]
print("原损坏行片段:", corrupted[:80])

clean_header = "- 损失：总损失 = 掩码重构 + codebook + commitment 三项之和（下式）；码字用 EMA 更新："
formula = (
    "\n\n\\[ \\mathcal{L}_{\\mathrm{token}} = "
    "\\underbrace{\\sum_{(f,t)} \\left\\| S(f,t) - \\hat{S}(f,t) \\right\\|_2^2}_{\\text{掩码重构}} "
    "\\;+\\; "
    "\\underbrace{\\alpha \\sum_i \\left\\| \\mathrm{sg}[E_i] - v_i \\right\\|_2^2}_{\\text{codebook}} "
    "\\;+\\; "
    "\\underbrace{\\beta \\sum_i \\left\\| E_i - \\mathrm{sg}[v_i] \\right\\|_2^2}_{\\text{commitment}} "
    "\\]"
)
t = t[:i] + clean_header + formula + t[j:]
p.write_text(t, encoding="utf-8")
print("[+] 已修复：公式移出列表项，独立成段")
