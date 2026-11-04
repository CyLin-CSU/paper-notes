---
date: 2026-11-02
title: "Mapping Effective Connectivity by Virtually Perturbing a Surrogate Brain"
authors: [Zixiang Luo, Kaining Peng, Zhichao Liang, Shengyuan Cai, Chenyu Xu, Dan Li, Yu Hu, Changsong Zhou, Quanying Liu]
venue: "Nature Methods 2025"
year: 2025
tags: [有效连接, 因果推断, 代理脑模型, 计算神经科学, 虚拟扰动, 全脑建模, fMRI]
status: "精读"
rating: 4
arxiv: "https://arxiv.org/abs/2301.00148"
code: "https://github.com/ncclab-sustech/NPI"
one-liner: "训一个 MLP 代理脑，逐区虚拟扰动、读 t+1 响应差得全脑有效连接：方向×强度×兴奋/抑制一次给出，RNN 仿真 r=0.95、对 GC/DCM 全面占优，CCEP 613 病人作真实锚点（r=0.33 > FC 的 0.20）"
---
# Mapping Effective Connectivity by Virtually Perturbing a Surrogate Brain

> **Nature Methods 2025**

**作者**：Zixiang Luo, Kaining Peng, Zhichao Liang, Shengyuan Cai, Chenyu Xu, Dan Li, Yu Hu, Changsong Zhou, Quanying Liu\*（通讯，南方科技大学生物医学工程系）

## 1 问题定位：EC 的干预定义在人类身上无人能做

EC、SC、FC 三个概念里，SC 是解剖布线（扩散 MRI 示踪），FC 是统计依赖（无方向、有伪连接），EC 才是有方向的因果影响。作者开篇把 EC 的金标准钉在「扰动并记录」上：光遗传、DBS、CCEP 都是真扰动，但都有创、空间覆盖受限，不可能对全脑逐区做。

计算方法两条路各有病灶，论文的归因很清楚：

- **模型依赖的路（DCM）**：EC 定义为状态空间模型里的耦合参数，结论依赖模型假设，模型失配直接偏置结果；
- **模型无关的路（GC）**：能判方向，但强度测不准、兴奋/抑制分不开。GC 本质是预测性改进，不是干预；
- 还有一条近年路线：直接拿训练后 RNN 的权重矩阵当 EC。论文引了 Das & Fiete（Nature Neuroscience 2020）的批评——强循环网络里从活动反推连接有**系统性误差**，学到的权重没有理由等于底层 EC，区域数量一大更不可信。

NPI 的立场是：别从模型权重里读因果，把模型当**可干预的替身**，用与实验神经科学同构的「扰动-记录」协议在模型内部做实验。这一定义对齐 Pearl/Woodward 的操作主义因果观（论文明确引了 Pearl《Causality》），因此推出来的 EC 与光遗传式的实验 EC 在语义上同族——这是它区别于 GC/DCM 的关键卖点，也是后面 CCEP 验证能成立的逻辑前提。

## 2 方法

### 2.1 代理脑：三步输入 MLP

把 N 个脑区的集体活动记为 \( x_t \in \mathbb{R}^N \)，代理模型是一个纯前馈 MLP：

\[
\hat{x}_{t+1} = f(x_t,\ x_{t-1},\ x_{t-2},\ \theta)
\]

结构 3N → 2N → 0.8N → N（网格搜索定的），损失就是单步预测的 MSE，Adam lr=10⁻³，60 epoch，单卡 RTX 4080——训练成本小到不像 Nature Methods 的方法，但后面验证做得扎实。逐被试训练（HCP 每人 4×15 分钟数据），所以 EBC 是个体化的。3 步输入比 1 步输入的预测略好（Supp Fig 8）；作者还对比了 CNN/RNN/VAR 等架构做代理，MLP 在 FC 重现与 EC 推断上最好（Supp Table 1）。

代理模型合格的门槛不是预测精度本身，而是**能否重现区间关系**：把输出递归喂回去做自由生成，生成信号的 FC 与真实 FC 对比。HCP 800 人平均 r=0.97（图 1f 标注 0.97，正文 2.1 节出现 0.98，两处以 0.97 为准）。

### 2.2 虚拟扰动读 EC

训练完冻结网络，逐源区、逐时刻做冲激扰动。扰动加在**网络的输入端**：源区 i 的当前时刻分量 \( x_t \) 抬高 \( \Delta \)，历史两步输入、隐层激活、权重都不动（原文 "perturb each input node of the ANN"）：

\[
\mathrm{EC}_{i\cdot} = \mathbb{E}_t\big[\, f(x_t + \Delta e_i,\ x_{t-1},\ x_{t-2}) - f(x_t,\ x_{t-1},\ x_{t-2}) \,\big]
\]

\( e_i \) 是第 i 维单位向量，\( \Delta \) 取 0.5 倍 BOLD 标准差。读出的是 t+1 时刻（fMRI 上即 0.72 s 后）所有目标区的响应差：符号给兴奋/抑制，幅度给强度，源区固定、目标遍历即「一到全」，逐区扫完即全到全。

三点值得记：

