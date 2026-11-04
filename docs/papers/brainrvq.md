---
date: 2026-11-04
title: "BrainRVQ: A High-Fidelity EEG Foundation Model via Dual-Domain Residual Quantization and Hierarchical Autoregression"
authors: [Mingzhe Cui, Tao Chen, Yang Jiao, Yiqin Wang, Lei Xie, Yi Pan, Luca Mainardi]
venue: "arXiv 2026"
year: 2026
tags: [EEG, 基础模型, tokenization, RVQ, 双域量化, 层次自回归, 掩码预训练]
status: "精读"
rating: 4
arxiv: "https://arxiv.org/abs/2602.16951"
code: "https://github.com/keqicmz/BrainRVQ"
one-liner: "共享编码器 + 时/频双路 RVQ(2×3 层×8192 码本)把同一 EEG patch 拆成两组残差码字,层间 teacher forcing 自回归重构:TUEG 9,200 h 预训练 5.82M 小模型,CHB-MIT AUC-PR 0.465(较 CBraMod +26%)、Mental Workload AUROC 0.862(+0.071)"
---
# BrainRVQ: A High-Fidelity EEG Foundation Model via Dual-Domain Residual Quantization and Hierarchical Autoregression

> **arXiv 2026**

**作者**:Mingzhe Cui, Tao Chen*, Yang Jiao, Yiqin Wang, Lei Xie, Yi Pan, Luca Mainardi(浙江大学;Yang Jiao、Yi Pan 来自中科院深圳先进院;Luca Mainardi、Tao Chen 挂米兰理工;通讯作者 Tao Chen,chentao98@zju.edu.cn)

## 1 问题定位:单域量化的信息损失与扁平码本的容量天花板

论文把现有 EEG 基础模型的表征保真度问题归为三条,每条都指向 tokenization 而不是骨干:

1. **单域 tokenization**:时域 tokenizer(如 LaBraM 的时域 VQ)擅长抓棘波这类瞬态事件,但丢全局谱模式;频域方法反之。单一视角的量化天然丢掉时频耦合信息;
2. **扁平量化容量不足**:单层 VQ 是硬容量天花板,容易码本坍缩;RVQ 在音频领域(SoundStream、EnCodec、AudioLM)已证明级联码本能以递增精度逼近信号——但直接搬到 EEG 有两个障碍:EEG 的层次结构(主导节律 + 细微细节)混着高噪声底,标准的「所有残差码独立等权预测」会让模型把容量浪费在重构背景噪声上;
3. **独立预测丢弃层次先验**:MAE 式掩码建模对每个 token 独立预测,第 1 层码捕捉的全局模式无法约束第 2、3 层的细化预测。

三条诊断对应的药方就是标题三件套:双域 RVQ(DD-RVQ)tokenizer、层次自回归预训练目标、重要性引导课程掩码。逻辑自洽,第 3 节的消融会回头检验每味药的实际疗效。

## 2 方法

### 2.1 总览:三阶段流水线

输入 \( X \in \mathbb{R}^{C \times T} \) 按通道切 1 s 非重叠 patch(\( P = 200 \),200 Hz),30 s 样本得到 19 × 30 = 570 个 patch。流程:DD-RVQ tokenizer 把每个 patch 量化成 2 域 × 3 层 = 6 个离散码 → 重要性引导课程掩码按 50% 比例选 patch 掩掉 → 掩码表征进 12 层 Transformer 编码器,以层次自回归目标逐层重构被掩码的码。下游只用预训练编码器(接池化头微调),token 推理时丢弃。

### 2.2 DD-RVQ:共享编码器、双套码本、双目标重构

对归一化 patch \( \bar{x}_{c,a} \in \mathbb{R}^{P} \),先做 DFT 得到频谱,取幅值 \( A[k] = |X_{freq}[k]| \) 与相位 \( \phi[k] = \arg(X_{freq}[k]) \) 作重构目标。时域 patch 本体过一个**共享 Transformer 编码器**得到统一潜在表示 \( h \in \mathbb{R}^d \)——注意是同一个 \( h \) 分别送进两个并行 RVQ(时域 \( Q_t \)、频域 \( Q_f \)),双域分化发生在码本与解码器层面,不在编码器层面。

