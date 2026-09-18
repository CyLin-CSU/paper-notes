# -*- coding: utf-8 -*-
"""给六篇论文笔记追加「要点速览 / 相关论文 / 个人思考」板块。"""
import pathlib

DOCS = pathlib.Path(r"C:\Users\ChengyeLin.LINOUP-XIAOXIN1\Desktop\work\paper-notes\docs\papers")

ENRICH = {
    "biot.md": dict(
        tldr=[
            "3.2M 参数；四种学习场景（监督 / 带缺失监督 / 无监督预训练 / 跨任务预训练）",
            "9 个数据集（EEG/ECG/HAR）上超过全部基线；带缺失设定下性能衰减最小",
            "多数据集联合预训练进一步提升：CHB-MIT balanced acc 0.664 → 0.707",
        ],
        relations=[
            ("LaBraM / NeuroLM / EEGPT / BrainGPT / TFM-Tokenizer", "全部把 BIOT 作为公共对照组——事实上的 baseline 标尺"),
            ("TFM-Tokenizer", "BIOT-TFM：仅把 BIOT 的输入 patch 投影替换为 TFM token，93% 指标-设定组合有提升 → 骨干仍有价值，弱在输入表示"),
            ("EEGPT（附录 F）", "批评其 FFT 只保留频谱能量、丢失相位，且 1s patch 的 FFT 过粗 → ERP/P300 等时域任务表现差（PhysioP300 仅 0.5485）"),
        ],
        thoughts=[
            "逐通道独立切分（缺失段直接丢 token）是它通吃异构格式的根本设计，后续所有工作都继承了这一点。",
            "线性注意力的 E/F 投影把注意力图固定为 N×d，隐含假设'全局信息可压缩进 d 个摘要位'——分类任务够用，但牺牲了精细的 token 间路由能力。",
            "频域在这里只是特征工程（FFT 能量 → FCN），模型本体仍在连续域运行——这为后来 LaBraM/TFM 的显式时频建模埋下了演进伏笔。",
        ],
    ),
    "labram.md": dict(
        tldr=[
            "2500 小时 / 约 20 个数据集预训练；Base 5.8M / Large 46M / Huge 369M（当时 BCI 最大）",
            "TUEV：Kappa 0.6745（Huge）、balanced acc 0.6616，全面超过 BIOT 等基线",
            "8192 神经 codebook；重构目标 = DFT 幅值 + 相位（重构原始波形不收敛）",
        ],
        relations=[
            ("NeuroLM", "同团队续作：tokenizer 改为时频双域重构 + GRL 文本空间对齐，token 并入 GPT-2 词表"),
            ("TFM-Tokenizer", "批评其 token '只当训练目标、推理时被丢弃'；LaBraM-TFM 替换其 tokenizer 后 93% 指标提升"),
            ("EEGPT / BrainGPT", "作为预训练基线被比较；BrainGPT 猜测其预训练语料偏癫痫临床域，domain 差异拖累一般下游任务"),
        ],
        thoughts=[
            "最有价值的发现是'重构域'的选择：EEG 低信噪比导致重构原始波形不收敛 → 改为频谱目标。这一思路后来被 NeuroLM（去掉相位）和 TFM（掩码频谱图）继续演进。",
            "线性探针在 TUEV 崩到 0.346，说明其表示与全量微调强绑定——对比 EEGPT 把 linear probing 做成核心卖点。",
            "对称掩码让一个样本产生 mask/补集两个互补视角，既是效率技巧（省一次 tokenizer 前向）也是数据增强（大模型受益更明显）。",
        ],
    ),
    "eegpt.md": dict(
        tldr=[
            "~10M 参数（8 个变体 0.4M–101M）；下游只用 linear probing 即达 SOTA",
            "TUEV balanced acc 0.6232，比 BIOT（0.5281）高 9.5%",
            "双自监督：表示对齐（L_A，JEPA 式）+ 掩码重构（L_R，MAE 式）；掩码 50% 时间 × 80% 通道",
        ],
        relations=[
            ("思想上", "承接 BYOL（momentum encoder）+ MAE（重构）+ JEPA（在表示空间预测）三条线"),
            ("LaBraM", "互补路线：LaBraM 走离散语义码，EEGPT 坚持连续表示但把自监督目标做得更好"),
            ("TFM-Tokenizer", "对照实验：EEGPT 依赖固定 58 通道布局的 Codex book，ear-EEG 跨设备实验无法参与"),
        ],
        thoughts=[
            "把 linear probing 当评估协议本身就是贡献：冻结 encoder 后性能完全归因于表示质量，排除了微调技巧的干扰。",
            "'encoder 看被 mask 的稀疏部分、momentum encoder 看全量'的反直觉设计，本质是用对齐任务逼迫稀疏视图输出全局语义（式 1→2 的显式表示 z）。",
            "附录证明去掉 predictor 会表示坍塌（重构 loss 不再下降）——对齐分支必须保留 query/位置等余量，防止模型走捷径。",
        ],
    ),
    "braingpt.md": dict(
        tldr=[
            "最大 1.09B（EEG 领域当时最大）；3750 万单电极样本 / 约 1B token",
            "12 个基准 × 5 类任务，单一 generalist 全面超过 specialist：SS +11.2%、MW +8.5%",
            "AR 比 MAE 平均高 2%+（同架构同损失对比）；联合训练全面优于逐任务训练（MW +3.9%）",
        ],
        relations=[
            ("NeuroLM", "两种多任务方案的对照：BrainGPT 用 TEG 联合微调（保留任务头），NeuroLM 用指令微调（统一到文本生成）"),
            ("EEGPT", "互补验证了 EEG 预训练的 scaling law（模型/数据规模均正相关）"),
            ("LaBraM / BIOT", "范式之争的直接证据：同设定下自回归（AR）优于双向掩码（MAE）2%+"),
        ],
        thoughts=[
            "TEG 的多任务信息不在图结构里，而在'共享参数被多任务梯度共同更新'：电极节点 V_m 是跨任务的原型记忆，电极集重叠即共享交集——小任务 MW 的 +3.9% 正来源于此。",
            "自回归直接回归连续值（MSE），绕开了离散化难题——与 LaBraM/TFM 的'先离散再预测'形成两条并行路线。",
            "电极级拆样本让样本量 ×E 倍膨胀（3750 万），这个数字要打折看：单电极序列丢掉了跨电极同步信息，空间整合完全依赖下游 TEG 补回。",
        ],
    ),
    "neurolm.md": dict(
        tldr=[
            "约 25000 小时 EEG 预训练；GPT-2 基座，B/L/XL = 254M / 500M / 1696M",
            "首个单模型多任务 EEG 模型：指令微调统一 6 种 BCI 任务",
            "token 接入方式：8192 codebook 并入 LLM 词表 + GRL 对抗式文本空间对齐",
        ],
        relations=[
            ("LaBraM", "同团队续作：tokenizer 继承 VQ + 频谱思想，但改为时域+幅值双域重构（发现相位贡献小）"),
            ("BrainGPT", "多任务路线之争的另一方：指令微调 vs 图联合微调"),
            ("CLIP 类模型", "对齐思路的差异：因 EEG-text 无成对数据，选择 space-wise（域分类器+GRL）而非 embedding-wise 对齐"),
        ],
        thoughts=[
            "论文很诚实：单模型多任务的性能仍逊于单任务 SOTA 的 LaBraM——其价值在范式（prompt 泛化到新任务、免逐任务微调），不在当前数字。",
            "EEG-text 没有成对数据 → 只能做粗粒度的空间对齐，这是当前范式的天花板；附录展望了'用预定义句子描述 EEG + 对比损失'的细粒度对齐方向。",
            "阶梯掩码是'把语言的自回归搬到多通道信号'的干净答案：同通道 token 预测同通道下一时刻，每个 token 可见所有通道的当前与历史。",
        ],
    ),
    "tfm-tokenizer.md": dict(
        tldr=[
            "总参数仅 ~1.9M（tokenizer 1.2M + 下游 0.7M），最小的那个反而最强",
            "多数据集设定 TUEV Kappa 0.6189（次优 0.5588，+11%）；IIIC Kappa 0.4979（比 LaBraM +36%）",
            "跨设备 ear-EEG 睡眠分期超过 BIOT/LaBraM 14%；plug-and-play 提升 BIOT/LaBraM 93% 指标",
        ],
        relations=[
            ("LaBraM", "直接批评其 token '只当训练目标'；LaBraM-TFM 实验证明换用 TFM tokenizer 后性能普遍提升"),
            ("BIOT", "批评其 FFT 整窗线性投影过于粗糙；BIOT-TFM 用 token 替换其输入投影后同样提升"),
            ("EEGPT", "单通道设计 vs 固定 58 通道布局：ear-EEG 实验中 EEGPT 因空间 embedding 无法扩展而缺席"),
        ],
        thoughts=[
            "去掉位置编码的反直觉设计有消融支撑：PE 会让同一 motif 因出现位置不同学成不同 token → 词表冗余；motif 词表要的正是平移不变性。",
            "token 可解释性分析（如 PLED 类的 token 4035 稳定对应'棘波-慢波'周期模式）是把 NLP 的 token 分析方法迁移到 EEG 的漂亮示范。",
            "作者自认局限：固定窗长可能把大 pattern 切断到不同窗口，导致同一事件被分到不同 token——这是切分式 tokenization 的共同软肋。",
        ],
    ),
}


def build_section(key: str, items) -> str:
    if key == "tldr":
        lines = ["## 要点速览\n", '!!! abstract "TL;DR"\n']
        lines += [f"    - {it}\n" for it in items]
        return "\n" + "".join(lines) + "\n"
    if key == "relations":
        lines = ["## 与其他论文的关系\n", "| 论文 / 工作 | 关系说明 |", "|---|---|"]
        lines += [f"| {a} | {b} |" for a, b in items]
        return "\n" + "\n".join(lines) + "\n"
    if key == "thoughts":
        lines = ["## 个人思考\n"]
        lines += [f"- {it}\n" for it in items]
        return "\n" + "".join(lines) + "\n"


def main() -> None:
    for fname, content in ENRICH.items():
        path = DOCS / fname
        text = path.read_text(encoding="utf-8")
        if "## 要点速览" in text:
            print("skip (already enriched):", fname)
            continue
        text = text.rstrip() + "\n"
        text += build_section("tldr", content["tldr"])
        text += build_section("relations", content["relations"])
        text += build_section("thoughts", content["thoughts"])
        path.write_text(text, encoding="utf-8")
        print("enriched:", fname)


if __name__ == "__main__":
    main()
