---
date: 2026-11-02
title: "Learnable Time-Frequency Transform With Application to EEG Signal Analysis"
authors: [Guoyang Liu, Lan Tian, Weidong Zhou]
venue: "IEEE TETCI 2026"
year: 2026
tags: [EEG, 时频分析, 可学习变换, 信号前端, S变换, 可解释性]
status: "精读"
rating: 4
doi: "10.1109/TETCI.2026.3684470"
code: ""
one-liner: "把时频变换的复值窗口本身做成可训练参数：每个频率一个自由复窗口，Wirtinger 共轭梯度端到端联合优化，理论上把 STFT/CWT/S 变换全部收为特例"
---
# Learnable Time-Frequency Transform With Application to EEG Signal Analysis

> **IEEE TETCI 2026**

**作者**：Guoyang Liu, Lan Tian, Weidong Zhou\*（通讯，山东大学）

## 1 问题定位：窗口选择这个「手工活」

时频谱图进神经网络是 EEG 分类的主流管线，但整条管线里最上游的一步——选什么窗、什么母小波——始终是手工的：STFT 的窗长窗型、CWT 的母小波、S 变换的高斯宽度，都按数据分布人工调。混合管线的变换和网络是**分开优化**的，变换端永远拿不到任务损失的梯度。

已有可学习前端的修法各有保留：LEAF 学 Gabor 滤波器组、SincNet 学 sinc 带通、CWConv 只学母小波的尺度和平移、DSTFT 把 STFT 超参数连续化。共同点是核函数被约束在特定函数族里，作者认为这限制了适配能力，也不构成一个「一般的」可学习时频变换框架。LTFT 的回答是去掉全部先验：每频率一个复值窗口，实部虚部都训。

这篇文章的定位其实是信号处理社区的（作者组此前做过 S 变换癫痫检测、S 变换 ECG 质量评估），和站内 EEG 基础模型那条线语言不同，但回答的问题相邻：**频域表示该在哪一层被学习**。

## 2 方法

### 2.1 定义与前向

\[ L(\tau, f) = \int_{-\infty}^{+\infty} x(t)\, w_f(\tau - t)\, e^{-2\mathrm{i}\pi f t}\, \mathrm{d}t = \big(x(\tau)\, e^{-2\mathrm{i}\pi f \tau}\big) * w_f(\tau) \]

形式上就是 STFT，唯一区别是窗口 \( w_f(\xi) \) 带**频率下标**（不同频率可以有不同的窗口）且是自由复值函数。转到频域，对固定 \( f \)，LTFT 系数是信号谱的循环移位与窗口谱的乘积再逆变换：

\[ L(\tau, f) = \mathcal{F}^{-1}_{\alpha\to\tau}\big\{ X(\alpha + f)\, W_f(\alpha) \big\} \]

离散实现（式 8–9）：对归一化频率 \( f_m = m/NT \)，定义循环移位谱 \( [X_m]_n = X[(n+m) \bmod N] \)，则

\[ L_m = \mathrm{IFFT}\big( X_m \odot W_m \big) \in \mathbb{C}^N \]

每个频率 bin 一次 IFFT 出一整行时频系数，谱图取 \( |L(\tau,f)|^2 \)。这个实现继承自 S 变换的 FFT 加速路线，训练完成后 \( W_f \) 可缓存，推理代价与 STFT 同阶。

### 2.2 反向传播：复参数的 Wirtinger 梯度

损失 \( E \) 是实的，窗口 \( w_f \in \mathbb{C} \)，所以用 Wirtinger 微分沿共轭梯度 \( \partial E/\partial w_f^*(\xi) \) 更新。设上游梯度 \( \Delta(\tau,f) = \partial E/\partial P(\tau,f) \)（\( P = |L|^2 \) 为谱图输出，由自动微分免费拿到）。链式展开共三段（式 12–14），每段恰好对应一次傅里叶变换，闭式是这样一步步推出来的而不是凑出来的：第一段对谱图输出，\( \partial E/\partial L^* = \Delta \odot L \)（式 12）——实损失对复输出的标准 Wirtinger 结果，乘的是 \( L \) 本身而非其共轭；第二段经 \( L^*(\tau,f) = \int X^*(\alpha+f)\, W_f^*(\alpha)\, e^{-i2\pi\alpha\tau}\, d\alpha \) 传到窗口谱，\( \partial E/\partial W_f^*(\alpha) = X^*(\alpha+f)\, \mathrm{FFT}[\Delta \odot L] \)（式 13）——信号谱直接调制窗口梯度；第三段按 DFT 定义逆变换回时域，天然就是一个 IFFT（式 14）。合并（式 15–16）得

