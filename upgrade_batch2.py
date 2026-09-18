# -*- coding: utf-8 -*-
"""大升级批处理：benchmark 表、批判链图、复现速查卡、相关阅读导航。"""
import pathlib

DOCS = pathlib.Path(r"C:\Users\ChengyeLin.LINOUP-XIAOXIN1\Desktop\work\paper-notes\docs")
PAPERS = DOCS / "papers" / "2026-09"

# ---------- 1. 对比页：benchmark 战绩表 + 批判链 ----------
p = DOCS / "comparison.md"
t = p.read_text(encoding="utf-8")

benchmark = """
## 🏆 跨论文 Benchmark 战绩表

所有数字均引自各论文自报结果（⚠️ 各论文预处理/数据划分存在差异，仅作量级参考）。`—` 表示该论文未报告该任务。

### TUAB（异常检测 · Balanced Accuracy）

| 模型 | Balanced Acc. | AUROC | 出处 |
|---|---|---|---|
| BIOT（多数据集预训练） | 0.7959 | 0.8815 | BIOT Table 4 |
| LaBraM-Huge | **0.8258** | **0.9162** | LaBraM Table 1 |
| EEGPT（linear probing, 25M） | 0.7983 | 0.8718 | EEGPT Table 2 |
| NeuroLM-XL（多任务） | 0.7969 | 0.7884 | NeuroLM Table 2 |
| BrainGPT-Giant | — | — | 未评测 |
| TFM-Tokenizer | 0.8032 | 0.8870 | TFM Table 1 |

### TUEV（事件分类）

| 模型 | Balanced Acc. | Cohen's Kappa | 出处 |
|---|---|---|---|
| BIOT（多数据集预训练） | 0.5281 | 0.5273 | BIOT Table 5 |
| LaBraM-Huge | 0.6616 | 0.6745 | LaBraM Table 2 |
| EEGPT（linear probing, 25M） | 0.6232 | 0.6351 | EEGPT Table 3 |
| NeuroLM-XL（多任务） | 0.4679 | 0.4570 | NeuroLM Table 2 |
| BrainGPT-Giant | — | — | 未评测 |
| TFM-Tokenizer | **0.5974** | **0.6189** | TFM Table 1 |

### 其他任务代表成绩

| 模型 | 任务与成绩 |
|---|---|
| LaBraM-Huge | SEED-V acc 0.4102；MoBI R² 0.3145 |
| NeuroLM-XL | TUSL balanced acc 0.6845；SEED balanced acc 0.6034 |
| BrainGPT-Giant | 12 基准 generalist：SS +11.2% / MW +8.5% / MI +6.05%（相对最优 specialist） |
| TFM-Tokenizer | IIIC Kappa 0.4979（+36% vs LaBraM）；CHB-MIT AUROC 0.8839；ear-EEG Kappa 0.3883（+14%） |

!!! note "数据快照"
    本表数字整理于 **2026-09-19**。新论文入库时请在对应行追加，并更新此日期。

## 🔗 论文互怼链

箭头方向 = 批评/改进指向。每条边标注批评点。

```mermaid
flowchart LR
    BIOT["BIOT<br/>2023"]:::old
    LABRAM["LaBraM<br/>2024"]:::mid
    EEGPT["EEGPT<br/>2024"]:::mid
    BRAINGPT["BrainGPT<br/>2024"]:::mid
    NEUROLM["NeuroLM<br/>2025"]:::new
    TFM["TFM-Tokenizer<br/>2026"]:::new

    TFM -- "token 只当训练目标、<br/>推理时丢弃" --> LABRAM
    TFM -- "整窗 FFT 线性投影<br/>过粗、无跨频段建模" --> BIOT
    EEGPT -- "FFT 只留能量丢相位，<br/>时域任务（P300/ERN）弱" --> BIOT
    BRAINGPT -- "MAE 双向补全破坏<br/>时序因果结构（-2%+）" --> LABRAM
    BRAINGPT -- "MAE 范式（同为对照）" --> BIOT
    NEUROLM -- "重构相位贡献小，<br/>砍掉相位只留幅值+时域" --> LABRAM
    NEUROLM -- "逐任务全量微调低效，<br/>无多任务推理" --> LABRAM
    TFM -- "固定空间 embedding<br/>无法跨设备（ear-EEG 缺席）" --> EEGPT

    classDef old fill:#eceff1,stroke:#90a4ae,color:#263238
    classDef mid fill:#fff3e0,stroke:#ffb74d,color:#3e2723
    classDef new fill:#e8f5e9,stroke:#66bb6a,color:#1b5e20
```

**解读**：BIOT 是公共对照组；LaBraM 承接其位置但转向离散码；EEGPT 坚持连续表示但改进自监督目标；BrainGPT 掀翻掩码范式；NeuroLM 把 token 接入 LLM；TFM 对前作做"输入表示"的终审。完整论述见各篇笔记的「与其他论文的关系」与「自问自答」板块。
"""
t = t.rstrip() + "\n" + benchmark
p.write_text(t, encoding="utf-8")
print("[+] comparison.md：benchmark 表 + 互怼链")

