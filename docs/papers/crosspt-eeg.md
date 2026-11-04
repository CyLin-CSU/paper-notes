---
date: 2026-11-04
title: "CrossPT-EEG: A Benchmark for Cross-Participant and Cross-Time Generalization of EEG-Based Visual Decoding"
authors: [Shuqi Zhu, Ziyi Ye, Qingyao Ai, Yiqun Liu]
venue: "arXiv 2024"
year: 2024
tags: [视觉解码, 基准, 跨被试泛化, 跨时间泛化, block设计, 数据集]
status: "精读"
rating: 3.5
arxiv: "https://arxiv.org/abs/2406.07151"
code: "https://anonymous.4open.science/r/EEG-ImageNet-anonymous-74B0"
one-liner: "清华 IR 组的 EEG 视觉解码泛化基准:16 人 × 22 session、4,000 张 ImageNet 图、7 天间隔两阶段范式,two-way ID 从被试内 ~0.95 崩到跨时间 0.51–0.62、跨被试 0.49–0.57——视觉解码轴第一条基准线,泛化代价的第一份系统账目"
---
# CrossPT-EEG: A Benchmark for Cross-Participant and Cross-Time Generalization of EEG-Based Visual Decoding

> **arXiv 2024**(2406.07151,v2 2025-12-16,cs.MM,预印本)· 清华大学计算机科学与技术系(Yiqun Liu / Qingyao Ai 组,Ziyi Ye 同时是 [EEG-SVRec](https://arxiv.org/abs/2404.01008) 与脑信号相关性反馈 TOIS 2024 的作者)——站内**「视觉解码」轴线的第一条基准线**。站内已有的视觉解码工作都在报「上限」:[GUIDED](guided.md) 的被试内重建与检索、[EEGDM](eegdm.md) 的生成质量;本篇是数据集 + 协议论文,回答反面问题——**这些能力在跨被试、跨时间条件下还剩多少**。与同批的 [EEGArena](eegarena.md)(基础模型横评基准)互补:那边测任务广度,这边把「泛化代价」做成 16 人 × 22 session 的受控账目。作者的出发口径是信息检索而非神经科学:跨时间泛化对应「用户下周回来系统还要能用」的脑机搜索接口场景。

**作者**:Shuqi Zhu, Ziyi Ye, Qingyao Ai, Yiqun Liu(全部来自清华大学计算机科学与技术系;通讯未标注,联系邮箱 zhusq22@mails.tsinghua.edu.cn)

!!! abstract "TL;DR"
    - 数据集:16 人(10 男 6 女,21–27 岁)× 22 session(16 人做 Stage 1,其中 6 人 7 天后再做 Stage 2),4,000 张 ImageNet21k 图像(80 类 × 50 张:40 粗粒度类与 Spampinato 2017 对齐 + 40 细粒度类按 WordNet 父节点分 5 组 × 8 类),共 87,850 个 EEG-image 对、20.85 GB,62 通道 1000 Hz、单图 500 ms——多粒度语义标注 + 跨时间设计是相对 Things-EEG2(10 人、16,740 图、100 ms)的差异化
    - 两阶段范式:Stage 1 复刻 Spampinato 2017 的 **block 设计**(每类 50 张连续呈现);Stage 2 至少间隔 7 天、**非 block 乱序**(每类 30 训 + 20 测)——四个任务:WT = Stage 2 内部 30/20;CT = 本人 Stage 1 训 → Stage 2 测;CP = 10 人 Stage 1 训 → 6 人 Stage 2 测;PT = 10 人 Stage 1 预训 + 本人 Stage 1 续训 → Stage 2 测
    - 核心结论是崩塌曲线(two-way identification,chance 0.5):被试内 WT 最高 **0.954**(MLP fine),跨时间 CT 掉到 **0.51–0.62**(经典模型 0.51–0.59,深模型 0.55–0.62),跨被试 CP 只剩 **0.49–0.57**;经典模型在 CP 全线贴随机(0.49–0.51),深模型里显著高于随机的只有 MLP/RGNN(coarse 口径;fine 口径 EEGNet 0.522 也勉强显著);趋势 WT ≫ PT > CT > CP
    - PT 预训练有正收益但很小:RGNN coarse 0.566→0.585、MLP fine 0.617→0.636(+0.02–0.03)——10 个被试的朴素有监督预训练买不到多少泛化
    - block 设计的水分被同数据集内对照直接量化:同一批模型 80 类 accuracy 从 Stage 1 到 Stage 2 掉 10–11 个点(MLP 0.404→0.297),且 Stage 1 测试集最前几张图准确率显著偏高(附录 A.5)——Li et al. 2020a 的 block design 批评在此复现
    - 打折点:被评模型停在 2020 年(最前沿是 RGNN,无 NICE/ATM/Conformer 一代)、只做分类不做重建、伪迹去除方法未说明、v2(2025-12)仍写「数据集 review 后公开」且代码还是匿名链

## 1 问题定位:视觉解码的 EEG 数据集缺口

论文开篇的处境描述与站内 [GUIDED](guided.md) 笔记的框架一致:fMRI/MEG 靠大资源(NSD:8 人 × 10,000 图 × 一年)撑起了重建高潮,EEG 便宜、便携、毫秒级,却受限于三条:(1) 缺大规模高质量数据集;(2) 标注粒度粗,做不了细粒度分析;(3) 普遍用 block 设计——同类图像连块呈现,EEG 信号在刺激前后带上时间标记,Li et al. 2020a 已证明这会虚高 within-session 分类结果。对现有数据集的点名批评有两个:Spampinato 2017(6 人 2,000 图)规模小;Things-EEG1/2 用 50/100 ms 的极短 RSVP,「只有早期神经响应被捕获」,研究不了完整的视觉时程。

作者的三个设计对应三条批评:4,000 图 + 两级粒度标注对规模与粒度;两阶段跨时间设计对 block 混淆。值得注意的是出发点:这是清华 IR 组(THUIR)的作品——Yiqun Liu 组此前有 brain-machine search interface 的 SIGIR Forum 立项文章、EEG-SVRec、TOIS 的 relevance feedback with brain signals,视觉解码基准服务于「图像搜索 BCI」的长期议程,所以 cross-time(用户隔周回访)和随机乱序(搜索结果不会按类分块出现)是第一需求,而非神经科学的事后补充。

作为基准类论文,本文的主产品不是方法而是**测量**:图 2 的任务划分协议和 Table 2/3 的崩塌数字。被评模型是配角(作者自己在 Limitation 里承认没纳入最新方法)。

## 2 基准设计:数据集、两阶段范式与四个任务

### 2.1 数据集与采集

- **被试**:16 人(10 男 6 女),21–27 岁(均值 24.06 ± 1.69),右利手大学生,每人每阶段约 2 小时(含 30 分钟设备准备),报酬每小时 11.8 美元;Stage 1 全员 16 人,其中 6 人于至少 7 天后参加 Stage 2(7 天间隔为规避记忆效应),合计 22 session。
- **刺激**:ImageNet21k 子集,80 类 × 50 张手工筛选(宽高 >300 px、无水印、主体突出);前 40 类为粗粒度、与 Spampinato 2017 的类别一致(ImageNet1k),后 40 类为细粒度、分 5 组 × 8 类,组内共享 WordNet 父节点(如乐器组:手风琴/大提琴/长笛/双簧管/小军鼓/长号)。因 ImageNet 版权,发布物只含图像 index + 类别 wnid,不含图像本体。
- **范式**(Figure 1):S1 类别标签呈现(空格键继续)→ S2 注视点 500 ms → S3 RSVP 每图 500 ms → S4 随机测试(类块结束后随机抽查当前类别,未通过的类别数据剔除)。每被试自选随机种子决定类序与图序,两阶段用不同种子。
- **硬件**:Scan NuAmps Express + 64 导 Quik-Cap(数据为 62 个 EEG 通道,M1/M2 作参考),Curry8 记录,1000 Hz,阻抗 <50Ω(原文如此,量级上应为 kΩ 笔误);27 寸 2560×1440 @60 Hz 显示器。
- **规模**:87,850 对 / 20.85 GB。理论满额 22 session × 4,000 = 88,000,缺口 150 对未解释(推测为 S4 剔除)。

### 2.2 预处理与特征

重参考用 offline linked mastoids(M1+M2 均值,Yao et al. 2019);带通 0.5–80 Hz;50 Hz 陷波;伪迹去除只写「消除异常幅值与眨眼/头动伪迹」——**方法、阈值、是否用 ICA 均未披露**。特征窗取刺激后 **40–440 ms**(400 ms,避开相邻刺激污染)。频域特征为五频段(delta 0.5–4 / theta 4–8 / alpha 8–13 / beta 13–30 / gamma 30–80 Hz)的微分熵(Welch 法估计功率谱后 \( \mathrm{DE} = -\int P(f)\log P(f)\,df \)),逐电极逐段;经典模型与 MLP/RGNN 吃 DE 特征,EEGNet 吃时域原始段(表中以 * 标注)。

### 2.3 四个任务与指标

任务划分(Figure 2,所有任务的测试集都落在 Stage 2,故主表「全体被试平均」的实际口径是 6 名两阶段被试):

| 任务 | 训练数据 | 测试数据 | 考察维度 |
|---|---|---|---|
| WT(Within-Time) | 同一被试 Stage 2 每类 30 张 | 同一被试 Stage 2 每类 20 张 | 非 block 条件下的被试内上界 |
| CT(Cross-Time) | 同一被试 Stage 1 全部 50 张 | 同一被试 Stage 2 全部 50 张 | 跨 session(≥7 天)泛化 |
| CP(Cross-Participant) | 其余 10 人(未参加 Stage 2)的 Stage 1 | 目标被试 Stage 2 | 跨被试 + 跨 session |
| PT(Pre-training) | 10 人 Stage 1 预训(半 lr 半 epochs)+ 目标被试 Stage 1 续训 | 目标被试 Stage 2 | 借他人数据能否救回跨时间 |

主指标用 two-way identification(承 fMRI 重建文献,Ozcelik & VanRullen 2023):每个测试样本随机抽对比样本做二选一判别,重复 k=500 次取平均,chance 0.5;accuracy/F1 放在附录。**注意正文的指标定义措辞含糊**:「randomly select k comparison samples from different categories」与 two-way ID 的通常定义(单次二选一、多次重复)对不上,k 的确切语义要进代码确认。

### 2.4 被评模型

经典四件套:Ridge、KNN、RandomForest、SVM(DE 特征,核函数与正则/树数/邻居数做了网格)。深度三件套:MLP(两层隐层 256/128 + BN + dropout 0.5)、EEGNet(时域输入,首层卷积核长 = 时间点数之半 = 200)、RGNN(Zhong et al. 2020 的正则化图网络,电极拓扑按设备坐标,加两层 BN)。统一 CE 损失、batch 80、单卡 4090;MLP/EEGNet 用 SGD(lr 1e-3 训 2000 epochs → 1e-4 再训 1000),RGNN 用 Adam 同调度。全部为本基准上重训。清单里没有任何 2021 年后的视觉解码模型——「被测方」比数据集本身旧。

## 3 实验与结果

**主表 1:粗粒度任务(40 类)two-way identification(Table 2,† = 显著高于随机 p<0.05)**:

| 模型 | WT | CT | CP | PT |
|---|---|---|---|---|
| Ridge | 0.861±0.022† | 0.509±0.011 | 0.501±0.007 | 0.508±0.010 |
| KNN | 0.892±0.026† | 0.517±0.019 | 0.491±0.006 | 0.521±0.017 |
| RandomForest | 0.909±0.031† | 0.511±0.019† | 0.507±0.011 | 0.524±0.020† |
| SVM | 0.935±0.039† | 0.536±0.018† | 0.506±0.015 | 0.544±0.017† |
| MLP | 0.938±0.024† | 0.552±0.012† | 0.524±0.016† | 0.570±0.020† |
| EEGNet* | 0.878±0.022† | 0.519±0.015† | 0.509±0.012 | 0.524±0.022† |
| RGNN | 0.933±0.025† | 0.566±0.015† | 0.526±0.018† | 0.585±0.027† |

**主表 2:细粒度任务(5 组 8 类平均,Table 3)**:

| 模型 | WT | CT | CP | PT |
|---|---|---|---|---|
| Ridge | 0.886±0.023† | 0.549±0.017† | 0.495±0.007 | 0.543±0.012† |
| KNN | 0.909±0.025† | 0.554±0.017† | 0.505±0.010 | 0.551±0.015† |
| RandomForest | 0.922±0.030† | 0.587±0.022† | 0.511±0.012 | 0.595±0.019† |
| SVM | 0.949±0.035† | 0.592±0.021† | 0.509±0.019 | 0.606±0.022† |
| MLP | 0.954±0.026† | 0.617±0.019† | 0.563±0.026† | 0.636±0.027† |
| EEGNet* | 0.893±0.023† | 0.566±0.027† | 0.522±0.026† | 0.579±0.025† |
| RGNN | 0.945±0.024† | 0.601±0.024† | 0.573±0.028† | 0.634±0.027† |

三条主要读数:① 崩塌幅度——全体模型 WT→CT 掉 0.34–0.40,CT→CP 再掉 0.03–0.05,coarse 口径下经典模型 CP 全部落在 0.49–0.51(chance 0.5),深模型只有 MLP/RGNN 在 CP 显著;② 任务难度排序 WT ≫ PT > CT > CP(Figure 4,MLP 与 RGNN 分布几乎一致),跨被试最难,与跨被试/跨 session 情绪识别文献的共识一致;③ PT 相对 CT 的增益 coarse +0.018–0.019、fine +0.019–0.033,一致但微弱。

**粗 vs 细粒度**:作者用匹配协议对照(随机抽 8 个粗粒度类做 WT,重复 5 次,Figure 3)——线性回归斜率 >1,粗粒度确实更容易。但注意 Table 2/3 **纵向不可比**:fine 的 CT/PT 数字普遍高于 coarse(MLP CT 0.617 vs 0.552),这是 8 类任务比 40 类任务本身更好分,不是细粒度更容易;论文未在正文点破这一层。

**block 设计水分(Table 5 vs 6,80 类 accuracy,chance 1.25%)**:

| 模型 | Stage 1(block) | Stage 2(非 block) | 差 |
|---|---|---|---|
| SVM | 0.392 | 0.281 | −0.111 |
| MLP | 0.404 | 0.297 | −0.107 |
| RGNN | 0.405 | 0.302 | −0.103 |
| EEGNet* | 0.260 | 0.169 | −0.091 |

同一批模型、同为 80 类,Stage 1 比 Stage 2 高 9–11 个点(coarse 口径差更大,MLP 0.534→0.395 达 13.9 个点)。附录 A.5 补了机制证据:按测试集内呈现顺序画准确率,最前几张图显著偏高,30/20 与 20/30 两种划分都出现——block 设计的时间标记直接可测。EEGNet 在两个阶段都垫底(Stage 1 acc 0.260,低于 SVM 的 0.392),作者归因于原版 EEGNet 不是为语义相关任务设计的。

**个体差异**(Table 7 / Figure 5):最好被试的 Stage 1 成绩远超平均(MLP fine 0.888 vs 平均 0.816;RGNN all 0.609 vs 0.405),且被试排名跨模型稳定——「有人天生好解码」的个体差异在这个数据集上肉眼可见。

## 4 关键发现

- **泛化崩塌的量级被钉死**:被试内 ~0.95 → 跨时间 0.51–0.62 → 跨被试 0.49–0.57。经典模型两步全崩(线性映射学到的就是个体系数),深模型的优势恰好集中在泛化场景——WT 上 SVM/MLP/RGNN 几乎持平,CP 上只剩 RGNN/MLP 显著;
- **block 设计的水分 ≈ 9–14 个 accuracy 点**,且可以用「测试集图像呈现顺序」这一单一变量复现;
- **朴素跨被试预训练的下界:+0.02–0.03**——不做任何对齐/解耦、只是「先在别人身上训再在自己身上续」,收益存在但薄;
- **深模型里 RGNN > EEGNet 的泛化差距**(coarse CP 0.526 vs 0.509)支持图结构归纳偏置(电极拓扑)对跨被试更友好,但绝对值都贴地。

## 架构图

![Figure 1 · CrossPT-EEG 数据集构建流程:实验范式 S1–S4、EEG 采集与多粒度标注、两阶段跨时间设计](../assets/crosspt-framework.png)

*Figure 1 · 上排实验范式:EEG 戴帽采集 → S1 类别标签呈现(空格键继续)→ S2 注视点 500 ms → S3 RSVP 每图 500 ms(Img1…ImgN)→ S4 随机测试(可选),Next category 回环;左下:连续采集的 EEG 按图像对齐(Img1–Img50),与图像 index、粒度、标签共同入库;右下 Cross-time Stages:Stage 1 每类 N=50 block 呈现(橙/蓝分块)→ 7 天间隔 → Stage 2 每类 N=30/N=20 乱序(紫色为乱序插入的类别);底部 Multi-Granularity Labels:熊猫/高尔夫球为 Coarse,罗威纳/萨摩耶为 Fine。注:图中 S1–S4 步骤标签与图例是 PDF 矢量叠加层,不在内嵌位图里*

## 流程

```mermaid
flowchart TD
    subgraph P["实验范式(S1–S4 循环)"]
        A["S1 类标签呈现(空格键继续)"] --> B["S2 注视点 500 ms"]
        B --> C["S3 RSVP:每图 500 ms"]
        C --> D["S4 随机测试(可选)<br/>未通过类别剔除"]
        D -->|"Next category"| A
    end
    P --> E["62 通道 × 1000 Hz 连续 EEG<br/>+ 图像 index / 粒度 / wnid 标签"]
    E --> F["预处理:M1+M2 重参考<br/>0.5–80 Hz 带通 + 50 Hz 陷波 + 伪迹去除"]
    F --> G["特征窗 40–440 ms"]
    G --> H["DE 频域特征<br/>δ/θ/α/β/γ 五频段 × 62 电极"]
    G --> I["时域原始段"]
    H --> J["Ridge / KNN / RF / SVM<br/>MLP / RGNN"]
    I --> K["EEGNet"]
    J --> L["two-way identification<br/>k=500,chance 0.5"]
    K --> L
    subgraph S["两阶段采集"]
        M["Stage 1 · 16 人 · block 设计<br/>每类 50 张连续呈现"] -->|"间隔 ≥7 天"| N["Stage 2 · 6 人 · 非 block 乱序<br/>每类 30 训 + 20 测"]
    end
    S --> J
    S --> K
    L --> O["WT:同一人 Stage 2 内 30 训 / 20 测"]
    L --> Q["CT:本人 Stage 1 → Stage 2"]
    L --> R["CP:10 人 Stage 1 → 6 人 Stage 2"]
    L --> T["PT:10 人 Stage 1 预训<br/>→ 本人 Stage 1 续训 → Stage 2"]
```

## 与其他论文的关系

| 论文 / 工作 | 关系说明 |
|---|---|
| [GUIDED / ATM](guided.md) | 同轴互补的一对:GUIDED 在 THINGS-EEG 上测被试内「上限」(200-way 检索 top-1 28.64%、2-way 94.92%),本篇测泛化「下限」;两者都用 two-way identification 量纲,但协议不可直比(80 次重复 ERP 平均 vs 单 trial、500 ms vs 1000 ms 窗、不同刺激集) |
| Things-EEG1/2(Grootswagers/Gifford 2022) | 最直接的对照数据集:THINGS 概念多(1,854/22,248 图)但呈现极短(50/100 ms)、无跨时间设计;本篇 4,000 图、500 ms、多粒度标注 + 两阶段——两边各拿了对方没有的东西 |
| Spampinato 2017(EEG-Classification)+ Li et al. 2020a | Stage 1 直接复刻其 block 范式(40 个粗粒度类同款);Li et al. 2020a 的 block design 批评是方法论依据,Table 5 vs 6 的水分量化与 A.5 时间效应分析就是对该批评的同库复现 |
| [EEGArena](eegarena.md) | 同为基准但颗粒度互补:EEGArena 用 20,000+ 次评测横评 30 个基础模型 × 57 任务,考「谁的方法强」;本篇只做一个任务族(视觉分类)但把被试/时间两个泛化维度切成受控协议——宽度基准 vs 深度基准 |
| [EEGPT](eegpt.md) / [CBraMod](cbramod.md) | 预训练轴线的「评测缺口」:基础模型论文都声称跨被试/跨数据集泛化,视觉解码侧此前没有受控的跨被试/跨时间协议——本篇的 WT/CT/CP/PT 恰好是它们需要的评测形状,尽管被评清单里还没有它们 |
| [BIOT](biot.md) | 泛化主张的对账对象:BIOT 主打跨被试/跨记录的通道无关建模;本篇 CP≈0.50–0.57 的地板说明这类主张在视觉解码任务上必须单独重验 |
| [EEGDM](eegdm.md) / [Not-All-EEG](not-all-eeg.md) | 生成线与本篇零交集(那边评生成质量、不评泛化),但生成线的检索指标在 CP 条件下会掉多少,本篇的崩塌数字是预告 |
| Ozcelik & VanRullen 2023 | 主指标的出处:fMRI 重建文献的 two-way identification 被搬进 EEG 分类基准,使重建线与基准线共享量纲 |

## 个人思考

- **基准的价值在「下限」而不在「上限」**。WT 0.95 → CT 0.55 → CP 0.52 这条崩塌曲线,是站内视觉解码线所有论文都没系统报过的维度:[GUIDED](guided.md) 自己报过被试内 28.64% → 跨被试 11.84% 的腰斩,但那是单模型单数据集;本篇用 7 个模型 × 4 任务 × 2 粒度的受控矩阵说明:跨被试 ≈ 接近重来,跨时间 ≈ 丢掉六成。任何在 THINGS-EEG 上刷 SOTA 的工作,宣称「可用于 BCI」之前应该先过 CT/CP 这两关——本篇最大的贡献是把这两关做成了标准化协议;
- **「预训练有用」的证据在这里很弱,但方向诚实**。PT 比 CT 只多 0.02–0.03:10 个被试 × 4,000 图的有监督预训练几乎买不到泛化。对照站内基础模型轴线的口径,本篇可以当「朴素预训练收益基线」——新方法的跨被试增益若不超过这个幅度,不足以支撑「预训练表征有跨被试不变性」的宣称。但边界要留:这里的预训练只是「换人训 + 半 lr 续训」,没有任何表征对齐、对抗解耦或通道无关设计,它给的是下界不是方法上限;CP 崩到 0.52 恰恰说明跨被试差异是主矛盾,谁若能在 CP 上把 0.52 拉到 CT 水平,就是下一个值得写的结果;
- **block 设计水分的 9–14 个点值得记住**。Stage 1 复刻 Spampinato、Stage 2 纠偏,同一数据集内直接给出膨胀幅度;加上 A.5 的「测试集最前几张图准确率异常高」,这是 Li et al. 2020a 之后少有的同库对照证据。站内在 [GUIDED](guided.md) 笔记里夸过 THINGS-EEG 的 RSVP 协议,本篇补上另一半:非 block 只去掉类内时间标记,去掉不了 session 间漂移——CT 掉的 0.34–0.40 里有多少是协议残余、多少是真实脑状态漂移(7 天间的睡眠、情绪、电极位置),数据集本身给不出答案,这恰是它留下的开放问题;
- **基准的「被测方」与「数据方」都不完整**。被测模型停在 2020 年(作者自认),没有 NICE/ATM/Conformer/EEGPT 一代,也没有任何重建任务——它目前更像「泛化协议参照系」而不是「SOTA 降落场」。数据侧,Stage 2 只有 6 人(且是自愿参加两阶段的 6 人,自选偏差未讨论),CP 的崩塌数字建立在 6 个测试被试上;80 类对细粒度解码只有 5 组 × 8 类,而 THINGS 有 1,854 概念。另外 v2(2025-12)仍写「review 后公开」、代码还是匿名链——数据可得性是复现前要确认的第一件事,这也限制了它现在作为基准的实际地位。

## 自问自答

??? question "Q1 · 0.95 → 0.55 → 0.52 三个数字各自该怎么用?"

    WT 是「同一人同一设备同一天」的理想上界,对应实验室演示;CT 是「同一人隔周回访」的真实个人化 BCI 场景,掉到 0.51–0.62 意味着逐 session 重校准不可省;CP 是「开箱即用」场景,0.49–0.57 意味着纯零样本部署在视觉解码上还不成立。三个数字共同给站内视觉解码论文提供了「应报而未报」的第三列:报完被试内 SOTA 之后,至少 CT 应作为必报项。使用时注意主表平均口径只有 6 名两阶段被试,置信区间不宽(±0.01–0.03)。

??? question "Q2 · fine(8 类)的 CT/PT 反而比 coarse(40 类)高,这两张表能横比吗?"

    不能。fine 是 5 组 8 类任务的平均,coarse 是 40 类任务,类别数不同、two-way ID 的配对分布也不同;fine CT 更高只说明 8 类任务的 DE 特征更可分。论文自己意识到这点,才做了 Figure 3 的匹配协议对照(随机抽 8 个粗粒度类做 WT,重复 5 次):斜率 >1,证明在协议对齐后粗粒度仍然更容易。所以正确用法是 Table 2 内部纵向比(模型排序、任务排序),fine 与 coarse 之间只比趋势、不比绝对值。

??? question "Q3 · PT 只涨 0.02–0.03,能得出「跨被试预训练没用」吗?"

    不能,只能得出「朴素预训练收益有下界」。这里的 PT = 在 10 人 Stage 1 上直接训(半 lr 半 epochs)再在本人 Stage 1 续训,没有任何跨被试对齐机制——而站内基础模型轴线(EEGPT 的通道嵌入、CBraMod 的多数据集掩码预训练、BIOT 的通道无关 tokenizer)赌的恰是「先学跨被试不变表征」。本篇的 CP 地板(0.52)与 PT 微增益(0.02–0.03)合起来其实是给这条轴线的一道考题:在 CrossPT-EEG 的 CP 任务上,这些方法能比 RGNN 的 0.526 高出多少?这篇论文没测,但协议已经铺好。

??? question "Q4 · Stage 1 的 block 设计数据是「脏数据」还是「素材」?"

    两者都是。对刷分类指标,它是被污染的:时间标记让 within-session 结果虚高 9–14 个点,Table 5 的数字不能当作真实解码能力引用(作者也明确说 not representative of real-world generalization)。但对研究时间效应本身,它是稀缺素材:同一批被试、同一批图、同一套硬件,block 与非 block 只差呈现顺序,测试集首图准确率异常高的模式(Figure 6)可以直接喂给「时间混淆检测/去混淆」类工作。另外 Stage 1 覆盖全部 16 人、数据量是 Stage 2 的 2.7 倍,做被试内表征分析(如 RSM)时仍是主力。

!!! abstract "复现速查卡"
    - **代码**:[anonymous.4open.science/r/EEG-ImageNet-anonymous-74B0](https://anonymous.4open.science/r/EEG-ImageNet-anonymous-74B0)(匿名预览链;v2 仍写「数据集 review 后公开」、正式 GitHub 未给——可得性先确认)
    - **数据**:16 人 × 22 session,87,850 对,20.85 GB;62 通道 × 1000 Hz × 500 ms;`.pth` 格式(Stage 1 拆两个文件),字段 eeg_data / granularity / subject / label(wnid)/ image(index)/ stage(仅 Stage 2);只给 ImageNet index + wnid,需自行取图
    - **预处理**:M1+M2 offline linked mastoids 重参考 → 0.5–80 Hz 带通 → 50 Hz 陷波 → 伪迹去除(**方法未披露**);特征窗 40–440 ms;DE 五频段(Welch)
    - **任务**:WT 同人 Stage 2 内 30/20;CT 本人 Stage 1 → Stage 2;CP 10 人 Stage 1 → 6 人 Stage 2;PT 10 人预训(半 lr 半 epochs)→ 本人 Stage 1 续训;主表平均口径 = 6 名两阶段被试
    - **训练**:CE 损失、batch 80、单卡 4090;MLP/EEGNet SGD lr 1e-3×2000ep → 1e-4×1000ep(EEGNet 首 conv 核长 200,F1 {8,16,32},D {2,4,8});RGNN Adam 同调度(GCN hidden {100,200,400} × hops {1,2,4} + 2 层 BN)
    - **指标**:two-way identification,k=500,chance 0.5(**k 的确切语义需进代码确认**)
    - **关键数字**:two-way ID coarse:MLP 0.938/0.552/0.524/0.570、RGNN 0.933/0.566/0.526/0.585;fine:MLP 0.954/0.617/0.563/0.636;block 水分:80 类 acc MLP 0.404→0.297、coarse 口径 0.534→0.395
    - **未披露**:伪迹去除细节、Tables 5/6 的划分协议、150 对数据缺口的构成、S1 呈现时长

---

**相关阅读**

:material-eye: [GUIDED · 视觉重建线(被试内上限,与本篇互补)](guided.md) ｜ :material-format-list-numbered: [EEGArena(基础模型横评基准,宽度对本篇深度)](eegarena.md) ｜ :material-layers: [EEGPT(预训练特征提取器,CP 协议的天然候选被测方)](eegpt.md) ｜ :material-creation: [CBraMod(多数据集预训练,跨被试主张待此基准对账)](cbramod.md) ｜ :material-heart-pulse: [BIOT(跨被试/跨记录建模的对账对象)](biot.md) ｜ :material-home: [首页](../index.md)
