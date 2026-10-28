"""PDF layout reader for Laws of Guyana editions (reads the cache only).

Turns one edition PDF into a list of paragraphs, each with its page, its text and the marginal notes printed beside
it. Marginal notes (the article's side heading and the "[N of YYYY]" amendment citations) are kept apart from the
body text. Publisher typesetting is normalised here once: quotes, dashes, spaces, line-end hyphenation.
"""
from __future__ import annotations

import re
import statistics
from dataclasses import dataclass, field

import fitz  # PyMuPDF

import fetch

RUNNING_RE = re.compile(r'^(\d+ )?(LAWS OF ?GUYANA|[A-Z][A-Za-z ()\-]+ Cap\. ?\d+ ?: ?\d+( \d+)?|Cap\. ?\d+ ?: ?\d+( [A-Z][A-Za-z ()\-]+)?)$')
FOOT_RE = re.compile(r'^\s*\d\s*/\s*2\s*0\s*\d\s*\d\s*$')
CITE_ONLY = re.compile(r'^\[[^\[\]]*\d{4}[^\[\]]*\]$')


@dataclass
class Para:
    page: int
    y: float
    x0: float
    text: str
    heading: bool = False          # centred, all capitals: a Part/Chapter/Title heading or a schedule heading
    margin: list[str] = field(default_factory=list)


# Per-edition character maps: the editions use different glyphs for the same quote mark.
QMAP_COMMON = {' ': ' ', '–': '-', '—': '-', '‒': '-', '…': '...', '“': '"', '”': '"',
               '’': "'", '‘': "'", '­': '', '\t': ' ', '•': '-'}
QMAPS = {
    # 2010 consolidation: U+201F and U+201E are apostrophes / single quotes ("Women‟s", "„discriminatory")
    'e2010': {'‟': "'", '„': "'"},
    # L.R.O. 1/2012: U+201A / U+201B are the double quotes (‚The Golden Arrow Head‛)
    'e2012': {'‚': '"', '‛': '"'},
    # L.R.O. 1/2022: a single U+201A is a comma ("paragraph‚ “the relevant")
    'e2022': {'‚': ','},
}


def norm(s: str, ed: str) -> str:
    for a, b in QMAP_COMMON.items():
        s = s.replace(a, b)
    for a, b in QMAPS.get(ed, {}).items():
        s = s.replace(a, b)
    s = re.sub(r'\s+', ' ', s)
    return s


def _spans(page) -> list[tuple]:
    out = []
    for bl in page.get_text('dict')['blocks']:
        for ln in bl.get('lines', []):
            for s in ln['spans']:
                if s['text'].strip():
                    x0, y0, x1, y1 = s['bbox']
                    out.append((x0, y0, x1, y1, s['size'], bool(s['flags'] & 16), s['text']))
    return out


def _rows(spans: list[tuple], tol: float = 3.0) -> list[list[tuple]]:
    """Group spans into printed lines by baseline. Superscripts ("25th") join the line they sit on."""
    big = sorted([s for s in spans if s[4] >= 8], key=lambda s: (s[3], s[0]))
    small = sorted([s for s in spans if s[4] < 8], key=lambda s: (s[3], s[0]))
    rows: list[list[tuple]] = []
    for s in big:
        for r in rows:
            if abs(r[0][3] - s[3]) <= tol:
                r.append(s)
                break
        else:
            rows.append([s])
    for s in small:
        mid = (s[1] + s[3]) / 2
        for r in rows:
            if min(x[1] for x in r) - 1 <= mid <= max(x[3] for x in r) + 1:
                r.append(s)
                break
        else:
            rows.append([s])
    for r in rows:
        r.sort(key=lambda s: s[0])
    rows.sort(key=lambda r: max(s[3] for s in r if s[4] >= 8) if any(s[4] >= 8 for s in r) else r[0][3])
    return rows


def _join(row: list[tuple]) -> str:
    out = ''
    prev = None
    for s in row:
        t = s[6]
        if prev is not None and s[0] - prev[2] > 1.0 and not out.endswith(' ') and not t.startswith(' '):
            out += ' '
        out += t
        prev = s
    return out


