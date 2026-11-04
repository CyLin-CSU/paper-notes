# -*- coding: utf-8 -*-
"""MkDocs 构建钩子：把最近一次 git 提交时间（精确到分钟）注入首页，并自动计算活跃状态。"""
import datetime
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent


def _last_commit_time() -> datetime.datetime:
    """取最近一次 git 提交的本地时间；失败则退回当前时间。"""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cI"],
            capture_output=True, text=True, check=True,
            cwd=str(ROOT),
        ).stdout.strip()
        return datetime.datetime.fromisoformat(out).astimezone()
    except Exception:
        return datetime.datetime.now()


def _commit_counts(days: int = 7) -> dict:
    """统计最近 days 天内每天的 git 提交数（按日期）。"""
    since = (datetime.date.today() - datetime.timedelta(days=days - 1)).isoformat()
    try:
        out = subprocess.run(
            ["git", "log", f"--since={since} 00:00", "--format=%as"],
            capture_output=True, text=True, check=True, cwd=str(ROOT),
        ).stdout
    except Exception:
        return {}
    counts: dict = {}
    for line in out.splitlines():
        d = line.strip()
        if d:
            counts[d] = counts.get(d, 0) + 1
    return counts


def _activity_calendar(days: int = 7) -> str:
    """生成 GitHub 风格的最近一周活跃热力图 HTML。"""
    counts = _commit_counts(days)
    today = datetime.date.today()
    cells, total = [], 0
    for i in range(days - 1, -1, -1):
        d = today - datetime.timedelta(days=i)
        ds = d.isoformat()
        n = counts.get(ds, 0)
        total += n
        level = 0 if n == 0 else 1 if n == 1 else 2 if n == 2 else 3 if n <= 4 else 4
        wd = "一二三四五六日"[d.weekday()]
        cells.append(
            f'<div class="ac-day"><div class="ac-cell" data-l="{level}" '
            f'title="{ds}（周{wd}）· {n} 次提交"></div>'
            f'<span class="ac-wd">{"今" if i == 0 else wd}</span></div>'
        )
    grid = "".join(cells)
    legend = "".join(f'<i data-l="{l}"></i>' for l in range(5))
    return (
        f'<div class="activity-calendar">'
        f'<span class="ac-total">本周提交 <b>{total}</b> 次</span>'
        f'<div class="ac-grid">{grid}</div>'
        f'<span class="ac-legend">少{legend}多</span>'
        f"</div>"
    )


def on_page_content(html, page, **kwargs):
    if page.file.src_uri != "index.md":
        return html
    t = _last_commit_time()
    stamp = t.strftime("%Y-%m-%d %H:%M")
    now = datetime.datetime.now().astimezone()
    days = (now - t).days
    if days <= 7:
        badge = "🟢 **活跃中**"
    elif days <= 30:
        badge = f"🟡 已 **{days}** 天未更新"
    else:
        badge = f"⚪ 已 **{days}** 天未更新"
    html = html.replace("<!-- LAST_UPDATE -->", stamp)
    html = html.replace("<!-- ACTIVITY_BADGE -->", badge)
    if "<!-- ACTIVITY_CALENDAR -->" in html:
        html = html.replace("<!-- ACTIVITY_CALENDAR -->", _activity_calendar())
    return html


# 兼容去掉阅读日期前缀之前的论文链接。
PAPER_REDIRECTS = {
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


def on_post_build(config, **kwargs):
    site = pathlib.Path(config["site_dir"])
    for old, new in PAPER_REDIRECTS.items():
        target = f"../{new}/"
        page = site / "papers" / old / "index.html"
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(
            '<!doctype html><html lang="zh"><meta charset="utf-8">'
            f'<meta http-equiv="refresh" content="0; url={target}">'
            '<meta name="robots" content="noindex"><title>页面已迁移</title>'
            f'<a href="{target}">打开论文笔记</a></html>',
            encoding="utf-8",
        )
