# -*- coding: utf-8 -*-
"""第二批伪公式 → LaTeX 转换（范数/损失/阶梯掩码等 12 处）。"""
import pathlib

P = pathlib.Path(r"C:\Users\ChengyeLin.LINOUP-XIAOXIN1\Desktop\work\paper-notes\docs\papers\2026-09")

PAIRS = {
    "0918-labram.md": [
        (r"`‖sg(ℓ2(p)) − ℓ2(v_z)‖²`",
         r"\( \left\| \mathrm{sg}(\ell_2(p)) - \ell_2(v_{z_i}) \right\|_2^2 \)"),
        (r"`‖ℓ2(p) − sg(ℓ2(v_z))‖²`",
         r"\( \left\| \ell_2(p) - \mathrm{sg}(\ell_2(v_{z_i})) \right\|_2^2 \)"),
        (r"`N = C·⌊t/w⌋`",
         r"\( N = C \cdot \lfloor t / w \rfloor \)"),
    ],
    "0918-eegpt.md": [
        (r"`H(d_φ(z), x⊙(1−M))`",
         r"\( \mathcal{H}(d_\phi(z),\ x \odot (1-M)) \)"),
        (r"`H(z, f_θ(x))`",
         r"\( \mathcal{H}(z,\ f_\theta(x)) \)"),
        (r"`token_{i,j} = Embed(p_{i,j}) + ς_i`",
         r"\( \mathrm{token}_{i,j} = \mathrm{Embed}(p_{i,j}) + \varsigma_i \)"),
        (r"`L_A = −(1/N) Σ ‖pred_j, LN(menc_j)‖²`",
         r"\( \mathcal{L}_A = -\tfrac{1}{N} \sum_{j=1}^{N} \left\| \mathrm{pred}_j,\ \mathrm{LN}(\mathrm{menc}_j) \right\|_2^2 \)"),
        (r"`L_R = −(1/|M|) Σ ‖rec_{i,j}, LN(p_{i,j})‖²`",
         r"\( \mathcal{L}_R = -\tfrac{1}{|\mathcal{M}|} \sum_{(i,j) \in \mathcal{M}} \left\| \mathrm{rec}_{i,j},\ \mathrm{LN}(p_{i,j}) \right\|_2^2 \)"),
        (r"`L = L_A + L_R`",
         r"\( \mathcal{L} = \mathcal{L}_A + \mathcal{L}_R \)"),
    ],
    "0918-neurolm.md": [
        (r"`p(I_11,...,I_CT) = Π_t p(I_1n,...,I_Cn | h_11,...,h_{C(t−1)})`",
         r"\( p(I_{11}, \ldots, I_{CT}) = \prod_{t=1}^{T} p(I_{1t}, \ldots, I_{Ct} \mid h_{11}, \ldots, h_{C(t-1)}) \)"),
        (r"`min L1 + λ Σ d_i log C(h_i)`",
         r"\( \min \mathcal{L}_1 + \lambda \sum_i d_i \log C(h_i) \)"),
    ],
    "0918-biot.md": [
        (r"`Z = BIOT(S)`，`Z̃ = predictor(BIOT(S̃))`",
         r"\( Z = \mathrm{BIOT}(S) \)，\( \tilde{Z} = \mathrm{predictor}(\mathrm{BIOT}(\tilde{S})) \)"),
    ],
    "0918-tfm-tokenizer.md": [
        (r"`L_token = Σ‖S(f,t) − Ŝ(f,t)‖² (掩码重构) + α Σ‖sg[E_i] − v_i‖² (codebook) + β Σ‖E_i − sg[v_i]‖² (commitment)`",
         r"\[ \mathcal{L}_{\mathrm{token}} = \underbrace{\sum_{(f,t)} \left\| S(f,t) - \hat{S}(f,t) \right\|_2^2}_{\text{掩码重构}} \;+\; \underbrace{\alpha \sum_i \left\| \mathrm{sg}[E_i] - v_i \right\|_2^2}_{\text{codebook}} \;+\; \underbrace{\beta \sum_i \left\| E_i - \mathrm{sg}[v_i] \right\|_2^2}_{\text{commitment}} \]"),
    ],
}

ok, miss = 0, []
for fname, pairs in PAIRS.items():
    f = P / fname
    t = f.read_text(encoding="utf-8")
    for old, new in pairs:
        if old in t:
            t = t.replace(old, new, 1)
            ok += 1
        else:
            miss.append((fname, old[:50]))
    f.write_text(t, encoding="utf-8")

print(f"[+] 转换 {ok} 处")
if miss:
    print("[!] 未命中:")
    for f, s in miss:
        print("   ", f, s)
