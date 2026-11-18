# data/ · 站点结构化数据

本目录是站点结构化数据的单一事实源（M1 基线，对应《全面改版方案》§3）。构建与校验：

- `tools/build_data.py`：从 `docs/papers/**` front matter 生成 `papers.json`（全量迁移首版）；
- `tools/check_data.py`：校验 ID 唯一性、引用完整性与 front matter 一致性，失败非零退出（deploy 工作流已挂钩）；
- 页面消费（/library/、/models/、/evidence/）为 M2 范围，本阶段先保证数据就绪。

## 文件与字段约定

### papers.json（由 build_data.py 生成，手工不直接改）

| 字段 | 约定 |
|---|---|
| `paper_id` | 与笔记 slug 一致（URL 绑定，勿改） |
| `group` | fm / generative / survey / reviews |
| `type` | research（fm·generative·survey 组）或 review（reviews 组） |
| `doi` | 纯号码（如 `10.1088/1741-2552/ae17e9`）；旧笔记存于 `arxiv` 字段的 DOI 由导入脚本兼容读取 |
| `arxiv` | arXiv 链接；非 URL 的遗留说明文本原样保留 |
| `verified_date` | front matter `date`（阅读即核验的日期） |

### models.json（手工维护）

| 字段 | 约定 |
|---|---|
| `model_id` | `<paper_id>-<变体小写>`（如 `reve-base`） |
| `paper_id` | 必须存在于 papers.json |
| `params` | 数值单位 M；区间用 `min_max` 两字段 |
| `weights` | open / partial / none；说明放 `weights_note` |
| `input` | 连续 patch / 离散 token / 时频图 / 谱图 等受控词 |

### datasets.json（手工维护）

`dataset_id` 用数据集标准名小写连字符（`tuab`、`bcic-iv-2a`）。`aliases` 收录各论文的叫法（对照 [数据集索引别名表](../docs/datasets.md#dataset-alias)）。`access` 取 open / registration / request。

### evidence.json（手工维护）

一条记录 = 一个设置下的一个量。字段：`evidence_id`（`<paper_id>-<短语义>`）、`paper_id`、`source`（原文表号/节号，如 `Table 3` / `§5.2`）、`model_id`（可空）、`dataset`（dataset_id，可空）、`metric`、`value`（对象或数值）、`unit`、`split`（被试内/跨被试/LOSO 等，可空）、`protocol`（微调/线性探针/生成评估等）、`status`（`verified` 站内已核原文 / `pending` 待核对 / `unreported` 论文未报告 / `na` 不适用）、`note`。

## 维护流程

导入 CSL JSON → 匹配 paper_id → 补出处与适用范围 → 预览变更 → `mkdocs build --strict` + `check_data.py` → 发布。相同数值只在本目录维护一份；页面与笔记引用时链接到对应 evidence_id 或注明表号。
