# -*- coding: utf-8 -*-
"""笔记重组：按月份日期归档 + 插入架构图 + 修正链接。"""
import pathlib

DOCS = pathlib.Path(r"C:\Users\ChengyeLin.LINOUP-XIAOXIN1\Desktop\work\paper-notes\docs")
PAPERS = DOCS / "papers"
MONTH = "2026-09"
DAY = "18"
DATE = f"{MONTH}-{DAY}"

# 旧文件名 -> (新文件名, [(图片, 说明), ...])
MAP = {
    "biot.md": ("0918-biot.md", [
        ("biot-arch.png", "Figure 1 · BIOT 整体架构：Module 1 生物信号 tokenization + Module 2 线性 Transformer 编码"),
        ("biot-token.png", "Figure 2 · Tokenization 细节：逐通道切段后用 segment/channel/position 三类 embedding 参数化"),
    ]),
    "labram.md": ("0918-labram.md", [
        ("labram-arch.png", "Figure 1 · Neural Transformer 整体架构：patch → temporal encoder → 时空 embedding → Transformer"),
        ("labram-tokenizer.png", "Figure 2 · 上：神经 tokenizer 训练（VQ + 频谱重构）；下：掩码 EEG 建模预训练"),
    ]),
    "neurolm.md": ("0918-neurolm.md", [
        ("neurolm-tokenizer.png", "Figure 2 · 文本对齐 tokenizer 训练：时频重构 + 域分类器（GRL 梯度反转）"),
        ("neurolm-training.png", "Figure 3 · 两阶段：多通道自回归预训练（左）→ 多任务指令微调（右）"),
    ]),
    "braingpt.md": ("0918-braingpt.md", [
        ("braingpt-overview.png", "Fig. 3 · 总体架构：左=单电极自回归预训练（ETE），右=多电极多任务微调（TEG 图网络）"),
    ]),
    "eegpt.md": ("0918-eegpt.md", [
        ("eegpt-arch.png", "Figure 1 · 双自监督结构：encoder 看 masked 部分 + predictor 对齐 momentum 输出 + reconstructor 重构"),
    ]),
    "tfm-tokenizer.md": ("0918-tfm-tokenizer.md", [
        ("tfm-framework.png", "Figure 2 · 框架总览：(a) 双路径 tokenizer 预训练 (b) 掩码策略 (c) 频谱窗口编码器 (d) 下游掩码 token 预测"),
    ]),
}


def main() -> None:
    month_dir = PAPERS / MONTH
    month_dir.mkdir(parents=True, exist_ok=True)
    for old, (new, figs) in MAP.items():
        src = PAPERS / old
        text = src.read_text(encoding="utf-8")
        # 1) frontmatter 加阅读日期
        text = text.replace("---\n", f"---\ndate: {DATE}\n", 1)
        # 2) 插入架构图板块（放在要点速览之前）
        fig_lines = ["## 架构图\n"]
        for img, desc in figs:
            fig_lines.append(f"![{desc}](../../assets/{img})\n")
            fig_lines.append(f"*{desc}*\n")
        fig_md = "\n".join(fig_lines) + "\n"
        if "## 要点速览" in text:
            text = text.replace("## 要点速览", fig_md + "\n## 要点速览", 1)
        else:
            text = text.rstrip() + "\n\n" + fig_md
        (month_dir / new).write_text(text, encoding="utf-8")
        src.unlink()
        print(f"[+] {old} -> papers/{MONTH}/{new}（含 {len(figs)} 张架构图）")

    # 3) 修正 index.md 与 topics/ 中的链接
    for page in [DOCS / "index.md", *DOCS.glob("topics/*.md")]:
        t = page.read_text(encoding="utf-8")
        orig = t
        for old, (new, _) in MAP.items():
            t = t.replace(f"papers/{old}", f"papers/{MONTH}/{new}")
            t = t.replace(f"../papers/{old}", f"../papers/{MONTH}/{new}")
        if t != orig:
            page.write_text(t, encoding="utf-8")
            print(f"[+] 链接已更新: {page.name}")


if __name__ == "__main__":
    main()
