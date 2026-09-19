# -*- coding: utf-8 -*-
"""把 12 处反引号伪公式转换为真正的 LaTeX（arithmatex 渲染）。"""
import pathlib

P = pathlib.Path(r"C:\Users\ChengyeLin.LINOUP-XIAOXIN1\Desktop\work\paper-notes\docs\papers\2026-09")

PAIRS = {
    "0918-braingpt.md": [
        (r"`x_i^e ∈ R^{T×D}`", r"\( x_i^e \in \mathbb{R}^{T \times D} \)"),
        (r"`V ∈ R^{E×D}`", r"\( \mathcal{V} \in \mathbb{R}^{E \times D} \)"),
        (r"`L(θ) = (1/T) Σ ρ(x_i^e[t] − ETE(x_i^e[≤t]))`",
         r"\( \mathcal{L}(\theta) = \tfrac{1}{T} \sum_{t=1}^{T} \rho\!\left( x_i^e[t] - \mathrm{ETE}(x_i^e[\le t]) \right) \)"),
        (r"`z_j ∈ R^{E_j×D}`", r"\( z_j \in \mathbb{R}^{E_j \times D} \)"),
        (r"`G ∈ R^{E×D}`", r"\( \mathcal{G} \in \mathbb{R}^{E \times D} \)"),
    ],
    "0918-neurolm.md": [
        (r"`V ∈ R^{K×D}`", r"\( \mathcal{V} \in \mathbb{R}^{K \times D} \)"),
        (r"`λ = 2/(1+e^{−10t/T}) − 1`",
         r"\( \lambda = \tfrac{2}{1+e^{-10t/T}} - 1 \)"),
    ],
    "0918-labram.md": [
        (r"`X ∈ R^{C×T}`", r"\( X \in \mathbb{R}^{C \times T} \)"),
        (r"`V ∈ R^{K×D}`", r"\( \mathcal{V} \in \mathbb{R}^{K \times D} \)"),
    ],
    "0918-biot.md": [
        (r"`X ∈ R^{N×l}`", r"\( X \in \mathbb{R}^{N \times l} \)"),
    ],
    "0918-eegpt.md": [
        (r"`ACC = (33.6·N)^0.029`", r"\( \mathrm{ACC} = (33.6 \cdot N)^{0.029} \)"),
        (r"`L_R = (0.72·N)^{−0.014}`", r"\( \mathcal{L}_R = (0.72 \cdot N)^{-0.014} \)"),
    ],
}

for fname, pairs in PAIRS.items():
    f = P / fname
    t = f.read_text(encoding="utf-8")
    for old, new in pairs:
        if old in t:
            t = t.replace(old, new, 1)
            print(f"[+] {fname}: {old[:36]}... → LaTeX")
        else:
            print(f"[!] 未命中 {fname}: {old[:40]}")
    f.write_text(t, encoding="utf-8")
