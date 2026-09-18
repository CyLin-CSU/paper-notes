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
