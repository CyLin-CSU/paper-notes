# -*- coding: utf-8 -*-
"""36 × 14 数据集使用矩阵 → data/use_matrix.json 关系记录（E 包迁移基线）。

解析 docs/datasets.md 的 mx-matrix HTML 表，每个非「·」格生成一条
{dataset, dataset_name, paper_id, use, note} 记录；数据集名映射到
datasets.json 的 dataset_id（能映射的用 id，暂无 id 的用原名）。
"""
import json
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
md = (ROOT / "docs" / "datasets.md").read_text(encoding="utf-8")
m = re.search(r'<table class="mx-matrix">.*?</table>', md, re.S)
assert m, "未找到矩阵表"
table = m.group(0)

# 列名 → paper_id（矩阵列头是简称）
COL2PAPER = {
    "BIOT": "biot", "LaBraM": "labram", "EEGPT": "eegpt", "BrainGPT": "braingpt",
    "NeuroLM": "neurolm", "TFM": "tfm-tokenizer", "EEGMoE": "eegmoe", "LUNA": "luna",
    "JET": "jet", "RF-GPT": "rf-gpt", "CBraMod": "cbramod", "EEGDM": "eegdm",
    "Not-All-EEG": "not-all-eeg", "REVE": "reve",
}
# 数据集名 → dataset_id（datasets.json 已收录的）
DS2ID = {d["name"]: d["dataset_id"] for d in json.loads(
    (ROOT / "data" / "datasets.json").read_text(encoding="utf-8"))}
DS2ID.update({"TUEG（总体）": "tueg", "SEED-IV / SEED-V": "seed-v"})

head = re.search(r"<thead><tr>(.*?)</tr></thead>", table, re.S).group(1)
cols = re.findall(r'<th scope="col">([^<]+)</th>', head)[1:]  # 首列是「数据集 \ 论文」
assert len(cols) == 14, f"列数异常：{len(cols)}"

USE = {"mx-p": "P", "mx-d": "D", "mx-b": "P+D"}
records, skipped = [], []
for tr in re.finditer(r"<tr><th scope=\"row\">(.*?)</th>(.*?)</tr>", table, re.S):
    ds_name = tr.group(1)
    cells = re.findall(r'<td class="mx-cell (mx-[pdbn])" title="([^"]*)">([^<]*)</td>', tr.group(2))
    if len(cells) != len(cols):
        skipped.append(ds_name)
        continue
    for (cls, title, _), col in zip(cells, cols):
        if cls not in USE:
            continue  # mx-n 未使用
        pid = COL2PAPER.get(col)
        if not pid:
            skipped.append(f"{ds_name} × {col}")
            continue
        records.append({
            "dataset": DS2ID.get(ds_name) or ds_name,
            "dataset_name": ds_name,
            "paper_id": pid,
            "use": USE[cls],
            "note": title,
        })

out = ROOT / "data" / "use_matrix.json"
out.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"[use-matrix] 关系记录 {len(records)} 条 → data/use_matrix.json；未映射跳过 {len(skipped)}：{skipped[:6]}")
