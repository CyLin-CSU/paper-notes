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
    return html
