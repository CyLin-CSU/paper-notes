# -*- coding: utf-8 -*-
"""主题页与对比页的组件升级：Mermaid 时间线、内容标签页、Chart.js 图表、脚注、键帽。"""
import pathlib
import re

DOCS = pathlib.Path(r"C:\Users\ChengyeLin.LINOUP-XIAOXIN1\Desktop\work\paper-notes\docs")

# ---------- 1. tokenization.md：演进时间线 Mermaid ----------
p = DOCS / "topics" / "tokenization.md"
t = p.read_text(encoding="utf-8")
if "timeline" not in t:
    anchor = "## 演进时间线\n\n"
    mermaid = (
        "```mermaid\n"
        "timeline\n"
        "    title EEG Tokenization 演进\n"
        "    2023 : BIOT : 规则切段，连续 token，无词表\n"
        "    2024 : LaBraM : VQ 词表 8192，仅作预训练目标\n"
        "    2025 : NeuroLM : 码字并入 GPT-2 词表，接入 LLM\n"
        "    2026 : TFM-Tokenizer : 时频 motif 词表，token 作为模型输入\n"
        "```\n\n"
    )
    t = t.replace(anchor, anchor + mermaid, 1)
    # 位置编码争论处加脚注
    t = t.replace(
        "token 利用率 12.87%→9.78%）",
        "token 利用率 12.87%→9.78%[^pe]",
    )
    t = t.rstrip() + "\n\n[^pe]: TFM-Tokenizer 附录 C.6 消融：位置编码会让同一 motif 因位置不同学成不同 token，移除后 Cohen's Kappa 0.5119→0.5337、利用率 12.87%→9.78%、类独有 token 1.94%→2.14%。\n"
    p.write_text(t, encoding="utf-8")
    print("[+] tokenization.md：时间线 + 脚注")

# ---------- 2. pretraining.md：三条路线改标签页 + 脚注 ----------
p = DOCS / "topics" / "pretraining.md"
t = p.read_text(encoding="utf-8")
tabs = """=== "对比学习 · BIOT"
    扰动版预测原版表示（BYOL 式）：随机丢弃部分通道和 token 得到扰动信号，predictor + 对比损失（温度 T=0.2）让扰动版预测原版表示。

    预训练语料：PREST + SHHS + Cardiology，共约 1000 万样本。

=== "掩码建模 · LaBraM / EEGPT / TFM"
    看一部分、恢复另一部分。三家的"恢复目标"完全不同：

    - LaBraM → 预测**离散码字**（BEiT 式，附对称掩码）
    - EEGPT → 对齐**表示**（JEPA 式）+ 重构原始 patch（MAE 式）
    - TFM → 重构**掩码频谱图**（频带+时间+对称掩码，训练 tokenizer 本身）

=== "自回归 · BrainGPT / NeuroLM"
    因果地预测下一单元，贴合 EEG 的时序因果结构：

    - BrainGPT → 回归**连续信号值**（单电极，MSE）
    - NeuroLM → 阶梯掩码下预测**离散码**（因果 LLM，多通道）
"""
pat = re.compile(r"\| 路线 \| 论文 \| 核心机制 \| 关键设计 \|.*?(?=\n## 掩码建模)", re.S)
t, n = pat.subn(tabs + "\n", t, count=1)
print("[+] pretraining.md 标签页:", bool(n))
# 脚注
t = t.replace(
    "BrainGPT 给出了同架构、同损失度量下的直接对比（其 Table V）：",
    "BrainGPT 给出了同架构、同损失度量下的直接对比（其 Table V）[^t5]：",
)
t = t.replace("时间/空间复杂度对 N 均为线性", "时间/空间复杂度对 N 均为线性")  # no-op 防误替换
t = t.rstrip() + "\n\n[^t5]: BrainGPT Table V：同一模型架构与参数下，用 cos/ℓ1/ℓ2 三种重构损失对比 MAE 与 AR，AR 平均准确率高 2% 以上，ℓ2 为最优度量。\n"
p.write_text(t, encoding="utf-8")
print("[+] pretraining.md：脚注")

