"""Two official Constitution amendment instruments, as separate historical acts.

Reads official PDF bytes only; does not replay changes into any existing act.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path
import pymupdf

HERE = Path(__file__).resolve().parent
PART = '90-constitution-instruments'
SOURCES = [
    (2015, 2, '2015-07-10', 'https://www.parliament.gov.gy/documents/acts/4034-4034-act_no._2_of_2015_(1).pdf'),
    (2016, 1, '2016-01-11', 'https://www.parliament.gov.gy/documents/acts/5713-act_no._1_of_2016.pdf'),
]


def build(cache):
    acts = []
    for year, number, day, url in SOURCES:
        raw = (cache / hashlib.sha256(url.encode()).hexdigest()).read_bytes()
        doc = pymupdf.open(stream=raw, filetype='pdf')
        assert len(doc) == 2
        page = doc[1].get_text()
        body = re.search(r'Enacted by the Parliament of Guyana:-\s*(.*?)\s*Passed by the National Assembly', page, re.S).group(1)
        notes = re.search(r'(Short title\..*?)\s*Enacted by the Parliament', page, re.S).group(1)
        captions = re.split(r'(?=Amendment of)', notes.strip())
        captions = [' '.join(s.split()) for s in captions if s.strip()]
        assert len(captions) == 2
        sections = list(re.finditer(r'(?:^|\n)\s*([12])\.\s+', body))
        assert [m.group(1) for m in sections] == ['1', '2']
        units = {}
        for i, m in enumerate(sections):
            stop = sections[i + 1].start() if i + 1 < len(sections) else len(body)
            paragraphs = [' '.join(p.split()) for p in re.split(r'\n[ \t]*\n', body[m.start():stop]) if p.strip()]
            n = int(m.group(1))
            assert len(paragraphs) == (10 if year == 2015 and n == 2 else 1)
            text = '\n'.join([captions[i], *paragraphs])
            units[f'sec-{n:03d}'] = {'label': f'Section {n}', 'kind': 'sec', 'text': f'# Section {n}\n{text}\n'}
        acts.append({'slug': f'constitution-amendment-{year}', 'short': f'Act {number} of {year}',
            'title': f'Constitution (Amendment) Act {year}', 'url': url, 'first_law': None, 'earlier_laws': [],
            'publisher': {'name': 'Parliament of Guyana', 'email': 'parliament@parliament.gov.gy.invalid'},
            'versions': [{'from': day, 'source_url': url, 'sha256': hashlib.sha256(raw).hexdigest(),
                'units': units, 'credits': {}, 'note': 'Oldest version available: the official Gazette instrument as enacted.'}]})
    return {'laws': {}, 'acts': acts, 'sources': [{'name': 'Parliament of Guyana: official Gazette Constitution amendment instruments',
        'url': 'https://parliament.gov.gy/publications/acts-of-parliament/', 'retrieved': '2026-11-03',
        'licence': 'Official legal texts; no reuse licence stated on the publisher homepage.',
        'notes': 'Acts 2 of 2015 and 1 of 2016, each with two sections.'}], 'applies': [],
        'decisions': [
            'Acts 2 of 2015 and 1 of 2016 are represented as separate historical amendment instruments, each with two section files. They do not replace any Constitution version.',
            'In-force dates are 10 July 2015 and 11 January 2016, printed on each official Gazette cover. Section 1 of each instrument gives its short title and no special commencement; the publication default in Interpretation and General Clauses Act section 15 applies. The Parliament listing dates differ and are not used.',
            'Section wording, numbers and marginal captions are preserved from the official PDF text layer; marginal notes form part of the written law under Interpretation and General Clauses Act section 57(3). Each body paragraph or entity item has its own line. Only Gazette running headers, arrangement, long title, enacting formula and certification are outside these section files.',
        ], 'ai_use': ['GPT-6 wrote the parser and validation code, selected two official instruments and inspected their page images. It did not write or amend legal wording.']}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--cache', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    c = build(args.cache)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(c, ensure_ascii=False, indent=1) + '\n', encoding='utf-8', newline='\n')
    print(f'{len(c["acts"])} acts, {sum(len(a["versions"]) for a in c["acts"])} versions')


if __name__ == '__main__':
    main()