RVQ 逐层量化残差:

\[
z_i^{(l)} = \arg\min_{k \in \{1,\dots,K_l\}} \| r^{(l-1)} - v_k^{(l)} \|_2, \qquad r^{(l)} = r^{(l-1)} - v_{z_i^{(l)}}^{(l)}, \qquad r^{(0)} = \tilde{e}
\]

最终量化表示为各层码字之和 \( h_q = \sum_{l=1}^{L} v_{z_i^{(l)}}^{(l)} \)。实现上每个域 \( L = 3 \) 层、每层码本 8192、码字 64 维;编码器输出与码字都做 ℓ2 归一化(单位超球面上算距离,方向学习),码本用 EMA 更新(衰减 0.99)防坍缩。

重构目标共三条(时域一条、频域两条):

\[
\mathcal{L}_{time} = \| \mathrm{Decoder}_t(h_q^{(t)}) - \bar{x}_{c,a} \|_2^2, \qquad \mathcal{L}_{freq} = \| y_A - A \|_2^2 + \| y_\phi - \phi \|_2^2
\]

总损失 = 双域重构 + 逐层逐域 commitment(β=1.0):

\[
\mathcal{L}_{total} = \mathcal{L}_{time} + \mathcal{L}_{freq} + \beta \sum_{d \in \{t,f\}} \sum_{l=1}^{L} \| \mathrm{sg}[r_d^{(l-1)}] - v_d^{(l)} \|_2^2
\]

### 2.3 层次自回归预训练:层间 teacher forcing

标准 MAE 式目标对每个 token 的各层码独立预测(式 8)。本文把位置 \( i \) 上所有层码的联合分布按层分解:

\[
P(z_i \mid X_{\backslash M}) = \prod_{l=1}^{L} P(z_i^{(l)} \mid z_i^{(1:l-1)}, X_{\backslash M})
\]

实现为共享编码器 \( f_\theta \) + L 个层级专属预测头 \( g_\theta^{(l)} \):预测第 l 层时,把前 l−1 层码的 embedding **累加**进编码器输出作条件:

\[
\hat{z}_i^{(l)} = g_\theta^{(l)}\left( \mathrm{LN}^{(l)}\left( h_i + \sum_{k=1}^{l-1} \mathrm{Embed}^{(k)}(z_i^{(k)}) \right) \right)
\]

直接自回归训练要用模型自己的预测 \( \hat{z}^{(l-1)} \) 条件下一层,误差会沿链累积;于是用 **teacher forcing**——训练时条件于 tokenizer 给出的真值码。总目标按层加权聚合,\( \lambda_l = 2^{-(l-1)} \)(即 λ = 1 / 0.5 / 0.25),粗层错误会沿链传播所以权重高;推理时改为完全自回归:先预测 \( \hat{z}^{(1)} \),取其 embedding 条件第 2 层,逐层迭代。这是 AudioLM/RQ-Transformer 式 coarse-to-fine 生成在 EEG 掩码建模上的移植。

### 2.4 重要性引导课程掩码

均匀随机掩码对事件稀疏、背景占多数的 EEG 是浪费:掩到背景等于做插值作业。本文给每个 patch 打复合信息分:频域两指标——神经频带比(4–30 Hz 功率占比,覆盖 θ/α/β)、伪迹惩罚(<2 Hz 基线漂移与 ≥45 Hz 肌电占比的倒数);时域用 Hjorth 参数(activity 取对数、mobility、complexity)加一个不规则性指标。加权聚合:

\[
S_{c,a} = \alpha_1 \tilde{S}_{neural} + \alpha_2 \tilde{S}_{clean} + \alpha_3 \tilde{S}_{complexity} + \alpha_4 \tilde{S}_{irreg} + \alpha_5 \tilde{S}_{mobility}
\]

