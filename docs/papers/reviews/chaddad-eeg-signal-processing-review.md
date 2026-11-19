---
date: 2026-11-19
title: "Electroencephalography Signal Processing: A Comprehensive Review and Analysis of Methods and Techniques"
authors: [Ahmad Chaddad, Yihang Wu, Reem Kateb, Ahmed Bouridane]
venue: "Sensors 2023"
year: 2023
tags: [综述, EEG, 信号处理, 去噪, 特征工程, 传统机器学习]
status: "精读"
rating: 3
doi: "10.3390/s23146434"
arxiv: ""
code: ""
one-liner: "传统流水线视角的 EEG 信号处理综述：采集→去噪（回归/BSS/CCA/小波/EMD，公式+伪代码）→特征工程（时频/高阶谱/非线性）→分类（ML+DL）四阶段方法对照；全文零处基础模型"
---

# Electroencephalography Signal Processing: A Comprehensive Review and Analysis of Methods and Techniques

> **Sensors 23(14):6434（2023）· Review**

**作者**：Ahmad Chaddad, Yihang Wu, Reem Kateb（Taibah University，沙特）+ 桂林电子科技大学 + Ahmed Bouridane（University of Sharjah，阿联酋）

## 1 问题定位与收录范围

EEG 信号信噪比低、非平稳、非线性、个体差异大，直接从原始信号提取任务信息困难——综述把解法组织成**采集 → 去噪 → 特征工程 → 分类**四阶段流水线（原文 Figure 2 与伪代码 Algorithm 1），逐阶段比较方法优劣。检索范围是"主要科学与工程数据库"，未给检索式与筛选流程（无 PRISMA；对照站内 [Yao 综述](yao-eegfm-survey.md) 的 PRISMA 协议），收录文献到 2023 年中。

**全文零处 foundation model / pretraining**（站内检索原文确认）——它是一篇传统信号处理方法学综述，与站内四篇 FM 综述不在同一轴上。站内价值：FM 综述里反复出现的痛点（预处理极简、参考电极选择、容积传导）在这篇里有系统的方法学展开，是那一层的教科书底座。

数学分布要说清：**公式集中在去噪一章**（原文式 1–8，论文自认"带数学公式与伪代码的去噪综述"是其独特贡献）；特征工程与分类两章原文以叙述加应用表为主，下文对应小节的公式为方法通式（站内补，便于查原理），不代表原文给出。

## 2 采集

侵入式 vs 非侵入式两条路线；便携设备单列一节——Emotiv EPOC（14 通道）、Muse 头带（10–20 系统 4 记录电极 AF7/AF8/TP9/TP10 + 参考 Fpz，用于卒中识别）等，代价是通道少、精度低。参考电极的选择问题在采集阶段就提出：EEG 记录的是活动电极与参考电极的电位差，参考点选在哪，数据就长什么样。

## 3 去噪：五族方法（原文式 1–8）

伪迹来源两类：生理性（眼动/眨眼、心电、肌电）与外部干扰。五族方法的取舍逻辑：有明确参考通道用回归；无参考、按统计独立性分离用 ICA；按方差排序去噪用 PCA；肌电伪迹自相关低、利用 EEG 与辅助通道的相关结构用 CCA；非平稳信号按尺度分解用小波；非线性非平稳、按局部振荡筛分用 EMD。

### 3.1 回归法（原文式 1）

同步记录眼电图（EOG），用回归系数估计伪迹在各地电通道中的占比，再从记录信号里减掉：

\[
eeg(t) = EEG(t) - \sum_{g=0}^{T} \beta_g \, eog(t-g)
\]

\( \beta_g \) 度量 \( t-g \) 时刻的 EOG 对当前记录的影响，多项形式允许滞后效应。两大缺陷：**双向污染**——EOG 记录里本身就混有脑电电位，减 EOG 的同时减掉了真信号；无明确参考通道的伪迹（如 EMG）没法回归。论文的判断：随着 PCA/ICA 成熟，回归不再是 EOG/ECG 去伪迹的默认选择。

### 3.2 盲源分离：ICA 与 PCA（原文式 2–3）

