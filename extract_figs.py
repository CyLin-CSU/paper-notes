# -*- coding: utf-8 -*-
"""从六篇论文 PDF 中裁剪出架构图（定位图注文字，裁剪页面顶部区域）。"""
import pathlib

import pymupdf

ZOTERO = pathlib.Path(r"C:\Users\ChengyeLin.LINOUP-XIAOXIN1\Zotero\storage")
OUT = pathlib.Path(r"C:\Users\ChengyeLin.LINOUP-XIAOXIN1\Desktop\work\paper-notes\docs\assets")
OUT.mkdir(parents=True, exist_ok=True)

# (pdf 相对路径, 页码从1计, 图注前缀, 输出名, 说明)
JOBS = [
    ("B8AZV4IZ", 3, "Figure 1:", "biot-arch.png", "BIOT 整体架构"),
    ("B8AZV4IZ", 4, "Figure 2:", "biot-token.png", "BIOT tokenization 细节"),
    ("3T34ZDD6", 3, "Figure 1:", "labram-arch.png", "LaBraM Neural Transformer 架构"),
    ("3T34ZDD6", 4, "Figure 2:", "labram-tokenizer.png", "LaBraM tokenizer 训练与掩码预训练"),
    ("ZHQWD63Z", 3, "Figure 2:", "neurolm-tokenizer.png", "NeuroLM 文本对齐 tokenizer 训练"),
    ("ZHQWD63Z", 5, "Figure 3:", "neurolm-training.png", "NeuroLM 两阶段训练流程"),
    ("RYP9WJ7B", 4, "Fig. 3:", "braingpt-overview.png", "BrainGPT 总体架构（ETE + TEG）"),
    ("SY2DLABR", 4, "Figure 1:", "eegpt-arch.png", "EEGPT 双自监督结构"),
    ("ZZGDIF42", 4, "Figure 2:", "tfm-framework.png", "TFM-Tokenizer 框架总览"),
]

SCALE = 2.2  # 渲染倍率，约 158 DPI


def main() -> None:
    for folder, page_no, caption, out_name, desc in JOBS:
        pdfs = list((ZOTERO / folder).glob("*.pdf"))
        if not pdfs:
            print("[!] 未找到 PDF:", folder)
            continue
        doc = pymupdf.open(pdfs[0])
        page = doc[page_no - 1]
        hits = page.search_for(caption)
        if hits:
            # 裁剪范围：跳过页眉，到图注底部
            clip = pymupdf.Rect(0, 25, page.rect.width, hits[0].y1 + 8)
        else:  # 兜底：整页
            print(f"[!] {out_name}: 未找到图注 '{caption}'，使用整页")
            clip = page.rect
        pix = page.get_pixmap(matrix=pymupdf.Matrix(SCALE, SCALE), clip=clip)
        out = OUT / out_name
        pix.save(out)
        print(f"[+] {out_name}  {pix.width}x{pix.height}px  {desc}")
        doc.close()


if __name__ == "__main__":
    main()
