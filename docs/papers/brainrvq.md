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

## 3 实验与结果

**预训练**:TUEG v2.0.1,26,846 sessions / 14,987 患者 / 超 27,000 h;预处理后保留 1,109,545 个 30 s 样本(≈9,200 h)——去 <5 min 录制、掐头去尾各 1 min、19 通道 10-20、0.3–75 Hz 带通 + 60 Hz 陷波、重采样 200 Hz、剔除任一点 |幅值| >100 µV 的样本、除以 100 µV 归一。tokenizer 训练 20 epoch(6×A800 约 12 h),预训练 20 epoch(6×A800 约 20 h)。全模型 12 层 / d=200 / 10 头 / FFN 800,**5.82M 参数**。

**下游协议**:加载预训练编码器,接池化 + 分类头,**端到端全微调**(AdamW,lr 5e-4,layer-wise decay 0.65,50 epoch,bs 64),5 seeds 报均值 ± 标准差。划分:CHB-MIT 按被试 1–19 / 20–21 / 22–23 切(跨被试),PhysioNet 1–70 / 71–89 / 90–109,SHU-MI 1–15 / 16–20 / 21–25,BCICIV-2a 1–5 / 6–7 / 8–9,Mental 1–28 / 29–32 / 33–36——五个任务均为**跨被试**;SEED-V 按被试内 trial 切(5/5/5,被试跨集共享);TUAB/TUEV 用官方 train/test 划分再 8:2 分验证。基线:EEGNet、ST-Transformer(有监督)+ BENDR、BIOT、LaBraM、CBraMod(基础模型,官方权重 + 官方微调协议;论文称「均在 TUH 语料上预训练」,BIOT 官方权重实为多生物信号混合预训练,此说法对 BIOT 不严格)。

**主结果**(Table 2,四个代表任务;二分类看 AUROC,多分类看 Kappa):

| 方法 | Mental AUROC | CHB-MIT AUROC | CHB-MIT AUC-PR | TUEV Kappa | BCICIV-2a Kappa |
|---|---|---|---|---|---|
| EEGNet | 0.732 | 0.805 | 0.191 | 0.358 | 0.269 |
| ST-Transformer | 0.713 | 0.824 | 0.142 | 0.377 | 0.273 |
| BENDR | 0.568 | 0.863 | 0.307 | 0.427 | 0.320 |
| BIOT | 0.754 | 0.876 | 0.328 | 0.527 | 0.300 |
| LaBraM | 0.772 | 0.868 | 0.329 | 0.664 | 0.316 |
| CBraMod | 0.791 | 0.889 | 0.369 | 0.677 | 0.352 |
| **BrainRVQ** | **0.862** | **0.928** | **0.465** | **0.690** | **0.388** |

**8 个数据集与 CBraMod 的全量对照**(主指标;括号内为监测指标口径)——这是检验摘要「consistently outperforms」的明细账:

| 数据集 | BrainRVQ | CBraMod | 差距 |
|---|---|---|---|
| Mental Workload(AUROC) | 0.862 | 0.791 | **+0.071** |
| CHB-MIT(AUROC / BalAcc) | 0.928 / 0.709 | 0.889 / **0.740** | +0.039 / **−0.031** |
| BCICIV-2a(Kappa) | 0.388 | 0.352 | +0.036 |
| SHU-MI(AUROC) | 0.717 | 0.699 | +0.018 |
| TUEV(Kappa) | 0.690 | 0.677 | +0.013 |
| TUAB(AUROC / BalAcc) | 0.900 / 0.831 | **0.923** / 0.829 | **−0.023** / +0.002 |
| SEED-V(Kappa) | 0.260 | 0.257 | +0.003 |
| PhysioNet(Kappa) | 0.523 | 0.522 | +0.001 |

真正拉开差距的是 Mental Workload 与 CHB-MIT 的排序指标;TUEV/PhysioNet/SEED-V 的领先在 0.001–0.013 之间,与 5-seed 标准差同量级;TUAB 的 AUROC/AUC-PR 输给 CBraMod(0.923/0.926),CHB-MIT 的 Balanced Accuracy 也低于 CBraMod(0.709 vs 0.740,正文如实只宣称「排序指标最优」)。

**组件消融**(Table 3;二分类 AUROC / 多分类 Kappa):

| 配置 | Mental | CHB-MIT | TUEV | BCICIV-2a |
|---|---|---|---|---|
| Full Model | 0.862 | 0.928 | 0.690 | 0.388 |
| w/o 频域码本(纯时域) | 0.845 | 0.887 | 0.639 | 0.373 |
| w/o 时域码本(纯频域) | 0.857 | 0.896 | 0.655 | 0.374 |
| 单层 VQ(去 RVQ) | 0.849 | 0.896 | 0.682 | 0.321 |
| 独立预测(去层次 AR) | 0.780 | 0.875 | 0.662 | 0.335 |
| 随机掩码(去课程掩码) | 0.852 | 0.910 | 0.673 | 0.363 |