def read_edition(url: str, ed: str, first_page: int, last_page: int, body_min: float) -> list[Para]:
    """Paragraphs of pages first_page..last_page (0-based, inclusive). body_min: smallest body font size."""
    doc = fitz.open(stream=fetch.cached(url), filetype='pdf')
    rows_all = []   # (page, y, x0, text, size, bold, centred, is_margin)
    for pno in range(first_page, last_page + 1):
        page = doc[pno]
        W = page.rect.width
        spans = _spans(page)
        # running head: everything at or above the "Cap. 1:01" header line; running foot: the L.R.O. line
        # the running head's last line names the chapter ("Cap. 6:01"); its spans may be split word by word
        top = [s for s in spans if s[1] < 140]
        head_y = 100
        for r in _rows(top):
            if re.search(r'Cap\.\s*\d+\s*:\s*\d+', ' '.join(x[6] for x in r)):
                head_y = max(x[3] for x in r) + 2
        spans = [s for s in spans if s[1] > head_y and not re.match(r'\s*L\.\s?R\.\s?O\.', s[6])
                 and not FOOT_RE.match(s[6])]
        spans = [s for s in spans if not re.fullmatch(r'\s*_+\s*', s[6])]
        normal = [s for s in spans if s[4] >= body_min]
        if not normal:
            continue
        wordy = [s for s in normal if len(re.findall(r'[A-Za-z0-9]', s[6])) >= 2] or normal
        bl = min(s[0] for s in wordy)
        x1s = sorted(s[2] for s in normal)
        br = x1s[int(0.9 * (len(x1s) - 1))]   # the justified right edge (a few lines overrun it)
        body, margin = [], []
        for s in spans:
            if (s[4] < body_min or not re.search(r'[A-Za-z0-9]', s[6])) and (s[2] <= bl + 1.5 or s[0] >= br - 1.5 or s[2] > br + 20 or s[0] < bl - 20):
                margin.append(s)
            else:
                body.append(s)
        for r in _rows(body):
            text = norm(_join(r), ed).strip()
            if not text or RUNNING_RE.match(text):
                continue
            x0 = r[0][0]
            x1 = max(s[2] for s in r)
            y = max(s[3] for s in r)
            size = max(s[4] for s in r)
            bold = all(s[5] for s in r if s[6].strip())
            centred = abs((x0 + x1) / 2 - (bl + br) / 2) < 25 and x0 > bl + 20
            is_margin = bool(CITE_ONLY.match(text))
            rows_all.append((pno, y, x0, text, size, bold, centred, is_margin, x1, br))
        for r in _rows(margin):
            text = norm(_join(r), ed).strip()
            if text:
                rows_all.append((pno, max(s[3] for s in r), r[0][0], text, r[0][4], False, False, True, 0, 0))
    # line spacing of the edition: median gap between consecutive body rows on one page
    gaps = []
    body_rows = [r for r in rows_all if not r[7]]
    for a, b in zip(body_rows, body_rows[1:]):
        if a[0] == b[0] and 0 < b[1] - a[1] < 40:
            gaps.append(b[1] - a[1])
    line = statistics.median(gaps) if gaps else 14
    para_gap = line * 1.45
    # the continuation x of each page: the commonest left edge of body rows
    cont_x = {}
    for p in {r[0] for r in body_rows}:
        xs = [round(r[2]) for r in body_rows if r[0] == p]
        cont_x[p] = statistics.mode(xs)
    paras: list[Para] = []
    prev = None
    for r in body_rows:
        pno, y, x0, text, size, bold, centred, _, x1, br = r
        heading = centred and (_is_heading(text) or (bold and not _starts_item(text) and len(text) < 120))
        start = prev is None or heading or bool(paras and paras[-1].heading)
        if not start:
            # the previous row stopped short of the justified right edge: the paragraph may have ended there.
            # A row starting "(c)" after a full-width row is a cross-reference wrapped onto a new line, not an item.
            short = prev[8] < prev[9] - 15
            ended = prev[8] < prev[9] - 25 and prev[3].rstrip()[-1:] in '.;:-'
            pt = prev[3].rstrip()
            item = _starts_item(text) and (short or pt[-1:] in '.;:-' or re.search(r'[;,:] (or|and)$', pt) is not None)
            if pno == prev[0]:
                # a row well short of the right edge ends its paragraph when the next row starts a new sentence
                # (lists printed without spacing, such as the entities in the Third Schedule)
                listed = prev[8] < prev[9] - 40 and text[:1].isupper() and not pt.endswith(',')
                start = y - prev[1] > para_gap or item or listed
            else:
                # a new page: a new paragraph only if the previous page's last row ended one
                start = item or ended
        if start:
            paras.append(Para(pno, y, x0, text, heading))
        else:
            paras[-1].text = _hyph_join(paras[-1].text, text)
        prev = r
    # marginal notes: attach each margin row to the paragraph whose first row is nearest on the same page,
    # preferring the paragraph that starts at or after it (side headings sit level with an article's first line)
    for r in rows_all:
        if not r[7]:
            continue
        pno, y = r[0], r[1]
        cands = [p for p in paras if p.page == pno]
        if not cands:
            cands = [p for p in paras if p.page > pno][:1] or [paras[-1]]
            cands[0].margin.append(r[3])
            continue
        # the paragraph covering y: last paragraph starting at or before y + 6
        before = [p for p in cands if p.y <= y + 6]
        tgt = before[-1] if before else cands[0]
        tgt.margin.append(r[3])
    for p in paras:
        p.text = re.sub(r'\s+', ' ', p.text).strip()
    return paras


HEAD_RE = re.compile(r"^[A-Z0-9 ,.'\-()&:;\"]+$")


def _is_heading(t: str) -> bool:
    t = t.replace(' etc.', '')
    letters = [c for c in t if c.isalpha()]
    return bool(letters) and HEAD_RE.match(t) is not None and not re.match(r'^\(?\d+[A-Z]*\)?\s*\.', t)


ITEM_RE = re.compile(r'^(\(\d+[A-Za-z]*\)|\([a-z]{1,2}\)|\((?:i|ii|iii|iv|v|vi|vii|viii|ix|x|xi|xii)\)|\((?:i|ii|iii|iv|v|vi|vii|viii|ix|x|xi|xii)a?\)|\d{1,3}[A-Z]{0,2}\s?\.\s?(?=[A-Z(\[])|"[A-Za-z])')


def _starts_item(t: str) -> bool:
    return bool(ITEM_RE.match(t))


HYPHEN_WORDS: set[str] = set()   # filled by parse.py with words seen unhyphenated, to undo line-end splits


def _hyph_join(a: str, b: str) -> str:
    a = a.rstrip()
    if a.endswith('-') and not a.endswith(' -') and b[:1].isalpha():
        # line-end hyphen: keep it, and mark the join so parse.py can decide once the vocabulary is known
        return a + '⁠' + b
    return a + ' ' + b
