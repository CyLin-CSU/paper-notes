# -*- coding: utf-8 -*-
"""AI 味去痕批量执行：脚本 2/3 —— 四篇综述笔记（Agent B 清单，含事实一致性三条）。"""
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1] / "docs" / "papers" / "reviews"

EDITS = [
    # yao
    ("yao-eegfm-survey.md", "特色是**自己跑了对比实验**：10 个模型 × 6 个数据集，原论文报告值（彩色）与自跑补齐值（黑色）分开标注。",
     "对比实验为作者自跑：10 个模型 × 6 个数据集，原论文报告值（彩色）与自跑补齐值（黑色）分开标注。"),
    ("yao-eegfm-survey.md", "§3.5 是全文最有价值的论点：现有 FM 预训练基本被 TUEG 一类临床癫痫数据主导，与 MI / 情绪等下游范式差异大，形成域差；",
     "§3.5 讨论预训练语料与下游任务的域差：现有 FM 预训练基本被 TUEG 一类临床癫痫数据主导，与 MI / 情绪等下游范式差异大；"),
    ("yao-eegfm-survey.md", "另有一个次要观察：睡眠数据时长可观但通道少（2–6 导），因此很少被用作 FM 预训练主料。",
     "睡眠数据时长可观但通道少（2–6 导），因此很少被用作 FM 预训练语料。"),
    ("yao-eegfm-survey.md", "### 3.2 三条作者口径的观察\n\n**生成式**三分支", "### 3.2 掩码率、AR 取舍与同架构对照\n\n三条作者口径的观察：\n\n**生成式**三分支"),
    ("yao-eegfm-survey.md", "- **掩码率 ~50%**，低于图像的 75–90%——解释是 EEG 语义冗余低于图像，激进掩码会破坏基本时序模式；\n- **AR 与时序结构天然契合**但受非平稳、低 SNR 拖累，所以双向掩码（MAE 式）反而更常用；\n- **同架构对照**（BrainGPT，站内口径）：",
     "- 掩码率 ~50%，低于图像的 75–90%——解释是 EEG 语义冗余低于图像，激进掩码会破坏基本时序模式；\n- AR 与时序结构契合，但受非平稳、低 SNR 拖累，双向掩码（MAE 式）因此更常用；\n- 同架构对照（BrainGPT，站内口径）："),
    ("yao-eegfm-survey.md", "| 骨干 | encoder-only Transformer | 压倒性多数，~12 层 + 线性/MLP 头 |",
     "| 骨干 | encoder-only Transformer | 多数模型采用，~12 层 + 线性/MLP 头 |"),
    ("yao-eegfm-survey.md", "四个读数：\n\n- **临床域 FM 大胜**：TUAB/TUEV 领先者均为 FM（自跑口径 Neuro-GPT 领先、原报告口径 CBraMod 更高），作者归因于预训练域与癫痫数据同源；\n- **MI 全线失守**：EEGNet 两个数据集最高，BENDR 2a 仅 0.4899——低 SNR + 范式域差双重归因；\n- **中间地带**：LaBraM-Base / CBraMod 在 SleepEDFx、SEED-V 尚有竞争力，说明跨范式泛化并非不可能；\n- **成本注脚**：EEGNet 0.003M vs Neuro-GPT 56.6M——增益换参数，资源受限场景要另算账。",
     "- 临床域 FM 领先：TUAB/TUEV 领先者均为 FM（自跑口径 Neuro-GPT 领先、原报告口径 CBraMod 更高），作者归因于预训练域与癫痫数据同源；\n- MI 域 FM 落后：EEGNet 在两个数据集上最高，BENDR 2a 仅 0.4899——低 SNR 与范式域差双重归因；\n- LaBraM-Base / CBraMod 在 SleepEDFx、SEED-V 上尚有竞争力，跨范式泛化有正例；\n- 参数量差距大：EEGNet 0.003M vs Neuro-GPT 56.6M，资源受限场景需另行权衡。"),
    ("yao-eegfm-survey.md", "另有两处跨报告数值不一致被点名：", "另有多处跨报告数值不一致被点名："),
    ("yao-eegfm-survey.md", "§5 技术设计总表与 [Chen 综述的拆解表](chen-representation-learning-review.md) 互为印证——两表字段口径不同（本表含注意力机制与数据集，Chen 表含损失与开源信息），合读可互补。",
     "§5 技术设计总表与 [Chen 综述的拆解表](chen-representation-learning-review.md) 字段口径不同：本表含注意力机制与数据集附注，Chen 表含损失与开源信息，两表合读覆盖更全。"),
    # chen
    ("chen-representation-learning-review.md", "值得记的两个 trade-off：patching 让长记录在算力上可行，但**切段边界会破坏细粒度时序模式**——",
     "patching 让长记录在算力上可行，代价是切段边界破坏细粒度时序模式——"),
    ("chen-representation-learning-review.md", "同一模型放到安慰剂臂 r=−0.03——阴性对照做得很干净。",
     "同一模型放到安慰剂臂 r=−0.03，阴性对照符合预期。"),
    ("chen-representation-learning-review.md", "这篇更全景、批判更轻（「独立验证仍缺」一句带过）；", "这篇覆盖面更广、批判较少（「独立验证仍缺」一句带过）；"),
    ("chen-representation-learning-review.md", "词元化五分类是本站 [Tokenization 演进专题](../../topics/tokenization.md) 之外**轴最接近的现成对照**：它按「切段几何」分类，站内按「词表怎么来、用在哪」，写词元化节时先引后立。",
     "词元化五分类与本站 [Tokenization 演进专题](../../topics/tokenization.md) 口径最接近：它按「切段几何」分类，站内按「词表来源与用途」分类；写词元化节时先引该文分类，再给站内对照。"),
    ("chen-representation-learning-review.md", "可解释性一节 beyond attention：归因分析（积分梯度、SHAP）",
     "可解释性一节超出注意力可视化范畴：归因分析（积分梯度、SHAP）"),
    ("chen-representation-learning-review.md", "数据侧结论：TUEG 与 SEED 系是绝对主力；", "数据侧结论：TUEG 与 SEED 系被最多模型用作预训练语料；"),
    # kuruppu
    ("kuruppu-critical-review.md", "## 4 批判性结论（§5 的干货）", "## 4 批判性结论（原文 §5）"),
    ("kuruppu-critical-review.md", "模型间有三个数量级跨度值得注意：数据量 4.5k → 878k channel-hours（约 200 倍）、参数 3.3M（BIOT）→ 1.7B（NeuroLM，约 500 倍）、模态组合（纯头皮 6 / 纯颅内 2 / 双模态 2）。",
     "模型间数据量差约 200 倍（4.5k → 878k channel-hours），参数量差约 500 倍（3.3M → 1.7B），模态组合分纯头皮（6）/纯颅内（2）/双模态（2）三种。"),
    ("kuruppu-critical-review.md", "汇总读法：任务数 1（Mentality）到 12（BrainWave），多数 ≤5；4/10 在分布内评测；**只有 BrainWave 和 Brant 做过真正的 OOD 评测**。共享任务只有 TUAB 与 TUEV",
     "任务数从 1（Mentality）到 12（BrainWave），多数 ≤5；4/10 在分布内评测。跨分布的完整 OOD 评测仅 BrainWave 与 Brant（Neuro-GPT 为外部数据集、EEGFormer 为新生儿子集，均为部分设置，见上表）。共享任务只有 TUAB 与 TUEV"),
    ("kuruppu-critical-review.md", "- **Scaling 证据弱**：", "- Scaling 证据弱："),
    ("kuruppu-critical-review.md", "- **线性探针显著落后微调**：五个报告 LP 的模型全线弱于 FT 与部分监督基线；FT 又略胜从头监督——作者据此**质疑 SSL 学到的表示质量**：增益可能主要来自架构与初始化而非预训练知识。",
     "- 线性探针显著落后微调：五个报告 LP 的模型均弱于 FT 与部分监督基线，FT 又略胜从头监督。作者据此质疑 SSL 学到的表示质量：增益可能主要来自架构与初始化，预训练知识的贡献存疑。"),
    ("kuruppu-critical-review.md", "- **通用时序 FM 意外能打**：PatchTST / TimesNet 微调后在病理检测、睡眠分期可打平甚至超过 EEG FM；BrainWave 的实验里 MOMENT 在癫痫检测与病理检测超过 EEG FM。EEG 专属归纳偏置（空间建模、头皮+颅内联合）是 EEG FM 的反超点。",
     "- 通用时序 FM 在部分任务上可打平或超过 EEG FM：PatchTST / TimesNet 微调后在病理检测、睡眠分期可打平甚至超过 EEG FM；BrainWave 的实验里 MOMENT 在癫痫检测与病理检测超过 EEG FM。EEG FM 的相对优势点在 EEG 专属归纳偏置（空间建模、头皮+颅内联合预训练）。"),
    ("kuruppu-critical-review.md", "- **预处理普遍极简**：", "- 预处理普遍极简："),
    ("kuruppu-critical-review.md", "- **数据多样性 vs 数据量**：", "- 数据多样性 vs 数据量："),
    ("kuruppu-critical-review.md", "- LP 落后 FT 的观察对本站 [REVE](../fm/reve.md) 微调策略（缓存 LP → 小学习率 FT）是提醒而非定论：",
     "- LP 落后 FT 的观察与本站 [REVE](../fm/reve.md) 微调策略（缓存 LP → 小学习率 FT）相关："),
    ("kuruppu-critical-review.md", "- 本篇的批判清单与 [EEGArena](../survey/eegarena.md) 高度互补：文中呼吁的「共享核心任务 + OOD + 强监督基线」正是 EEGArena 已经做成的事，两篇可当「诊断书与药方」连读。",
     "- 本篇的批判清单与 [EEGArena](../survey/eegarena.md) 相互对应：文中呼吁的「共享核心任务 + OOD + 强监督基线」正是 EEGArena 已经做成的事，两篇可连读对照。"),
    # kwon
    ("kwon-neural-fm-perspective.md", "作者的总结论：三者 illustrate FM 架构能提升解码性能，但都属「第一代」",
     "作者的总结论：三者说明 FM 架构能提升解码性能，但都属「第一代」"),
    ("kwon-neural-fm-perspective.md", "三者共同点：编码的是**表面时序/空间相关**，不是深层神经生物学机制。",
     "三者共同点：编码的是表面时序/空间相关，未触及深层神经生物学机制。"),
    ("kwon-neural-fm-perspective.md", "价值在**议程**不在证据：全文无自家实验，是立场文章。但「电极拓扑 / MNI 投影 / 3D 坐标 PE」清单与站内 [LUNA](../fm/luna.md)、[REVE](../fm/reve.md) 的拓扑无关路线互相印证——方向共识已在，差距在没人把三原则同时做进一个预训练管线。",
     "全文无自家实验，属立场文章，增量在设计清单：「电极拓扑 / MNI 投影 / 3D 坐标 PE」与站内 [LUNA](../fm/luna.md)、[REVE](../fm/reve.md) 的拓扑无关路线互相印证；三原则尚无人在同一预训练管线中同时实现。"),
    ("kwon-neural-fm-perspective.md", "要点：同一神经事件跨模态的时频特征差异巨大，需要**尺度不变特征**；", "要点：同一神经事件跨模态的时频特征差异巨大，需要尺度不变特征；"),
    ("kwon-neural-fm-perspective.md", "作者设想的目标形态是共享 tokenization", "作者设想的目标形态是共享 tokenization"),
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
        fail.append((fname, old[:60]))

for fname, t in files.items():
    (ROOT / fname).write_text(t, encoding="utf-8")
print(f"脚本2：成功 {done}/{len(EDITS)}")
for f, o in fail:
    print("  未命中：", f, "|", o)