**ICA** 把观测信号当作源的线性混合：

\[
X = AS
\]

\( X \) 为 EEG 数据矩阵，\( A \) 为混合矩阵，\( S \) 为统计独立的源（脑活动源 + 伪迹源）。求 \( A \) 的迭代思路是利用源的非高斯性（FastICA 类算法：中心化 → 白化 → 迭代更新分离矩阵至收敛），得到独立分量后人工或自动识别伪迹分量、置零再重构。局限：EEG 与 EMG 在时域、频域、空间上重度重叠，常规 ICA 分不干净——论文引 ERASE（把颈/头部肌电参考通道作为额外输入进 ICA，提高 EMG 在少数分量中的功率，比传统 ICA 平均多去 26% 的 EMG 伪迹）。

**PCA** 走方差路线，对协方差矩阵做特征分解：

\[
XX^{\top}\omega_i = \lambda_i \omega_i
\]

特征值排序后取前 \( d \) 个特征向量作投影矩阵 \( W^* \)，\( D^* = W^{*\top}D \) 降维——小特征值方向对应噪声，丢弃即部分去噪。弱点：方差大 ≠ 脑信号（眼电伪迹方差往往最大），投影子空间的选取依赖阈值。

### 3.3 典型相关分析 CCA（原文式 4）

利用肌电伪迹自相关低于脑活动这一性质，求两组信号（EEG 与辅助通道如 EOG/ECG）的最大相关线性组合：

\[
\max_{u,v} \frac{u^{\top} R_{xy} v}{\sqrt{u^{\top} R_{xx} u \; v^{\top} R_{yy} v}}
\]

\( R_{xx}, R_{yy} \) 为两组数据各自的协方差矩阵，\( R_{xy} \) 为互协方差。求解是广义特征值问题；得到典型变量后减去与伪迹相关的成分。论文定位：**肌电伪迹场景下 CCA 通常优于 ICA**。

### 3.4 小波变换（原文式 5–6）

离散小波变换把信号投影到尺度-平移网格：

\[
DWT(m,n) = \int_{-\infty}^{+\infty} x(t)\,\psi_{m,n}(t)\,dt
\]

多分辨率分解（Mallat 滤波器组：低通得近似系数、高通得细节系数，逐层递推）：

\[
x(t) = \sum_{j=1}^{K}\sum_{k=-\infty}^{\infty} d_j(k)\,\psi_{j,k}(t) \;+\; \sum_{k=-\infty}^{\infty} a_K(k)\,\phi_{K,k}(t)
\]

\( d_j(k) \) 是尺度 \( 2^j \) 的小波（细节）系数，\( a_K(k) \) 是最粗尺度的尺度（近似）系数。去噪 = 对细节系数做软/硬阈值处理、保留近似系数、逆变换重构。优点是无冗余；缺点是**缺平移不变性**（信号平移后系数剧变）——平稳小波变换（SWT）可补此缺陷但引入冗余且慢。小波常与其他方法组合（WT+ICA 分离 EMG/ECG；自适应阈值小波 + 50 Hz IIR 陷波处理眼电与工频）。

### 3.5 经验模态分解 EMD（原文式 7）

面向非线性非平稳信号的自适应分解，不设基函数，靠信号自身极值点筛分（sifting）：找局部极值 → 插值上下包络 → 均值作为"细节"剥离，反复迭代直到满足 IMF 条件（过零点数与极值点数相等/近似、包络均值为零）：

\[
x(t) = \sum_{i=1}^{n} C_i(t) + r_N(t)
\]

\( C_i \) 为本征模态函数（IMF，从高频到低频依次筛出），\( r_N \) 为单调残差。伪迹（常为高频细节）筛出后剔除、其余重构。弱点：依赖极值点，对尖峰噪声敏感，会产生**模态混叠**——论文引 EEMD（加白噪声多次分解取平均）与 MAMA-EMD（移动平均预处理 + 最小弧长判据缓解多点尖峰）两代改进。EEMD+CCA 组合用于低 SNR 单通道场景（EEMD 造出足够多的"通道"供 CCA/ICA 利用）。

### 3.6 去噪评价指标（原文式 8）