权重 \( (\alpha_1,\dots,\alpha_5) = (0.30, 0.25, 0.20, 0.15, 0.10) \),min-max 归一化。课程通过重要性加权采样实现:

\[
\hat{S}_{c,a}(t) = w(t) \cdot S_{c,a} + (1 - w(t)) \cdot U_{c,a}, \qquad U_{c,a} \sim \mathrm{Uniform}(0,1)
\]

\( w(t) \) 从 0.2 线性升到 0.7:早期近似均匀采样保覆盖,后期偏向高信息 patch。采样用 softmax(温度 τ=0.8),掩码率 0.5(消融确认 0.4–0.6 为倒 U 峰值区)。

## 架构图

![Figure 1 · BrainRVQ 总体框架:(A) DD-RVQ tokenizer;(B) 层次自回归掩码预训练;(C) 下游适配](../assets/brainrvq-framework.png)

*Figure 1 · (A) DD-RVQ for EEG Tokenization——异构 EEG 经 Neural Transformer Encoder 得潜在表示,时域支路直接进 RVQ(quantize_t),频域支路经 DFT 进 RVQ(quantize_f),各自 3 层码本级联,Decoder_t 重构波形、Decoder_f 重构幅值与相位,Embedding Loss + 重构损失联合优化(图中右上角的「Restruction Loss」为原文拼写错误);(B) Pre-training Process——Information Masking 选高信息 patch,Temporal Conv → Transformer Blocks → Hierarchical RVQ Predictor 逐层自回归预测 token(Z^(l) 条件于前层);(C) Downstream Tasks——预训练编码器接任务头微调*

## 与其他论文的关系

| 论文 / 工作 | 关系说明 |
|---|---|
| [LaBraM](labram.md) | 范式直系:同走「token 只当预训练目标、推理丢弃、下游微调连续编码器」路线;LaBraM 的单层时域 VQ 正是本文批评的「单域 + 扁平量化」,换成了双域 3 层 RVQ |
| [NeuroRVQ](neurorvq.md) | RVQ 分支姊妹篇:NeuroRVQ 用多尺度卷积在**单时域**做 RVQ、以重构保真为主卖点;BrainRVQ 共享编码器 + **双域双码本** + 层间自回归。两篇对相位的态度不同——NeuroRVQ 用圆周相位损失处理角度周期性,BrainRVQ 直接 MSE 重构相位(平均 r 只有 0.577) |
| [CodeBrain](codebrain.md) | 「双域 tokenization」的最近竞品,也是本文最该比而没比的对手:CodeBrain 用独立时/频卷积编码器 + 双 VQ 码本 + Mamba 骨干,BrainRVQ 用共享 Transformer 编码器 + 双 RVQ + BERT 式掩码 AR——双域在编码器层(前者)还是码本层(后者)是两条可对照的设计路线 |
| [CBraMod](cbramod.md) | 最强基线与同语料同伴:同为 TUEG 预训练、同为 TUAB/TUEV 官方划分;监测指标口径 8 个数据集 7 胜 1 负(唯一败仗 TUAB),另有 CHB-MIT BalAcc、TUAB AUC-PR 两个次指标落后,且 7 胜里 4 场在噪声内——「超越 CBraMod」的成色要按任务拆开看 |
| [TFM-Tokenizer](tfm-tokenizer.md) | token 用法的分岔口:TFM 把离散 token 做成下游输入与可插拔组件;BrainRVQ 与 LaBraM 一样让 token 止步于预训练目标——RVQ 的层次结构目前只用来「教」编码器,没进入推理链路 |
| [NeuroLM](neurolm.md) | 层次化的两种含义:NeuroLM 的层次在词表层级(VQ 码并入 GPT-2 词表),BrainRVQ 的层次在 RVQ 深度(层间自回归);NeuroLM 曾实验证实相位重构对下游贡献很小,与本文保留全权重相位损失形成张力 |
| [BIOT](biot.md) | 预训练语料口径的对照:BIOT 官方权重是多生物信号混合预训练(EEG+ECG+HAR),本文表格统一说成「TUH 预训练」——复现横向对比时注意 BIOT 的语料其实不同源 |
| SoundStream / EnCodec / AudioLM | RVQ 与 coarse-to-fine 自回归的出处:本文是音频压缩/生成范式在 EEG 掩码预训练上的一次较完整移植(级联码本 + 层间 teacher forcing + 层加权) |

