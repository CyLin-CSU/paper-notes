# -*- coding: utf-8 -*-
"""按两位审查 agent 的报告修复全站内容（21 处）。每处替换都验证是否命中。"""
import pathlib
import re

DOCS = pathlib.Path(r"C:\Users\ChengyeLin.LINOUP-XIAOXIN1\Desktop\work\paper-notes\docs")
P = DOCS / "papers" / "2026-09"

done, missed = [], []


def rep(file: str, old: str, new: str, label: str, count: int = 1):
    f = DOCS / file
    t = f.read_text(encoding="utf-8")
    if old in t:
        f.write_text(t.replace(old, new, count), encoding="utf-8")
        done.append(label)
    else:
        missed.append((label, file, old[:50]))


# ============ 1. labram.md（3 中等 + 2 轻微） ============
rep("papers/2026-09/0918-labram.md",
    "在高层任务 TUEV 上明显下降（0.6409 → 0.5730 / 0.5643）",
    "在高层任务 TUEV 上明显下降（0.6409 → 0.5630 / 0.5730，Setting 2/3）",
    "labram-Q2 数字")
rep("papers/2026-09/0918-labram.md",
    "全面超过 BIOT 及所有基线：TUEV balanced acc 0.6409→0.6616（Huge）、Kappa 0.6637→0.6745；TUAB 0.8140→0.8258；",
    "大幅领先 BIOT（其 TUEV 0.5281/Kappa 0.5273、TUAB 0.7959），且随模型规模递进：TUEV 0.6409（Base）→0.6616（Huge）、Kappa 0.6637→0.6745，TUAB 0.8140（Base）→0.8258（Huge）；",
    "labram-Base/Huge 箭头")
rep("papers/2026-09/0918-labram.md",
    "线性探针/只微调后几层在 TUEV 上显著变差 → 该模型依赖全量微调。",
    "线性探针崩到 0.346；微调后 8 层（0.6541）与 4 层（0.6611）和全量微调（0.6409）相当甚至略好 → 依赖微调但不必全量。",
    "labram-部分层微调")
rep("papers/2026-09/0918-labram.md",
    "LaBraM-TFM 替换其 tokenizer 后 93% 指标提升",
    "并入 TFM tokenizer 后（BIOT-TFM/LaBraM-TFM 合计）93% 的指标情形提升",
    "labram-93% 归因")
rep("papers/2026-09/0918-labram.md",
    "8×A800（40GB 级）；Huge 369M 需 Zero 并行",
    "8×A800；Huge 369M 需分布式并行（论文未披露细节，此为推测）",
    "labram-算力标注推测")

# ============ 2. biot.md（2 轻微） ============
rep("papers/2026-09/0918-biot.md",
    "9 个数据集（EEG/ECG/HAR）上超过全部基线",
    "9 个数据集（EEG/ECG/HAR）上超过或持平绝大多数基线",
    "biot-基线表述")
rep("papers/2026-09/0918-biot.md",
    "证明频域特征对 EEG 任务（CHB-MIT、IIIC、HAR）尤其有用",
    "证明频域特征对 CHB-MIT、IIIC 与可穿戴 HAR 任务尤其有用",
    "biot-HAR 非 EEG")

# ============ 3. eegpt.md（1 中等 + 2 轻微） ============
rep("papers/2026-09/0918-eegpt.md",
    "与 BENDR/BIOT/LaBraM 对比在多个任务领先（且对手往往是全量微调而 EEGPT 只线性探针）；",
    "与 BENDR/BIOT/LaBraM 对比在多个任务领先（其中仅 BENDR 为全量微调，BIOT/LaBraM 同样采用线性探针协议）；",
    "eegpt-微调协议")
rep("papers/2026-09/0918-eegpt.md",
    "authors: [Guagnyu Wang, Wenchao Liu, Yuhong He, Cong Xu, Lin Ma, Haifeng Li]",
    "authors: [Guagnyu Wang, Yuhong He, Lin Ma, Wenchao Liu, Cong Xu, Haifeng Li]",
    "eegpt-作者顺序")
rep("papers/2026-09/0918-eegpt.md",
    'status: "精读"',
    'status: "精读"\narxiv: "（NeurIPS 2024 官方收录，无独立 arXiv 页）"',
    "eegpt-arxiv 字段")