# ---------- 3. spatial.md：四种方案改标签页 ----------
p = DOCS / "topics" / "spatial.md"
t = p.read_text(encoding="utf-8")
tabs = """=== "① 通道 embedding 表 · BIOT"
    **机制**：每个通道名一个可学习向量，逐通道切段后加到 token 上。

    **优点**：简单直接；缺通道直接丢 token，结构不变。

    **局限**：向量表受训练时见过的通道限制，未见通道无对应 embedding。

=== "② 10-20 系统空间编码 · LaBraM / NeuroLM"
    **机制**：为 10-20 系统全部电极建空间 embedding 列表，按通道名索引。

    **优点**：统一坐标系；LaBraM 消融证明去掉后预训练不收敛。

    **局限**：非标准设备（ear-EEG 等）无对应 embedding。

=== "③ 单通道独立建模 · TFM / BrainGPT（电极级）"
    **机制**：tokenizer / 训练样本以单通道为单位，多通道只是结果拼接。

    **优点**：天然 device-agnostic，任意电极组合；预训练数据量 ×E 倍。

    **局限**：丢失跨电极同步信息，需下游模块补偿空间整合。

=== "④ 图结构整合 · BrainGPT（TEG）"
    **机制**：全电极建一张可学习图，样本只激活自己的子图（β mask），GAT 注意力交互。

    **优点**：多任务共享电极原型节点 + 一套 GAT 权重；任意配置统一训练。

    **局限**：空间整合只在下游阶段；电极集不相交的任务间共享大幅缩水。
"""
pat = re.compile(r"\| 方案 \| 论文 \| 机制 \| 优点 \| 局限 \|.*?(?=\n## 方案③的代价与补偿)", re.S)
t, n = pat.subn(tabs + "\n", t, count=1)
print("[+] spatial.md 标签页:", bool(n))
p.write_text(t, encoding="utf-8")

# ---------- 4. comparison.md：Chart.js 柱状图 ----------
p = DOCS / "comparison.md"
t = p.read_text(encoding="utf-8")
anchor = "# 六篇方法对比\n"
chart = """# 六篇方法对比

## 📊 TUEV Cohen's Kappa 横向对比（多数据集预训练设定）

数据来源：TFM-Tokenizer 论文 Table 1（统一评测口径）。† 表示在四个 EEG 数据集上复现预训练。

<canvas id="kappa-chart" height="130"></canvas>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var el = document.getElementById("kappa-chart");
  if (!el || typeof Chart === "undefined") return;
  new Chart(el, {
    type: "bar",
    data: {
      labels: ["BIOT", "EEGPT", "NeuroLM-B", "LaBraM-Base †", "CBraMod †", "TFM-Tokenizer"],
      datasets: [{
        label: "TUEV Cohen's Kappa",
        data: [0.5273, 0.5085, 0.4285, 0.5175, 0.5588, 0.6189],
        backgroundColor: [
          "#9e9e9e", "#8d6e63", "#90a4ae", "#7986cb", "#ffb74d",
          "rgba(48, 161, 78, 0.85)"
        ],
        borderRadius: 6
      }]
    },
    options: {
      indexAxis: "y",
      plugins: { legend: { display: false } },
      scales: { x: { min: 0.3, max: 0.7 } }
    }
  });
});
</script>
"""
t = t.replace(anchor + "\n", chart + "\n", 1)
p.write_text(t, encoding="utf-8")
print("[+] comparison.md 图表")

# ---------- 5. index.md：键帽样式 ----------
p = DOCS / "index.md"
t = p.read_text(encoding="utf-8")
t = t.replace("`Ctrl + K` 全文搜索", "++ctrl+k++ 全文搜索", 1)
p.write_text(t, encoding="utf-8")
print("[+] index.md 键帽")