## 个人思考

- **「consistently outperforms」与明细账之间有一段距离**。8 个数据集里真正拉开的是 Mental Workload(+0.071 AUROC)和 CHB-MIT AUC-PR(+0.096);TUEV +0.013、SHU-MI +0.018 是小胜,PhysioNet +0.001、SEED-V +0.003 落在 5-seed 标准差内,TUAB 排序指标反输 CBraMod 0.023。诚实的读法是:**在同源语料(TUEG ⊃ TUAB/TUEV)的临床任务上有实质或边际增益,在运动想象/情绪这类「语料外」任务上基本打平**——而后者才是检验 tokenization 质量而非语料熟悉度的试金石。摘要的营销措辞与表格的混合证据,阅读时要拿第 3 节那张 8 行对照表压一压;
- **「双域」的「双」到编码器为止是假的——这不是缺点,但这笔账论文没算**。共享编码器输出同一个 h,两套码本量化同一向量,时/频分化完全由两个解码器的重构目标(波形 vs 幅相)反向逼出来;Fig. 1 却在频域支路画了 DFT 模块,与正文「DFT 只提供重构目标」的表述矛盾(图文各说各话,复现前必须问作者)。对照 CodeBrain 的独立时/频编码器,BrainRVQ 的双域是码本层的便宜版——消融证明便宜版也有效(去任一码本都掉分),但同一 h 进两套 8192×3 码本,6 个 token/patch 里有多少是冗余编码?一个零成本的检验:用时域 token 互预测频域 token,看互信息有多高;
- **层次自回归是全文最硬的贡献,但 teacher forcing 的软肋也被 λ 藏起来了**。独立预测消融平均 −8.3%,是四个组件里代价最大的;L0 29% > L1 22% > L2 14% 的精度单调性与 λ=[1, 0.5, 0.25] 的加权设计自洽。不过训练条件于真值码、推理条件于自己的预测,exposure bias 沿三层链累积——恰好最细层(误差最会滚雪球的那层)权重被压到 0.25,这个问题从损失函数视角里消失了。论文没做 scheduled sampling,也没报告推理态(自回归条件)下的重构质量与训练态差多少;
- **同源语料 + 同源评测的泄漏疑云,是整条 TUEG 预训练线的系统性盲区**。TUEG 与 TUAB/TUEV 同属 Temple 大学医院语料,论文未声明是否把评测集的被试/时段从预训练语料中剔除;CBraMod、LaBraM 的 TUH 版本同样没说,所以横向 SOTA 仍共享这一混淆。BrainRVQ 在 TUEV/TUAB 上对 CBraMod 的增量本来就薄(Kappa +0.013、BalAcc +0.002/−0.002),若有残留泄漏,这几个数字的解读要更保守。值得表扬的是工程务实:5.82M 参数、6×A800 约 32 h 跑完两阶段预训练,且 scaling 曲线(1k→9k h、4→12 层)未见饱和——这套配方的天花板远没摸到,小模型 + 单机构语料是目前证据下最划算的区间。

---

**相关阅读**

:material-vector-link: [NeuroRVQ(RVQ 分支先行者:多尺度卷积单时域)](neurorvq.md) ｜ :material-vector-circle: [CodeBrain(双域 VQ + Mamba 的最近竞品)](codebrain.md) ｜ :material-tag: [LaBraM(单层 VQ + token 作目标的范式起点)](labram.md) ｜ :material-vector-polyline: [TFM-Tokenizer(token 作输入的可插拔路线)](tfm-tokenizer.md) ｜ :material-compare: [CBraMod(同语料最强基线)](cbramod.md) ｜ :material-routes: [Tokenization 演进](../topics/tokenization.md) ｜ :material-home: [首页](../index.md)
