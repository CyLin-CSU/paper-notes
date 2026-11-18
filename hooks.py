# -*- coding: utf-8 -*-
"""MkDocs 构建钩子：

1. 注入最近一次 git 提交时间（北京时间，精确到分钟）与活跃状态徽标（纯文本）。
2. 生成最近一周活跃热力图（按北京时间统计，标注明确日期范围）。
3. 为论文笔记的全部历史地址生成一步重定向页：
   - 日期前缀地址（目录拍平与分类迁移前）：papers/<MMDD-slug>/ → papers/<group>/<slug>/
   - 无前缀旧址（分类迁移前）：papers/<slug>/ → papers/<group>/<slug>/
   带锚点的访问由页面内脚本转发到新页对应锚点；无 JS 时回退链接可点击。
"""
import datetime
import html
import json
import pathlib
import posixpath
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent
TZ_BJ = datetime.timezone(datetime.timedelta(hours=8), name="UTC+8")

# 分类迁移前的日期前缀 slug → 无前缀 slug。
DATE_PREFIX_SLUGS = {
    '0918-biot': 'biot',
    '0918-braingpt': 'braingpt',
    '0918-eegpt': 'eegpt',
    '0918-labram': 'labram',
    '0918-neurolm': 'neurolm',
    '0918-tfm-tokenizer': 'tfm-tokenizer',
    '0921-rf-gpt': 'rf-gpt',
    '0923-jet': 'jet',
    '0924-eegmoe': 'eegmoe',
    '0924-luna': 'luna',
    '0928-cbramod': 'cbramod',
    '1017-eegdm': 'eegdm',
    '1028-not-all-eeg': 'not-all-eeg',
    '1102-defossez-speech': 'defossez-speech',
    '1102-learnable-tf': 'learnable-tf',
    '1102-ssm2mel': 'ssm2mel',
    '1102-surrogate-brain': 'surrogate-brain',
    '1104-brainrvq': 'brainrvq',
    '1104-codebrain': 'codebrain',
    '1104-crosspt-eeg': 'crosspt-eeg',
    '1104-delta': 'delta',
    '1104-eegarena': 'eegarena',
    '1104-guided': 'guided',
    '1104-neurodetr': 'neurodetr',
    '1104-neurorvq': 'neurorvq',
}

# 组间迁移旧地址 → 当前 slug。key 可含分组目录（如 'survey/<slug>'），
# 对应旧地址 papers/survey/<slug>/；'papers/<key>/' 整体作为重定向页写入。
GROUP_MOVE_SLUGS = {
    'survey/yao-eegfm-survey': 'yao-eegfm-survey',
    'survey/chen-representation-learning-review': 'chen-representation-learning-review',
    'survey/kuruppu-critical-review': 'kuruppu-critical-review',
    'survey/kwon-neural-fm-perspective': 'kwon-neural-fm-perspective',
}

REDIRECT_TEMPLATE = (
    '<!doctype html><html lang="zh"><meta charset="utf-8">'
    '<meta http-equiv="refresh" content="0; url={rel}">'
    '<meta name="robots" content="noindex"><title>页面已迁移</title>'
    '<script>if (location.hash) location.replace("{rel}" + location.hash);</script>'
    '<p>页面已迁移，<a href="{rel}">打开论文笔记</a>；未自动跳转请点击该链接。</p></html>'
)


def _git(args: list) -> str:
    return subprocess.run(["git"] + args, capture_output=True, check=True,
                          encoding="utf-8", errors="replace",
                          cwd=str(ROOT)).stdout


def _last_commit_time() -> datetime.datetime:
    """最近一次 git 提交时间，折算到北京时间；失败退回当前北京时间。"""
    try:
        out = _git(["log", "-1", "--format=%cI"]).strip()
        return datetime.datetime.fromisoformat(out).astimezone(TZ_BJ)
    except Exception:
        return datetime.datetime.now(TZ_BJ)


