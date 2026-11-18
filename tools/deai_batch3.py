# -*- coding: utf-8 -*-
"""AI 味去痕批量执行：脚本 3/3 —— REVE / eegarena / tokenization（Agent C 清单）+ chen 模型计数。"""
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1] / "docs"

EDITS = [
    ("papers/fm/reve.md",
     "**decoder 不发布是行业先例**。MAE 的 decoder 能重构原始 EEG——等于自带一个「从表示反推脑信号」的工具，作者以隐私为由扣下 decoder 只放 encoder。EEG FM 论文第一次认真对待「重建能力的隐私面」，这个决定比成绩数字更值得被后来者记住。",
     "**decoder 不发布，理由是隐私**。MAE 的 decoder 能重构原始 EEG，等于提供从表示反推脑信号的工具；作者只放 encoder。这是站内 EEG FM 笔记里第一个以隐私为由限制发布的组件。"),
    ("papers/fm/reve.md",
     "**全局 token 二次损失是全文最可偷的组件**。实现只有 attention pooling + 两层 FFN，消融收益明确且机制清晰（信息瓶颈对抗末层过拟合）。任何做 MAE 式预训练、又在乎冻结特征的pipeline都值得加上——它和 EEGPT 的对齐损失、LUNA 的可见 patch 小系数一起，构成了「让预训练表示免微调可用」的三个独立方案；",
     "**全局 token 二次损失：实现小、消融收益明确**。只有 attention pooling + 两层 FFN，机制是信息瓶颈对抗末层过拟合。做 MAE 式预训练、在乎冻结特征的 pipeline 可以直接加上——它和 EEGPT 的对齐损失、LUNA 的可见 patch 小系数，构成三个独立的「冻结可用」方案；"),
    ("papers/fm/reve.md",
     "ISRUC 平衡精度 0.7819 略低于 CBraMod 0.7865，但 Kappa 0.7500 更高——且 REVE 修了基线代码里下巴电极混入的 bug（诚实细节 +1）。",
     "ISRUC 平衡精度 0.7819 略低于 CBraMod 0.7865，但 Kappa 0.7500 更高——且 REVE 修了基线代码里下巴电极混入的 bug。"),
    ("papers/fm/reve.md",
     "这与 TFM 的频带掩码消融（结构化 > 随机 +8%）互为印证：掩码的结构要匹配信号的结构。",
     "TFM 的频带掩码消融（结构化 > 随机 +8%）方向相同：两类块掩码挖的都是信号的自相关冗余。"),
    ("papers/fm/reve.md",
     "哪种更可取取决于你信「架构先验」还是「数据先验」，这篇论文没有也不能替你回答，但它提供了两种来源贡献的同框对照（PhysioNet-MI 单任务）；",
     "架构先验和数据先验哪个更可取，这个消融回答不了；它给出的是两种来源贡献的同框对照（PhysioNet-MI 单任务）；"),
    ("papers/fm/reve.md",
     "REVE 在这个任务上用了 Euclidean Alignment 预处理（He & Wu 2019，基线都没用）——该预处理在 MI 任务上是公认的大杀器。",
     "REVE 在这个任务上用了 Euclidean Alignment 预处理（He & Wu 2019，基线都没用）——该预处理在 MI 任务上提升明显。"),
    ("papers/fm/reve.md",
     "**预训练价值消融是双刃剑**。", "**预训练价值消融可以反过来读**。"),
    ("papers/fm/reve.md",
     "消融的脚注说得很诚实：可学习 PE 变体在见过的配置上不差（0.701 vs 0.707），4D 编码的全部价值都在泛化侧；坐标加 0.25cm 噪声则是对电极摆放差异的显式建模。",
     "消融脚注给了对照数字：可学习 PE 变体在见过的配置上不差（0.701 vs 0.707），差距出在没见过的布局与更长序列；坐标加 0.25cm 噪声则是对电极摆放差异的显式建模。"),
    ("papers/fm/reve.md",
     "跨设定泛化是位置编码的兑现处：预训练只见 10s 段，ISRUC/HMC 的 30s 输入照常工作；TUEV 的双极蒙太奇训练里从未出现。",
     "位置编码的设计直接受跨设定泛化检验：预训练只见 10s 段，ISRUC/HMC 的 30s 输入照常工作；TUEV 的双极蒙太奇训练里从未出现。"),
    ("papers/fm/reve.md",
     "数据 scaling 曲线在 EEG 上仍然是稀缺品——这个问题保持开放。",
     "EEG 上还没有数据量 scaling 曲线，这个问题保持开放。"),
    ("papers/fm/reve.md",
     "正文按 §1 问题定位（montage 绑定为何是第一瓶颈）、§2 方法（4D 位置编码 / 块掩码 / 全局 token 损失 / 数据哲学）、§3 实验与结果（微调与线性探针、预训练价值消融）展开；语料规模、组件数字与表 3/表 4 口径在对应段落与文末复现速查卡中。",
     "组件消融数字见 §2 各小节，语料构成见 §2.5，复现参数见文末速查卡。"),
    ("papers/survey/eegarena.md",
     "## 1 问题定位:给 EEG FM 补一场有强对手的擂台赛",
     "## 1 问题定位:既有基准缺强基线，FM 排名混着归因"),
    ("papers/survey/eegarena.md",
     "两条排除规则很关键：预训练数据与下游数据直接重叠的结果被剔除出总排名",
     "两条排除规则：预训练数据与下游数据直接重叠的结果被剔除出总排名"),
    ("topics/tokenization.md",
     "各模型的代码地址、权重状态与参数口径统一由[模型对比页](../models.md)（数据源 `data/models.json`）维护，此处只保留与 tokenizer 复现直接相关的注释：",
     "代码地址、权重状态与参数口径的完整清单在[模型对比页](../models.md)（数据源 `data/models.json`）；这里只补与 tokenizer 复现相关的注释："),
    # 事实一致性（Agent B 范围外提示 a/b）
    ("papers/reviews/chen-representation-learning-review.md",
     "选出 19 个模型列表。", "选出 18 个模型（原文文字称 19，按其 Table 1 行数为 18）。"),
    ("papers/reviews/chen-representation-learning-review.md",
     "19 个模型按七个字段逐项拆开。", "18 个模型按七个字段逐项拆开。"),
    ("papers/reviews/chen-representation-learning-review.md",
     "把上表 19 个模型按字段聚族：", "把上表 18 个模型按字段聚族："),
    ("papers/reviews/chen-representation-learning-review.md",
     "预测 3 篇（Brant-2、EEGPT=站内 BrainGPT、Neuro-GPT、NeuroLM）、混合 1 篇（Brant-2）",
     "预测 3 篇（EEGPT=站内 BrainGPT、Neuro-GPT、NeuroLM）、混合 1 篇（Brant-2 同时做重构与预测）"),
    ("papers/reviews/chen-representation-learning-review.md",
     "19 模型组件拆解", "18 模型组件拆解"),
    ("papers/reviews/chen-representation-learning-review.md",
     "one-liner 中的 19 个 FM", "one-liner 中的 18 个 FM"),
]

done, fail = 0, []
files = {}
for rel, old, new in EDITS:
    path = ROOT / rel
    if rel not in files:
        files[rel] = path.read_text(encoding="utf-8")
    t = files[rel]
    if old in t:
        files[rel] = t.replace(old, new, 1)
        done += 1
    else:
        fail.append((rel, old[:60]))

for rel, t in files.items():
    (ROOT / rel).write_text(t, encoding="utf-8")
print(f"脚本3：成功 {done}/{len(EDITS)}")
for f, o in fail:
    print("  未命中：", f, "|", o)