\[
MSE = \tfrac{1}{n}\sum_{i=1}^{n}(y_i-\hat{y}_i)^2,\quad RMSE = \sqrt{MSE},\quad SNR = 10\log_{10}\frac{\sum y_i^2}{\sum (y_i-\hat{y}_i)^2},\quad PRD = \sqrt{\tfrac{\sum|y_i-\hat{y}_i|^2}{\sum y_i^2}}\times 100\%
\]

\( y \) 为原始信号、\( \hat{y} \) 为去噪后信号；PRD 越低越接近原信号。

## 4 特征工程：三族原理（通式为站内补）

### 4.1 时频分析

建立时间-频率的联合表示，核心是滑窗加窗谱：

\[
X(\tau,\omega) = \int x(t)\, w(t-\tau)\, e^{-j\omega t}\,dt \quad (\text{STFT})
\]

窗长固定是 STFT 的分辨率枷锁（时间/频率分辨率不可兼得）；论文还提到用 CNN 优化 Wigner–Ville 分布作为免参数的高分辨率时频输入。EEG 常用落地：分窗打分定位癫痫段、频带功率（δ/θ/α/β/γ）特征、SVD 去噪后检测峰特征。

### 4.2 高阶谱分析

功率谱只是二阶统计，丢相位、且对高斯噪声无差别响应。高阶谱定义为高阶累积量的多维傅里叶变换，以三阶的双谱为代表：

\[
B(\omega_1,\omega_2) = E\big[X(\omega_1)\,X(\omega_2)\,X^*(\omega_1+\omega_2)\big]
\]

性质：理论上对高斯过程恒为零——**天然抑制高斯噪声**；保留非高斯/非线性信息（相位耦合）。论文引的落地：HOS 特征 + PCA 做癫痫信号非线性识别、神经营销 EEG 分析（HOS + 高斯核 SVM 平均 73.24%）、情绪状态判别（95.7%）。

### 4.3 非线性动力学

线性方法刻画不了 EEG 的动态结构，转用混沌/复杂度指标族（原文列举，未给公式；下式为各指标通式）：

- **最大 Lyapunov 指数**（轨道发散速率，\( d_j(t) \approx d_0\,e^{\lambda t} \)，\( \lambda_{\max} = \tfrac{1}{\Delta t}\langle \ln \tfrac{d_j(t)}{d_0} \rangle \)，\( \lambda>0 \) 即混沌）；
- **关联维 / 分形维**（Grassberger–Procaccia：\( C(r) \propto r^{D_2} \)，双对数斜率即关联维）；
- **熵族**：近似熵 ApEn、样本熵 SampEn（\( -\ln(A/B) \)，长度 \( m \) 的相似模式在 \( m+1 \) 仍相似的条件概率）、排列熵、小波熵；
- **复杂度**：Lempel–Ziv（语法压缩行程数），论文引自适应/多尺度 LZC 区分三种情绪状态、等符号熵（ESE）。

## 5 分类：传统 ML 与 DL

### 5.1 传统机器学习

论文收录族谱：NB、决策树、KNN、SVM、随机森林、LDA。方法原理（通式）：

- **SVM**：间隔最大化 \( \min \tfrac{1}{2}\|w\|^2 + C\sum_i \xi_i \;\; \text{s.t.}\; y_i(w^{\top}x_i + b) \ge 1-\xi_i \)，核技巧 \( K(x,x') = \langle\phi(x),\phi(x')\rangle \)（RBF/多项式/sigmoid）；论文的应用表里 **SVM 是出镜率最高的分类器**（癫痫、抑郁、精神分裂、情绪等表 4/5）。
- **KNN**：欧氏距离最近 \( k \) 邻居多数表决；MI 二分类加高斯噪声增强后平均 88.57%（论文引文口径）。
- **随机森林**：bootstrap 采样 + 节点随机特征子集，分裂准则 Gini \( G = 1-\sum_k p_k^2 \)；在负情绪 EEG 性别识别与眩晕分级上优于 AdaBoost/KNN。
- **LDA**：Fisher 准则 \( \max_w \frac{w^{\top} S_B w}{w^{\top} S_W w} \)（类间散布/类内散布之比最大化），MI 下肢分类与 KNN 组合报 84.62%。
- 决策树：信息增益 \( IG = H(D) - \sum_i \frac{|D_i|}{|D|}H(D_i) \)；NB：\( \arg\max_c\, p(c)\prod_i p(x_i\mid c) \)。
- MI 经典路线 FBCSP（滤波器组共空间模式）出现在其参考文献（BCI Competition IV 2a/2b）。