def _commit_counts(days: int = 7) -> dict:
    """按北京时间日期统计最近 days 天的 git 提交数。"""
    today = datetime.datetime.now(TZ_BJ).date()
    since = (today - datetime.timedelta(days=days - 1)).isoformat()
    try:
        out = _git(["log", f"--since={since} 00:00", "--format=%cI"])
    except Exception:
        return {}
    counts: dict = {}
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            d = datetime.datetime.fromisoformat(line).astimezone(TZ_BJ).date()
        except ValueError:
            continue
        counts[d.isoformat()] = counts.get(d.isoformat(), 0) + 1
    return counts


def _activity_calendar(days: int = 7) -> str:
    """最近 days 天的活跃热力图（GitHub 风格，注明日期范围，北京时间）。"""
    counts = _commit_counts(days)
    today = datetime.datetime.now(TZ_BJ).date()
    start = today - datetime.timedelta(days=days - 1)
    cells, total = [], 0
    for i in range(days - 1, -1, -1):
        d = today - datetime.timedelta(days=i)
        ds = d.isoformat()
        n = counts.get(ds, 0)
        total += n
        level = 0 if n == 0 else 1 if n == 1 else 2 if n == 2 else 3 if n <= 4 else 4
        wd = "一二三四五六日"[d.weekday()]
        label = d.strftime("%m-%d")  # 「今」也标成明确日期
        cells.append(
            f'<div class="ac-day"><div class="ac-cell" data-l="{level}" '
            f'title="{ds}（周{wd}，北京时间）· {n} 次提交"></div>'
            f'<span class="ac-wd">{label}</span></div>'
        )
    grid = "".join(cells)
    legend = "".join(f'<i data-l="{l}"></i>' for l in range(5))
    rng = f"{start.strftime('%m-%d')}–{today.strftime('%m-%d')}"
    return (
        f'<div class="activity-calendar">'
        f'<span class="ac-total">{rng}（北京时间）提交 <b>{total}</b> 次</span>'
        f'<div class="ac-grid">{grid}</div>'
        f'<span class="ac-legend">少{legend}多</span>'
        f"</div>"
    )


def on_page_content(html, page, **kwargs):
    if page.file.src_uri == "index.md":
        html = _render_home_extras(html)
    elif page.file.src_uri == "library.md":
        html = _render_library(html)
    elif page.file.src_uri == "evidence.md":
        html = _render_evidence(html)
    elif page.file.src_uri == "models.md":
        html = _render_models(html)
    elif page.file.src_uri.startswith("papers/"):
        html = _render_paper_toolbar(html, page)
    return html


def _bibtex(p: dict) -> str:
    fields = [f"title = {{{p['title']}}}",
              "author = {" + " and ".join(p.get("authors", [])) + "}",
              f"year = {{{p.get('year') or ''}}}"]
    if p.get("venue"):
        fields.append(f"journal = {{{p['venue']}}}")
    if p.get("doi"):
        fields.append(f"doi = {{{p['doi']}}}")
    if p.get("arxiv") and str(p["arxiv"]).startswith("http"):
        fields.append(f"url = {{{p['arxiv']}}}")
    return "@article{" + p["paper_id"] + ",\n  " + ",\n  ".join(fields) + ",\n}"


def _render_paper_toolbar(html, page):
    """单篇页标题区工具条（方案 G/B）：来源链接、复制引用、保存阅读、证据反查。"""
    m = re.match(r"papers/(fm|generative|survey|reviews)/([a-z0-9-]+)\.md", page.file.src_uri)
    if not m:
        return html
    paper_id = m.group(2)
    papers = {r["paper_id"]: r for r in _load_json("papers.json")}
    p = papers.get(paper_id)
    if not p:
        return html
    links = []
    if p.get("doi"):
        links.append(f'<a href="https://doi.org/{_esc(p["doi"])}">DOI</a>')
    if p.get("arxiv") and str(p["arxiv"]).startswith("http"):
        links.append(f'<a href="{_esc(p["arxiv"])}">arXiv</a>')
    if p.get("code"):
        links.append(f'<a href="{_esc(p["code"])}">代码/项目</a>')
    links.append(f'<a href="../evidence/?paper={_esc(paper_id)}">实验证据</a>')
    bibtex = json.dumps(_bibtex(p), ensure_ascii=False)
    title = json.dumps(p["title"], ensure_ascii=False)
    toolbar = (
        f'<div class="paper-toolbar" data-paper="{_esc(paper_id)}">'
        f'<span class="pt-links">{" · ".join(links)}</span>'
        f'<button type="button" class="pt-cite" data-cite={bibtex}>复制引用</button>'
        f'<button type="button" class="pt-save" data-title={title}>保存阅读</button>'
        f"</div>"
    )
    return re.sub(r"(</h1>)", r"\1" + toolbar, html, count=1)