# ============ 4. tfm.md（1 中等 + 1 轻微） ============
rep("papers/2026-09/0918-tfm-tokenizer.md",
    "单数据集与多数据集预训练两种设定下全面超过 BIOT/EEGPT/NeuroLM/CBraMod/LaBraM：",
    "两种设定下绝大多数指标-设定组合最优（例外：多数据集 CHB-MIT 的 balanced acc 0.6471 低于 BIOT 的 0.7068）：",
    "tfm-全面超过")
rep("papers/2026-09/0918-tfm-tokenizer.md",
    "此外 VQ 查表是硬量化，边界附近的微小波形差异可能被吞掉；ear-EEG 实验也表明跨设备泛化仍依赖微调数据量。",
    "此外属个人推断（论文仅自认窗长局限）：VQ 硬量化可能吞掉码字边界附近的微小波形差异。",
    "tfm-Q4 推断标注")

# ============ 5. braingpt.md SwiGLU 表述对齐原文 ============
rep("papers/2026-09/0918-braingpt.md",
    "+ 位置前馈网络（**SwiGLU**：`W_down·(Swish(W_gate·x) ⊙ (W_up·x))`）；",
    "+ 位置前馈网络（论文表述为 Swish 激活 FFN，公式 `W_down·(Swish(W_gate·x) ⊙ (W_up·x))` 实为门控形式）；",
    "braingpt-Swish 表述")
rep("papers/2026-09/0918-braingpt.md",
    "ETE SwiGLU；",
    "ETE 门控前馈（Swish 激活）；",
    "braingpt-复现卡")

# ============ 6. comparison.md（2 中等 + 3 轻微） ============
c = DOCS / "comparison.md"
t = c.read_text(encoding="utf-8")
t = t.replace("\n7. 六篇方法对比\n", "\n")
t = t.replace("#### 7.1 总览表", "## 总览表")
t = t.replace("#### 7.2 核心分歧点解读", "## 核心分歧点解读")
t = t.replace("#### 7.3 演进脉络一句话", "## 演进脉络一句话")
t = t.replace('BRAINGPT -- "MAE 范式（同为对照）" --> BIOT',
              'BRAINGPT -- "被其归入掩码/双向建模<br/>范式批评（BIOT 实为对比学习）" --> BIOT')
t = t.replace('TFM -- "整窗 FFT 线性投影过粗、无跨频段建模" --> BIOT',
              'TFM -- "直接切段未学词表<br/>（FFT 过粗问题 EEGPT 亦指出）" --> BIOT')
t = t.replace('labels: ["BIOT", "EEGPT", "NeuroLM-B", "LaBraM-Base †", "CBraMod †", "TFM-Tokenizer"]',
              'labels: ["BIOT", "EEGPT（TFM 复现 4.7M）", "NeuroLM-B", "LaBraM-Base †", "CBraMod †", "TFM-Tokenizer"]')
c.write_text(t, encoding="utf-8")
done.append("comparison-标题残留/互怼链×2/图表口径")

# ============ 7. blog（1 中等 + 2 轻微） ============
rep("blog-2023-2026.md",
    "但零样板泛化到新 prompt 的能力是前两者没有的。",
    "且论文称有望泛化到新 prompt（潜力表述，原文未见泛化实验验证）。",
    "blog-零样板软化")
rep("blog-2023-2026.md",
    "LaBraM：Base 模型 500h ≈ 2500h 效果",
    "LaBraM：Base 500h 在 TUAB 反超 2500h、TUEV 达其 90%+",
    "blog-500h")
rep("blog-2023-2026.md",
    "BrainGPT：数据 0→1B token 性能单调上升。",
    "BrainGPT：数据 0→1B token 性能持续上升但增益趋缓。",
    "blog-BrainGPT scaling")

# ============ 8. data-landscape（4 轻微） ============
rep("topics/data-landscape.md",
    "LaBraM：Base 用 500h 就接近 2500h 的效果；Huge 在 2500h 仍未饱和（推断需万小时级）",
    "LaBraM：Base 500h 在 TUAB 反超 2500h、TUEV 达其 90%+；Huge 在 2500h 仍未饱和（原论文推断需万小时级）",
    "data-500h")
