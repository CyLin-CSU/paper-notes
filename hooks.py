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
    return subprocess.run(["git"] + args, capture_output=True, text=True, check=True,
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
    if page.file.src_uri != "index.md":
        return html
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