def _build_atom(site, config):
    """site/atom.xml：从 git 提交历史生成已发布笔记的更新订阅（方案 G）。"""
    try:
        log = _git(["log", "--format=%cI\x1f%s\x1f%H", "--name-only", "-60"])
    except Exception:
        return
    entries, seen = [], set()
    for block in log.split("\n\n"):
        lines = [l for l in block.splitlines() if l.strip()]
        if len(lines) < 2:
            continue
        ts, subject, sha = (lines[0].split("\x1f") + ["", ""])[:3]
        for path in lines[2:]:
            mm = re.match(r"docs/papers/(fm|generative|survey|reviews)/([a-z0-9-]+)\.md$", path)
            if not mm or mm.group(2) in seen:
                continue
            seen.add(mm.group(2))
            slug = mm.group(2)
            entries.append((ts, slug, sha))
    if not entries:
        return
    base = (config.get("site_url") or "https://cylin-csu.github.io/paper-notes/").rstrip("/")
    items = []
    for ts, slug, sha in entries[:30]:
        items.append(
            f'<entry><id>urn:paper-notes:{sha}:{slug}</id>'
            f"<updated>{ts}</updated>"
            f"<link rel=\"alternate\" href=\"{base}/papers/reviews/{slug}/\"/>"
            f"<title>{_esc(slug)} 已发布/更新</title></entry>"
        )
    feed = (
        '<?xml version="1.0" encoding="utf-8"?>'
        f'<feed xmlns="http://www.w3.org/2005/Atom"><title>Paper Notes 更新</title>'
        f'<link href="{base}/"/><id>urn:paper-notes:feed</id>'
        f"<updated>{entries[0][0]}</updated>{''.join(items)}</feed>"
    )
    (site / "atom.xml").write_text(feed, encoding="utf-8")
    print(f"[hooks] Atom 订阅已生成：{min(len(entries), 30)} 条（site/atom.xml）")


def _render_home_extras(html):
    t = _last_commit_time()
    html = html.replace("<!-- LAST_UPDATE -->", t.strftime("%Y-%m-%d %H:%M"))
    now = datetime.datetime.now(TZ_BJ)
    days = (now.date() - t.date()).days
    if days <= 7:
        badge = "🟢 活跃中"
    elif days <= 30:
        badge = f"🟡 已 {days} 天未更新"
    else:
        badge = f"⚪ 已 {days} 天未更新"
    html = html.replace("<!-- ACTIVITY_BADGE -->", badge)
    if "<!-- ACTIVITY_CALENDAR -->" in html:
        html = html.replace("<!-- ACTIVITY_CALENDAR -->", _activity_calendar())
    return html


# ---------------------------------------------------------------------------
# 结构化数据页（library / evidence / models）：构建时从 data/ 渲染完整 HTML，
# JS 仅做筛选与对比的渐进增强——禁用脚本时页面仍完整可读。
# ---------------------------------------------------------------------------

DATA_DIR = pathlib.Path(__file__).resolve().parent / "data"

GROUP_LABEL = {"fm": "EEG 基础模型", "generative": "生成式模型",
               "reviews": "综述与观点", "survey": "相关研究"}
WEIGHT_LABEL = {"open": "权重开源", "partial": "部分放出", "none": "无权重"}


def _load_json(name: str):
    return json.loads((DATA_DIR / name).read_text(encoding="utf-8"))


def _esc(s) -> str:
    return html.escape(str(s if s is not None else ""))


