# How this repository was made (Guyana)

This file is written by the build on 2026-10-28, the day the source data was retrieved. Everything below is enough to rebuild this repository hash for hash.

## Sources

| Source | Address | Retrieved | Requests | Licence |
| --- | --- | --- | ---: | --- |
| Laws of Guyana, Ministry of Legal Affairs (L.R.O. 1/2022) | <https://www.mola.gov.gy/laws-of-guyana> | 2026-10-28 | 56 | none stated |
| Acts of Parliament, Parliament of Guyana | <https://parliament.gov.gy/publications/acts-of-parliament/> | 2026-10-28 | 209 | none stated |
| Internet Archive Wayback Machine (earlier editions of Cap. 1:01) | <https://web.archive.org/> | 2026-10-28 | 12 | none stated |

Every response is cached by the sha256 of its URL, and the table above lists every source with its retrieval date. Lexifina keeps its fetch scripts privately; `tools/parse.py` reads only the cache and writes `corpus.json`, so the same cache always gives the same corpus.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `constitution` | Constitution of the Co-operative Republic of Guyana | 6 | 2007-08-28 to 2022-12-31 |

The build made 6 commits:

| Commits | Kind |
| ---: | --- |
| 1 | first version of an act |
| 3 | one law on its in-force day |
| 2 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `futuro`: laws not yet in force on 2026-10-28.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 30 laws in the record.
- 9 tags.

## Dates

Each commit is dated at noon (America/Guyana) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: Interpretation and General Clauses Act, Cap. 2:01, s. 15: "Every Act shall be published in the Gazette and shall come into operation on the date of publication unless it is provided in that Act or some other written law that it shall come into operation on some other date." https://www.mola.gov.gy/laws/Volume 1 Cap. 1.01 - 3.041785164106.pdf

## Commands, in order

```sh
# fill the cache from the sources listed above (network; Lexifina's fetch scripts are kept privately)
python -X utf8 tools/parse.py                  # cache -> corpus.json (no network)
python -X utf8 tools/build.py <folder> --repo <empty folder> --docs-date 2026-10-28
python -X utf8 tools/check_repo.py <repo> --corpus <folder>/corpus.json --write
python -X utf8 tools/build.py <folder> --repo <another empty folder> --docs-date 2026-10-28 --compare <repo>
```

In the main Lexifina repository these files live as follows:
- `fetch.py`, `parse.py` and `repo/`: in `scripts/guyana-law/`.
- `build.py`, `check_repo.py` (`check.py` there) and `on.py`: in `scripts/gitlaw_common/`, with the corpus format in `SCHEMA.md`.

## Exact inputs

- `corpus.json` sha256 `5881baa77bcf546ea77c2f2bdf1448107814ef73ee70dbe7701436a07231efd6` (2018200 bytes)
- Script blob hashes (`git hash-object`):

| Script | Blob |
| --- | --- |
| build.py | `727357e12b2533e202258d8bf11c2b5d869ca8f6` |
| check.py | `0f457d2b473ba31682d0c0b32e9dcad30e613895` |
| on.py | `644a6c0857fbcc72562032b58d57aa113fee0641` |
| fetch.py | `1ec4ccc430a57c8e89e09c8975255ebfef444586` |
| parse.py | `d993a7ea701f130c8dfaebbc7691f17b4f7dd575` |

- Tools:
  - Python 3.14.0
  - git version 2.52.0.windows.1
  - curl 8.21.0 (Windows) libcurl/8.21.0 Schannel zlib/1.3.2 WinIDN WinLDAP

## Checks

6 versions of 1 acts read back from git on the day each took effect and on the day before: 0 mismatches. Trailers: 0 commits whose trailers git cannot parse. Health: 0 merge commits on main, 0 commit dates that go backwards, 0 commits dated after the build.

Not yet run for this build.

These results are from the check run on the build before this one, from the same corpus.

## Decisions made by hand