1. **等价于期望 Jacobian**。小 Δ 下，冲激响应差 \( f(x_t+\Delta e_i) - f(x_t) \approx \Delta\,\partial f/\partial x_i \)，除以 Δ 就是 Jacobian 中「输入 i」对应的那一列（转置过来即 EC 矩阵的第 i 行）；再对所有观测到的状态取平均，得到的就是训练后网络 Jacobian 在**数据的状态分布**上的期望（Supp Note 4）。Ext Data Fig 2 把三方都对上了：数值算出的 ANN Jacobian、NPI-EC、以及 RNN 数据上真值 RNN 的 Jacobian 彼此一致。这给了方法一个干净的理论身份，也划出了它的边界：期望是对「被试实际流经的状态分布」取的，所以这份 EC 同时由网络结构与其状态统计共同决定，读出的是**局部线性化增益**，不是大扰动下的系统响应；
2. **状态依赖**。真实刺激的响应随脑状态变（论文引了颅内刺激响应随状态变化的病例证据，Scangos et al. 2021 的抑郁症病人单例报道），所以他们在每个时刻的状态各扰动一次、再平均——EC 是「典型状态下」的平均效应，不是某一时刻的效应。次数上这意味着每个源区要做 T 次扰动（单被试 4 个 session 共约 5,000 个时间点），期望就是对这批实际流经的状态取平均；
3. **扰动幅度小**。Δ=0.5σ 落在小信号区，恰好对应 Jacobian 解释；但 CCEP 的真实刺激是强扰动，两种扰动机制的口径差异是后文验证的一个隐性前提。

## 架构图

![Figure 1 · NPI 框架：观测信号 → 训练代理脑 → 虚拟扰动 → 全脑 EC](../assets/surrogate-npi-framework.png)

*Figure 1 · NPI 全流程：(a) 观测的多脑区信号；(b) MLP 学单步动力学；(c) 逐区虚拟扰动；(d) 读出全脑 EC。(e,f) 递归生成验证 FC（r=0.97）；(g,h) 扰动响应差给兴奋（b→a 升）/抑制（b→c 降）；(i) 合成数据上 NPI-EC 对真值 r=0.95；(j) 真实 fMRI 上的 seed-based EC*

![Figure 3 · HCP 800 人的群体级 EBC](../assets/surrogate-human-ebc.png)

*Figure 3 · Human EBC：(a) 800 人平均的全脑 EC 矩阵（按 7 个功能网络分块，红兴奋/蓝抑制，色标 Exc/Inh）；(b) 皮层区归入七个功能网络；(c) 模型 FC 对经验 FC r=0.97；(d) 逐网络的 seed-based FC 空间模式；(e) 逐网络的 seed-based EC（红兴奋/蓝抑制）；(f,g) 兴奋/抑制 EC 强度均为对数正态分布；(h) 二值化后的节点度分布*

## 与其他论文的关系

站内三篇候选对照都查过，没有与本篇的真实对话（本篇不引它们，主题坐标系也不同），下面如实标注；本篇真正的参照系是经典 EC 方法。

| 论文 / 工作 | 关系说明 |
|---|---|
| [BrainGPT](braingpt.md) | 都把神经网络训成神经信号的代理模型，用途相反：BrainGPT 是 EEG 上的表征/解码工具（模型输出是目的），NPI 把代理模型当**被解剖的对象**（模型只是扰动实验的容器）。站内 EEG 基础模型训完后是否也能这样扰动出「区间因果」，本篇提供了模板，但 EEG 的源定位模糊与容积传导会让「区」的定义先出问题——暂无直接对话 |
| [EEGDM](eegdm.md) | 两种「模型作工具」的分工：EEGDM 用生成模型产数据训表征，模型是数据工厂；NPI 用模型做反事实实验，模型是实验室。同一个代理模型在两个框架里甚至可以复用——暂无直接对话 |
| [EEGMoE](eegmoe.md) | 被试间差异的两种处理：EEGMoE 用专家分化吸收个体差异，NPI 逐被试训代理并用「跨 session 一致性 > 跨被试相关性」证明个体信号大于方法噪声。两个证据可以互相支撑，但技术上没有交集——暂无直接对话 |
| Granger 因果 | 论文的主要对比基线，三套仿真全胜（r=0.95 那套 p<10⁻³）。GC 是预测性定义，方向判得动、强度与符号测不准；NPI 的干预主义定义与实验 EC 同族，这是它敢叫 EC 而 GC 不敢的差别 |
| DCM | 模型依赖路线的代表。EC 定义为状态空间耦合参数，节点一多参数爆炸（66 节点上 DCM 实际不可用，公开合成数据上被 NPI 以 AUC 显著压制）。但 DCM 在小规模、假设充分时有完整的统计推断框架，NPI 没有等价物 |
| Das & Fiete（2020） | 本篇动机的直接来源之一：强循环网络中从活动反推连接有系统性误差。NPI 的回答是绕开权重读出，改做行为学式的扰动实验 |
| Pearl / Woodward 的因果观 | NPI 的 EC 定义显式对齐干预主义因果（do-操作/操作主义），是全文语义合法性的地基——EC 推得对不对，取决于「代理模型的扰动响应 ≈ 真实脑的扰动响应」这个迁移假设，而这是全文唯一无法直接验证的一环（CCEP 只是间接证据） |

---

**相关阅读**

:material-arrow-left: [BrainGPT（同样训代理模型，但作表征工具而非实验对象）](braingpt.md) ｜ :material-creation: [EEGDM（模型作生成工具 vs 本篇作科学工具）](eegdm.md) ｜ :material-chart-timeline-variant: [EEGMoE（被试间差异的另一种处理）](eegmoe.md) ｜ :material-home: [首页](../index.md)
