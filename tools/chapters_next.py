"""corpus.d/85-commercial.json: commercial and employment chapters of the Laws of Guyana.

Built exactly like chapters_extra.py's parts (chapters_extra.act: parse.read_all, parse.tidy_sections, the same
layout reader and repairs). Every chapter here is one mola.gov.gy still serves in the L.R.O. 1/2012 revised edition
as its current text ('mola2012'), so each has one version, dated 2012-12-31. Reads only the cache; deterministic;
the part is written atomically.

    python -X utf8 chapters_next.py                (CHAPTERS_EXTRA_DIR=... to write the part elsewhere)
    python -X utf8 verify_chapters.py corpus.d/85-commercial.json
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import chapters_extra as cx  # noqa: E402

_ch = cx._ch
OUT_DIR = cx.OUT_DIR
RETRIEVED = cx.RETRIEVED
V17, V18 = cx.MOLA + 'Volume 17 Cap. 89.02 - 91.01', cx.MOLA + 'Volume 18 Cap. 91.02 - 96.01'


MARK = r'1953\s+Ed\.\s+c\.\s*\d+'   # verify starts after the edition note (the text layer sets s. 1 before the long title)


def _m(vol: str, n: str, first: int, last: int, size: float = 9.5) -> tuple[dict, str]:
    url = vol + n + '.pdf'
    return {'e2012': (url, first, last, size)}, url


PARTS = {
    '85-commercial': [
        _ch('partnership', 'Partnership Act', '89:02', '20 of 1900', 'mola2012', *_m(V17, '1695666957', 4, 22),
            ['28 of 1902', '1 of 1903', '6 of 1905']),
        _ch('merchandise-marks', 'Merchandise Marks Act', '90:04', '2 of 1888', 'mola2012', *_m(V17, '1695664721', 3, 14),
            ['5 of 1910', '16 of 1912', '27 of 1914', '4 of 1972']),
        _ch('business-names', 'Business Names (Registration) Act', '90:05', '11 of 1919', 'mola2012',
            *_m(V17, '1695664679', 3, 17), ['11 of 1926', '38 of 1955', '4 of 1972', '8 of 2000']),
        _ch('sale-of-goods', 'Sale of Goods Act', '90:10', '26 of 1913', 'mola2012', *_m(V17, '1695664580', 5, 32),
            ['4 of 1972'], marker=MARK),
        _ch('pledge-of-goods', 'Pledge of Goods Act', '90:11', '12 of 1916', 'mola2012', *_m(V17, '1695664531', 3, 11),
            ['15 of 1966A'], marker=MARK),
        _ch('bills-of-sale', 'Bills of Sale Act', '90:12', '22 of 1916', 'mola2012', *_m(V17, '1695664487', 3, 18),
            ['4 of 1972']),
        _ch('bills-of-exchange', 'Bills of Exchange Act', '90:13', '13 of 1891', 'mola2012',
            *_m(V17, '1695664434', 6, 61),
            ['17 of 1907', '2 of 1915', '35 of 1918', '56 of 1932', '39 of 1933', '4 of 1972', '29 of 1991']),
        _ch('traders-breach-of-contract', 'Traders (Breach of Contract) Act', '91:03', '4 of 1861', 'mola2012',
            *_m(V18, '1695664130', 2, 5), ['4 of 1972']),
        _ch('termination-of-employment', 'Termination of Employment and Severance Pay Act', '96:01', '19 of 1997',
            'mola2012', *_m(V18, '1695660952', 3, 20), ['7 of 1999']),
    ],
}
SKIPPED = [
    _ch('money-lenders', 'Money Lenders Act', '91:05', '11 of 1957', 'mola2012', *_m(V18, '1695664041', 3, 27),
        ['4 of 1972'],
        skip='the Second Schedule (s. 17 forms) is a ledger table with turned headings, and its last two pages are '
             'printed as images (no OCR); the Moneylenders Rules begin at PDF page 29'),
]
ALL = [ch for chs in PARTS.values() for ch in chs]
ALL_DEFINED = ALL + SKIPPED


def _sale_of_goods(ed: str, ps: list) -> list:
    """s. 16 of Cap. 90:10: its side note ("Sale by / sample.") is set in body-size type, so the reader runs it into
    the section's first line ("Sale by 16. (1) ... by sample. sample where"). Take the side-note pieces out: the
    section reads as printed ("16. (1) A contract of sale is a contract for sale by sample where ...")."""
    bad = 'Sale by 16. (1) A contract of sale is a contract for sale by sample. sample where'
    n = 0
    for p in ps:
        if p.text.startswith(bad):
            p.text = '16. (1) A contract of sale is a contract for sale by sample where' + p.text[len(bad):]
            p.margin.append('Sale by sample.')
            n += 1
    assert n == 1, n
    return ps


cx.FIXES[('sale-of-goods', 'e2012')] = _sale_of_goods

DECISIONS = {
    '85-commercial': cx.COMMON_DECISIONS + [
        'Commercial and employment chapters (Partnership Act Cap. 89:02, Merchandise Marks Act Cap. 90:04, Business Names (Registration) Act Cap. 90:05, Sale of Goods Act Cap. 90:10, Pledge of Goods Act Cap. 90:11, Bills of Sale Act Cap. 90:12, Bills of Exchange Act Cap. 90:13, Traders (Breach of Contract) Act Cap. 91:03, Termination of Employment and Severance Pay Act Cap. 96:01): mola.gov.gy still serves each in L.R.O. 1/2012, so each has one version, 2012-12-31. The Parliament index of Acts names no later Act amending any of them (searched by title); it has gaps, so later amendments may exist that no source online shows.',
        'Layout repair in this part: the side note of s. 16 of Cap. 90:10 ("Sale by sample.") is set in body-size type and was read into the section\'s first line; it is taken out, so the section reads as printed.',
        'Not added from this group: the Trade Marks Act Cap. 90:01 (its 203-page PDF is mostly forms and subsidiary legislation, left for a later pass); the Money Lenders Act Cap. 91:05 (the forms of its Second Schedule are a ledger table with turned headings and two pages printed only as images, which are not read without OCR).',
    ],
}
AI_USE = ['Corpus part {part}: Claude Code with Claude Opus 5.5 (claude-opus-5-5) wrote chapters_next.py, chose the chapters and page ranges and read the amending-law lists from the front pages (checked against the page text); it did not write or alter any legal text.']


def build(part: str) -> dict:
    chs = PARTS[part]
    return {'laws': cx.laws(chs), 'acts': [cx.act(ch) for ch in chs], 'sources': cx.sources(part, chs),
            'applies': [], 'decisions': DECISIONS[part], 'ai_use': [a.format(part=part) for a in AI_USE]}


def main(argv: list[str]) -> None:
    OUT_DIR.mkdir(exist_ok=True)
    for part in (argv or list(PARTS)):
        c = build(part)
        out = OUT_DIR / f'{part}.json'
        tmp = out.with_suffix('.json.tmp')
        tmp.write_text(json.dumps(c, ensure_ascii=False, indent=1) + '\n', encoding='utf-8', newline='\n')
        os.replace(tmp, out)
        for a in c['acts']:
            print(part, a['slug'], [(v['from'], len(v.get('units') or {})) for v in a['versions']])


if __name__ == '__main__':
    main(sys.argv[1:])