论文的横评结论：监督式（SVM/KNN）普遍优于无监督；单一分类器只适用特定场景，多分类器多数投票（SVM+LDA+ANN 组合报 85.36%）是常见补救。

### 5.2 深度学习

流程（原文 Figure 4）：去噪 + 特征工程 → 重排成 2D/3D 输入 → CNN 训练调优选最优。方法原理（通式）：

- **CNN**：卷积 \( h_{ij} = \sigma(\sum_m w_{im} x_{m+j} + b) \) + 池化降采样，逐层提特征；
- **RNN/LSTM**：\( f_t = \sigma(W_f[h_{t-1},x_t]+b_f) \)、\( i_t/o_t \) 同构，细胞状态 \( c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t \)，\( h_t = o_t \odot \tanh(c_t) \)——门控保长程依赖，适配 EEG 时序；
- **GAN**：生成器-判别器极小极大博弈 \( \min_G \max_D\; E[\log D(x)] + E[\log(1-D(G(z)))] \)，用于 EEG 数据增强与伪迹生成。

论文引的应用数字：MFCC 特征 + CNN 的卒中评估比逻辑回归高 22.86 个百分点；VGG-16/ResNet-50 卒中检测 90%；AlexNet 视觉化睡眠障碍判别 93.33%（优于 GoogLeNet）；CNN+RNN 睡眠分期 79.7%（Fp1/Fp2 双通道）；DeprNet 抑郁检测；端到端驾驶员认知负荷分类；轻量多维注意力网络回应跨数据集泛化与可解释性。

## 6 挑战与展望（原文 §3）

挑战五条：噪声与非平稳；**容积传导**（多源信号叠加，源定位困难）；**参考电极选择**（选点不同则数据不同）；个体差异；深度学习可解释性。展望三条：XAI（Smooth-Grad 类方法已用于情绪识别与棘波检测）、域适应、联邦学习。

## 7 证据边界与站内视角

- 综述自身无实验，评价性结论均为转述（如"DL 与 ML 在癫痫检测准确率相当"注明为文献综合口径）；无 PRISMA 检索协议，收录范围不可复现。
- 数学分布：公式集中在去噪一章（原文式 1–8）；特征工程与分类两章原文为叙述 + 应用表，本文两节中的通式为站内补注，引用原文时勿把通式当作原文内容。
- 与站内 FM 综述的分工：[Yao](yao-eegfm-survey.md) / [Chen](chen-representation-learning-review.md) 记录 FM 现状，[Kuruppu](kuruppu-critical-review.md) 批判评测，[Kwon](kwon-neural-fm-perspective.md) 给规范主张，本篇补**传统信号处理方法学底盘**——FM 论文集体跳过的去噪与特征工程环节在这里有完整方法清单；[Kuruppu §5.1](kuruppu-critical-review.md) 批评 FM「Minimal data preprocessing」，本文即该环节的背景文献。
- 时间边界：2023 年中截稿，无任何基础模型/大规模预训练内容；引用它定位「传统四阶段范式」即可，不要引它描述 FM 现状。

---

**相关阅读**

:material-vector-link: [预训练范式对比（本文的去噪/特征两阶段在 FM 里被掩码建模整体替换）](../../topics/pretraining.md) ｜ :material-clipboard-check: [Kuruppu 批判综述（「Minimal data preprocessing」的出处）](kuruppu-critical-review.md) ｜ :material-book-open-variant: [Yao FM 综述（有 PRISMA 协议的对照面）](yao-eegfm-survey.md) ｜ :material-lighthouse: [EEGArena（FM 时代的统一评测）](../survey/eegarena.md)