def _render_library(html):
    papers = _load_json("papers.json")
    items = []
    for p in sorted(papers, key=lambda r: (-(r["year"] or 0), r["paper_id"])):
        links = []
        if p.get("doi"):
            links.append(f'<a href="https://doi.org/{_esc(p["doi"])}">DOI</a>')
        if p.get("arxiv") and str(p["arxiv"]).startswith("http"):
            links.append(f'<a href="{_esc(p["arxiv"])}">arXiv</a>')
        if p.get("code"):
            links.append(f'<a href="{_esc(p["code"])}">代码/项目</a>')
        note = f'<span class="lib-note">{_esc(p["one_liner"])}</span>' if p.get("one_liner") else ""
        meta = f'{_esc(p["venue"])} · {GROUP_LABEL.get(p["group"], p["group"])}'
        items.append(
            f'<div class="lib-item" data-group="{_esc(p["group"])}" data-type="{_esc(p["type"])}" '
            f'data-year="{p["year"] or 0}" data-code="{"1" if p.get("code") else "0"}" '
            f'data-doi="{"1" if p.get("doi") else "0"}">'
            f'<div class="lib-head"><a class="lib-title" href="../papers/{p["group"]}/{p["paper_id"]}/">{_esc(p["title"])}</a>'
            f'<span class="lib-year">{p["year"] or "?"}</span></div>'
            f'<div class="lib-meta">{meta} · {note}</div>'
            f'<div class="lib-links">{" · ".join(links) if links else "—"}</div>'
            f"</div>"
        )
    return html.replace("<!-- LIBRARY_LIST -->", "\n".join(items))


def _render_evidence(html):
    papers = {r["paper_id"]: r for r in _load_json("papers.json")}
    models = {r["model_id"]: r for r in _load_json("models.json")}
    datasets = {r["dataset_id"]: r for r in _load_json("datasets.json")}
    evidence = _load_json("evidence.json")
    status_label = {"verified": "已核原文", "pending": "待核对", "unreported": "论文未报告", "na": "不适用"}
    cards = []
    for e in evidence:
        p = papers.get(e["paper_id"], {})
        m = models.get(e.get("model_id") or "", {})
        d = datasets.get(e.get("dataset") or "", {})
        value_html = []
        for k, v in (e.get("value") or {}).items():
            value_html.append(f"<div><code>{_esc(k)}</code> = {_esc(v)}</div>")
        card = (
            f'<div class="ev-item" id="ev-{_esc(e["evidence_id"])}" data-paper="{_esc(e["paper_id"])}" '
            f'data-dataset="{_esc(e.get("dataset") or "")}" data-status="{_esc(e.get("status"))}">'
            f'<div class="ev-head"><span class="ev-status ev-{_esc(e.get("status"))}">{_esc(status_label.get(e.get("status"), e.get("status")))}</span>'
            f'<a class="ev-paper" href="../papers/{p.get("group", "fm")}/{_esc(e["paper_id"])}/">{_esc(p.get("title", e["paper_id"]))}</a>'
            f'<span class="ev-source">出处：{_esc(e.get("source", "—"))}</span></div>'
            f'<div class="ev-body">'
            f'<div><b>指标</b>：{_esc(e.get("metric", "—"))}</div>'
            f'{"<div><b>模型</b>：" + _esc(m.get("name", e.get("model_id"))) + "</div>" if m or e.get("model_id") else ""}'
            f'{"<div><b>数据集</b>：" + _esc(d.get("name", e.get("dataset"))) + "</div>" if d or e.get("dataset") else ""}'
            f'<div><b>协议</b>：{_esc(e.get("protocol", "—"))}</div>'
            f'{"<div><b>划分</b>：" + _esc(e["split"]) + "</div>" if e.get("split") else ""}'
            f'<div class="ev-values">{"".join(value_html) or "—"}</div>'
            f'<div class="ev-note">{_esc(e.get("note", ""))}</div>'
            f"</div></div>"
        )
        cards.append(card)
    return html.replace("<!-- EVIDENCE_LIST -->", "\n".join(cards))


