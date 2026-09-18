# -*- coding: utf-8 -*-
"""修复 biot.md 中被转义破坏的公式块（使用原始字符串重写）。"""
import pathlib
import re

p = pathlib.Path(r"C:\Users\ChengyeLin.LINOUP-XIAOXIN1\Desktop\work\paper-notes\docs\papers\2026-09\0918-biot.md")
t = p.read_text(encoding="utf-8")

clean = r"""其线性注意力的核心公式（Linformer 式低秩投影）：

\[ \mathbf{H} = \mathrm{softmax}\left( \frac{(\mathbf{X}\mathbf{W}_Q)(\mathbf{E}\mathbf{X}\mathbf{W}_K)^{\top}}{\sqrt{k}} \right)(\mathbf{F}\mathbf{X}\mathbf{W}_V) \]

其中 \(\mathbf{E} \in \mathbb{R}^{N \times d}\)、\(\mathbf{F} \in \mathbb{R}^{d \times N}\)（\(d \ll N\)），注意力图由 \(N \times N\) 压缩为 \(N \times d\)。"""

pat = re.compile(r"其线性注意力的核心公式.*?压缩为.*?。", re.S)
t2, n = pat.subn(lambda _: clean, t, count=1)
assert n == 1, "未找到损坏的公式块"
p.write_text(t2, encoding="utf-8")
print("[+] 公式块已用原始字符串重写")
print("[+] 校验无残留损坏:", "\\x0c" not in repr(t2) and "\\x0b" not in repr(t2))
