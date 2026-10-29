# Guyana: law history in git

The law of Guyana as a git history: one file per provision, one commit per law on the day it took effect, and the law that made each change as the commit's author. `git blame` names the law behind every paragraph; `git log` lists every change to an article; the tool below gives the text in force on any day.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `gy/`.

**What is in it now**

| Folder | Act | Versions | History |
| --- | --- | ---: | --- |
| `constitution/` | Constitution of the Co-operative Republic of Guyana (Cap. 1:01, Act 2 of 1980) | 6 | From the oldest consolidation online (in force 28 August 2007) to the 2022 revised edition, today's official text |
| `civil-law/` | Civil Law of Guyana Act (Cap. 6:01, Act 15 of 1916) | 1 | The revised edition L.R.O. 1/2012; the 2022 edition prints the same text. **Section 5(1)(b) is not current:** see below |
| `criminal-law-offences/` | Criminal Law (Offences) Act (Cap. 8:01, Act 18 of 1893) | 2 | The revised editions L.R.O. 1/2012 and 1/2022 |
| `criminal-law-procedure/` | Criminal Law (Procedure) Act (Cap. 10:01, Act 19 of 1893) | 1 | The revised edition L.R.O. 1/2012, which mola.gov.gy still serves as the current chapter. **Acts 4 of 2023 and 11 of 2024 are not applied:** see below |
| `high-court/` | High Court Act (Cap. 3:02, Act 10 of 1915) | 2 | The revised editions L.R.O. 1/2012 and 1/2022 |
| `labour/` | Labour Act (Cap. 98:01, Act 2 of 1942) | 1 | The revised edition L.R.O. 1/2012, which mola.gov.gy still serves as the current chapter |
| `evidence/` | Evidence Act (Cap. 5:03, Act 20 of 1893) | 2 | The revised editions L.R.O. 1/2012 and 1/2022 (the 2022 edition includes Acts 1 of 2014, 13 of 2018 and 15 of 2021, committed as unexplained) |
| `limitation/` | Limitation Act (Cap. 7:02, Act 1 of 1856) | 1 | The revised edition L.R.O. 1/2012; the 2022 edition prints the same text |
| `defamation/` | Defamation Act (Cap. 6:03, Act 17 of 1959) | 2 | The revised editions L.R.O. 1/2012 and 1/2022 |
| `interpretation/` | Interpretation and General Clauses Act (Cap. 2:01, Act 8 of 1970) | 1 | The revised edition L.R.O. 1/2012; the 2022 edition prints the same text |
| `companies/` | Companies Act (Cap. 89:01, Act 29 of 1991) | 1 | The revised edition L.R.O. 1/2012, which mola.gov.gy still serves as the current chapter (sections 1-285 and 305-540, six schedules) |
| `summary-jurisdiction-appeals/` | Summary Jurisdiction (Appeals) Act (Cap. 3:04, Act 6 of 1929) | 1 | The revised edition L.R.O. 1/2022 (the archived 2012 edition already lists Act 13 of 2014, so it cannot be dated) |
| `summary-jurisdiction-magistrates/` | Summary Jurisdiction (Magistrates) Act (Cap. 3:05, Act 10 of 1893) | 1 | The revised edition L.R.O. 1/2012; the 2022 edition prints the same text |
| `summary-jurisdiction-petty-debt/` | Summary Jurisdiction (Petty Debt) Act (Cap. 7:01, Act 11 of 1893) | 1 | The revised edition L.R.O. 1/2012; the 2022 edition prints the same text |
| `summary-jurisdiction-procedure/` | Summary Jurisdiction (Procedure) Act (Cap. 10:02, Act 12 of 1893) | 1 | The revised edition L.R.O. 1/2012, which mola.gov.gy still serves as the current chapter |
| `domestic-violence/` | Domestic Violence Act (Cap. 11:09, Act 18 of 1996) | 1 | The revised edition L.R.O. 1/2012, which mola.gov.gy still serves as the current chapter |
| `wills/` | Wills Act (Cap. 12:02, Act 12 of 1906) | 1 | The revised edition L.R.O. 1/2012, still served as current. **Act 21 of 2024 is not applied:** see below |
| `family-dependants-provision/` | Family and Dependants Provision Act (Cap. 12:24, Act 22 of 1990) | 1 | The revised edition L.R.O. 1/2012, which mola.gov.gy still serves as the current chapter |
| `matrimonial-causes/` | Matrimonial Causes Act (Cap. 45:02, Act 34 of 1919) | 1 | The revised edition L.R.O. 1/2012, still served as current. **Act 13 of 2024 is not applied:** see below |
| `maintenance/` | Maintenance Act (Cap. 45:03, Act 14 of 1903) | 1 | The revised edition L.R.O. 1/2012, which mola.gov.gy still serves as the current chapter |
| `status-of-children/` | Status of Children Act (Cap. 46:05, Act 19 of 2009) | 1 | The revised edition L.R.O. 1/2012, which mola.gov.gy still serves as the current chapter |
| `deeds-registry/` | Deeds Registry Act (Cap. 5:01, Act 17 of 1919) | 1 | The revised edition L.R.O. 1/2022 (the archived 2012 edition already lists Act 5 of 2014, so it cannot be dated) |
| `land-registry/` | Land Registry Act (Cap. 5:02, Act 18 of 1959) | 1 | The revised edition L.R.O. 1/2012; the 2022 edition prints the same text |
| `title-to-land/` | Title to Land (Prescription and Limitation) Act (Cap. 60:02, Act 62 of 1952) | 1 | The revised edition L.R.O. 1/2012, which mola.gov.gy still serves as the current chapter |
| `landlord-and-tenant/` | Landlord and Tenant Act (Cap. 61:01, Act 26 of 1947) | 1 | The revised edition L.R.O. 1/2012, which mola.gov.gy still serves as the current chapter |
| `state-lands/` | State Lands Act (Cap. 62:01, Act 32 of 1903) | 1 | The revised edition L.R.O. 1/2012, which mola.gov.gy still serves as the current chapter |
| `rent-restriction/` | Rent Restriction Act (Cap. 36:23, Act 23 of 1941) | 1 | The revised edition L.R.O. 1/2012, which mola.gov.gy still serves as the current chapter |
| `partnership/` | Partnership Act (Cap. 89:02, Act 20 of 1900) | 1 | The revised edition L.R.O. 1/2012, which mola.gov.gy still serves as the current chapter |
| `merchandise-marks/` | Merchandise Marks Act (Cap. 90:04, Act 2 of 1888) | 1 | The revised edition L.R.O. 1/2012, which mola.gov.gy still serves as the current chapter |
| `business-names/` | Business Names (Registration) Act (Cap. 90:05, Act 11 of 1919) | 1 | The revised edition L.R.O. 1/2012, which mola.gov.gy still serves as the current chapter |
| `sale-of-goods/` | Sale of Goods Act (Cap. 90:10, Act 26 of 1913) | 1 | The revised edition L.R.O. 1/2012, which mola.gov.gy still serves as the current chapter |
| `pledge-of-goods/` | Pledge of Goods Act (Cap. 90:11, Act 12 of 1916) | 1 | The revised edition L.R.O. 1/2012, which mola.gov.gy still serves as the current chapter |
| `bills-of-sale/` | Bills of Sale Act (Cap. 90:12, Act 22 of 1916) | 1 | The revised edition L.R.O. 1/2012, which mola.gov.gy still serves as the current chapter |
| `bills-of-exchange/` | Bills of Exchange Act (Cap. 90:13, Act 13 of 1891) | 1 | The revised edition L.R.O. 1/2012, which mola.gov.gy still serves as the current chapter |
| `traders-breach-of-contract/` | Traders (Breach of Contract) Act (Cap. 91:03, Act 4 of 1861) | 1 | The revised edition L.R.O. 1/2012, which mola.gov.gy still serves as the current chapter |
| `termination-of-employment/` | Termination of Employment and Severance Pay Act (Cap. 96:01, Act 19 of 1997) | 1 | The revised edition L.R.O. 1/2012, which mola.gov.gy still serves as the current chapter |

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
- **Against the official text today**: for each act, every word of the latest version is printed in the official L.R.O. 1/2022 PDF on mola.gov.gy, and every word that PDF prints for the act is in the repository, except what is left out on purpose (running heads, marginal notes, long titles, Part/Chapter/Title headings and repeal-only notes). On 2026-10-28: 0 words added in all three acts; 0 words unaccounted for in the Civil Law Act and the Criminal Law (Offences) Act, and 4 (side references) in the Constitution. The further chapters are checked the same way by `tools/verify_chapters.py` against the PDF mola.gov.gy serves today (2026-10-29: 0 words added in all eight; 0 unaccounted in Caps. 3:02, 6:03, 7:02, 89:01 and 98:01, 4 chapter-title words in Cap. 10:01, 3 side-reference words in Cap. 5:03 and 2 heading words in Cap. 2:01). The sixteen chapters added on 2026-10-29 in `a separate part of the corpus`, `75-family.json` and `80-land.json` pass the same check against today's mola.gov.gy PDF: 0 words added in all sixteen; the only words unaccounted for are the chapter title on the arrangement page (3 to 8 words) and side references ("Ed", "c"). The nine commercial and employment chapters in `a separate part of the corpus` (2026-10-29) pass it too: 0 words added in all nine; unaccounted only chapter titles and running heads (0 to 8 words) and the side note of s. 16 of Cap. 90:10, and every section listed in each arrangement of sections is present. Lexifina's code --older` runs the same check on the L.R.O. 1/2012 versions (0 words added; the only words unaccounted for are editor's notes and headings). Every version carries the sha256 of the PDF it was parsed from.
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
- **The 2010 consolidation** is a PDF with irregular spacing; Lexifina's code splits words it prints run together only into words found in the later editions.
- **Civil Law Act and Criminal Law (Offences) Act before 2012.** Only the revised editions of 2012 and 2022 are online, so each starts at 31 December 2012 as "oldest version available" and names the laws its front page lists. Their changes between 2012 and 2022 are revision edits that no Act explains (the 2022 edition of Cap. 8:01 lists no amending Act after 2010).
- **Acts printed as scans.** Act 12 of 2021 (Civil Law), the Data Protection Act 2023 (Act 18 of 2023) and the Criminal Law Miscellaneous Act, Act 10 of 2025, exist only as scanned Gazette pages with no text layer. Recent Acts on the Parliament website are often scans, which is why the Data Protection Act is not here. They are not applied: no model may write legal text here.
- **Criminal Law (Procedure) Act, High Court Act and Labour Act** start at 31 December 2012 (L.R.O. 1/2012, read from the Internet Archive) like the two acts above. For Caps. 10:01 and 98:01 the Ministry of Legal Affairs still serves the 2012 edition as the current chapter, so they have one version. The italic cross-headings between sections ("Gaol Delivery") are left out like Part headings; this applies to every act with sections, including five in the Criminal Law (Offences) Act ("Conspiracy", "Injury to Growing Things", "False Pretences", "Counterfeiting Coin", "Supplemental Provisions"), which until 29 October 2026 were printed as the last line of the section before them. The 2022 edition of Cap. 3:02 includes Act 9 of 2013; its changes are committed as unexplained on 31 December 2022.
- **Criminal Law (Procedure) Act: two later Acts are missing.** Act 4 of 2023 (Criminal Law (Procedure) (Amendment) Act 2023, Official Gazette 12 May 2023) and Act 11 of 2024 (Criminal Law Procedure (Paper Committals) Act 2024, Official Gazette 15 July 2024) are printed only as scans with no text layer, and no revised edition online includes them. Which sections they change could not be read, so they have no commit: `criminal-law-procedure/` is the 2012 text and is **not the law in force** on the points those Acts change (among them committal for trial).
- **Companies Act (Cap. 89:01)** has one version, 31 December 2012: the Ministry serves the 2012 edition (L.R.O. 1/2012) as the current chapter, byte-identical to the Internet Archive capture of 30 July 2022, and its front page lists no amending Act after Act 11 of 1999. Sections 286-304 were repealed by Act 21 of 1998 and have no file. Acts after 2012 that might amend it under another title (the anti-money-laundering amendment Acts 2015-2023) were searched for "Companies Act" with no hit, but several are partly scans, so a later amendment by another Act cannot be ruled out. The Statement in lieu of Prospectus (Second Schedule, Part I) is a two-column form: each item is one line, followed by its entries ("1. Shares", "Cash $"). The subsidiary legislation printed after the Act is not included.
- **Evidence Act, Limitation Act, Defamation Act, Interpretation and General Clauses Act** start at 31 December 2012 (L.R.O. 1/2012, read from the Internet Archive); the 2022 edition (today's text on mola.gov.gy) is a second version where its words differ. The Evidence Act's 2022 edition includes Acts 1 of 2014, 13 of 2018 and 15 of 2021; their changes are committed as unexplained on 31 December 2022, not on each Act's own date. The Evidence Act's Schedule is a table; each table row is one line, its cells in column order.
- **Sexual Offences Act (Cap. 8:03)** is not here: its 2012 edition already includes Act 2 of 2013, so it cannot be dated 31 December 2012, and that Act is not on the Parliament website to date it.
- **Summary jurisdiction, family and land chapters (added 29 October 2026).** Caps. 3:05, 7:01 and 5:02 start at 31 December 2012 (L.R.O. 1/2012, read from the Internet Archive); their 2022 editions print the same text, so they have one version. Caps. 10:02, 11:09, 12:02, 12:24, 36:23, 45:02, 45:03, 46:05, 60:02, 61:01 and 62:01 are still served by the Ministry in the 2012 edition, so they have that one version. Caps. 3:04 and 5:01 start at 31 December 2022: their archived 2012 editions already list Acts of 2014 (13 of 2014 and 5 of 2014), so they are not the text of 31 December 2012 and are not used. Column headings of form tables set in small or turned type (Cap. 10:02 Forms 54-55, Cap. 7:01 Form 10, Cap. 11:09 Form 4) and the left heading of the scale in s. 38 of Cap. 10:02 are each one line, read left to right. The reviser's note printed after the Rent Restriction Act's Schedule is its own file, `rent-restriction/note-1.md`. Subsidiary legislation printed after each Act is not included.
- **Matrimonial Causes Act and Wills Act: later Acts are missing.** Act 13 of 2024 (Matrimonial Causes (Amendment) Act 2024, Official Gazette 27 August 2024) and Act 21 of 2024 (Wills (Amendment) Act 2024, Official Gazette 27 December 2024) are printed only as scans with no text layer, and the Ministry still serves the 2012 editions. They have no commit: `matrimonial-causes/` and `wills/` are the 2012 text and are **not the law in force** on the points those Acts change. The Parliament index has gaps, so other chapters may also have later amendments that no source online shows.
- **Not added yet:** the Summary Jurisdiction (Offences) Act (Cap. 8:02), whose PDFs have layout slips the reader does not yet repair; the Adoption of Children Act (Cap. 46:04), whose Schedule is a register table on a turned page and whose amending Act 8 of 2021 is a scan; and the Married Persons (Property) Act (Cap. 45:04), whose 2012 edition already lists Acts of 2014.
- **Other acts.** Only these thirty-six acts are here so far. The Laws of Guyana publish only the current revised edition of each chapter, and the Parliament website holds Acts as passed from 1928 (with gaps), so other acts need the same edition-and-replay work.

## How it is built

Lexifina reads the sources listed here and records each act's dated versions, and the laws that made each change, in one corpus file. `tools/build.py` writes this repository from that file, and the same corpus always gives the same commit hashes; `REPRODUCE.md` gives the details and the checks. A model (Claude) wrote Lexifina's code; it wrote no legal text, and no model runs when the history is built.

Lexifina's code reads each PDF's text layer with PyMuPDF and separates the text from running heads and marginal notes by position and font size; Lexifina's code splits it into provisions, normalises typesetting, replays the Acts and writes `corpus.json`; the shared builder `tools/build.py` turns that into the commits.

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