def _render_models(html):
    models = _load_json("models.json")
    papers = {r["paper_id"]: r for r in _load_json("papers.json")}
    # 无 JS 回退：窄表列出全部模型的关键字段
    rows = []
    for m in sorted(models, key=lambda r: (r["paper_id"], r["model_id"])):
        p = papers.get(m["paper_id"], {})
        rows.append(
            f"<tr><td><a href=\"../papers/{p.get('group', 'fm')}/{m['paper_id']}/\">{_esc(m['name'])}</a></td>"
            f"<td>{_esc(p.get('venue', ''))}</td>"
            f"<td>{_esc(m['params_m'])}M</td>"
            f"<td>{_esc(m['input'])}</td>"
            f"<td>{_esc(WEIGHT_LABEL.get(m.get('weights'), m.get('weights')))}</td></tr>"
        )
    fallback = (
        '<div class="models-fallback"><table><thead><tr><th>模型</th><th>发表</th>'
        f'<th>参数量</th><th>输入</th><th>权重</th></tr></thead><tbody>{"".join(rows)}</tbody></table>'
        "<p>启用脚本后可用上方选择器做 2–4 个模型的逐字段并排对比。</p></div>"
    )
    payload = json.dumps(models, ensure_ascii=False).replace("</", "<\\/")
    html = html.replace("<!-- MODELS_FALLBACK -->", fallback)
    html = html.replace(
        '<script type="application/json" id="models-data"></script>',
        f'<script type="application/json" id="models-data">{payload}</script>',
    )
    return html


# ---------------------------------------------------------------------------
# 论文笔记历史地址 → 当前分类路径（一步重定向）
# ---------------------------------------------------------------------------

def _paper_pages(config) -> dict:
    """从构建产物收集 papers/<group>/<slug>/ → 页面目录 URL（如 fm/biot/）。

    on_post_build 阶段 config 里已不含文件集合，且 mkdocs 每次构建会先清空
    site 目录，因此产物目录就是当前分类的事实源。含 meta refresh 的页面
    是历史迁移留下的重定向页，不算当前论文页。
    """
    pages = {}
    seen = {}
    group_dirs = {"fm", "generative", "survey", "reviews"}
    redirect_re = re.compile(r'http-equiv="refresh"')
    for idx in (pathlib.Path(config["site_dir"]) / "papers").glob("*/*/index.html"):
        group, slug = idx.parent.parent.name, idx.parent.name
        if group not in group_dirs:
            continue
        if redirect_re.search(idx.read_text(encoding="utf-8")):
            continue  # 旧地址重定向页（组间迁移），不是当前论文页
        if slug in seen and seen[slug] != group:
            raise RuntimeError(f"论文 slug 重复：{slug} 同时位于 papers/{seen[slug]}/ 与 papers/{group}/")
        seen[slug] = group
        pages[slug] = f"{group}/{slug}/"
    return pages


def on_post_build(config, **kwargs):
    site = pathlib.Path(config["site_dir"])
    pages = _paper_pages(config)

    # 重定向来源：日期前缀地址 + 组间迁移旧地址 + 无前缀旧址
    # （reve / uni-ntfm 等无前缀出生的也覆盖）
    sources = dict(DATE_PREFIX_SLUGS)
    sources.update(GROUP_MOVE_SLUGS)
    for slug in pages:
        sources.setdefault(slug, slug)

    written, missing = 0, []
    for old, slug in sorted(sources.items()):
        if slug not in pages:
            missing.append(f"{old} -> {slug}")
            continue
        rel = posixpath.relpath("papers/" + pages[slug], f"papers/{old}/")
        page = site / "papers" / old / "index.html"
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(REDIRECT_TEMPLATE.format(rel=rel), encoding="utf-8")
        written += 1

    if missing:
        raise RuntimeError(f"[hooks] 论文重定向目标缺失（检查 mkdocs nav 与文件）：{missing}")
    print(f"[hooks] 论文历史地址重定向已生成：{written} 条（含锚点转发与无 JS 回退）")
    _build_atom(site, config)
