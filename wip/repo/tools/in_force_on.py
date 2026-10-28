"""Prints the law of Guyana as it stood on a given day, read from this repository's history.

    python tools/in_force_on.py 2009-03-16 constitution 119D        # art. 119D the day before Act 5 of 2009 (none)
    python tools/in_force_on.py 2009-03-17 constitution 119D        # art. 119D as inserted by Act 5 of 2009
    python tools/in_force_on.py 2016-01-11 constitution sch-3       # the Third Schedule after Act 1 of 2016
    python tools/in_force_on.py 2010-01-01 constitution             # the whole Constitution on 1 January 2010
    python tools/in_force_on.py --law 2013-01-01 constitution 7     # also name the law behind that wording
    python tools/in_force_on.py 2026-10-28 criminal-law-offences 100  # s. 100 of the Criminal Law (Offences) Act

A thin wrapper around tools/on.py: the version is chosen by each commit's `In-force:` trailer, never by its commit
date. An article number may carry its letter suffix as printed ("6A", "119D", "212DD"); "preamble" and "sch-1" to
"sch-4" name the preamble and the schedules; in the other acts a number is a section. Standard library only.
"""
import re
import runpy
import sys
from pathlib import Path


def unit(act: str, arg: str) -> str:
    """An article of the Constitution (art-NNN) or a section of an Act (sec-NNN), by its printed number."""
    m = re.fullmatch(r'(?:art-?|sec-?|s\.?)?(\d{1,3})([A-Za-z]{0,2})', arg)
    if not m:
        return arg
    prefix = 'art' if act == 'constitution' else 'sec'
    return f'{prefix}-{int(m.group(1)):03d}{m.group(2).lower()}'


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    args = [a for a in sys.argv[1:] if a != '--law']
    if len(args) == 3:
        i = len(sys.argv) - 1 - sys.argv[::-1].index(args[2])
        sys.argv[i] = unit(args[1], args[2])
    sys.argv[0] = str(Path(__file__).with_name('on.py'))
    runpy.run_path(sys.argv[0], run_name='__main__')
