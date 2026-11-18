---
title: 动手看懂 EEG 信号处理
tags: [工具, 交互示例, 信号处理]
---

# 动手看懂 EEG 信号处理

> 三个轻量交互示例，用**固定种子的合成信号**演示论文里的三个基本操作：切段（tokenization）、时频变换（TFM / BrainBERT 类输入）、掩码（MAE / REVE 类预训练）。全部计算在你的浏览器里完成，参数只保留能解释方法差异的采样率、窗口长度、频率与掩码比例。已知频率的合成正弦可自查谱峰位置（见示例二的验收说明）。禁用脚本时本页显示各示例的静态说明。

## 示例一 · 波形 → patch {: #demo-patch }

连续信号按窗长切段是所有 FM 的第一步（BIOT 1s 重叠 0.1s、REVE 同款；CBraMod 1s；BrainGPT 1s）。改「窗长」看 patch 数量与边界变化，改「频率 2」看波形叠加。

<div class="eeg-demo">
<div class="eeg-ctrl">
  采样率 <input type="number" id="d1-sr" value="256" min="64" max="512" step="32"> Hz ·
  时长 <input type="number" id="d1-dur" value="4" min="2" max="8" step="1"> s ·
  频率 1 <input type="number" id="d1-f1" value="10" min="1" max="60"> Hz ·
  频率 2 <input type="number" id="d1-f2" value="30" min="1" max="80"> Hz ·
  窗长 <input type="number" id="d1-win" value="1" min="0.1" max="2" step="0.1"> s ·
  重叠 <input type="number" id="d1-ov" value="0.1" min="0" max="0.9" step="0.1">
  <span id="d1-info"></span>
</div>
<canvas id="d1-canvas" width="760" height="180"></canvas>
<p class="eeg-cap">合成信号 = 10 Hz 正弦 + 30 Hz 正弦（幅度减半）+ 固定种子噪声；竖线为 patch 边界。每个 patch 经线性嵌入成为 transformer 的一个 token——patch 内含全部频率成分。</p>
</div>

## 示例二 · 窗口变化 → 时频图 {: #demo-tf }

时频 patching（BrainBERT 的 STFT/Superlet 输入）先做 2D 谱图再切 token。**短窗时间准、频率糊；长窗反之**——拖动窗长看 10 Hz 与 30 Hz 两条谱峰怎么变。

<div class="eeg-demo">
<div class="eeg-ctrl">
  STFT 窗长 <input type="range" id="d2-win" min="32" max="256" step="16" value="64"> <span id="d2-winlabel">64 样本（0.25 s）</span>
</div>
<canvas id="d2-canvas" width="760" height="220"></canvas>
<p class="eeg-cap">纵轴 0–50 Hz、横轴时间。验收自查：30 Hz 成分幅度为 10 Hz 的一半，谱图上两条亮带的纵轴位置应分别停在 10 与 30 Hz（对应颜色刻度）。窗长短时 10 Hz 峰展宽（频率分辨率 = 采样率 / 窗长）。</p>
</div>

## 示例三 · 随机掩码 vs 时空块掩码 {: #demo-mask }

MAE 式随机点掩码 vs REVE 式时空块掩码（空间半径连续通道 + 时间连续窗）。EEG 邻域高度自相关——随机点留下的信息可以从旁边「插值」出来，块掩码把整片邻域一起挖掉。

<div class="eeg-demo">
<div class="eeg-ctrl">
  掩码比例 <input type="range" id="d3-ratio" min="10" max="80" step="5" value="40"> <span id="d3-ratiolabel">40%</span> ·
  块掩码空间半径 <input type="number" id="d3-rs" value="2" min="1" max="4"> 通道 ·
  时间半径 <input type="number" id="d3-rt" value="1" min="1" max="4"> patch
  <span id="d3-info"></span>
</div>
<canvas id="d3-canvas" width="760" height="220"></canvas>
<p class="eeg-cap">8 个模拟通道 × 24 个时间 patch 的网格：灰 = 可见（encoder 输入），红 = 被掩（decoder 重构目标）。左半随机点、右半连续块——同比例下块掩码覆盖的邻域更大，逼模型学结构而非插值。</p>
</div>

---

**对应论文**：切段与重叠 — [BIOT](papers/fm/biot.md) · [REVE](papers/fm/reve.md)；时频输入 — [BrainBERT（Chen 综述拆解表）](papers/reviews/chen-representation-learning-review.md) · [TFM-Tokenizer](papers/fm/tfm-tokenizer.md)；掩码 — [预训练范式专题](topics/pretraining.md) · [REVE 块掩码消融](papers/fm/reve.md)。

**相关阅读**：[论文库](library.md) ｜ [模型对比](models.md) ｜ [首页](index.md)
