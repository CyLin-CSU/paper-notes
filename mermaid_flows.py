# -*- coding: utf-8 -*-
"""把六篇论文笔记的「流程」板块替换为 Mermaid 流程图。"""
import pathlib
import re

PAPERS = pathlib.Path(r"C:\Users\ChengyeLin.LINOUP-XIAOXIN1\Desktop\work\paper-notes\docs\papers\2026-09")

MERMAID = {
    "0918-biot.md": r"""```mermaid
flowchart LR
    A["原始多通道信号"] --> B["重采样 200Hz"]
    B --> C["95 分位数归一化"]
    C --> D["逐通道切段 1s / 重叠 0.5s"]
    D --> E["缺失 token 丢弃 + 展平成句"]
    E --> F["token embedding：FFT 能量 + 通道 + 位置"]
    F --> G["线性 Transformer ×4（低秩 E/F 投影）"]
    G --> H["mean pooling"]
    H --> I["ELU + 线性分类头"]
```""",
    "0918-labram.md": r"""```mermaid
flowchart TD
    subgraph S1["阶段一：神经 Tokenizer 训练"]
        A["EEG channel patch"] --> B["Temporal Encoder"]
        B --> C["VQ 查表（8192 码本）"]
        C --> D["Neural Decoder 重构 DFT 幅值 + 相位"]
    end
    subgraph S2["阶段二：掩码 EEG 建模"]
        E["随机掩码 50%（+ 对称掩码）"] --> F["预测被掩 patch 的码字索引"]
    end
    subgraph S3["阶段三：下游微调"]
        G["换任务预测头 + 平均池化"]
    end
    S1 --> S2 --> S3
```""",
    "0918-neurolm.md": r"""```mermaid
flowchart TD
    subgraph P1["阶段一：文本对齐 Tokenizer"]
        A["EEG patch → VQ Encoder"] --> B["查表 → 时域 / 频域双 Decoder"]
        A -. "梯度反转 GRL" .-> C["域分类器：EEG 还是文本"]
    end
    subgraph P2["阶段二：多通道自回归"]
        D["码字并入 GPT-2 词表"] --> E["阶梯掩码：同通道预测下一时刻"]
    end
    subgraph P3["阶段三：多任务指令微调"]
        F["EEG tokens + SEP + 文本指令"] --> G["仅对答案部分计算损失"]
    end
    P1 --> P2 --> P3
```""",
    "0918-braingpt.md": r"""```mermaid
flowchart LR
    subgraph Pre["Stage I · 单电极自回归预训练"]
        A["多电极 EEG 拆成单电极序列"] --> B["拼接电极条件 token"]
        B --> C["共享 ETE 因果 Transformer"]
        C --> D["预测下一 token（MSE）"]
    end
    subgraph Down["Stage II · 多任务微调"]
        E["每电极序列末接可学习 token"] --> F["冻结 ETE 提取电极表示"]
        F --> G["注入全局电极图（子图激活）"]
        G --> H["GAT 图注意力 ×K 层"]
        H --> I["池化 → 任务头"]
    end
    Pre ==> Down
```""",
    "0918-eegpt.md": r"""```mermaid
flowchart TD
    A["EEG 58ch × 4s → 250ms patch"] --> B["掩码 50% 时间 × 80% 通道"]
    B --> C["Encoder 处理 masked 部分 + Summary Tokens"]
    B --> D["Momentum Encoder 处理全量（EMA 0.01）"]
    C --> E["Predictor（RoPE + query）预测全部时段特征"]
    E --> F["对齐损失 L_A（与 Momentum 输出）"]
    C --> G["Reconstructor（含 skip）重构 masked 原始 patch"]
    G --> H["重构损失 L_R"]
    F --> I["总损失 L = L_A + L_R"]
    D --> F
```""",
    "0918-tfm-tokenizer.md": r"""```mermaid
flowchart LR
    subgraph T1["阶段一：Tokenizer 训练（单通道）"]
        A["原始 patch → Temporal Encoder"] --> F["拼接 → Temporal Transformer → VQ 8192"]
        B["STFT 频谱窗 → 频率 patch 切分"] --> C["Frequency Transformer"]
        C --> D["门控聚合"] --> F
    end
    F --> G["冻结 tokenizer → token 查表（码字初始化）"]
    G --> H["下游线性注意力 Transformer"]
    H --> I["掩码 token 预测（交叉熵）"]
    I --> J["下游任务微调"]
```""",
}


def main() -> None:
    for fname, mermaid in MERMAID.items():
        path = PAPERS / fname
        text = path.read_text(encoding="utf-8")
        # 匹配「#### x.x 流程」到下一个四级标题之间的内容
        pat = re.compile(r"(#### [\d.]+ 流程\n).*?(\n#### [\d.]+ )", re.S)
        if "```mermaid" in text:
            print("skip (already mermaid):", fname)
            continue
        new_text, n = pat.subn(lambda m: m.group(1) + "\n" + mermaid + "\n" + m.group(2), text, count=1)
        if n == 0:
            print("[!] 未匹配到流程板块:", fname)
            continue
        path.write_text(new_text, encoding="utf-8")
        print("[+] 流程图已替换:", fname)


if __name__ == "__main__":
    main()
