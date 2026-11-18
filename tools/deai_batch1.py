# -*- coding: utf-8 -*-
"""AI 味去痕批量执行：脚本 1/3 —— 站点级页面（Agent A 清单 18 条）。"""
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1] / "docs"

EDITS = [
    ("landscape-2026.md", "## 1 领域现状一句话", "## 1 领域现状"),
    ("landscape-2026.md", "**架构移植期已经结束，评测清算期刚刚开始。** 2021–2024 是把 BERT / MAE / GPT 范式搬进 EEG 的收编期",
     "2021–2024 是把 BERT / MAE / GPT 范式搬进 EEG 的收编期"),
    ("landscape-2026.md", "合成的结论是：**FM 的优势有条件（任务域、协议、数据规模），不是普适的**。",
     "综合这两项评测：FM 的优势取决于任务域、协议与数据规模。"),
    ("landscape-2026.md", "——凡做「冻结可用」主张的工作（[EEGPT](papers/fm/eegpt.md) 的对齐目标、[REVE](papers/fm/reve.md) 的全局 token 瓶颈）都是在对着这个观察设计，其普遍性尚待更大范围验证。",
     "——做「冻结可用」主张的工作（[EEGPT](papers/fm/eegpt.md) 的对齐目标、[REVE](papers/fm/reve.md) 的全局 token 瓶颈）针对这个观察设计，其普遍性尚待更大范围验证。"),
    ("landscape-2026.md", "领域最大的悬而未决问题是「堆数据有没有用」。站内可核查的四组证据，口径各不相同，不能合并成一条曲线：",
     "「堆数据有没有用」是领域内尚无定论的问题。站内可核查的四组证据口径各不相同，不能合并成一条曲线："),
    ("landscape-2026.md", "三个观察（依据见对应笔记与综述）：\n\n", ""),
    ("landscape-2026.md", "这正是 §3 评测痛点（协议不可比）的直接代价。",
     "——即 §3 评测痛点（协议不可比）的直接代价。"),
    ("models.md", "**布局**一栏描述模型对电极配置的假设（固定 10-20 / ACPE 非绑定 / query 压缩 / 坐标生成），是跨数据集泛化能力的第一决定因素；",
     "**布局**一栏描述模型对电极配置的假设（固定 10-20 / ACPE 非绑定 / query 压缩 / 坐标生成），是影响跨数据集泛化的主要设计因素；"),
    ("blog-2023-2026.md", "**离散码字，三种角色。** 三篇选读把离散码字用在了三个不同位置：LaBraM（ICLR 2024）将离散码字用作掩码预测目标",
     "**离散码字，三种角色。** LaBraM（ICLR 2024）将离散码字用作掩码预测目标"),
    ("blog-2023-2026.md", "把这些行并排看：LaBraM 的曲线止于 2500h，EEGPT 的受控对照限于 BCIC-2A/2B，NeuroLM 的 2.5 万小时是单一临床体系的训练规模，EEGArena 是固定架构后的受控对照。各研究回答的问题不同，本选读范围内拼不出一条「多少小时才够」的通用曲线——2.5 万小时是 NeuroLM 的训练规模，不是领域上限。",
     "各研究的改动变量与评测条件不同，回答的问题也不同：LaBraM 的消融止于 2500h，EEGPT 的对照限于 BCIC-2A/2B，NeuroLM 的 2.5 万小时是单一临床体系的训练规模，EEGArena 是固定架构的受控对照——本选读范围内拼不出一条「多少小时才够」的通用曲线，2.5 万小时也不是领域上限。"),
    ("blog-2023-2026.md", "论文报告没有 RF 先验的通用 VLM 直接读谱图基本失败——「长得像图」不等于「有对应先验」。",
     "论文报告没有 RF 先验的通用 VLM 直接读谱图基本失败——谱图以图像形式呈现，模型缺的仍是射频领域先验。"),
    ("blog-2023-2026.md", "多任务的组织出现在两个不同阶段，分开看：", "多任务的组织出现在两个阶段："),
    ("blog-2023-2026.md", "论文如实报告性能仍逊于单任务 SOTA；", "论文报告性能仍逊于单任务 SOTA；"),
    ("blog-2023-2026.md", "各自做了什么取舍？对照读[Tokenization 专题](topics/tokenization.md)", "对照读[Tokenization 专题](topics/tokenization.md)"),
    ("comparison.md", "**维度小结**：模型设计的演进不是「更大」，而是**注意力计算图的形状逐渐匹配 EEG 的 (通道 × 时间) 结构**——每一步都在回答「哪些 patch 天生该互相看」。",
     "**维度小结**：本维度的共性问题是注意力计算图的形状如何匹配 EEG 的 (通道 × 时间) 结构。"),
    ("comparison.md", "**维度小结**：频域证据分篇看——TFM 在 tokenizer 内做频率轴注意力与频带掩码（其消融中频带掩码贡献最大）；CBraMod 在 patch embedding 加 rFFT 能量支路（消融：时+频 > 纯时 > 纯频）；LUNA 在 patch embedding 加 FFT 幅相支路并报告去掉后 AUROC 最多降 0.011–0.012。三家的消融各自支持频域支路在自己的任务与指标上有贡献，任务与协议不同，不构成跨研究的统一结论。",
     "**维度小结**：三家的消融各自支持频域支路在自己的任务与指标上有贡献——TFM 频带掩码贡献最大（其消融）、CBraMod 时+频 > 纯时 > 纯频、LUNA 去掉幅相支路 AUROC 最多降 0.011–0.012——任务与协议不同，不构成跨研究的统一结论。"),
    ("comparison.md", "**维度小结**：规模轴上被验证过的规律只有两条——**结构先验可以替代规模**（CBraMod 4M、TFM 1.9M、EEGMoE 1.68M），以及**效率在特定场景是硬需求**（LUNA 面向可穿戴、JET 面向实时生成）；「大模型 + 大数据」的 scaling 叙事在 EEG 上至今没有被干净地兑现",
     "**维度小结**：规模轴上被验证过的结果有两组——结构先验替代规模（CBraMod 4M、TFM 1.9M、EEGMoE 1.68M），以及效率型设计（LUNA 面向可穿戴、JET 面向实时生成）；「大模型 + 大数据」的 scaling 叙事在 EEG 上证据仍不完整"),
    ("index.md", "完整 **31 篇**可筛选目录见 **[论文库](library.md)**（类型 / 分组 / 年份 / 代码与 DOI 可用性筛选，链接可复现筛选状态）；按字段并排比较见 **[模型对比](models.md)**。",
     "完整 31 篇可筛选目录见 [论文库](library.md)（类型 / 分组 / 年份 / 代码与 DOI 可用性筛选，链接可复现筛选状态）；按字段并排比较见 [模型对比](models.md)。"),
]

done, fail = 0, []
files = {}
for fname, old, new in EDITS:
    path = ROOT / fname
    if fname not in files:
        files[fname] = path.read_text(encoding="utf-8")
    t = files[fname]
    if old in t:
        files[fname] = t.replace(old, new, 1)
        done += 1
    else:
        fail.append((fname, old[:50]))

for fname, t in files.items():
    (ROOT / fname).write_text(t, encoding="utf-8")
print(f"脚本1：成功 {done}/{len(EDITS)}")
for f, o in fail:
    print("  未命中：", f, "|", o)
