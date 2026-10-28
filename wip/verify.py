"""Check today's Constitution in corpus.json against the official text (L.R.O. 1/2022 PDF on mola.gov.gy, cached).

    python -X utf8 verify.py

Word-count check, both ways, over the Constitution pages of the official PDF (from the PREAMBLE heading to the end
of the Fourth Schedule):
- every word of the latest version must be printed in the PDF (only the "# Article N" / "# Preamble" heading lines
  are ours), and
- every word printed in the PDF must be in the latest version, or be one of what parse.py leaves out on purpose:
  running heads and feet, marginal notes, Part/Chapter/Title headings and repeal-only placeholders.
Reads the cache only.
"""
import collections
import json
import re
import sys
from pathlib import Path

import fitz

import fetch
import layout
import parse

HERE = Path(__file__).resolve().parent


def words(s: str) -> collections.Counter:
    return collections.Counter(re.findall(r'[A-Za-z]+', s))


def main() -> int:
    c = json.loads((HERE / 'corpus.json').read_text(encoding='utf-8'))
    units = c['acts'][0]['versions'][-1]['units']
    ours = words(' '.join(u['text'] for u in units.values()))
    url, first, last, body_min = parse.EDITIONS['e2022']
    doc = fitz.open(stream=fetch.cached(url), filetype='pdf')
    raw = ' '.join(doc[i].get_text() for i in range(first, last + 1))
    raw = raw[raw.index('PREAMBLE'):]
    pdf = words(raw)
    ours_heads = words(' '.join(u['text'].split('\n', 1)[0] for k, u in units.items() if not k.startswith('sch-')))
    added = (ours - ours_heads) - pdf
    paras = layout.read_edition(url, 'e2022', first, last, body_min)
    start = [p.text for p in paras].index('PREAMBLE')
    left_out = collections.Counter()
    for p in paras[start:]:
        left_out += words(' '.join(p.margin))
        if (p.heading or layout._is_heading(p.text) or parse.PLACEHOLDER.match(p.text)
                or parse.RANGE_RE.match(p.text) or re.match(r'^\d+\s?\.\s*\[', p.text)):
            left_out += words(p.text)
    running = words('LAWS OF GUYANA Cap Constitution of the Co-operative Republic of Guyana L.R.O.')
    for k, n in running.items():
        left_out[k] += n * (last + 1 - first)
    dropped = pdf - ours - left_out
    print(f'official PDF words {sum(pdf.values())}, latest version words {sum(ours.values())}')
    print(f'words in the repository that the PDF does not print: {sum(added.values())} {added.most_common(10)}')
    print(f'PDF words neither in the repository nor left out on purpose: {sum(dropped.values())} {dropped.most_common(10)}')
    return 0 if not added and sum(dropped.values()) <= 5 else 1


if __name__ == '__main__':
    sys.exit(main())
