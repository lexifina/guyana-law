"""corpus.d/70-summary-jurisdiction.json, 75-family.json, 80-land.json: more chapters of the Laws of Guyana.

Three parts, each its own file (and its own .PUBLISH once verified), built the same way as chapters.py and
chapters_more.py (parse.read_all, parse.tidy_sections, the same layout reader). Reads only the cache; deterministic;
each part written atomically.

Three kinds of chapter, by what the official source holds:
- 'two': mola.gov.gy serves the L.R.O. 1/2022 edition and the Internet Archive holds the L.R.O. 1/2012 PDF (22 June
  2022 captures of mola.gov.gy/sites/default/files): two versions, 2012-12-31 and 2022-12-31 (if the texts differ).
- 'mola2012': mola.gov.gy still serves the L.R.O. 1/2012 edition as the chapter's current text: one version.
- 'only2022': the archived L.R.O. 1/2012 PDF already lists an Act of 2014 (the Sexual Offences Act trap), so it is
  not the text of 31 December 2012 and is not used: one version, L.R.O. 1/2022, dated 2022-12-31.

    python -X utf8 chapters_extra.py                 (CHAPTERS_EXTRA_DIR=... to write the parts elsewhere)
    python -X utf8 verify_chapters.py corpus.d/75-family.json [--older]
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import chapters  # noqa: E402
import parse  # noqa: E402

WB, MOLA, PARL = chapters.WB, chapters.MOLA, chapters.PARL
OUT_DIR = Path(os.environ.get('CHAPTERS_EXTRA_DIR', HERE / 'corpus.d'))
RETRIEVED = '2026-10-29'
CAPTURED = '22 June 2022'
ARCH = WB + '{ts}id_/https://mola.gov.gy/sites/default/files/{f}'


def _ch(slug, short, cap, first, kind, editions, current, amenders, after2012=(), missing=(), lro2012_lists=None):
    n, y = first.split(' of ')
    return {'slug': slug, 'short': short, 'cap': cap, 'title': f'{short} (Cap. {cap})',
            'first': (f'act-{n}-{y}', f'Act No. {n} of {y}', f'Act No. {n} of {y} (named as the origin of Cap. {cap})'),
            'kind': kind, 'editions': editions, 'current': current, 'amenders': list(amenders),
            'after2012': list(after2012), 'missing': list(missing), 'lro2012_lists': lro2012_lists}


V1, V2, V3 = MOLA + 'Volume 1 Cap. 1.01 - 3.04', MOLA + 'Volume 2 Cap. 3.05 - 6.02', MOLA + 'Volume 3 Cap. 6.03 - 10.07'
V4, V5 = MOLA + 'Volume 4 Cap. 10.08 - 12.21', MOLA + 'Volume 5 Cap. 12.22 - 17.02'
V9, V12 = MOLA + 'Volume 9 Cap. 36.02 - 46.07', MOLA + 'Volume 12 Cap. 59.01 - 68.09'

# editions: {ed: (url, first page, last page (0-based, inclusive: the Act, before its subsidiary legislation),
# smallest body font size)}. Amending laws as each chapter's front page lists them (read from the page's words in
# column order, metadata only); 'after2012' = listed only in the 2022 edition.
PARTS = {
    '70-summary-jurisdiction': [
        _ch('summary-jurisdiction-appeals', 'Summary Jurisdiction (Appeals) Act', '3:04', '6 of 1929', 'only2022',
            {'e2022': (V1 + '1785164383.pdf', 4, 33, 9.5)}, V1 + '1785164383.pdf',
            ['31 of 1942', '32 of 1942', '29 of 1955', '19 of 1958', 'O. 37/1966A', '4 of 1972', '17 of 1977',
             '21 of 1978', '4 of 1980', '2 of 1989', '13 of 2014', '21 of 2022'],
            lro2012_lists=('Act No. 13 of 2014', ARCH.format(ts='20220622191008', f='Cap.304.pdf'))),
        _ch('summary-jurisdiction-magistrates', 'Summary Jurisdiction (Magistrates) Act', '3:05', '10 of 1893', 'two',
            {'e2012': (ARCH.format(ts='20220622191044', f='Cap%20305.pdf'), 6, 45, 9.5),
             'e2022': (V2 + '1785164452.pdf', 6, 45, 9.5)}, V2 + '1785164452.pdf',
            ['6 of 1903', '17 of 1905', '18 of 1905', '29 of 1909', '5 of 1915', '9 of 1915', '16 of 1917',
             '14 of 1924', '30 of 1928', '46 of 1929', '3 of 1937', '15 of 1937', '11 of 1953', '45 of 1955',
             '41 of 1957', 'O. 37/1966A', '4 of 1971', '4 of 1972', 'O. 166/1974', 'O. 24/1986', '14 of 1988',
             '15 of 1988', '19 of 1990', '25 of 1997']),
        _ch('summary-jurisdiction-petty-debt', 'Summary Jurisdiction (Petty Debt) Act', '7:01', '11 of 1893', 'two',
            {'e2012': (ARCH.format(ts='20220622193037', f='Cap%20701.pdf'), 5, 40, 9.5),
             'e2022': (V3 + '1785168328.pdf', 5, 40, 9.5)}, V3 + '1785168328.pdf',
            ['11 of 1894', '13 of 1894', '12 of 1895', '12 of 1897', '6 of 1904', '18 of 1905', '7 of 1908',
             '9 of 1915', '4 of 1928', '51 of 1932', '33 of 1948', '4 of 1972', '21 of 1978', '20 of 1993',
             '24 of 2009']),
        _ch('summary-jurisdiction-offences', 'Summary Jurisdiction (Offences) Act', '8:02', '17 of 1893', 'two',
            {'e2012': (ARCH.format(ts='20220622193442', f='Cap%20802.pdf'), 13, 137, 9.5),
             'e2022': (V3 + '1785254422.pdf', 13, 137, 9.5)}, V3 + '1785254422.pdf',
            ['13 of 1894', '12 of 1895', '17 of 1895', '12 of 1896', '22 of 1898', '36 of 1902', '42 of 1902',
             '26 of 1903', '20 of 1904', '7 of 1905', '18 of 1912', '12 of 1915', '26 of 1918', '10 of 1920',
             '11 of 1920', '34 of 1922', '21 of 1923', '24 of 1923', '30 of 1924', '11 of 1925', '34 of 1927',
             '39 of 1927', '2 of 1929', '43 of 1929', '24 of 1930', '1 of 1931', '21 of 1932', '13 of 1933',
             '6 of 1937', '15 of 1937', '22 of 1940', '14 of 1941', '6 of 1942', '6 of 1946', '23 of 1949',
             '51 of 1952', '12 of 1953', '26 of 1954', '30 of 1954', '39 of 1955', '56 of 1955', '18 of 1957',
             '24 of 1969', 'O. 15/1970', '4 of 1972', '25 of 1973', 'O. 88/1975', '21 of 1978', '3 of 1983',
             '11 of 1984', '1 of 1988', '2 of 1989', '12 of 1989', '19 of 1990', '24 of 1990', '8 of 1997',
             '18 of 1997', '10 of 1998', '19 of 2007', '15 of 2008', '29 of 2009', '7 of 2010'],
            after2012=['11 of 2021']),
        _ch('summary-jurisdiction-procedure', 'Summary Jurisdiction (Procedure) Act', '10:02', '12 of 1893', 'mola2012',
            {'e2012': (V3 + '1696971380.pdf', 8, 131, 9.5)}, V3 + '1696971380.pdf',
            ['25 of 1893', '11 of 1894', '13 of 1894', '12 of 1895', '4 of 1901', '16 of 1902', '26 of 1903',
             '6 of 1904', '15 of 1906', '16 of 1909', '6 of 1912', '13 of 1915', '34 of 1922', '24 of 1927',
             '11 of 1931', '21 of 1932', '51 of 1932', '9 of 1933', '11 of 1939', '32 of 1947', '34 of 1948',
             '14 of 1959', '29 of 1961', '3 of 1963', '24 of 1969', 'O. 15/1970', '28 of 1970', '4 of 1972',
             'O. 166/1974', 'O. 167/1974', '21 of 1978', '4 of 1980', 'O. 22/1988', 'O. 27/1988', '2 of 1989',
             '11 of 1997', '13 of 1998', 'O. 5/2007', '6 of 2012']),
    ],
    '75-family': [
        _ch('domestic-violence', 'Domestic Violence Act', '11:09', '18 of 1996', 'mola2012',
            {'e2012': (V4 + '1696970601.pdf', 4, 43, 9.5)}, V4 + '1696970601.pdf', []),
        _ch('wills', 'Wills Act', '12:02', '12 of 1906', 'mola2012',
            {'e2012': (V4 + '1696970484.pdf', 2, 7, 9.5)}, V4 + '1696970484.pdf', [],
            missing=[('act-21-2024', 'Act No. 21 of 2024', 'Wills (Amendment) Act 2024', '27 December 2024',
                      PARL + '24362-24154-act_no._21_of_2024.pdf')]),
        _ch('family-dependants-provision', 'Family and Dependants Provision Act', '12:24', '22 of 1990', 'mola2012',
            {'e2012': (V5 + '1696970331.pdf', 2, 30, 9.5)}, V5 + '1696970331.pdf', ['10 of 2012']),
        _ch('matrimonial-causes', 'Matrimonial Causes Act', '45:02', '34 of 1919', 'mola2012',
            {'e2012': (V9 + '1696828171.pdf', 3, 19, 9.5)}, V9 + '1696828171.pdf',
            ['1 of 1951', '34 of 1951', '45 of 1952', 'O. 1/1977', 'O. 6/1986'],
            missing=[('act-13-2024', 'Act No. 13 of 2024', 'Matrimonial Causes (Amendment) Act 2024', '27 August 2024',
                      PARL + '24357-24095-act_no._13_of_2024.pdf')]),
        _ch('maintenance', 'Maintenance Act', '45:03', '14 of 1903', 'mola2012',
            {'e2012': (V9 + '1696828132.pdf', 2, 10, 9.5)}, V9 + '1696828132.pdf',
            ['3 of 1908', '4 of 1972', '12 of 1983', '19 of 1990', '24 of 1997']),
        _ch('adoption-of-children', 'Adoption of Children Act', '46:04', '18 of 2009', 'mola2012',
            {'e2012': (V9 + '1696827923.pdf', 4, 42, 9.5)}, V9 + '1696827923.pdf', ['10 of 2011'],
            missing=[('act-8-2021', 'Act No. 8 of 2021', 'Adoption of Children (Amendment) Act 2021', '9 August 2021',
                      PARL + '22851-act_no._8_of_2021.pdf')]),
        _ch('status-of-children', 'Status of Children Act', '46:05', '19 of 2009', 'mola2012',
            {'e2012': (V9 + '1696827883.pdf', 4, 34, 9.5)}, V9 + '1696827883.pdf', []),
    ],
    '80-land': [
        _ch('deeds-registry', 'Deeds Registry Act', '5:01', '17 of 1919', 'only2022',
            {'e2022': (V2 + '1785167325.pdf', 4, 49, 9.5)}, V2 + '1785167325.pdf',
            ['19 of 1927', '44 of 1929', '2 of 1931', '11 of 1934', '4 of 1936', '14 of 1938', '32 of 1956',
             '27 of 1957', '16 of 1965', '24 of 1969', '22 of 1970', '4 of 1972', 'O. 166/1974', '14 of 1982',
             '2 of 1993', '5 of 2014', '3 of 2022'],
            lro2012_lists=('Act No. 5 of 2014', ARCH.format(ts='20220622191946', f='Cap%20501.pdf'))),
        _ch('land-registry', 'Land Registry Act', '5:02', '18 of 1959', 'two',
            {'e2012': (ARCH.format(ts='20220622192023', f='Cap%20502.pdf'), 8, 100, 9.5),
             'e2022': (V2 + '1785166295.pdf', 8, 99, 9.5)}, V2 + '1785166295.pdf',
            ['1 of 1972', '5 of 1972', 'O. 80/1980', '14 of 1982', 'O. 31/1992', 'O. 7/1993', '13 of 1993',
             '4 of 1997', '3 of 2003']),
        _ch('title-to-land', 'Title to Land (Prescription and Limitation) Act', '60:02', '62 of 1952', 'mola2012',
            {'e2012': (V12 + '1696626307.pdf', 3, 15, 9.5)}, V12 + '1696626307.pdf', ['6 of 2011']),
        _ch('landlord-and-tenant', 'Landlord and Tenant Act', '61:01', '26 of 1947', 'mola2012',
            {'e2012': (V12 + '1696625534.pdf', 5, 54, 9.5)}, V12 + '1696625534.pdf', ['4 of 1972', 'O. 23/1986']),
        _ch('state-lands', 'State Lands Act', '62:01', '32 of 1903', 'mola2012',
            {'e2012': (V12 + '1696625429.pdf', 4, 23, 9.5)}, V12 + '1696625429.pdf',
            ['11 of 1971', '1 of 1972', '4 of 1972', '9 of 1977', '20 of 1989']),
        _ch('rent-restriction', 'Rent Restriction Act', '36:23', '23 of 1941', 'mola2012',
            {'e2012': (V9 + '1696910931.pdf', 3, 47, 9.5)}, V9 + '1696910931.pdf',
            ['13 of 1947', '30 of 1948', '24 of 1950', '20 of 1958', '24 of 1969', '31 of 1969', '6 of 1981',
             '8 of 1981']),
    ],
}
ALL = [ch for chs in PARTS.values() for ch in chs]

# per-act layout repairs before segmentation: {(slug, ed): fix(ed, paragraphs) -> paragraphs}
FIXES: dict = {}


def act(ch: dict) -> dict:
    fix = (lambda ed, ps: FIXES[(ch['slug'], ed)](ed, ps) if (ch['slug'], ed) in FIXES else ps)
    eds = parse.read_all(ch['editions'], 'sec', fix)
    eds = {ed: (parse.tidy_sections(u), m) for ed, (u, m) in eds.items()}
    for u, _m in eds.values():   # a space the text layer lacks after a comma ("repealed,the")
        for k in u:
            u[k] = [re.sub(r',(?=[a-z])', ', ', line) for line in u[k]]
    units = {ed: parse.as_units(parse.clean_units(u)) for ed, (u, _m) in eds.items()}
    last_year = ch['amenders'][-1].split(' of ')[-1].split('/')[-1] if ch['amenders'] else None
    versions = []
    if 'e2012' in units:
        url = ch['editions']['e2012'][0]
        if ch['kind'] == 'mola2012':
            note = ('Revised edition L.R.O. 1/2012 (the Laws of Guyana as they stood on 31 December 2012), which the '
                    'Ministry of Legal Affairs still serves as the chapter\'s current text on mola.gov.gy. '
                    + (f'It lists no amending Act after {last_year}.' if last_year else 'It lists no amending Act.'))
        else:
            note = chapters.E2012_NOTE.format(cap=CAPTURED)
        versions.append({'from': '2012-12-31', 'source_url': url, 'sha256': parse.sha(url), 'units': units['e2012'],
                         'credits': {}, 'note': note})
    if 'e2022' in units:
        url = ch['editions']['e2022'][0]
        if ch['kind'] == 'only2022':
            label, arch = ch['lro2012_lists']
            versions.append({'from': '2022-12-31', 'source_url': url, 'sha256': parse.sha(url), 'units': units['e2022'],
                             'credits': {},
                             'note': 'Revised edition L.R.O. 1/2022 (the Laws of Guyana as they stood on 31 December '
                                     '2022), today\'s official text on mola.gov.gy, and the oldest version here: the '
                                     'L.R.O. 1/2012 PDF of this chapter archived from mola.gov.gy (Internet Archive, '
                                     f'{CAPTURED}) already lists {label} among the amending laws, so it is not the '
                                     'text of 31 December 2012 and is not used.'})
        elif units['e2022'] != units['e2012']:
            note = ('The 2022 revised edition (L.R.O. 1/2022; the Laws of Guyana as they stood on 31 December 2022), '
                    "today's official text on mola.gov.gy. ")
            if ch['after2012']:
                note += ('It lists ' + ', '.join(f'Act No. {n}' for n in ch['after2012']) + ' among the amending '
                         'laws; its changes are committed as unexplained on the edition\'s date, because the editions '
                         'do not say which words each Act changed.')
            else:
                note += (f'It lists no amending Act after {last_year}; its changes are revision edits that no Act '
                         'explains, committed as unexplained.')
            versions.append({'from': '2022-12-31', 'source_url': url, 'sha256': parse.sha(url), 'units': units['e2022'],
                             'credits': {}, 'note': note})
        else:
            versions[0]['note'] += (' The 2022 revised edition (L.R.O. 1/2022, today\'s text on mola.gov.gy) prints '
                                    'the same text.')
    if ch['missing']:
        versions[-1]['note'] += (' Not applied: ' + '; '.join(f'{label} ({title}, Official Gazette {day})'
                                                              for _k, label, title, day, _u in ch['missing'])
                                 + ', printed by Parliament only as a scan without a text layer (no OCR); the '
                                   'sections it amends show their earlier text.')
    earlier = [ch['first'][0]] + [chapters.law_key(n)[0] for n in ch['amenders']]
    return {'slug': ch['slug'], 'short': ch['short'], 'title': ch['title'], 'url': ch['current'],
            'first_law': None, 'earlier_laws': earlier, 'versions': versions}


def laws(chs: list) -> dict:
    out = {}
    for ch in chs:
        k, label, title = ch['first']
        out.setdefault(k, chapters.blank_law(label, title))
        for n in ch['amenders'] + ch['after2012']:
            k, label, kind = chapters.law_key(n)
            out.setdefault(k, chapters.blank_law(label, f'{label} (named as amending Cap. {ch["cap"]})', kind))
    return out


COMMON_DECISIONS = [
    'Chapters read like the other chapters (parse.read_all, parse.tidy_sections, layout.py): long titles, the arrangement of sections, Part headings, cross-headings and marginal notes are left out; sections printed only as a repeal note have no file; schedules are units of their own; subsidiary legislation printed after the Act is not included. Acts of origin are named by number only ("Act No. 12 of 1893"), as the front pages give no titles; amending laws are read from the front page\'s words in column order (metadata, not law text).',
    'Where mola.gov.gy still serves the L.R.O. 1/2012 PDF as the chapter\'s current text, the chapter has that one version, dated 2012-12-31 (the edition\'s date) and credited to the publisher as the oldest version available. Amending Acts passed after 2012 that the Parliament index names and that are printed only as scans are named in the version note and the README and not applied; the Parliament index has gaps, so other later amendments may exist that no source online shows.',
]

DECISIONS = {
    '70-summary-jurisdiction': COMMON_DECISIONS + [
        'Summary Jurisdiction (Magistrates) Act Cap. 3:05, (Petty Debt) Act Cap. 7:01 and (Offences) Act Cap. 8:02: L.R.O. 1/2012 read from Internet Archive captures of mola.gov.gy (22 June 2022) as the 2012-12-31 version; the differences in L.R.O. 1/2022 (today\'s chapter PDF on mola.gov.gy) are unexplained changes on 2022-12-31. Cap. 8:02\'s 2022 edition lists Act No. 11 of 2021 (Summary Jurisdiction (Offences) (Amendment) Act 2021); its changes are among the unexplained ones, not on the Act\'s own date.',
        'Summary Jurisdiction (Appeals) Act Cap. 3:04: the L.R.O. 1/2012 PDF archived from mola.gov.gy already lists Act No. 13 of 2014 among the amending laws, so it cannot be dated 31 December 2012 (the Sexual Offences Act precedent); the Act starts with L.R.O. 1/2022 on 2022-12-31 as the oldest version available.',
        'Summary Jurisdiction (Procedure) Act Cap. 10:02: mola.gov.gy still serves L.R.O. 1/2012 (it lists Act No. 6 of 2012 and Order No. 5 of 2007 as the last amendments), so one version, 2012-12-31.',
    ],
    '75-family': COMMON_DECISIONS + [
        'Family law chapters (Domestic Violence Act Cap. 11:09, Wills Act Cap. 12:02, Family and Dependants Provision Act Cap. 12:24, Matrimonial Causes Act Cap. 45:02, Maintenance Act Cap. 45:03, Adoption of Children Act Cap. 46:04, Status of Children Act Cap. 46:05): mola.gov.gy still serves each in L.R.O. 1/2012, so each has one version, 2012-12-31.',
        'Not applied (scans without a text layer, no OCR): Act No. 8 of 2021 (Adoption of Children (Amendment) Act 2021, Official Gazette 9 August 2021), Act No. 13 of 2024 (Matrimonial Causes (Amendment) Act 2024, Official Gazette 27 August 2024), Act No. 21 of 2024 (Wills (Amendment) Act 2024, Official Gazette 27 December 2024). Which sections they amend and when they commence cannot be read, so they have no commit; the Acts here are the text of L.R.O. 1/2012, which is not the law in force on those points.',
        'Married Persons (Property) Act Cap. 45:04 was not added: its L.R.O. 1/2012 edition on mola.gov.gy already lists Acts No. 11 and 12 of 2014, so it cannot be dated 31 December 2012, and Act 12 of 2014 is not in the Parliament index. The Data Protection Act 2023 (Act No. 18 of 2023) is printed only as a scan and is in no revised edition, so it is not included.',
    ],
    '80-land': COMMON_DECISIONS + [
        'Land Registry Act Cap. 5:02: L.R.O. 1/2012 read from the Internet Archive capture of mola.gov.gy (22 June 2022) as the 2012-12-31 version; L.R.O. 1/2022 (today\'s chapter PDF on mola.gov.gy) is compared with it, and any difference is an unexplained change on 2022-12-31.',
        'Deeds Registry Act Cap. 5:01: the L.R.O. 1/2012 PDF archived from mola.gov.gy already lists Act No. 5 of 2014 among the amending laws, so it cannot be dated 31 December 2012; the Act starts with L.R.O. 1/2022 on 2022-12-31 as the oldest version available. (The mola.gov.gy index links Cap. 5:01 to the Deeds and Commercial Registries Authority Act and Cap. 5:11 to the Deeds Registry Act; the PDF used is the one whose front page reads "DEEDS REGISTRY ACT CHAPTER 5:01".)',
        'Title to Land (Prescription and Limitation) Act Cap. 60:02, Landlord and Tenant Act Cap. 61:01, State Lands Act Cap. 62:01 and Rent Restriction Act Cap. 36:23: mola.gov.gy still serves each in L.R.O. 1/2012, so each has one version, 2012-12-31.',
    ],
}

AI_USE = ['Corpus part {part}: Claude Code with Claude Opus 5.5 (claude-opus-5-5) wrote chapters_extra.py, chose the chapters and page ranges and read the amending-law lists from the front pages (by a word-position script, checked against the page); it did not write or alter any legal text.']


def sources(part: str, chs: list) -> list:
    caps = ', '.join(ch['cap'] for ch in chs)
    out = [{'name': f'Laws of Guyana, Ministry of Legal Affairs (chapter PDFs of Caps. {caps})',
            'url': 'https://www.mola.gov.gy/laws-of-guyana', 'retrieved': RETRIEVED, 'requests': len(chs),
            'licence': 'none stated', 'notes': 'L.R.O. 1/2022 for Vols. 1-3; L.R.O. 1/2012 still served for later volumes'}]
    arch = [ch for ch in chs if ch['kind'] in ('two', 'only2022')]
    if arch:
        out.append({'name': 'Internet Archive Wayback Machine (L.R.O. 1/2012 PDFs of Caps. '
                            + ', '.join(ch['cap'] for ch in arch) + ', mola.gov.gy/sites/default/files)',
                    'url': 'https://web.archive.org/', 'retrieved': RETRIEVED, 'requests': len(arch),
                    'licence': 'none stated',
                    'notes': 'captures of 22 June 2022, timestamps pinned in each version\'s source_url; the copies of '
                             'Caps. 3:04 and 5:01 were read only for their front pages (not used, see decisions)'})
    miss = [m for ch in chs for m in ch['missing']]
    if miss:
        out.append({'name': 'Acts of Parliament, Parliament of Guyana (' + ', '.join(m[1] for m in miss) + ')',
                    'url': 'https://parliament.gov.gy/publications/acts-of-parliament/', 'retrieved': RETRIEVED,
                    'requests': len(miss), 'licence': 'none stated',
                    'notes': 'scans without a text layer; dates read from the Gazette head printed on each page'})
    return out


def build(part: str) -> dict:
    chs = PARTS[part]
    return {'laws': laws(chs), 'acts': [act(ch) for ch in chs], 'sources': sources(part, chs), 'applies': [],
            'decisions': DECISIONS[part], 'ai_use': [a.format(part=part) for a in AI_USE]}


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
