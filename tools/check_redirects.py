# -*- coding: utf-8 -*-
"""部署前产物检查：校验论文历史地址重定向页的目标存在、无自环、数量达标。

用法：python tools/check_redirects.py [site_dir]   # 默认 site
任一失败以非零码退出，中断 GitHub Actions 发布。
"""
import pathlib
import re
import sys

EXPECTED_MIN = 52  # 25 个日期前缀地址 + 27 个无前缀旧址


def main(site_dir: str) -> int:
    papers = pathlib.Path(site_dir) / "papers"
    if not papers.is_dir():
        print(f"[check-redirects] 未找到 {papers}，请先 mkdocs build")
        return 1
    checked, bad = 0, []
    for page in sorted(papers.glob("*/index.html")):
        html = page.read_text(encoding="utf-8")
        m = re.search(r'http-equiv="refresh" content="0; url=([^"]+)"', html)
        if not m:
            continue  # 正常页面（分组目录下没有 index.html，不会进到这里）
        checked += 1
        rel = m.group(1)
        target = (page.parent / rel).resolve()
        if not (target / "index.html").exists():
            bad.append(f"papers/{page.parent.name}/: 目标不存在 {rel}")
        elif target == page.parent.resolve():
            bad.append(f"papers/{page.parent.name}/: 重定向自环")
    print(f"[check-redirects] 共校验 {checked} 条重定向")
    for b in bad:
        print(f"[check-redirects] 坏重定向：{b}")
    if checked < EXPECTED_MIN:
        print(f"[check-redirects] 重定向数量少于预期（≥{EXPECTED_MIN}）")
        return 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "site"))
