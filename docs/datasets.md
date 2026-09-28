---
title: 数据集索引
tags: [索引, 数据集]
---

# 数据集索引

十一篇精读论文（核心六篇 + RF-GPT / JET / EEGMoE / LUNA / CBraMod）用到的全部数据集汇总。**↑ = 预训练语料，↓ = 下游评估**（JET 的 P 指生成训练使用）。同一数据集在不同论文中命名可能不同，见底部[别名说明](#dataset-alias)。

## 📊 数据集 × 论文使用矩阵

<div class="mx-wrap">
<table class="mx-matrix">
<thead><tr><th>数据集 \ 论文</th><th>BIOT</th><th>LaBraM</th><th>EEGPT</th><th>BrainGPT</th><th>NeuroLM</th><th>TFM</th><th>EEGMoE</th><th>LUNA</th><th>JET</th><th>RF-GPT</th><th>CBraMod</th></tr></thead>
<tbody><tr><th>TUAB</th><td class="mx-cell mx-d" title="下游评估">D</td><td class="mx-cell mx-d" title="下游评估">D</td><td class="mx-cell mx-d" title="下游评估">D</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-d" title="下游评估">D</td><td class="mx-cell mx-d" title="下游评估">D</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-d" title="下游评估">D</td><td class="mx-cell mx-b" title="生成训练 + TS-FID 评估">P+D</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-b" title="预训练 + 下游">P+D</td></tr><tr><th>TUEV</th><td class="mx-cell mx-d" title="下游评估">D</td><td class="mx-cell mx-d" title="下游评估">D</td><td class="mx-cell mx-d" title="下游评估">D</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-d" title="下游评估">D</td><td class="mx-cell mx-d" title="下游评估">D</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-b" title="生成训练 + TS-FID 评估">P+D</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-b" title="预训练 + 下游">P+D</td></tr><tr><th>TUEG（总体）</th><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-p" title="预训练语料">P</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-p" title="预训练语料">P</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-p" title="预训练语料">P</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-p" title="预训练语料">P</td></tr><tr><th>TUSZ</th><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-p" title="预训练语料">P</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-p" title="预训练语料">P</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-b" title="生成训练 + TS-FID 评估">P+D</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-p" title="预训练语料">P</td></tr><tr><th>TUEP / TUAR / TUSL</th><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-p" title="预训练语料">P</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-p" title="预训练语料">P</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-d" title="TUAR/TUSL 下游；TUEP 含于 TUEG 预训练">D</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-p" title="预训练语料">P</td></tr><tr><th>SEED（原始）</th><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-p" title="预训练语料">P</td><td class="mx-cell mx-p" title="预训练语料">P</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-d" title="下游评估">D</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-p" title="预训练语料">P</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td></tr><tr><th>SEED-IV / SEED-V</th><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-b" title="预训练 + 下游">P+D</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-d" title="下游评估">D</td><td class="mx-cell mx-p" title="预训练语料">P</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-d" title="下游评估">D</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-d" title="下游评估">D</td></tr><tr><th>DEAP / FACED</th><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-d" title="下游评估">D</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-d" title="下游评估">D</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-d" title="下游评估">D</td></tr><tr><th>PhysioMI</th><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-p" title="预训练语料">P</td><td class="mx-cell mx-p" title="预训练语料">P</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-p" title="预训练语料">P</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-p" title="EEGMMIDB 预训练">P</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-d" title="下游评估">D</td></tr><tr><th>HGD</th><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-p" title="预训练语料">P</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td></tr><tr><th>BCIC4-1 / MIBCI</th><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-p" title="预训练语料">P</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-d" title="下游评估">D</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-p" title="预训练语料">P</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td></tr><tr><th>BCIC-2A / 2B</th><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-d" title="下游评估">D</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-d" title="下游评估">D</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-d" title="下游评估">D</td></tr><tr><th>Grasp and Lift</th><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-p" title="预训练语料">P</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-p" title="预训练语料">P</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td></tr><tr><th>SHHS</th><td class="mx-cell mx-p" title="预训练语料">P</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td></tr><tr><th>EDF / HMC（睡眠）</th><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-d" title="下游评估">D</td><td class="mx-cell mx-d" title="下游评估">D</td><td class="mx-cell mx-d" title="下游评估">D</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td></tr><tr><th>EESM23（ear-EEG）</th><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-d" title="下游评估">D</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td></tr><tr><th>EEGMat / STEW（负荷）</th><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-d" title="下游评估">D</td><td class="mx-cell mx-d" title="下游评估">D</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-b" title="EEGMat 预训练 + STEW 下游">P+D</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-d" title="下游评估">D</td></tr><tr><th>Inria BCI / TVNT（P300）</th><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-p" title="预训练语料">P</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-p" title="预训练语料">P</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td></tr><tr><th>KaggleERN / PhysioP300</th><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-d" title="下游评估">D</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td></tr><tr><th>TSU（SSVEP）</th><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-p" title="预训练语料">P</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td></tr><tr><th>M3CV</th><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-p" title="预训练语料">P</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td></tr><tr><th>PTB-XL / Cardiology（ECG）</th><td class="mx-cell mx-b" title="预训练 + 下游">P+D</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td></tr><tr><th>HAR（可穿戴）</th><td class="mx-cell mx-d" title="下游评估">D</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td></tr><tr><th>MoBI（步态）</th><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-d" title="下游评估">D</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td></tr><tr><th>Raw EEG / Resting / Siena / SPIS / 自采集</th><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-p" title="预训练语料">P</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-p" title="预训练语料">P</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-p" title="Siena 预训练；TUEG 另计">P</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td></tr><tr><th>SHU-MI</th><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-d" title="下游评估">D</td></tr><tr><th>ISRUC</th><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-d" title="下游评估">D</td></tr><tr><th>CHB-MIT</th><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-d" title="下游评估">D</td></tr><tr><th>BCIC2020-3</th><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-d" title="下游评估">D</td></tr><tr><th>Mumtaz2016</th><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-d" title="下游评估">D</td></tr><tr><th>SEED-VIG</th><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-d" title="下游评估">D</td></tr><tr><th>DREAMER（未见验证）</th><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-d" title="下游评估">D</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-p" title="EEGMoE 预训练语料之一">P</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td></tr><tr><th>合成 RF 波形（MATLAB 六技术 + TorchSig）</th><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-n" title="未使用">·</td><td class="mx-cell mx-p" title="RF-GPT 生成/指令数据语料（12,000 场景 / 0.625M 指令对）">P</td><td class="mx-cell mx-n" title="未使用">·</td></tr></tbody>
</table>
</div>

<p class="mx-legend">图例：<span class="mx-cell mx-p">P</span> 预训练语料　<span class="mx-cell mx-d">D</span> 下游评估　<span class="mx-cell mx-b">P+D</span> 两者兼有　<span class="mx-cell mx-n">·</span> 未使用　（悬停查看说明；ECG 与 IMU 数据仅 BIOT 跨模态使用；SEED-IV/V 为 LaBraM 预训练 + LaBraM/NeuroLM/BrainGPT 相关任务；LUNA 预训练 = TUEG + Siena；EEGMoE 预训练 = 6 个认知任务数据集；JET 的 P+D = 生成训练 + TS-FID 评估；RF-GPT 的 P = 合成指令语料；CBraMod 的 P+D = TUEG 系预训练 + 剔除下游后重评的防泄漏版）</p>

---

## 临床 EEG（Temple 大学 TUEG 体系）

| 数据集 | 任务 | 配置 | 规模 | 使用情况 |
|---|---|---|---|---|
| **TUEG** | 临床 EEG 语料 | 17–23ch / 250–1024Hz | ~24,000h | NeuroLM↑ · LUNA↑（21,787h） · CBraMod↑（清洗后 >9000h） |
| **TUAB** | 异常检测（二分类） | 23ch / 256Hz / 10s | 409,455 样本 | BIOT↓ LaBraM↓ NeuroLM↓ EEGPT↓ TFM↓ LUNA↓ JET⚙（生成） CBraMod↓（防泄漏重训版仍 SOTA） |
| **TUEV** | 事件分类（6 类） | 23ch / 256Hz / 5s | 112,491 样本 | BIOT↓ LaBraM↓ NeuroLM↓ EEGPT↓ TFM↓ JET⚙（生成） CBraMod↓（防泄漏重训） |
| **TUSL** | 慢波分类（3 类） | 23ch / 256Hz / 10s | 245 样本 | NeuroLM↓ LUNA↓ · LaBraM↑ |
| **TUSZ** | 癫痫事件检测 | 19–23ch / 256Hz | 1,138.5h | LaBraM↑ NeuroLM↑ · JET⚙（生成） |
| **TUEP** | 癫痫/非癫痫 | 19–23ch / 256Hz | 591.2h | LaBraM↑ NeuroLM↑ |
| **TUAR** | 伪迹标注（5 类） | 23ch / 256Hz | 92.2h | LaBraM↑ NeuroLM↑ · LUNA↓（SOTA 0.921） |

## 情绪识别

| 数据集 | 任务 | 配置 | 规模 | 使用情况 |
|---|---|---|---|---|
| **SEED** | 3 类情绪 | 62ch / 1000Hz | 15 被试 | NeuroLM↓ · EEGPT↑ LaBraM↑ EEGMoE↑ |
| **SEED-IV** | 4 类情绪 | 62ch / 1000Hz | 15 被试 | BrainGPT↓ · LaBraM↑ NeuroLM↑ |
| **SEED-V** | 5 类情绪 | 62ch / 1000Hz | 20 被试 | LaBraM↓ BrainGPT↓ LUNA↓（未见拓扑） CBraMod↓（开源 16 人版） |
| **DEAP** | 情绪 (4 类) | 32ch / 128Hz | 32 被试 | BrainGPT↓ EEGMoE↓（V/A LOSO） |
| **MAHNOB-HCI** | 情绪（维度模型） | 32ch / 256Hz | 27 被试 | EEGMoE↑（预训练） |
| **FACED** | 9 类情绪 | 30ch / 1000Hz | 123 被试 | BrainGPT↓ CBraMod↓ |
| **Emobrain** | 情绪 (IAPS 诱发) | 64ch / 1024Hz | 16 被试 | LaBraM↑ NeuroLM↑ |

## 运动想象 / 执行

| 数据集 | 任务 | 配置 | 规模 | 使用情况 |
|---|---|---|---|---|
| **PhysioMI**（EEG Motor Movement/Imagery，EEGMMIDB） | MI & ME | 64ch / 160Hz | 109 被试 | EEGPT↑ LaBraM↑ NeuroLM↑ EEGMoE↑ CBraMod↓ |
| **HGD** | MI（4 类） | 128ch | 14 被试 | EEGPT↑ |
| **MIBCI** | MI（2 类） | 64ch / 512Hz | 52 被试 | BrainGPT↓ |
| **BCI Competition IV-1**（BCIC4-1） | MI（2 类+空闲） | 38–59ch / 100Hz | 7 被试 | BrainGPT↓ · LaBraM↑ NeuroLM↑ EEGMoE↑ |
| **BCI Competition IV-2a**（BCIC4-2a） | MI（4 类） | 22ch / 250Hz | 9 被试 | EEGMoE↓（LOSO） CBraMod↓ |
| **SHU-MI** | MI（2 类：左右手） | 32ch / 250Hz | 25 被试 | CBraMod↓ |
| **Grasp and Lift** | 抓握动作 | 32ch / 500Hz | 12 被试 | LaBraM↑ NeuroLM↑ |

## 睡眠分期

| 数据集 | 任务 | 配置 | 规模 | 使用情况 |
|---|---|---|---|---|
| **SHHS** | 睡眠分期 | 2ch / 125Hz / 30s | 5,445 录音（500 万样本） | BIOT↑ |
| **EDF** | 睡眠分期（5 类） | 2ch / 100Hz | 78 晚 | BrainGPT↓ |
| **HMC** | 睡眠分期（5 类） | 4ch / 256Hz / 30s | 151 被试 | NeuroLM↓ BrainGPT↓ |
| **EESM23** | **ear-EEG** 睡眠分期 | 4ch（耳道电极） | 10 被试 | TFM 跨设备评估 |
| **ISRUC** | 睡眠分期（5 类） | 6ch（对侧导联）/ 200Hz | 100 晚 | CBraMod↓ |

## 认知负荷

| 数据集 | 任务 | 配置 | 规模 | 使用情况 |
|---|---|---|---|---|
| **EEGMat**（NeuroLM 中称 Workload，CBraMod 中称 MentalArithmetic） | 高/低认知负荷 | 19ch / 500Hz | 36 被试（BrainGPT 报 34） | NeuroLM↓ BrainGPT↓ EEGMoE↑（预训练） CBraMod↓ |
| **STEW** | 负荷（3 类） | 14ch / 128Hz | 45 被试 | BrainGPT↓ EEGMoE↓（LOSO） |
| **SEED-VIG** | 警觉度回归（PERCLOS 标签） | 17ch / 200Hz | 23 被试 | CBraMod↓ |

## ERP / P300 / SSVEP

| 数据集 | 任务 | 配置 | 规模 | 使用情况 |
|---|---|---|---|---|
| **Inria BCI** | P300 拼写 | 56ch / 600Hz | 26 被试 | LaBraM↑ NeuroLM↑ |
| **Target vs Non-Target** | P300 oddball | 32ch / 512Hz | 50 被试 | LaBraM↑ NeuroLM↑ |
| **PhysioP300** | P300 目标检测 | — | 9 被试 | EEGPT↓ |
| **KaggleERN** | 错误相关负电位 ERN | 56ch | 26 被试 | EEGPT↓ |
| **TSU** | SSVEP（40 目标） | 64ch / 250Hz | 35 被试 | EEGPT↑ |
| **M3CV** | 多范式生物识别 | — | 106 被试 | EEGPT↑ |

## 癫痫 / 精神诊断 / 想象语音

| 数据集 | 任务 | 配置 | 规模 | 使用情况 |
|---|---|---|---|---|
| **CHB-MIT** | 癫痫检测（2 类） | 16 双极导联 / 256Hz | 23 患者（儿科）/ 326,993 样本 | CBraMod↓ |
| **Mumtaz2016** | 抑郁症诊断（2 类） | 19ch / 256Hz | 34 MDD + 30 正常 | CBraMod↓ |
| **BCIC2020-3** | 想象语音（5 词） | 64ch / 256Hz | 15 被试 / 6,000 样本 | CBraMod↓ |

## ECG / 可穿戴 / 跨模态 / 其他

| 数据集 | 任务 | 配置 | 规模 | 使用情况 |
|---|---|---|---|---|
| **PTB-XL** | ECG 心律失常（二分类） | 12 导联 / 500Hz | 21,911 录音 | BIOT↓ |
| **Cardiology（5 套合集）** | ECG | 6/12 导联 / 500Hz | 21,264 录音 | BIOT↑ |
| **HAR** | 可穿戴 IMU 动作（6 类） | 9 坐标 / 50Hz | 30 被试 | BIOT↓ |
| **MoBI** | 步态关节角回归 | 60ch / 100Hz | 8 被试 | LaBraM↓ |
| **Raw EEG Data**（Trujillo 2020） | 信息整合分类 | 64ch / 256Hz | — | LaBraM↑ NeuroLM↑ |
| **Resting State**（Trujillo 2017） | 静息态 | 64ch / 256Hz | 22 被试 | LaBraM↑ NeuroLM↑ |
| **Siena Scalp** | 临床 EEG | 31ch / 512Hz | 14 患者 | LaBraM↑ NeuroLM↑ LUNA↑（预训练） |
| **SPIS** | 静息+持续注意 | 64ch / 2048Hz | 10 被试 | LaBraM↑ NeuroLM↑ |
| **Self-collected** | 混合任务 | 62ch / 1000Hz | 140+ 被试 | LaBraM↑ NeuroLM↑ |
| **DREAMER** | 情绪（预训练未见） | — | 23 被试 | BrainGPT 迁移性验证 · EEGMoE↑（预训练） |
| **合成 RF 波形** | RF 信号合成（6 无线技术 + TorchSig 调制） | — | ~12,000 场景 | RF-GPT↑（生成/指令语料，零人工标注） |

## 别名说明 {: #dataset-alias }

| 别名 | 指向 |
|---|---|
| EEGMat = Workload | 同一数据集（Zyma et al. 2019 心算范式），BrainGPT 称 EEGMat、NeuroLM 称 Workload |
| BCI Competition IV-1 = BCIC4-1 | 同一数据集（Blankertz et al. 2007） |
| PhysioMI = EEGMMIDB = EEG Motor Movement/Imagery Dataset | PhysioNet 上的 BCI2000 采集数据（Schalk et al. 2004） |
| BCI Competition IV-2a = BCIC4-2a | 同一数据集（Brunner et al. 2008 Graz data set a），EEGMoE 记作 BCIC4-2a |
| SEED 系列 | SEED / SEED-IV / SEED-V / SEED-GER / SEED-FRA 的统称 |
| EDF | Sleep-EDFx 数据库的子集（Kemp et al. 2000），BrainGPT 基准中称 EDF |
| SEED 系列与 NeuroLM | NeuroLM 预训练的 "SEED Series" 指 SEED-IV/V/GER/FRA，不含原始 SEED（原始 SEED 对 NeuroLM 为下游） |
