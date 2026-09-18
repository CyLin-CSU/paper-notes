# -*- coding: utf-8 -*-
"""把《EEG基础模型六篇论文总结.md》拆分为 MkDocs 站点的独立页面。"""
import re
import pathlib

BASE = pathlib.Path(r"C:\Users\ChengyeLin.LINOUP-XIAOXIN1\Desktop\work")
SRC = BASE / "EEG基础模型六篇论文总结.md"
DOCS = BASE / "paper-notes" / "docs"

META = {
    1: dict(
        slug="biot", year="2023",
        title="BIOT: Cross-data Biosignal Learning in the Wild",
        venue="NeurIPS 2023",
        authors=["Chaoqi Yang", "M. Brandon Westover", "Jimeng Sun"],
        tags=["EEG", "tokenization", "线性注意力", "基础模型", "生物信号"],
        status="精读", rating="4.5",
        code="https://github.com/ycq091044/BIOT",
        arxiv="https://arxiv.org/abs/2305.10351",
        one_liner="逐通道切段 + 线性注意力的跨格式生物信号统一编码器",
    ),
    2: dict(
        slug="labram", year="2024",
        title="LaBraM: Large Brain Model for Learning Generic Representations with Tremendous EEG Data in BCI",
        venue="ICLR 2024",
        authors=["Wei-Bang Jiang", "Li-Ming Zhao", "Bao-Liang Lu"],
        tags=["EEG", "VQ-VAE", "掩码预训练", "基础模型", "神经codebook"],
        status="精读", rating="4.5",
        code="https://github.com/935963004/LaBraM",
        arxiv="https://arxiv.org/abs/2405.18765",
        one_liner="VQ 神经 tokenization + 频谱重构 + 掩码码字预测的 EEG 大模型",
    ),
    3: dict(
        slug="eegpt", year="2024",
        title="EEGPT: Pretrained Transformer for Universal and Reliable Representation of EEG Signals",
        venue="NeurIPS 2024",
        authors=["Guagnyu Wang", "Wenchao Liu", "Yuhong He", "Cong Xu", "Lin Ma", "Haifeng Li"],
        tags=["EEG", "双自监督", "表示对齐", "线性探针", "JEPA"],
        status="精读", rating="4",
        code="https://github.com/BINE022/EEGPT",
        arxiv="",
        one_liner="表示对齐 + 掩码重构双自监督的 10M 通用 EEG 特征提取器，linear probing 达 SOTA",
    ),
    4: dict(
        slug="braingpt", year="2024",
        title="BrainGPT: Unleashing the Potential of EEG Generalist Foundation Model by Autoregressive Pre-training",
        venue="arXiv 2024",
        authors=["Tongtian Yue", "Xuange Gao", "Shuning Xue", "Yepeng Tang", "Longteng Guo", "Jie Jiang", "Jing Liu"],
        tags=["EEG", "自回归", "多任务", "电极级建模", "scaling law"],
        status="精读", rating="4",
        code="", arxiv="https://arxiv.org/abs/2410.19779",
        one_liner="电极级建模 + GPT 式自回归 + 任务共享电极图的首个 EEG generalist（至 1.09B）",
    ),
    5: dict(
        slug="neurolm", year="2025",
        title="NeuroLM: A Universal Multi-task Foundation Model for Bridging the Gap between Language and EEG Signals",
        venue="ICLR 2025",
        authors=["Wei-Bang Jiang", "Yansen Wang", "Bao-Liang Lu", "Dongsheng Li"],
        tags=["EEG", "LLM", "指令微调", "多任务", "VQ-VAE"],
        status="精读", rating="4",
        code="https://github.com/935963004/NeuroLM",
        arxiv="https://arxiv.org/abs/2409.00101",
        one_liner="把 EEG 当外语接进 GPT-2：文本对齐 tokenizer + 多通道自回归 + 指令微调",
    ),
    6: dict(
        slug="tfm-tokenizer", year="2026",
        title="TFM-Tokenizer: Tokenizing Single-Channel EEG with Time-Frequency Motif Learning",
        venue="ICLR 2026",
        authors=["Jathurshan Pradeepkumar", "Xihao Piao", "Zheng Chen", "Jimeng Sun"],
        tags=["EEG", "tokenization", "时频motif", "VQ-VAE", "单通道"],
        status="精读", rating="4.5",
        code="https://github.com/Jathurshan0330/TFM-Tokenizer",
        arxiv="https://arxiv.org/abs/2502.16060",
        one_liner="单通道时频 motif 词表，离散 token 真正作为基础模型的输入",
    ),
}


def demote(text: str) -> str:
    """所有标题降一级（### x -> ## x），避免和页内 H1 冲突。"""
    return re.sub(r"^(#{2,5}) ", r"#\1 ", text, flags=re.M)


def frontmatter(m: dict) -> str:
    authors = ", ".join(m["authors"])
    tags = ", ".join(m["tags"])
    lines = [
        "---",
        f'title: "{m["title"]}"',
        f"authors: [{authors}]",
        f'venue: "{m["venue"]}"',
        f"year: {m['year']}",
        f"tags: [{tags}]",
        f'status: "{m["status"]}"',
        f"rating: {m['rating']}",
    ]
    if m["arxiv"]:
        lines.append(f'arxiv: "{m["arxiv"]}"')
    if m["code"]:
        lines.append(f'code: "{m["code"]}"')
    lines += [f'one-liner: "{m["one_liner"]}"', "---", ""]
    return "\n".join(lines)


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    # 按 "## N. " 顶层标题切块
    parts = re.split(r"^## ", text, flags=re.M)
    sections = {}
    for part in parts[1:]:
        m = re.match(r"(\d)\.", part)
        if m:
            sections[int(m.group(1))] = part

    papers_dir = DOCS / "papers"
    papers_dir.mkdir(parents=True, exist_ok=True)

    for i in range(1, 7):
        body = sections[i]
        # 去掉首行的 "N. " 编号，作为 H1
        body = re.sub(r"^\d+\.\s*", "", body, count=1)
        body = demote(body)
        meta = META[i]
        page = frontmatter(meta) + f"# {meta['title']}\n\n> **{meta['venue']}**\n\n" + body
        out = papers_dir / f"{meta['slug']}.md"
        out.write_text(page, encoding="utf-8")
        print("written:", out.name)

    # 六篇对比 -> comparison.md
    comp = "# 六篇方法对比\n\n" + demote(sections[7])
    (DOCS / "comparison.md").write_text(comp, encoding="utf-8")
    print("written: comparison.md")

    # 标签索引占位（tags 插件自动填充）
    (DOCS / "tags.md").write_text("# 标签索引\n\n点击下方标签查看对应论文。\n", encoding="utf-8")
    print("written: tags.md")


if __name__ == "__main__":
    main()
