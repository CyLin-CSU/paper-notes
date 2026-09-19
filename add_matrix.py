# -*- coding: utf-8 -*-
"""datasets.md 顶部插入「数据集 × 论文使用矩阵」热力图。"""
import pathlib

P = pathlib.Path(r"C:\Users\ChengyeLin.LINOUP-XIAOXIN1\Desktop\work\paper-notes\docs\datasets.md")

# 列顺序按发表时间；取值：P=预训练语料  D=下游评估  B=两者都用  ·=未使用
# 依据：各论文 Appendix（预训练集列表）与下游评测章节
ROWS = [
    # (数据集, BIOT, LaBraM, EEGPT, BrainGPT, NeuroLM, TFM)
    ("TUAB",            "·", "D", "D", "·", "D", "D"),
    ("TUEV",            "D", "D", "D", "·", "D", "D"),
    ("TUEG（总体）",     "·", "P", "·", "·", "P", "·"),
    ("TUSZ",            "·", "P", "·", "·", "P", "·"),
    ("TUEP / TUAR / TUSL", "·", "P", "·", "·", "P", "·"),
    ("SEED 系列",       "·", "P", "P", "D", "P", "·"),
    ("SEED-IV / SEED-V", "·", "·", "·", "D", "P", "·"),
    ("DEAP / FACED",    "·", "·", "·", "D", "·", "·"),
    ("PhysioMI",        "·", "P", "P", "·", "P", "·"),
    ("HGD",             "·", "·", "P", "·", "·", "·"),
    ("BCIC4-1 / MIBCI", "·", "P", "·", "D", "·", "·"),
    ("Grasp and Lift",  "·", "P", "·", "·", "P", "·"),
    ("SHHS",            "P", "·", "·", "·", "·", "·"),
    ("EDF / HMC（睡眠）", "·", "·", "·", "D", "D", "·"),
    ("EESM23（ear-EEG）", "·", "·", "·", "·", "·", "D"),
    ("EEGMat / STEW（负荷）", "·", "·", "·", "D", "D", "·"),
    ("Inria BCI / TVNT（P300）", "·", "P", "·", "·", "P", "·"),
    ("TSU（SSVEP）",    "·", "·", "P", "·", "·", "·"),
    ("M3CV",            "·", "·", "P", "·", "·", "·"),
    ("KaggleERN / PhysioP300", "·", "·", "D", "·", "·", "·"),
    ("PTB-XL / Cardiology（ECG）", "PB", "·", "·", "·", "·", "·"),
    ("HAR（可穿戴）",    "D", "·", "·", "·", "·", "·"),
    ("MoBI（步态）",     "·", "D", "·", "·", "·", "·"),
    ("Raw EEG / Resting / Siena / SPIS / 自采集", "·", "P", "·", "·", "P", "·"),
    ("DREAMER（未见验证）", "·", "·", "·", "D", "·", "·"),
]
COLS = ["BIOT", "LaBraM", "EEGPT", "BrainGPT", "NeuroLM", "TFM"]

CELL = {
    "P": ('<td class="mx-cell mx-p" title="预训练语料">P</td>'),
    "D": ('<td class="mx-cell mx-d" title="下游评估">D</td>'),
    "B": ('<td class="mx-cell mx-b" title="预训练 + 下游">P+D</td>'),
    "PB": ('<td class="mx-cell mx-p" title="预训练语料（ECG）">P</td>'),
    "·": ('<td class="mx-cell mx-n" title="未使用">·</td>'),
}

head = "".join(f"<th>{c}</th>" for c in COLS)
rows = []
for name, *vals in ROWS:
    cells = "".join(CELL[v] for v in vals)
    rows.append(f"<tr><th>{name}</th>{cells}</tr>")
matrix = (
    '<div class="mx-wrap">\n<table class="mx-matrix">\n'
    f"<thead><tr><th>数据集 \\ 论文</th>{head}</tr></thead>\n"
    f"<tbody>{''.join(rows)}</tbody>\n</table>\n</div>\n\n"
    '<p class="mx-legend">图例：<span class="mx-cell mx-p">P</span> 预训练语料　'
    '<span class="mx-cell mx-d">D</span> 下游评估　'
    '<span class="mx-cell mx-n">·</span> 未使用　'
    "（悬停单元格查看说明；ECG 与 IMU 数据仅 BIOT 跨模态使用）</p>"
)

t = P.read_text(encoding="utf-8")
if "mx-matrix" not in t:
    anchor = "## 临床 EEG（Temple 大学 TUEG 体系）"
    section = f"## 📊 数据集 × 论文使用矩阵\n\n{matrix}\n\n---\n\n"
    t = t.replace(anchor, section + anchor, 1)
    P.write_text(t, encoding="utf-8")
    print("[+] 矩阵已插入 datasets.md")

# CSS
css = pathlib.Path(r"C:\Users\ChengyeLin.LINOUP-XIAOXIN1\Desktop\work\paper-notes\docs\stylesheets\extra.css")
c = css.read_text(encoding="utf-8")
if "mx-matrix" not in c:
    c += """
/* 数据集×论文使用矩阵 */
.mx-wrap { overflow-x: auto; }
.mx-matrix { border-collapse: separate; border-spacing: 3px; width: auto; }
.mx-matrix th {
  font-size: 0.7rem;
  text-align: center;
  white-space: nowrap;
  background: transparent;
}
.mx-matrix tbody th {
  text-align: left;
  padding-right: 0.6rem;
  font-weight: 500;
}
.mx-cell {
  display: inline-block;
  min-width: 2.1rem;
  text-align: center;
  padding: 0.25rem 0.3rem;
  border-radius: 4px;
  font-size: 0.68rem;
  font-weight: 700;
  cursor: default;
}
.mx-p { background: #40c46333; color: #1a7f37; }
.mx-d { background: #4083ec33; color: #1f5fbf; }
.mx-b { background: #8250df33; color: #6639ba; }
.mx-n { color: var(--md-default-fg-color--lighter); }
[data-md-color-scheme="slate"] .mx-p { color: #7ee787; }
[data-md-color-scheme="slate"] .mx-d { color: #79c0ff; }
[data-md-color-scheme="slate"] .mx-b { color: #d2a8ff; }
.mx-legend { font-size: 0.72rem; color: var(--md-default-fg-color--light); }
.mx-legend .mx-cell { margin: 0 0.15rem; }
"""
    css.write_text(c, encoding="utf-8")
    print("[+] 矩阵 CSS 已追加")
