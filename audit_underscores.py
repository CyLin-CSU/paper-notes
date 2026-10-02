"""Audit bare underscores outside math segments in a note file."""
import re
import sys

p = sys.argv[1] if len(sys.argv) > 1 else r'docs/papers/2026-09/0923-jet.md'

with open(p, encoding='utf-8') as f:
    raw = f.read()

# strip fenced code blocks entirely (mermaid/Python examples contain pseudo-symbols by design)
raw = re.sub(r'```.*?```', '', raw, flags=re.S)
# strip HTML comments (e.g. <!-- LAST_UPDATE --> placeholders)
raw = re.sub(r'<!--.*?-->', '', raw, flags=re.S)
lines = raw.splitlines()

bad = []
in_dollar_block = False
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if in_dollar_block:
        # inside a multi-line $$ display block: pure math, skip
        if '$$' in stripped:
            in_dollar_block = False
        continue
    if stripped.startswith('$$'):
        # $$ fence line: opener (block follows) or a complete one-line block
        if not (stripped.endswith('$$') and len(stripped) > 4):
            in_dollar_block = True
        continue
    s = line
    # remove display math and inline math ($$..$$ inline, \( \), \[ \])
    s = re.sub(r'\$\$.*?\$\$', '', s)
    s = re.sub(r'\\\[.*?\\\]', '', s)
    s = re.sub(r'\\\(.*?\\\)', '', s)
    # markdown links: keep link text, drop URL target (underscores in URLs are safe)
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)
    # remove inline code spans (markdown does not process emphasis inside them)
    s = re.sub(r'`[^`]*`', '', s)
    n = s.count('_')
    if n >= 2:
        bad.append((i, n, line.strip()[:100]))

for i, n, txt in bad:
    print(f'line {i}  ({n} underscores): {txt}')
print('total suspicious lines:', len(bad))