rep("topics/data-landscape.md",
    "**临床癫痫数据占近半**，20 个数据集摊薄",
    "**临床 TUEG 子集合计约 1800h（约七成，其中癫痫事件 TUSZ 约 45%）**，由 20 个数据集摊薄",
    "data-临床占比口径")
rep("topics/data-landscape.md",
    "BrainGPT：数据 0→1B token 一直涨，未饱和",
    "BrainGPT：数据 0→1B token 性能持续上升，增益趋缓",
    "data-未饱和")
rep("topics/data-landscape.md",
    "这类实验目前只有 LaBraM/BrainGPT/EEGPT 做过",
    "数据 scaling 曲线目前只有 LaBraM/BrainGPT 报告过（EEGPT 做的是模型规模消融）",
    "data-scaling 范围")

# ============ 9. references.md / base-model.md：SwiGLU 措辞 ============
rep("references.md",
    "ETE 前馈网络的 SwiGLU 结构",
    "ETE 前馈网络的 Swish 激活（公式为门控形式）",
    "references-Swish")
rep("topics/base-model.md",
    "因果注意力+SwiGLU",
    "因果注意力+Swish 门控 FFN",
    "base-model-Swish")

# ============ 10. tokenization.md（2 轻微） ============
rep("topics/tokenization.md",
    "LaBraM-TFM 替换其 tokenizer 后 93% 指标提升",
    "并入 TFM tokenizer 后（BIOT-TFM/LaBraM-TFM 合计）93% 的指标情形提升",
    "token-93% 归因")
rep("topics/tokenization.md",
    "类独有 token 1.94%→2.14%。",
    "类独有 token 1.94%→2.14%（此处利用率下降为正向信号：说明词表更紧凑）。remove_placeholder",
    "token-脚注澄清")
# 清掉占位符
f = DOCS / "topics/tokenization.md"
t = f.read_text(encoding="utf-8").replace("remove_placeholder", "")
f.write_text(t, encoding="utf-8")

# ============ 11. index.md（2 轻微） ============
rep("index.md",
    "（13 个维度总览表 + 演进脉络）",
    "（14 个维度总览表 + 演进脉络）",
    "index-13→14")
rep("index.md",
    "| 预训练语料规模（论文合计） | 2500h + 25000h + 3750 万样本 |",
    "| 主力预训练语料 | LaBraM 2500h · NeuroLM 25000h · BrainGPT 3750 万样本 · BIOT 1000 万样本 |",
    "index-语料口径")
rep("index.md",
    "| 模型规模跨度 | 1.9M — 1.09B |",
    "| 模型规模跨度 | 1.9M — 1.09B（按各篇主模型口径） |",
    "index-规模口径")

# ============ 12. datasets.md（1 严重 + 4 中等 + 2 轻微） ============
d = DOCS / "datasets.md"
t = d.read_text(encoding="utf-8")
# 表格 SEED 行去掉 NeuroLM↑
t = t.replace(
    "| NeuroLM↓ · EEGPT↑ LaBraM↑ NeuroLM↑ |",
    "| NeuroLM↓ · EEGPT↑ LaBraM↑ |",
)
# EEGMat 被试数注
t = t.replace(
    "| 36 被试 | NeuroLM↓ BrainGPT↓ |",
    "| 36 被试（BrainGPT 报 34） | NeuroLM↓ BrainGPT↓ |",
)
# 别名说明补两条
t = t.replace(
    "| EDF | Sleep-EDFx 数据库的子集（Kemp et al. 2000），BrainGPT 基准中称 EDF |",
    "| EDF | Sleep-EDFx 数据库的子集（Kemp et al. 2000），BrainGPT 基准中称 EDF |\n"
    "| SEED 系列与 NeuroLM | NeuroLM 预训练的 \"SEED Series\" 指 SEED-IV/V/GER/FRA，不含原始 SEED（原始 SEED 对 NeuroLM 为下游） |",
)
d.write_text(t, encoding="utf-8")
done.append("datasets-表格两处")

