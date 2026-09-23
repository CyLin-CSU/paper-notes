"""Audit bare underscores outside math segments in a note file."""
import re
import sys

p = sys.argv[1] if len(sys.argv) > 1 else r'docs/papers/2026-09/0923-jet.md'

with open(p, encoding='utf-8') as f:
    lines = f.readlines()

bad = []
for i, line in enumerate(lines, 1):
    s = line
    # remove display math and inline math
    s = re.sub(r'\\\[.*?\\\]', '', s)
    s = re.sub(r'\\\(.*?\\\)', '', s)
    # remove inline code spans (markdown does not process emphasis inside them)
    s = re.sub(r'`[^`]*`', '', s)
    n = s.count('_')
    if n >= 2:
        bad.append((i, n, line.strip()[:100]))

for i, n, txt in bad:
    print(f'line {i}  ({n} underscores): {txt}')
print('total suspicious lines:', len(bad))
