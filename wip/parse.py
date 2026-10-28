"""Build corpus.json for Guyana from the cache only (no network).

    python -X utf8 parse.py              write corpus.json (atomically)
    python -X utf8 parse.py --compare    print the differences between the Constitution editions

The Constitution's history is built from three official consolidations of Cap. 1:01 and the amending Acts as
published by Parliament (see EDITIONS, LAWS and VERSIONS below; every choice is listed in DECISIONS).
"""
from __future__ import annotations

import difflib
import hashlib
import json
import os
import re
import sys
from pathlib import Path

import fetch
import layout

HERE = Path(__file__).resolve().parent

# ------------------------------------------------------------------ the Constitution editions

E2010 = ('https://web.archive.org/web/20121226190242id_/http://legalaffairs.gov.gy:80/information/laws-of-guyana/'
         'doc_download/2-chapter-00101.html')
E2012 = 'https://web.archive.org/web/20210404214043id_/https://mola.gov.gy/sites/default/files/Cap.101%20Constitution.pdf'
E2012_2016 = ('https://web.archive.org/web/20160119185919id_/http://legalaffairs.gov.gy/information/laws-of-guyana/'
              '410-chapter-101-the-constitution-of-the-co-operative-republic-of-guyana/file')
E2022 = 'https://www.mola.gov.gy/laws/Volume 1 Cap. 1.01 - 3.041785162884.pdf'

# (key, url, first page, last page (0-based, inclusive), smallest body font size)
EDITIONS = {
    'e2010': (E2010, 25, 215, 10.0),
    'e2012': (E2012, 29, 264, 9.5),
    'e2022': (E2022, 25, 227, 9.5),
}

ART_RE = re.compile(r'^(\d{1,3})\s?([A-Z]{0,2})\s?\.\s*(.*)$')
RANGE_RE = re.compile(r'^(\d{1,3})\s?\.?\s*-\s*(\d{1,3})\s?\.?\s*(\[.*)$')
RANGE_SPLIT = re.compile(r'(?<=\])\s+(?=\d{1,3}\s?\.?\s*-\s*\d{1,3}\s?\.?\s*\[)')
SCHED_RE = re.compile(r'^(FIRST|SECOND|THIRD|FOURTH) SCHEDULE\b')
SCHED_NO = {'FIRST': 1, 'SECOND': 2, 'THIRD': 3, 'FOURTH': 4}


def art_key(n: int, s: str) -> str:
    return f'art-{n:03d}{s.lower()}'


def _order(n: int, s: str) -> tuple:
    return (n, len(s), s)


def segment(paras: list[layout.Para]) -> tuple[dict, dict]:
    """Paragraphs -> {unit key: [lines]} and {unit key: [marginal notes]}."""
    units: dict[str, list[str]] = {}
    margins: dict[str, list[str]] = {}
    cur = None
    last = (0, 0, '')
    mode = 'before'
    for p in paras:
        t = p.text
        if mode == 'before':
            if t == 'PREAMBLE':
                mode, cur = 'preamble', 'preamble'
                units[cur], margins[cur] = [], list(p.margin)
            continue
        m_s = SCHED_RE.match(t)
        if m_s and (p.heading or t.isupper() or mode in ('art', 'sch')):
            mode, cur = 'sch', f'sch-{SCHED_NO[m_s.group(1)]}'
            units[cur], margins[cur] = [t], list(p.margin)
            continue
        if mode == 'sch':
            units[cur].append(t)
            margins[cur] += p.margin
            continue
        m_r = RANGE_RE.match(t)
        if m_r and int(m_r.group(1)) > last[0]:
            # a run of repealed articles ("79. - 88. [Articles 79 to 88 repealed ...]"): one unit per article
            for part in RANGE_SPLIT.split(t):
                m_r = RANGE_RE.match(part)
                a, b = int(m_r.group(1)), int(m_r.group(2))
                for n in range(a, b + 1):
                    k = art_key(n, '')
                    units[k], margins[k] = [m_r.group(3)], list(p.margin)
            cur, last, mode = None, _order(b, ''), 'art'
            continue
        m_a = ART_RE.match(t)
        if m_a:
            n, s = int(m_a.group(1)), m_a.group(2)
            if _order(n, s) > last and n <= last[0] + 12:
                cur, last, mode = art_key(n, s), _order(n, s), 'art'
                units[cur], margins[cur] = [m_a.group(3)], list(p.margin)
                continue
        if layout._is_heading(t) and len(t) > 2:
            # Part / Chapter / Title headings between articles are structure, not text of an article
            if mode == 'preamble':
                mode, cur = 'art', None
            continue
        if cur is None:
            continue
        units[cur].append(t)
        margins[cur] += p.margin
    return units, margins