# ---------- 2. 每篇：复现速查卡 ----------
REPRO = {
    "0918-biot.md": """!!! abstract "复现速查卡"
    - **代码**：[github.com/ycq091044/BIOT](https://github.com/ycq091044/BIOT)（PyTorch Lightning 1.6.4 / Torch 1.13.1）
    - **关键超参**：4 层 Transformer × 8 头；低秩投影 d≪N；token 1s/重叠 0.5s；EEG 重采样 200Hz；Adam lr=1e-3；温度 T=0.2（无监督预训练）
    - **数据**：预训练 PREST+SHHS（约 1000 万样本，SHHS 需在 sleepdata.org 申请）；16 个标准双极导联
    - **算力参考**：8×RTX A6000，单任务训练 max epoch 100
""",
    "0918-labram.md": """!!! abstract "复现速查卡"
    - **代码**：[github.com/935963004/LaBraM](https://github.com/935963004/LaBraM)（PyTorch 2.0.1 + CUDA 11.8）
    - **关键超参**：码本 8192×64；patch 200 点（1s）；掩码率 0.5 + 对称掩码；Base 5.8M（12 层/200 维/10 头）；lr 5e-4 cosine；EMA 0.996；温度未用于掩码（交叉熵）
    - **数据**：约 2500h / 20 数据集（TUSZ 1138h 为主力）；下游 TUAB/TUEV 划分严格沿用 BIOT
    - **算力参考**：8×A800（40GB 级）；Huge 369M 需 Zero 并行
""",
    "0918-eegpt.md": """!!! abstract "复现速查卡"
    - **代码**：[github.com/BINE022/EEGPT](https://github.com/BINE022/EEGPT)
    - **关键超参**：58 电极 / 256Hz / 输入 4s；patch 64 点（250ms）；掩码 50% 时间 × 80% 通道；momentum 动量 0.01；最优变体 large：d=512、8 层、4 个 summary token；AdamW OneCycle（2.5e-4 起）
    - **数据**：预训练 PhysioMI + HGD + TSU + SEED + M3CV；下游 7 数据集
    - **算力参考**：8×RTX 3090，200 epochs，bf16；下游只训线性层所以极轻
""",
    "0918-braingpt.md": """!!! abstract "复现速查卡"
    - **代码**：论文声明将开源（截至精读时未见仓库，复现前先确认）
    - **关键超参**：电极词表覆盖 E 个电极；patch 1s × D 采样点；ETE SwiGLU；预训练 lr 1e-4 / 3 epochs / batch 4096；微调 10 epochs（ETE 冻结，只训 TEG）；DeepSpeed Zero2/3 + bf16
    - **数据**：3750 万单电极样本（≈1B token），来自 12 个基准的预训练拆分
    - **算力参考**：8×A800-80G；Giant 1.09B 需 Zero3 + 梯度检查点
""",
    "0918-neurolm.md": """!!! abstract "复现速查卡"
    - **代码**：[github.com/935963004/NeuroLM](https://github.com/935963004/NeuroLM)（PyTorch 2.2.2 + CUDA 12.1）
    - **关键超参**：GPT-2 基座（B/L/XL = 254M/500M/1696M）；码本 8192×128；序列最长 1024（短则零填充+掩码注意力）；patch 200 点；GRL 系数 λ 从 0 渐增；推理取 argmax 而非 beam search
    - **数据**：约 25000h（TUEG ~24000h 为主力）；每批混入少量纯文本防遗忘
    - **算力参考**：8×A100-80G
""",
    "0918-tfm-tokenizer.md": """!!! abstract "复现速查卡"
    - **代码**：[github.com/Jathurshan0330/TFM-Tokenizer](https://github.com/Jathurshan0330/TFM-Tokenizer)（含预训练权重与全部预处理脚本）
    - **关键超参**：tokenizer ~1.2M + 下游 ~0.7M；STFT 窗 200 点/Hann/hop 100；码本 8192；token embedding 64；频带掩码率 0.5 + 时间掩码 + 对称掩码；tokenizer 内**无位置编码**；Ray Tune + Optuna 调参
    - **数据**：TUEV/TUAB/CHB-MIT/IIIC（遵循 BIOT 划分）；跨设备 EESM23
    - **算力参考**：无 GPU 规模要求披露——tokenizer 极小，消费级单卡可训
""",
}
for fname, card in REPRO.items():
    fp = PAPERS / fname
    t = fp.read_text(encoding="utf-8")
    if "复现速查卡" in t:
        continue
    t = t.rstrip() + "\n\n" + card + "\n"
    fp.write_text(t, encoding="utf-8")
    print("[+] 复现速查卡:", fname)

# ---------- 3. 每篇：相关阅读导航 ----------
ORDER = [
    ("0918-biot.md", "BIOT", "papers/2026-09/0918-biot.md"),
    ("0918-labram.md", "LaBraM", "papers/2026-09/0918-labram.md"),
    ("0918-eegpt.md", "EEGPT", "papers/2026-09/0918-eegpt.md"),
    ("0918-braingpt.md", "BrainGPT", "papers/2026-09/0918-braingpt.md"),
    ("0918-neurolm.md", "NeuroLM", "papers/2026-09/0918-neurolm.md"),
    ("0918-tfm-tokenizer.md", "TFM-Tokenizer", "papers/2026-09/0918-tfm-tokenizer.md"),
]
for i, (fname, name, _) in enumerate(ORDER):
    fp = PAPERS / fname
    t = fp.read_text(encoding="utf-8")
    if "相关阅读" in t:
        continue
    prev = ORDER[(i - 1) % len(ORDER)]
    nxt = ORDER[(i + 1) % len(ORDER)]
    nav = (
        f"\n---\n\n**相关阅读**\n\n"
        f":material-arrow-left: [上一篇：{prev[1]}]({prev[2]}) ｜ "
        f":material-arrow-right: [下一篇：{nxt[1]}]({nxt[2]}) ｜ "
        f":material-vector-link: [Tokenization 演进](../../topics/tokenization.md) ｜ "
        f":material-chart-box: [战绩总表](../../comparison.md#跨论文-benchmark-战绩表)\n"
    )
    t = t.rstrip() + "\n" + nav
    fp.write_text(t, encoding="utf-8")
    print("[+] 相关阅读:", fname)