\[ \frac{\partial E}{\partial w_m^*} = \mathrm{IFFT}\big( X_m^* \odot \mathrm{FFT}(\Delta_m \odot L_m) \big) \]

前向的 \( L_m \) 直接复用，每频率代价 \( O(N\log N) \)，两个 FFT、两次逐点乘、一个 IFFT，完全不需要手写复数自动微分。窗口用带动量 SGD 更新（式 17）。两个值得注意的训练细节：正则化只加在网络参数 \( \theta \) 上（L2，\( \lambda = 0.001 \)，式 10 称「对所有网络」），**窗口 \( w \) 完全不正则**——这是一个大胆的选择，后面 MI 实验里「峰值后回落」的过拟合迹象与此直接相关（论文内部有个小矛盾：V-A 节又称合成实验的交叉熵「无任何正则惩罚」，与式 10 对不上）；窗口初始化为 S 变换的频率依赖高斯窗，即起点就是标准 ST。

### 2.3 与传统变换的关系：三退化一

这节是论文理论贡献的核心，证明自由复值窗口是三类传统变换的超集：

- **STFT**：取 \( w_f(\xi) = g(\xi) \)（与频率无关的固定窗），LTFT 退化为任意窗的 STFT；
- **CWT**：取 \( w_f(\xi) = \frac{1}{\sqrt{s(f)}}\, \psi^*\!\big(\tfrac{\xi}{s(f)}\big) e^{2\mathrm{i}\pi f \xi} \)（母小波的缩放调制版，\( s(f) \) 建立频率-尺度对应），则 \( L(\tau,f) = e^{-2\mathrm{i}\pi f \tau}\, \mathrm{CWT}(\tau,f) \)——即**相位校正 CWT**，绝对参考相位被保留（S 变换作者 Stockwell 强调过的性质）；
- **S 变换**：取 \( w_f(\xi) = \frac{|f|}{\sqrt{2\pi}} e^{-\xi^2 f^2/2} \)（频率依赖高斯窗），LTFT 恰为标准 S 变换。

超集关系本身不保证学到更好的变换，但它给了两条实际好处：初始化点（ST）有已知的好性质，且训完的窗口偏离初始化多少、在哪些频率偏离，可以直接当可解释性证据读。

## 架构图

![Figure 1 · 四种时频变换的对照：STFT 固定窗、CWT 母小波、ST 高斯窗均为预定义，LTFT 的核完全可学习](../assets/lft-overview.png)

*Figure 1 · 四种时频变换对照：前三行的核是手工预定义的，LTFT（末行）的核完全可学习，谱图每个像素都是学出来的表示*

![Figure 9 · LTFT + CNN + BiLSTM 的五类癫痫分类架构：逐 1 s 段变换，CNN 提特征，BiLSTM 建模段间时序，多数投票出结果](../assets/lft-cnn-bilstm.png)

*Figure 9 · Bonn 五类任务架构：每段 1 s EEG 独立过 LTFT 层（0–31 Hz，32×256 谱图，池化后 32×32），双卷积层 + 2×2 池化得 8×8×8 特征图，BiLSTM(256) 建模 23 个段的时序，多数投票定记录级标签*

---

**相关阅读**

:material-arrow-left: [Not-All-EEG（损失端频率加权 vs 变换端可学习窗口）](not-all-eeg.md) ｜ :material-creation: [TFM-Tokenizer（STFT 谱图 tokenizer，LTFT 的潜在替换对象）](tfm-tokenizer.md) ｜ :material-waveform: [BIOT（FFT 能量特征进 embedding）](biot.md) ｜ :material-chart-timeline-variant: [LaBraM（DFT 幅相作重构目标）](labram.md) ｜ :material-home: [首页](../index.md)