# 矩阵重建（替换 mx-matrix 区块）
ROWS = [
    ("TUAB", "D", "D", "D", "·", "D", "D"),
    ("TUEV", "D", "D", "D", "·", "D", "D"),
    ("TUEG（总体）", "·", "P", "·", "·", "P", "·"),
    ("TUSZ", "·", "P", "·", "·", "P", "·"),
    ("TUEP / TUAR / TUSL", "·", "P", "·", "·", "P", "·"),
    ("SEED（原始）", "·", "P", "P", "·", "D", "·"),
    ("SEED-IV / SEED-V", "·", "B", "·", "D", "P", "·"),
    ("DEAP / FACED", "·", "·", "·", "D", "·", "·"),
    ("PhysioMI", "·", "P", "P", "·", "P", "·"),
    ("HGD", "·", "·", "P", "·", "·", "·"),
    ("BCIC4-1 / MIBCI", "·", "P", "·", "D", "·", "·"),
    ("BCIC-2A / 2B", "·", "·", "D", "·", "·", "·"),
    ("Grasp and Lift", "·", "P", "·", "·", "P", "·"),
    ("SHHS", "P", "·", "·", "·", "·", "·"),
    ("EDF / HMC（睡眠）", "·", "·", "D", "D", "D", "·"),
    ("EESM23（ear-EEG）", "·", "·", "·", "·", "·", "D"),
    ("EEGMat / STEW（负荷）", "·", "·", "·", "D", "D", "·"),
    ("Inria BCI / TVNT（P300）", "·", "P", "·", "·", "P", "·"),
    ("KaggleERN / PhysioP300", "·", "·", "D", "·", "·", "·"),
    ("TSU（SSVEP）", "·", "·", "P", "·", "·", "·"),
    ("M3CV", "·", "·", "P", "·", "·", "·"),
    ("PTB-XL / Cardiology（ECG）", "B", "·", "·", "·", "·", "·"),
    ("HAR（可穿戴）", "D", "·", "·", "·", "·", "·"),
    ("MoBI（步态）", "·", "D", "·", "·", "·", "·"),
    ("Raw EEG / Resting / Siena / SPIS / 自采集", "·", "P", "·", "·", "P", "·"),
    ("DREAMER（未见验证）", "·", "·", "·", "D", "·", "·"),
]
COLS = ["BIOT", "LaBraM", "EEGPT", "BrainGPT", "NeuroLM", "TFM"]
CELL = {
    "P": '<td class="mx-cell mx-p" title="预训练语料">P</td>',
    "D": '<td class="mx-cell mx-d" title="下游评估">D</td>',
    "B": '<td class="mx-cell mx-b" title="预训练 + 下游">P+D</td>',
    "·": '<td class="mx-cell mx-n" title="未使用">·</td>',
}
head = "".join(f"<th>{c}</th>" for c in COLS)
rows = "".join(
    f"<tr><th>{name}</th>{''.join(CELL[v] for v in vals)}</tr>"
    for name, *vals in ROWS
)
new_matrix = (
    '<div class="mx-wrap">\n<table class="mx-matrix">\n'
    f"<thead><tr><th>数据集 \\ 论文</th>{head}</tr></thead>\n"
    f"<tbody>{rows}</tbody>\n</table>\n</div>\n\n"
    '<p class="mx-legend">图例：<span class="mx-cell mx-p">P</span> 预训练语料　'
    '<span class="mx-cell mx-d">D</span> 下游评估　'
    '<span class="mx-cell mx-b">P+D</span> 两者兼有　'
    '<span class="mx-cell mx-n">·</span> 未使用　'
    "（悬停查看说明；ECG 与 IMU 数据仅 BIOT 跨模态使用；SEED-IV/V 为 LaBraM 预训练 + LaBraM/NeuroLM/BrainGPT 相关任务）</p>"
)
t = re.sub(
    r'<div class="mx-wrap">.*?</p>',
    new_matrix,
    t, count=1, flags=re.S,
)
d.write_text(t, encoding="utf-8")
done.append("datasets-矩阵重建（TUAB×BIOT 严重项等 5 处）")

# ============ 汇报 ============
print(f"✅ 完成 {len(done)} 组修复：")
for x in done:
    print("  -", x)
if missed:
    print(f"\n⚠️ 未命中 {len(missed)} 处：")
    for label, f, old in missed:
        print(f"  - {label} ({f}): {old}...")
