# Guyana: law history in git

The law of Guyana as a git history: one file per provision, one commit per law on the day it took effect, and the law that made each change as the commit's author. `git blame` names the law behind every paragraph; `git log` lists every change to an article; the tool below gives the text in force on any day.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `gy/`.

**What is in it now**

| Folder | Act | Versions | History |
| --- | --- | ---: | --- |
| `constitution/` | Constitution of the Co-operative Republic of Guyana (Cap. 1:01, Act 2 of 1980) | 6 | From the oldest consolidation online (in force 28 August 2007) to the 2022 revised edition, today's official text |
| `civil-law/` | Civil Law of Guyana Act (Cap. 6:01, Act 15 of 1916) | 1 | The revised edition L.R.O. 1/2012; the 2022 edition prints the same text. **Section 5(1)(b) is not current:** see below |
| `criminal-law-offences/` | Criminal Law (Offences) Act (Cap. 8:01, Act 18 of 1893) | 2 | The revised editions L.R.O. 1/2012 and 1/2022 |

The Constitution's six versions:

| In force | Version | Author |
| --- | --- | --- |
| 2007-08-28 | The 2010 consolidation of Cap. 1:01 (Ministry of Legal Affairs), which includes Act 22 of 2007 | publisher: oldest version available |
| 2009-03-17 | Article 119D inserted (Parliamentary Oversight Committee on the Security Sector) | Act No. 5 of 2009 |
| 2012-12-31 | Revised edition L.R.O. 1/2012: gender-neutral rewrite and corrections | publisher: unexplained |
| 2015-07-10 | Nine entities added to the Third Schedule (financial autonomy, art. 222A) | Act No. 2 of 2015 |
| 2016-01-11 | The Parliament Office added to the Third Schedule | Act No. 1 of 2016 |
| 2022-12-31 | Revised edition L.R.O. 1/2022: revision edits | publisher: unexplained |

Each folder's `README.md` lists every provision, how often it changed and when.

**Civil Law Act, section 5(1)(b).** Act No. 12 of 2021 (Civil Law of Guyana (Amendment) Act 2021, Official Gazette 11 August 2021) substituted section 5(1)(b) (intestate succession where there are no descendants). The 2022 revised edition does not include it, and the Gazette print of the Act is a scan with no text layer, so its words are not in this repository: `civil-law/sec-005.md` shows paragraph (b) as it stood before 11 August 2021.

## A lawyer's questions as git commands

