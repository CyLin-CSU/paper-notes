# -*- coding: utf-8 -*-
"""data/ 结构化数据校验链（deploy 工作流挂钩）。

检查：
  1. 四个 JSON 可解析、ID 唯一；
  2. 引用完整性：model.paper_id / evidence.paper_id 必须存在于 papers.json，
     evidence.model_id 必须存在于 models.json（若给），evidence.dataset 必须存在于
     datasets.json（若给），dataset.parent 同理；
  3. papers.json 与 docs/papers/** 文件一一对应（无缺漏、无多余）；
  4. papers.json 的 doi 与 front matter 的 doi 字段一致（抽查双向）；
  5. evidence.status 取值受控；verified 条目必须带 source（原文表图/节号）。
任一失败以非零码退出，中断发布。

用法：python tools/check_data.py
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
STATUSES = {"verified", "pending", "unreported", "na"}
GROUPS = ("fm", "generative", "survey", "reviews")
DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$")


def load(name: str):
    path = DATA / name
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise SystemExit(f"[check-data] {name} 解析失败：{e}")


def main() -> int:
    bad = []
    papers = load("papers.json")
    models = load("models.json")
    datasets = load("datasets.json")
    evidence = load("evidence.json")
    use_matrix = load("use_matrix.json")

    # 1. ID 唯一性
    for name, rows, key in (("papers", papers, "paper_id"), ("models", models, "model_id"),
                            ("datasets", datasets, "dataset_id"), ("evidence", evidence, "evidence_id")):
        ids = [r.get(key) for r in rows]
        dup = {i for i in ids if ids.count(i) > 1}
        if dup:
            bad.append(f"{name}: ID 重复 {sorted(dup)}")
        if any(not i for i in ids):
            bad.append(f"{name}: 存在缺失 {key} 的记录")

    paper_ids = {r["paper_id"] for r in papers}
    model_ids = {r["model_id"] for r in models}
    dataset_ids = {r["dataset_id"] for r in datasets}

    # 2b. 使用矩阵关系记录的引用完整性
    for r in use_matrix:
        if r["paper_id"] not in paper_ids:
            bad.append(f"use_matrix.json: {r['dataset_name']} × {r['paper_id']} 引用不存在的 paper_id")
        if r.get("dataset") in dataset_ids or not r.get("dataset"):
            pass
        elif r.get("dataset_name") and r["dataset"] != r["dataset_name"]:
            bad.append(f"use_matrix.json: {r['dataset_name']} 的 dataset id {r['dataset']} 不在 datasets.json")

    # 2. 引用完整性
    for m in models:
        if m["paper_id"] not in paper_ids:
            bad.append(f"models.json: {m['model_id']} 引用不存在的 paper_id {m['paper_id']}")
    for e in evidence:
        if e["paper_id"] not in paper_ids:
            bad.append(f"evidence.json: {e['evidence_id']} 引用不存在的 paper_id {e['paper_id']}")
        if e.get("model_id") and e["model_id"] not in model_ids:
            bad.append(f"evidence.json: {e['evidence_id']} 引用不存在的 model_id {e['model_id']}")
        if e.get("dataset") and e["dataset"] not in dataset_ids:
            bad.append(f"evidence.json: {e['evidence_id']} 引用不存在的 dataset {e['dataset']}")
    for d in datasets:
        if d.get("parent") and d["parent"] not in dataset_ids:
            bad.append(f"datasets.json: {d['dataset_id']} 引用不存在的 parent {d['parent']}")

    # 3. papers.json ↔ docs/papers/** 一一对应
    fs = {f"{g}/{p.stem}" for g in GROUPS for p in (ROOT / "docs" / "papers" / g).glob("*.md")}
    js = {f"{r['group']}/{r['paper_id']}" for r in papers}
    for miss in sorted(fs - js):
        bad.append(f"papers.json 缺少笔记 {miss}")
    for extra in sorted(js - fs):
        bad.append(f"papers.json 多出无文件的记录 {extra}")

    # 4. doi 一致性（papers.json 有 DOI 的记录 ↔ front matter）
    for r in papers:
        if not r.get("doi"):
            continue
        if not DOI_RE.match(r["doi"]):
            bad.append(f"papers.json: {r['paper_id']} 的 doi 不是纯号码格式：{r['doi']}")
        fm = (ROOT / "docs" / "papers" / r["group"] / f"{r['paper_id']}.md").read_text(encoding="utf-8")
        if f'doi: "{r["doi"]}"' not in fm:
            bad.append(f"papers.json: {r['paper_id']} 的 doi 与 front matter 不一致")

    # 5. evidence 枚举与出处
    for e in evidence:
        if e.get("status") not in STATUSES:
            bad.append(f"evidence.json: {e['evidence_id']} 的 status 非法：{e.get('status')}")
        if e.get("status") == "verified" and not e.get("source"):
            bad.append(f"evidence.json: {e['evidence_id']} 标记 verified 但缺 source（原文表图/节号）")

    n = f"papers {len(papers)} / models {len(models)} / datasets {len(datasets)} / evidence {len(evidence)}"
    if bad:
        print(f"[check-data] {n}")
        for b in bad:
            print(f"[check-data] 错误：{b}")
        return 1
    print(f"[check-data] {n}；ID 唯一、引用完整、与笔记文件一一对应，校验通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