- Constitution: no dated versions are published, and the Act of 1980 as enacted and five amending laws (1, 12, 35, 36 of 1991; 5 of 2003; Order 38 of 1987) are not online, so the history starts at the oldest consolidation available (the 2010 consolidation, which includes Act 22 of 2007) and is replayed forward from the Acts as published in the Gazette and the two revised editions (L.R.O. 1/2012 and 1/2022).
- In-force dates follow the Interpretation and General Clauses Act, Cap. 2:01, s. 15: an Act comes into operation on the day it is published in the Gazette unless it says otherwise. Acts 5 of 2009, 2 of 2015 and 1 of 2016 name no other day, so their Gazette dates are used, read from the Gazette print itself (the Parliament index dates are wrong for some Acts).
- A revised edition is dated by the day it states its text as at: 31 December 2012 for L.R.O. 1/2012 and 31 December 2022 for L.R.O. 1/2022 (Ministry of Legal Affairs; Law Revision Act, Cap. 2:02, s. 9: the authorised pages are the Statute Book as in force on the relevant revision date). The dates of the Law Revision Orders themselves were not found.
- Differences between consecutive editions that no Act explains are committed by the publisher as "unexplained": the gender-neutral rewrite and corrections of L.R.O. 1/2012 (for example art. 1 "Referendum to Republic" in the 2010 consolidation, "Co-operative Republic" from 2012), and the revision edits of L.R.O. 1/2022.
- Article 119D (Act 5 of 2009) is in the words of the Gazette print: it says "a Standing Committee" and "To assist it in its work", where both revised editions print "a standing Committee" and "To assist in its work". The text is taken from L.R.O. 1/2012 with those two words restored, each checked against the Gazette OCR text in parse.py; the 2012 edition's wording then shows as an unexplained change.
- Act 2 of 2015 and Act 1 of 2016 add entities to the Third Schedule; the added lines are in the words of each Act ("The Office of the Ombudsman", "The Parliament Office"). L.R.O. 1/2022 prints them as "The office of the Ombudsman" and "The Parliament office.", which shows as an unexplained change on 2022-12-31.
- Act 24 of 2006 (Gazette 2 May 2006) made article 61 apply to the Eighth Parliament as if "four months" stood for "three months" without changing its words. It predates the oldest version available, so it has no commit; it is listed with the earlier laws.
- Marginal notes (the side headings and "[N of YYYY]" citations) are left out of the text. Cap. 2:01 s. 57(3) makes marginal notes part of the written law, but the 2010 consolidation prints them interleaved with the text, so they cannot be extracted reliably for every version. Each file starts with "# Article N" instead.
- Part, Chapter and Title headings are left out: they are structure, not text of an article. Articles printed only as a repeal note ("[Article 11 repealed by Act No. 10 of 2003]") have no file, since nothing of them is in force. Repeal notes inside an article are kept as printed.
- In the schedules, the side reference printed under the heading ("Article 222A") is left out, and list entries that the 2010 and 2012 PDFs print run together on one line are split one per line.
- Typesetting is normalised in layout.py and parse.py: one form of quotes (the 2010 PDF uses U+201F as an apostrophe, the 2012 PDF U+201A/U+201B as double quotes, and the 2022 PDF one U+201A as a comma), dashes as "-", "..." for leaders, one space, "(3) (a)" as "(3)(a)" and "60 (2)" as "60(2)", and line-end hyphens removed only when the unhyphenated word occurs elsewhere in the three editions. Words that the 2010 PDF prints without spaces ("performthefunctions") are split into words that occur in at least two editions.
- Images in the Second Schedule (flag, coat of arms) are not text and are not reproduced.

## What AI did and did not do

The fetch, parse and check scripts were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above, through code that anyone can rerun.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- Claude Code with Claude Opus 5.5 (claude-opus-5-5) wrote fetch.py, sources.py, layout.py and parse.py and chose the sources and editions; it did not write or alter any legal text. parse.py is deterministic and runs no model; every line of law comes from an official PDF in the cache.