| Question | Command |
| --- | --- |
| What did art. 7 say on 1 January 2010? | `python tools/in_force_on.py 2010-01-01 constitution 7` |
| Section 5 of the Civil Law Act, or s. 100 of the Criminal Law (Offences) Act, today | `python tools/in_force_on.py 2026-10-28 civil-law 5` |
| The same, with raw git (bash) | `git show $(git rev-list -1 --before="2010-01-01T23:59:59Z" main -- constitution/art-007.md):constitution/art-007.md` |
| The same, in PowerShell | `$r = git rev-list -1 --before="2010-01-01T23:59:59Z" main -- constitution/art-007.md; git show "$($r):constitution/art-007.md"` |
| Which law wrote each line of the Third Schedule? | `git blame constitution/sch-3.md` |
| Every change to art. 7, word by word | `git log -p --word-diff constitution/art-007.md` |
| Every law in the record, in order | `git log --reverse --format="%ad %an" --date=short main` |
| Everything one Act changed | `git show law/act-5-2009` (tags `law/<key>` mark each law's commit) |
| The whole Constitution on a date | `python tools/in_force_on.py 2010-01-01 constitution` |
| Which law gave a provision its wording on a date | `python tools/in_force_on.py --law 2016-01-11 constitution sch-3` |

After a rebuild, refresh tags with `git fetch --force --tags`: a plain fetch keeps stale tags.

## Dates

- Each commit is dated at **noon, America/Guyana, on the day the change took effect**. The in-force day is also in the `In-force:` trailer, which the tools read; publication dates are trailers too.
- **Default rule.** Interpretation and General Clauses Act, Cap. 2:01, s. 15: "Every Act shall be published in the Gazette and shall come into operation on the date of publication unless it is provided in that Act or some other written law that it shall come into operation on some other date." Acts 5 of 2009, 2 of 2015 and 1 of 2016 name no other day, so each is dated by its Gazette issue, read from the Gazette print (17 March 2009, 10 July 2015, 11 January 2016). The Parliament website's own index dates are wrong for some Acts and are not used.
- **Revised editions.** Under the Law Revision Act, Cap. 2:02, s. 9, the pages authorised by a Law Revision Order are "the sole and proper Statute Book of Guyana ... as in force on the relevant revision date". The Ministry of Legal Affairs gives that date as 31 December 2012 for L.R.O. 1/2012 and 31 December 2022 for L.R.O. 1/2022, and those are the dates used. The dates of the Orders themselves were not found.
- `--before="YYYY-MM-DD"` alone uses your clock's time of day, so a law that took effect that day may be missed before noon. Use `T23:59:59Z` as above, or the tool.

## How it is checked

- Every version is read back from git on the day it took effect and on the day before (`tools/check_repo.py`); both must match `corpus.json`. Results are in `REPRODUCE.md`.
- Health checks: no merge commits on `main`, commit dates never go backwards, nothing dated in the future, and every commit's trailers parse with `git interpret-trailers --parse`.
- **Against the official text today** (`tools/verify.py`): for each act, every word of the latest version is printed in the official L.R.O. 1/2022 PDF on mola.gov.gy, and every word that PDF prints for the act is in the repository, except what is left out on purpose (running heads, marginal notes, long titles, Part/Chapter/Title headings and repeal-only notes). On 2026-10-28: 0 words added in all three acts; 0 words unaccounted for in the Civil Law Act and the Criminal Law (Offences) Act, and 4 (side references) in the Constitution. `verify.py --older` runs the same check on the L.R.O. 1/2012 versions (0 words added; the only words unaccounted for are editor's notes and headings). Every version carries the sha256 of the PDF it was parsed from.
- The words the Acts added were checked against the Gazette print: Article 119D (Act 5 of 2009, a scan with an OCR text layer) and the Third Schedule entries (Acts 2 of 2015 and 1 of 2016).
- The repository is rebuilt from the same data a second time and must give identical hashes.

## What "author" means

The author of a commit is the law that made the change, with an e-mail address that cannot exist (`act-5-2009@lawsofguyana.invalid`), so `git blame` and `git log --author` name laws. The committer is always Lexifina.

- **The first commit** is the oldest text available, credited to the publisher, and names the 27 laws that produced it: the Act of 1980 and every amendment the Laws of Guyana list up to Act 22 of 2007.
- **Credits come only from the sources.** The three later Acts are credited because each one's own text inserts exactly the words that appear.
- **Unexplained changes** are committed by the publisher, the Ministry of Legal Affairs, and labelled "unexplained". They are the revised editions' own changes, which the Law Revision Act allows (s. 11: correcting errors, shortening phrasing, formal alterations): in 2012 the Constitution was rewritten in gender-neutral terms ("he" became "he or she"; 137 provisions changed in all, along with corrections such as art. 1, which the 2010 consolidation misprinted as "the Referendum to Republic of Guyana"); in 2022, 61 provisions changed (for example "office of President" became "office of the President", and "offense" became "offence"). Both editions also differ from the Acts in small ways, which therefore show as unexplained too. Article 119D says "a Standing Committee" and "To assist it in its work" in the Gazette, and "a standing Committee" and "To assist in its work" in both editions.
- Blame credits whole lines (one paragraph per line). Use `git log -p --word-diff` to see exactly which words each change made.

## What it does not show

- **No history before 2007.** The Act of 1980 as enacted is not online, nor are five amending laws (Acts 1, 12, 35 and 36 of 1991, Act 5 of 2003) and Order 38 of 1987, so the Constitution's history before the 2010 consolidation cannot be rebuilt. It starts at the oldest consolidation online.
- **Act 24 of 2006** made article 61 apply to the Eighth Parliament as if "four months" stood for "three months", without changing its words. It predates the oldest version, so it has no commit.
- **Marginal notes are not included.** Cap. 2:01, s. 57(3) makes marginal notes part of the written law, but the 2010 consolidation prints them run into the text, so they could not be extracted reliably for every version. Each file starts with `# Article N` instead.
- **Headings and repealed articles.** Part, Chapter and Title headings are left out. Articles printed only as a repeal note ("[Article 11 repealed by Act No. 10 of 2003]") have no file; repeal notes inside an article are kept as printed.
- **Images.** The flag and the coat of arms in the Second Schedule are images and are not reproduced.
- **The 2010 consolidation** is a PDF with irregular spacing; parse.py splits words it prints run together only into words found in the later editions.
- **Civil Law Act and Criminal Law (Offences) Act before 2012.** Only the revised editions of 2012 and 2022 are online, so each starts at 31 December 2012 as "oldest version available" and names the laws its front page lists. Their changes between 2012 and 2022 are revision edits that no Act explains (the 2022 edition of Cap. 8:01 lists no amending Act after 2010).
- **Acts printed as scans.** Act 12 of 2021 (Civil Law), the Data Protection Act 2023 (Act 18 of 2023) and the Criminal Law Miscellaneous Act, Act 10 of 2025, exist only as scanned Gazette pages with no text layer. Recent Acts on the Parliament website are often scans, which is why the Data Protection Act is not here. They are not applied: no model may write legal text here.
- **Other acts.** Only these three acts are here so far. The Laws of Guyana publish only the current revised edition of each chapter, and the Parliament website holds Acts as passed from 1928 (with gaps), so other acts need the same edition-and-replay work.

## How it is built

`tools/fetch.py` downloads each source once with curl into a cache named by the sha256 of the URL (1 request per second per host). `tools/layout.py` reads each PDF's text layer with PyMuPDF and separates the text from running heads and marginal notes by position and font size; `tools/parse.py` splits it into provisions, normalises typesetting, replays the Acts and writes `corpus.json`; the shared builder `tools/build.py` turns that into the commits. `REPRODUCE.md` lists every source, command, tool version and decision, and the result of the hash-for-hash rebuild.

## Sources

| Source | What it gives | Used for |
| --- | --- | --- |
| [Laws of Guyana](https://www.mola.gov.gy/laws-of-guyana), Ministry of Legal Affairs | The current revised edition (L.R.O. 1/2022), one PDF per chapter, with a list of amending laws per chapter and "[N of YYYY]" marginal citations | Today's text |
| [Acts of Parliament](https://parliament.gov.gy/publications/acts-of-parliament/), Parliament of Guyana | Acts as published in the Official Gazette, 1928-2025 (1977-1980, 1991 and 2002 missing) | The amending Acts and their Gazette dates |
| [Internet Archive](https://web.archive.org/) | The 2010 consolidation of Cap. 1:01 (legalaffairs.gov.gy, captured 26 December 2012) and L.R.O. 1/2012 (captured 19 January 2016, 4 April 2021 and 8 March 2022, byte-identical) | The earlier versions |
| [Official Gazette](https://officialgazette.gov.gy/) | The Gazette | Not used yet |

## Licence

See [LICENSE](LICENSE). The legal texts are official publications of Guyana, which state no licence; Lexifina's arrangement, messages, tables and tools are CC0.

This repository is not legal advice. Guyana's official language is English, so there is no separate summary in another language.
