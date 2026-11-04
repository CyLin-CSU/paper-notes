# 论文笔记站点 · 说明与操作文档

更新日期：2026-11-04

[在线站点](https://cylin-csu.github.io/paper-notes/) · [GitHub 仓库](https://github.com/CyLin-CSU/paper-notes)

## 一、项目位置与内容

| 位置 | 用途 |
|---|---|
| 工作区 `C:\Users\ChengyeLin.LINOUP-XIAOXIN1\Desktop\paper-notes` | 说明文档、BrainLLM 资料与站点工程 |
| 工作区下的 `paper-notes/` | **Git 仓库与 MkDocs 工程，构建和发布都在这里执行** |
| `docs/papers/` | 单篇论文笔记，直接放在此目录，文件名不带阅读日期，目前 25 篇 |
| `docs/topics/` | 五个主题专题，跨论文做宏观对照 |
| `docs/assets/` | 论文图与站点图片 |
| `docs/comparison.md` | 综合比较入口，覆盖范围以页面说明为准 |
| `mkdocs.yml` | 导航、主题、插件与数学渲染配置 |

技术栈：MkDocs Material、MathJax、giscus、jieba 中文搜索、GitHub Actions。

本说明在工作区与站点工程中各保留一份；修改时同步两份，工程内的 `README.md` 随 Git 提交。

## 二、主题专题怎么组织

| 专题 | 文件 | 主要回答什么 |
|---|---|---|
| Tokenization | `docs/topics/tokenization.md` | 信号怎么切分、token 是什么、词表用在哪里 |
| 预训练 | `docs/topics/pretraining.md` | tokenizer 怎么训练；主模型掩码什么、预测什么 |
| 通道与多任务 | `docs/topics/multi-task.md` | 不同通道怎么适配；不同任务怎么共享参数 |
| 数据 | `docs/topics/data-landscape.md` | 数据来源、规模与任务构成 |
| 基座与参数量 | `docs/topics/base-model.md` | 从零训练还是复用权重；主模型与 tokenizer 各有多大 |

原 `spatial.md` 已并入 `multi-task.md`，通道适配与多任务不再拆成两页。

新增论文可以**先加入主题专题，暂不创建单篇页面**。尚无单篇页面时直接链接原文，创建笔记后改为站内链接。生成式模型与跨领域论文是否纳入，按当前任务明确范围，不自动扩展。

## 三、写作约定

这些约定适用于站内论文页、架构基础页、工作区中的单篇笔记与论文汇总。

### 1. 先给宏观对照，再讲特色

- **表格只放同一层级的信息**。例如掩码建模用“论文 / 掩码部分 / 重建或预测部分”，不塞网络层数、掩码比例等实现细节。
- **同义术语统一**。同类目标统一写“原始信号 patch”“信号 embedding”“离散 token”“时频图”；不因为细节不同就换一个名字。
- **实质区别保留**。输入连续表示与输入离散 token 不混写；下一时间步预测与 RVQ 层级预测不混写；监督事件检测不当成掩码预训练。
- **首页卡片保持简洁**。发表信息、一句核心方法、两个标签；不列实验数字，不堆机构、模块缩写和强弱评价。
- **特色设计放表外**。每篇 1–2 点，写清组件做什么，不重复整张表。
- **论文页直接进入正文**。开头只保留简短发表信息和作者；不写站内轴线、源头地位等长介绍，不设置 TL;DR 卡片、自问自答、实验结果、个人思考和复现速查卡；不额外绘制流程图，保留论文原图。
- **句子短，直接说机制**。例如“可学习 query 汇聚通道”“冻结 encoder，只训练分类头”，少用口号、强弱排名和连续比喻。
- **细节按问题取舍**。损失对 tokenizer 训练有区分价值时保留；宏观掩码表可以不列损失。公式与必要训练细节放单篇笔记，重点解释方法机制。

### 2. 三个训练阶段分开写

| 阶段 | 记录内容 |
|---|---|
| Tokenizer 训练 | 是否有码表、掩码什么、重建什么、损失是什么 |
| 主模型预训练 | 输入什么、掩码什么、预测什么 |
| 下游适配 | 保留什么模块、训练什么模块、任务之间怎么共享 |

没有离散码表的，在 tokenizer 表中写“无码表”，相关训练栏填“—”。VQ 随检测模型联合训练的，要明确写“联合训练”，不虚构独立预训练阶段。

### 3. 数字与结论的口径

- **模型参数量**：优先报主模型；重要 tokenizer 单列，不把 encoder、预测头、重构头、动量副本全部相加后当成下游主模型。估算值注明依据，原文未单列就写“未单列”。
- **数据规模**：小时数、片段数、token 数、数据集数分开，说明单通道还是多通道片段，不直接比较不同口径。
- **引用实验结论时**：注明指标、数据集与训练设定；区分相对百分比和百分点，区分冻结 encoder 与全量微调。
- **证据边界**：优先核对本地 PDF、论文原文和官方实现。事实、作者解释、个人推断分开写；不把“某个实验有效”改写成普遍规律。
- **创新表述**：写具体改进，不自动加“首个”“唯一”“全面优于”等没有核对过的结论。

## 四、新增内容的两种流程

### 只更新主题专题

1. 在 Zotero 核对标题、作者、年份、DOI / arXiv 编号，先去重。
2. 查原文的方法、数据、下游协议与参数量，按专题表格补行。
3. 尚无单篇笔记时，直接链接 DOI、arXiv 或作者原文，不创建空白页面。
4. 必要时更新专题入口文字；不增加单篇精读数量，也不把旧比较页的范围直接改成新专题的论文总数。

### 创建单篇论文笔记

在站点工程中运行：

```powershell
conda activate pythonProject1
cd C:\Users\ChengyeLin.LINOUP-XIAOXIN1\Desktop\paper-notes\paper-notes
python new_note.py note <slug> "论文标题"
```

脚本生成 `docs/papers/<slug>.md`，例如 `labram.md`。阅读日期只记在元数据 `date` 中；导航和首页按发表年份排序，导航显示“论文名（会议/期刊 年份）”。`year`、`venue`、作者和链接需要人工核对。

正文按“问题定位 → 方法 → 关键设计 → 与其他论文的关系”组织。论文原图与公式按需要补充，不为了填模板凑内容。

- 图片保存到 `docs/assets/`，论文笔记用 `../assets/文件名.png` 引用。
- 使用 `extract_figs.py` 前，检查其 `ZOTERO` 与 `OUT` 路径，确保图片输出到当前工程的 `docs/assets/`。
- 新页面登记到 `mkdocs.yml`，再更新首页卡片与实际阅读统计。
- 需要时补充 `datasets.md`、`references.md`，并运行 `python new_note.py log "更新说明"` 记录首页时间线。

Zotero 导入脚本只接受 **CSL JSON**：

```powershell
python zotero_import.py imports/xxx.json <slug>
```

它生成元数据与笔记骨架，不等于完成论文阅读，也不自动登记导航。

## 五、检查与发布

激活 `pythonProject1` 后，在站点工程中运行：

```powershell
python -m mkdocs build
python -m mkdocs serve
```

`serve` 用于本地预览。发布前检查表格列数、链接、公式，以及新增内容是否出现在对应页面；不因文档修改运行训练实验。

确认当前改动后提交：

```powershell
git status --short
git diff --check
git add -A -- docs mkdocs.yml README.md .gitignore
git commit -m "更新主题专题与写作说明"
git push origin master
```

推送 `master` 会触发 `.github/workflows/deploy.yml`，构建后发布到 `gh-pages`。日常不需要再手动执行 `mkdocs gh-deploy`；发布完成以 Actions 成功及线上页面更新为准。

`site/`、`imports/`、`__pycache__/`、`.history/` 不提交。`.history/` 是编辑器备份，也不进入站点内容。

## 六、公式与常用组件

| 内容 | 写法 |
|---|---|
| 行内公式 | `\( x \in \mathbb{R}^{C \times T} \)` |
| 独立公式 | `\[ ... \]` |
| 提示框 | `!!! note "标题"`，正文缩进 4 个空格 |
| 图片 | `![图名](../assets/文件名.png)` |
| 术语提示 | 在 `docs/includes/abbreviations.md` 中维护 |

用 Python 写含 LaTeX 的 Markdown 时，使用原始字符串，避免 `\t`、`\n` 等转义破坏公式。表格单元格保持在同一行。

首页“最近更新”、活跃状态与日历由构建钩子生成；论文卡片、阅读统计与导航需要人工维护。线上内容未变化时，先检查 Actions 状态，再强制刷新浏览器。
