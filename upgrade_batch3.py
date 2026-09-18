# -*- coding: utf-8 -*-
"""综述博客页（对外分享版）与 Zotero 同步指南的生成脚本。"""
import pathlib

DOCS = pathlib.Path(r"C:\Users\ChengyeLin.LINOUP-XIAOXIN1\Desktop\work\paper-notes\docs")

BLOG = '''---
title: 综述 · EEG 基础模型三年演进（2023–2026）
tags: [综述, EEG, 基础模型]
---

# 综述：EEG 基础模型三年演进（2023–2026）

> 基于 6 篇代表性论文（BIOT / LaBraM / EEGPT / BrainGPT / NeuroLM / TFM-Tokenizer）的精读综述。
> 完整方法拆解见站内[论文笔记](papers/2026-09/0918-biot.md)，本文是对外的观点性总结。

## TL;DR

三年间，EEG 基础模型在三个维度上完成了从 0 到 1：**输入表示**从规则切段进化到可学习的时频 motif 词表；**预训练目标**从对比学习/掩码建模扩展到自回归；**使用范式**从"一任务一模型"进化到接 LLM 的多任务指令推理。但所有模型的通用性仍被同一个东西卡住：**数据**——2.5 万小时已是极限规模，且被临床癫痫域重度偏斜。

## 一、输入表示：token 的三次升维

BIOT（NeurIPS'23）确立了"逐通道切段"的统一格式：通道可缺、长度可变、缺失即丢 token，配合线性注意力处理长句子。它的 token 是连续的、无词表的——"tokenize 了，但没有词汇表"。

LaBraM（ICLR'24）补上了词表：VQ-VAE 式码本（8192）+ 傅里叶频谱重构目标。关键实验发现是**重构域的选择**：EEG 低信噪比导致原始波形不可重构，频谱可以。但它的码字只当预训练的监督信号，推理时被丢弃。

NeuroLM（ICLR'25）让码字真正上岗：并入 GPT-2 词表，EEG 变成"外语句子"。TFM-Tokenizer（ICLR'26）则给出终审意见——LaBraM 的 token 化不彻底；它学的是**时频 motif** 词表（频域路径显式建模跨频段依赖），并把 token 作为下游模型的真正输入，以 1.9M 参数拿下多项 SOTA。

**演进的逻辑主线**：预处理产物 → 训练靶子 → 真实输入。

## 二、预训练目标：掩码建模的内部革命与自回归的挑战

掩码建模内部经历了三次目标更替：原始波形（不收敛，失败）→ 频谱（LaBraM）→ 表示（EEGPT 的 JEPA 式对齐 + MAE 式重构双自监督）。EEGPT 的贡献是指出"掩码后恢复什么"比"是否掩码"更重要——在表示空间对齐比在信号空间重构学到的东西更通用，这让它用 linear probing 就达到 SOTA。

BrainGPT（2024）则质疑范式本身：同架构同损失的消融显示，**自回归比掩码建模平均高 2%+**——EEG 是连续因果的信息流，双向补全破坏了它的自然结构。它把模型推到 1.09B 参数并验证了 scaling law，代价是需要下游图网络把单电极预训练丢掉的空间信息补回来。

## 三、使用范式：从 specialist 到 generalist 的两条路

BrainGPT 用**任务共享图网络**联合训练 12 个基准——多任务信息的载体不是图结构，而是"电极节点被多任务梯度共同更新"；小任务受益最大（+3.9%），本质是隐式数据增强。

NeuroLM 走了更激进的路：把 EEG 当外语接进 GPT-2，指令微调统一六种任务。它诚实报告了性能仍逊于单任务 SOTA，但零样板泛化到新 prompt 的能力是前两者没有的。**多任务的价值目前在范式与效率，不在数字**。

## 四、绕不开的天花板：数据

- LaBraM：Base 模型 500h ≈ 2500h 效果，Huge 在 2500h 仍未饱和；
- NeuroLM：L 与 XL 验证困惑度接近 → 25000h 喂不饱十亿参数；
- BrainGPT：数据 0→1B token 性能单调上升。

规模瓶颈之外是**域偏斜**：能拿到万小时级的只有临床 TUEG 体系，这解释了为什么 pretrain-then-finetune 在脑机接口类任务上的收益普遍不如临床任务——BrainGPT 甚至观察到预训练 specialist 弱于从头训练。

## 五、给研究者的三点启示

1. **做 tokenization 的人该看 TFM**：词表要学、位置编码要去、单通道要独立——三个反直觉设计都有消融支撑；
2. **做预训练的人该看 EEGPT 与 BrainGPT 的分歧**：掩码 vs 自回归之争目前 AR 略胜，但双向建模在"整段理解"任务上的潜力未被证伪；
3. **做应用的人该看 NeuroLM 的 limitation 章节**：多任务统一模型的现实成本（超参敏感、粗粒度对齐）写得非常坦诚。

## 延伸阅读

- 完整对比：[六篇方法对比](comparison.md)（13 维度表 + benchmark 战绩 + 论文互怼链）
- 主题深挖：[Tokenization 演进](topics/tokenization.md) · [预训练范式](topics/pretraining.md) · [通道异构](topics/spatial.md) · [数据全景](topics/data-landscape.md) · [多任务路线](topics/multi-task.md)
- 每篇精读：见左侧「论文笔记」
'''

