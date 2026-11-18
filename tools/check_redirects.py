# -*- coding: utf-8 -*-
"""部署前产物检查：按「旧地址 → 目标」逐项校验论文历史重定向。

期望映射（单一事实源）：
  1. hooks.DATE_PREFIX_SLUGS 的日期前缀旧址；
  2. site/papers/<group>/<slug>/ 收集到的全部当前 slug 的无前缀旧址。
逐项检查：重定向页存在、meta refresh 落点与 hooks 的相对路径算法一致、
无自环、meta 落点与回退链接一致、目标页本身不是重定向（无跳转链）；
site 中出现期望清单之外的重定向页同样报错。
任一失败以非零码退出，中断 GitHub Actions 发布。

用法：python tools/check_redirects.py [site_dir]   # 默认 site
"""
import pathlib
import posixpath
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from hooks import DATE_PREFIX_SLUGS  # noqa: E402  与构建钩子共用同一份映射

REDIRECT_RE = re.compile(r'http-equiv="refresh" content="0; url=([^"]+)"')
LINK_RE = re.compile(r'<a href="([^"]+)">')
GROUPS = {"fm", "generative", "survey"}


def collect_pages(papers: pathlib.Path) -> dict:
    """当前论文页：site/papers/<group>/<slug>/index.html → 'group/slug/'。"""
    pages, seen = {}, {}
    for idx in sorted(papers.glob("*/*/index.html")):
        group, slug = idx.parent.parent.name, idx.parent.name
        if group not in GROUPS:
            continue
        if slug in seen and seen[slug] != group:
            raise SystemExit(f"[check-redirects] 论文 slug 跨分组重复：{slug}")
        seen[slug] = group
        pages[slug] = f"{group}/{slug}/"
    return pages


def collect_old_redirects(papers: pathlib.Path) -> dict:
    """site 中实际存在的旧地址重定向页：papers/<old>/index.html → (meta_url, link_url)。"""
    found = {}
    for idx in sorted(papers.glob("*/index.html")):
        if idx.parent.name in GROUPS:
            continue  # 分组目录自身（fm/generative/survey）不是旧地址页
        html = idx.read_text(encoding="utf-8")
        m = REDIRECT_RE.search(html)
        if m:
            a = LINK_RE.search(html)
            found[idx.parent.name] = (m.group(1), a.group(1) if a else None)
    return found


def expected_rel(old: str, target: str) -> str:
    """与 hooks.py 完全相同的相对路径算法。"""
    return posixpath.relpath("papers/" + target, f"papers/{old}/")


def main(site_dir: str) -> int:
    papers = pathlib.Path(site_dir) / "papers"
    if not papers.is_dir():
        print(f"[check-redirects] 未找到 {papers}，请先 mkdocs build")
        return 1
    pages = collect_pages(papers)
    if not pages:
        print("[check-redirects] 未找到任何论文页")
        return 1

    # 期望映射：日期前缀旧址 + 每个当前 slug 的无前缀旧址
    expected = dict(DATE_PREFIX_SLUGS)
    for slug in pages:
        expected.setdefault(slug, slug)

    bad, missing = [], []
    found = collect_old_redirects(papers)

    for old, slug in sorted(expected.items()):
        if slug not in pages:
            missing.append(f"{old} -> {slug}（目标论文不存在）")
            continue
        rel = expected_rel(old, pages[slug])
        if old not in found:
            bad.append(f"{old}: 缺少重定向页（期望 papers/{old}/ → {rel}）")
            continue
        meta_url, link_url = found[old]
        if posixpath.normpath(meta_url) != posixpath.normpath(rel):
            bad.append(f"{old}: 落点不符，期望 {rel}，实际 {meta_url}")
        elif posixpath.normpath(meta_url) == ".":
            bad.append(f"{old}: 重定向自环")
        elif link_url != meta_url:
            bad.append(f"{old}: 回退链接 {link_url} 与 meta 落点 {meta_url} 不一致")
        else:
            tgt_html = (papers / pages[slug] / "index.html").read_text(encoding="utf-8")
            if REDIRECT_RE.search(tgt_html):
                bad.append(f"{old}: 目标 {pages[slug]} 也是重定向页（跳转链）")

    extra = sorted(set(found) - set(expected))
    for old in extra:
        bad.append(f"{old}: site 中存在期望清单之外的重定向页（{found[old][0]}）")

    print(f"[check-redirects] 期望映射 {len(expected)} 条，site 实际 {len(found)} 条，逐项对照完成")
    for b in bad + missing:
        print(f"[check-redirects] 坏重定向：{b}")
    if missing:
        print("[check-redirects] 存在无法生成的期望映射（见上），先修复 nav 或文件")
        return 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "site"))