四个组件的平均相对代价:独立预测 −8.3%(最重)> 单层 VQ −5.9% > 随机掩码 −3.0%;双域中频域码本比时域码本更不可或缺(TUEV 上纯时域 −7.4% vs 纯频域 −5.1%)。任务侧规律清晰:临床事件分类(TUEV)吃时域形态,认知状态与运动想象吃频域节律与多尺度细化(单层 VQ 在 BCICIV-2a 掉 17.3%)。

**附录补充要点**(均自 PDF 附录读出):

- **RVQ 深度**(Table 11):1/2/3/5/7 层在 BCICIV-2a 上 Kappa 0.322 / 0.383 / 0.388 / 0.382 / 0.337,3 层为拐点;重构质量同趋势(Table 15:MSE 348.69 / 224.59 / 157.18 / 129.82 / 139.04 ×10⁻³,r 0.807→0.918→0.928)——5 层以后深层码本在拟合噪声状残差;
- **重构质量**(Table 14,7,928 样本):时域 r=0.904(SNR 8.1 dB)、幅值 r=0.956(11.2 dB)、**相位 r=0.577(2.0 dB)**——定性示例(0.891–0.979)明显是挑过的;
- **码本利用率**(Table 5):六个码本全部 100% 利用,归一化熵 >0.99,Gini 0.104–0.174,Top-10% 码只占 13.7–18.1% 用量——无坍缩;越深层的分布越均匀(Gini 0.174→0.104);
- **token 预测精度**(Fig 5):Layer-0 ≈29%、Layer-1 ≈22%、Layer-2 ≈14%,单调递减与 λ 加权自洽;
- **Scaling**(Tables 16–19):数据 1k→9k h,Mental AUROC 0.810→0.862、BCICIV-2a Kappa 0.318→0.388(+22% rel),无饱和;模型 4→12 层(1.96M→5.82M),Kappa 0.345→0.388,10 层后边际递减;
- **低资源**(Table 20):30% 微调数据下 SEED-V Kappa 0.238(保留全量性能的 91.5%)、SHU-MI AUROC 0.685(保留 95.5%),均优于 CBraMod 30% 版本;
- **掩码行为**(Fig 13):随机掩码下掩码/可见 patch 信息分几乎相同(0.332 vs 0.336),重要性掩码拉开到 0.393 vs 0.274(Δ+0.119)。

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

!!! abstract "复现速查卡"
    - **代码**:[github.com/keqicmz/BrainRVQ](https://github.com/keqicmz/BrainRVQ)(训练代码已放出;README 自述缺 ShockDataset 依赖、无环境锁定;**权重待论文接收后公开**)
    - **数据**:TUEG v2.0.1,26,846 sessions / 14,987 患者 / >27,000 h → 预处理后 1,109,545 个 30 s 样本(≈9,200 h);管线 = 去 <5 min、掐头去尾各 1 min、19 通道 10-20、0.3–75 Hz 带通 + 60 Hz 陷波、200 Hz 重采样、剔除任一点 |幅值| >100 µV、÷100 µV 归一
    - **Tokenizer**:12 层 encoder(d=200,10 头)+ 3 层 decoder;RVQ 3 层 × 8192 × 2 域,码字 64 维;EMA 0.99,ℓ2 归一化,β=1.0;20 epoch,bs 128,AdamW 5e-4(wd 5e-2),cosine + 5 warmup;6×A800 ≈ 12 h
    - **预训练**:12 层 encoder(d=200,10 头,FFN 800,全模型 5.82M);mask 0.5(可学习 mask token,symmetric loss true 但未定义);λ = 1 / 0.5 / 0.25;α = (0.30, 0.25, 0.20, 0.15, 0.10),w: 0.2→0.7,τ=0.8;20 epoch,bs 64;6×A800 ≈ 20 h
    - **下游**:端到端微调 50 epoch,AdamW 5e-4,layer decay 0.65,bs 64,drop path 0.1;5 seeds;CHB-MIT/PhysioNet/SHU-MI/BCICIV-2a/Mental 为跨被试划分,SEED-V 为被试内 trial 划分
    - **关键数字**:Mental AUROC 0.862 / CHB-MIT AUROC 0.928·AUC-PR 0.465 / TUEV Kappa 0.690 / BCICIV-2a Kappa 0.388;消融:独立预测 −8.3%、单层 VQ −5.9%、随机掩码 −3.0%;重构 r:时域 0.904、幅值 0.956、相位 0.577;码本利用率 100%(Gini 0.104–0.174);token 预测精度 29% / 22% / 14%

---

**相关阅读**

:material-vector-link: [NeuroRVQ(RVQ 分支先行者:多尺度卷积单时域)](neurorvq.md) ｜ :material-vector-circle: [CodeBrain(双域 VQ + Mamba 的最近竞品)](codebrain.md) ｜ :material-tag: [LaBraM(单层 VQ + token 作目标的范式起点)](labram.md) ｜ :material-vector-polyline: [TFM-Tokenizer(token 作输入的可插拔路线)](tfm-tokenizer.md) ｜ :material-compare: [CBraMod(同语料最强基线)](cbramod.md) ｜ :material-routes: [Tokenization 演进](../topics/tokenization.md) ｜ :material-home: [首页](../index.md)