ZOTERO = '''# Zotero → 论文笔记 同步指南

目标：Zotero 里新增一篇文献后，自动在站点生成笔记骨架（含元数据），减少手工输入。

## 方案 A：半自动（推荐，零代码维护）

1. Zotero 安装插件 **Better BibTeX**（导出 citekey 与元数据）与 **Zotero Integration**（Obsidian 用，若用 Obsidian 管理笔记）；
2. 在 Zotero 中选中论文 → 右键 **Export Entry** → 格式选 `CSL JSON` 或 `BibTeX`，存到 `paper-notes/imports/`；
3. 运行下面的辅助脚本把 JSON 转成笔记骨架：

```bash
python zotero_import.py imports/xxx.json
```

4. 补全正文（问题定位/方法/自问自答），按 README 第四节走完发布流程。

## 方案 B：zotero_import.py 的工作方式

脚本读取 CSL JSON，自动填充 frontmatter 的 title/authors/year/venue/arxiv，
生成 `docs/papers/当月/当日-slug.md` 骨架，并打印需要在 mkdocs.yml nav 里登记的行。
slug 默认取第一作者姓 + 年份（如 `yang2023`），可在命令行覆盖。

## 手动维护清单（每次新增文献）

- [ ] frontmatter 元数据齐全（venue/tags/rating）
- [ ] mkdocs.yml nav 登记一行
- [ ] 首页卡片墙加一张卡
- [ ] datasets.md / references.md 视情况补充
- [ ] new_note.py log 写一条时间线
'''

GEN = '''# -*- coding: utf-8 -*-
"""把 Zotero 导出的 CSL JSON 转成笔记骨架。

用法：python zotero_import.py imports/xxx.json [slug]
"""
import datetime
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DOCS = ROOT / "docs"


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    data = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    item = data[0] if isinstance(data, list) else data
    title = item.get("title", "Untitled")
    authors = [a.get("family", a.get("literal", "?")) for a in item.get("author", [])]
    year = (item.get("issued", {}).get("date-parts") or [[""]])[0][0] or ""
    venue = item.get("container-title", "") or item.get("publisher", "")
    arxiv = ""
    for u in item.get("URL", ""), :
        if "arxiv" in str(u):
            arxiv = u
    d = datetime.date.today()
    slug = sys.argv[2] if len(sys.argv) > 2 else f"{authors[0].lower() if authors else 'anon'}{d.year}"
    month_dir = DOCS / "papers" / d.strftime("%Y-%m")
    month_dir.mkdir(parents=True, exist_ok=True)
    out = month_dir / f"{d.strftime('%m%d')}-{slug}.md"
    fm = (
        "---\\n"
        f'title: "{title}"\\n'
        f"date: {d.isoformat()}\\n"
        f"authors: [{', '.join(authors)}]\\n"
        f'venue: "{venue}"\\n'
        f"year: {year}\\n"
        "tags: []\\n"
        'status: "粗读"\\n'
        "rating:\\n"
        f'arxiv: "{arxiv}"\\n'
        'code: ""\\n'
        'one-liner: ""\\n'
        "---\\n\\n"
        f"# {title}\\n\\n> **{venue} {year}**\\n\\n## 问题定位\\n\\n## 方法\\n\\n## 架构图\\n\\n"
        "![架构图](../../assets/待补充.png)\\n\\n## 创新点\\n\\n## 流程\\n\\n"
        "## 实验与结果\\n\\n## 与其他论文的关系\\n\\n## 个人思考\\n\\n## 自问自答\\n"
    )
    out.write_text(fm.encode().decode("unicode_escape"), encoding="utf-8")
    print(f"[+] {out}")
    print(f"[i] nav 登记：      - {d.strftime('%m%d')} · {title}: papers/{d.strftime('%Y-%m')}/{out.name}")


if __name__ == "__main__":
    main()
'''

(DOCS / "blog-2023-2026.md").write_text(BLOG, encoding="utf-8")
(ROOT := pathlib.Path(r"C:\Users\ChengyeLin.LINOUP-XIAOXIN1\Desktop\work")).joinpath("ZOTERO同步指南.md").write_text(ZOTERO, encoding="utf-8")
(ROOT / "paper-notes" / "zotero_import.py").write_text(GEN, encoding="utf-8")
print("[+] blog-2023-2026.md / ZOTERO同步指南.md / zotero_import.py")