# ------------------------------------------------------------------ line-end hyphens

WORD_RE = re.compile(r"[A-Za-z]+(?:-[A-Za-z]+)*")


def vocabulary(texts: list[str]) -> tuple[set, set]:
    plain, hyph = set(), set()
    for t in texts:
        for w in WORD_RE.findall(t.replace('⁠', ' ')):
            (hyph if '-' in w else plain).add(w.lower())
    return plain, hyph


def unhyphen(t: str, plain: set, hyph: set, unknown: list) -> str:
    def fix(m):
        a, b = m.group(1), m.group(2)
        joined, kept = (a + b).lower(), f'{a}-{b}'.lower()
        if kept in hyph:
            return f'{a}-{b}'
        if joined in plain:
            return a + b
        unknown.append(f'{a}-{b}')
        return f'{a}-{b}'
    return re.sub(r'([A-Za-z]+)-⁠([A-Za-z]+)', fix, t).replace('⁠', ' ')


def tidy(line: str) -> str:
    line = re.sub(r'\s+', ' ', line).strip()
    line = re.sub(r'\s+([,;:.])(?=\s|$)', r'\1', line)
    line = re.sub(r'\(\s+', '(', line)
    line = re.sub(r'\s+\)', ')', line)
    line = re.sub(r'\[\s+', '[', line)
    line = re.sub(r'\s*-$', ' -', line)          # "shall-" / "shall -" / "shall—": one form for a closing dash
    line = re.sub(r'^\((\d+[A-Z]*|[a-z]{1,4})\)(?=[A-Za-z])', r'() ', line)   # "(1)Any" -> "(1) Any"
    return line


def read_all() -> dict[str, tuple[dict, dict]]:
    out = {}
    for ed, (url, a, b, bm) in EDITIONS.items():
        out[ed] = segment(layout.read_edition(url, ed, a, b, bm))
    texts = [l for u, _ in out.values() for ls in u.values() for l in ls]
    plain, hyph = vocabulary(texts)
    unknown: list[str] = []
    for ed, (u, m) in out.items():
        for k in u:
            u[k] = [tidy(unhyphen(l, plain, hyph, unknown)) for l in u[k]]
            u[k] = [l for l in u[k] if l]
    return out


def compare():
    eds = read_all()
    names = list(eds)
    keys = sorted(set().union(*[set(u) for u, _ in eds.values()]))
    print({e: len(u) for e, (u, _) in eds.items()})
    for a, b in zip(names, names[1:]):
        ua, ub = eds[a][0], eds[b][0]
        print(f'===== {a} -> {b}')
        for k in keys:
            if ua.get(k) == ub.get(k):
                continue
            if k not in ua:
                print(f'+ {k} added'); continue
            if k not in ub:
                print(f'- {k} removed'); continue
            print(f'~ {k}')
            for l in difflib.unified_diff(ua[k], ub[k], lineterm='', n=0):
                if l.startswith(('---', '+++', '@@')):
                    continue
                print('   ', l[:300])


if __name__ == '__main__':
    if '--compare' in sys.argv:
        compare()
