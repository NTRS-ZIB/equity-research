#!/usr/bin/env python3
"""Rebuild index.html from the ticker files in this folder.

Reads every *_Research_Report.html and *_Catalyst_Calendar.html, pulls the ticker,
company name, headline and as-of date out of each, and writes a landing page in the
house style. Nothing is hand-maintained: adding a ticker file is all it takes.
"""

import re
import sys
import html
import pathlib
import datetime
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent
MONTHS = {m: i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June",
     "July", "August", "September", "October", "November", "December"], 1)}

# Full name and three-letter abbreviation, both lowercased. Lookups are exact
# against these keys rather than prefix matches, so "Jan" resolves but "Janice"
# does not.
MONTH_LOOKUP = {}
for _name, _num in MONTHS.items():
    MONTH_LOOKUP[_name.lower()] = _num
    MONTH_LOOKUP[_name.lower()[:3]] = _num

WARNINGS = []


def warn(message):
    """Record a problem and put it on stderr, so a drop is visible in the log.

    Identical messages are collapsed, so the closing count reports distinct
    problems rather than how many times each was noticed. Messages name the
    document they came from, so two files failing the same way stay two
    warnings rather than merging into one.
    """
    if message in WARNINGS:
        return
    WARNINGS.append(message)
    print("warning: " + message, file=sys.stderr)


def plain(fragment):
    """Tags out, then entities decoded, in that order.

    Stripping while the value is still markup means an escaped &lt;b&gt;
    survives as literal text instead of becoming a tag the strip has already
    passed. Decoding afterwards collapses every encoding of a character to the
    character itself, so callers can split on plain text and the html.escape()
    in build() is the only escaping applied.
    """
    return html.unescape(re.sub(r'<[^>]+>', '', fragment)).strip()


def read(path):
    """Pull ticker, company, headline and as-of date out of a delivered file."""
    t = path.read_text(encoding="utf-8", errors="replace")
    if "</style>" not in t:
        warn("%s: no </style> marker; file is malformed, skipped" % path.name)
        return None
    body = t.split("</style>", 1)[-1]

    func = re.search(
        r'<p class="functional">(.*?)</p>', body, re.S)
    if not func:
        warn("%s: no functional line found, skipped" % path.name)
        return None

    # Decode before splitting, so &middot;, &#183;, &#xB7; and a literal U+00B7
    # are all the same character by the time the separator is applied. One
    # pattern then covers every encoding, with nothing to enumerate.
    parts = [p.strip() for p in plain(func.group(1)).split("·")]
    if len(parts) < 4:
        warn("%s: functional line has %d fields, expected 4, skipped"
             % (path.name, len(parts)))
        return None

    ticker = parts[0]
    company = parts[1]
    asof = re.sub(r'^as of\s+', '', parts[3], flags=re.I).strip()

    h1 = re.search(r'<h1 class="headline">(.*?)</h1>', body, re.S)
    headline = re.sub(r'\s+', ' ', plain(h1.group(1))).strip() if h1 else ""

    return dict(ticker=ticker, company=company, asof=asof, headline=headline,
                file=path.name)


def sort_key(asof, source):
    """Newest first; anything unparseable sorts last.

    source is the filename the date came from, and is required rather than
    optional: a warning that a date will not parse, without saying which
    document holds it, reports that something is wrong without saying where.
    """
    # Section 12.9 sets the date form as month, day, year. Bound to that rule alone:
    # a parser accepting the old day-first form as well would sort a document that had
    # never been converted, and say nothing about it.
    m = re.match(r'(\w+)\s+(\d{1,2}),\s*(\d{4})', asof or "")
    if not m:
        warn("%s: date %r does not parse as 'Month D, YYYY', sorting last"
             % (source, asof))
        return datetime.date.min
    month_name, day, year = m.group(1), m.group(2), m.group(3)
    month = MONTH_LOOKUP.get(month_name.lower())
    if month is None:
        warn("%s: unrecognised month %r in date %r, sorting last"
             % (source, month_name, asof))
        return datetime.date.min
    try:
        return datetime.date(int(year), month, int(day))
    except ValueError:
        # The regex admits any one or two digit day, so 31 February reaches
        # here. The docstring promises this sorts last rather than raising.
        warn("%s: impossible date %r, sorting last" % (source, asof))
        return datetime.date.min


def collect():
    rows = {}
    for path in sorted(ROOT.glob("*_Research_Report.html")):
        if path.name.startswith("TEMPLATE"):
            continue
        d = read(path)
        if d:
            rows.setdefault(d["ticker"], {})["report"] = d
    for path in sorted(ROOT.glob("*_Catalyst_Calendar.html")):
        if path.name.startswith("TEMPLATE"):
            continue
        d = read(path)
        if d:
            rows.setdefault(d["ticker"], {})["calendar"] = d
    return rows


def build(rows):
    def newest(entry):
        return max((sort_key(v["asof"], v["file"]) for v in entry.values()),
                   default=datetime.date.min)

    ordered = sorted(rows.items(), key=lambda kv: (-newest(kv[1]).toordinal(), kv[0]))

    cells = []
    for ticker, entry in ordered:
        any_doc = entry.get("report") or entry.get("calendar")
        company = html.escape(any_doc["company"])
        headline = html.escape((entry.get("report") or any_doc).get("headline", ""))

        links = []
        for label, key in (("Research report", "report"), ("Catalyst calendar", "calendar")):
            d = entry.get(key)
            if d:
                links.append(
                    '<a class="doc" href="{f}"><strong>{l}</strong>'
                    '<em>As of {a}</em></a>'.format(
                        f=html.escape(urllib.parse.quote(d["file"])), l=label,
                        a=html.escape(d["asof"])))
            else:
                # A missing document is SHOWN, never omitted. An index that silently drops
                # a half-covered ticker reads exactly like one nobody has started.
                links.append(
                    '<span class="doc missing"><strong>{l}</strong>'
                    '<em>Not published</em></span>'.format(l=label))

        # data-name and data-sort serve the search and sort in site.js. Both are DERIVED
        # here rather than written by hand, and the sort key is the same newest() the row
        # ordering uses, so the two cannot disagree.
        cells.append(
            '      <article class="card" data-ticker="{t}" data-name="{n}" data-sort="{s}">\n'
            '        <div class="card-id"><div class="tkr">{t}</div>'
            '<div class="co">{c}</div></div>\n'
            '        <div class="card-body">\n'
            '          <p class="label">Working tension</p>\n'
            '          <p>{h}</p>\n'
            '        </div>\n'
            '        <div class="card-docs">{d}</div>\n'
            '      </article>'.format(
                t=html.escape(ticker), n=html.escape(any_doc["company"].lower()),
                s=newest(entry).isoformat(), c=company, h=headline,
                d="".join(links)))

    # Section 12.9 sets the date form as month, day, year. This line WRITES a date; the
    # sort_key above READS one. The v1.98 conversion rebound eight readers across the
    # check chain and this builder and missed this single writer, so the index carried
    # "rebuilt 11 August 2026" above 34 documents reading "as of August 4, 2026". The
    # grep control run afterwards searched for old PARSING patterns and could not have
    # found a formatter. Counting readers is not the same as counting encoders.
    today = datetime.date.today()
    built = "%s %d, %d" % (today.strftime("%B"), today.day, today.year)

    return TEMPLATE.format(entries="\n".join(cells), count=len(ordered),
                           docs=sum(len(e) for e in rows.values()), built=built)


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#0B1C2C" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0B1117" media="(prefers-color-scheme: dark)">
<title>NTRS_ZIB Research &middot; Coverage Universe</title>
<meta name="description" content="Independent equity research on power, datacentre and digital-asset infrastructure. Two documents per issuer. Every material claim is sourced. No ratings.">
<link rel="icon" href="favicon.ico" sizes="32x32">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head>
<body>
<a class="skip" href="#coverage">Skip to coverage</a>

<header class="topbar">
  <div class="topbar-inner">
    <a class="mark" href="index.html">
      <div class="mark-box">NTRS_ZIB</div>
      <div class="mark-name">NTRS_ZIB Research<span>Independent coverage</span></div>
    </a>
    <nav class="nav" aria-label="Primary">
      <a href="index.html" aria-current="page">Coverage</a>
      <a href="method.html">Method</a>
      <a href="about.html">About</a>
      <a href="https://github.com/NTRS-ZIB/equity-research">Source</a>
    </nav>
    <div class="theme" role="group" aria-label="Colour theme">
      <button type="button" data-theme="system" aria-pressed="true">Sys</button>
      <button type="button" data-theme="light" aria-pressed="false">Light</button>
      <button type="button" data-theme="dark" aria-pressed="false">Dark</button>
    </div>
  </div>
</header>

<section class="hero">
  <div class="hero-inner">
    <p class="kicker">Power &middot; Datacentre &middot; Digital-asset infrastructure</p>
    <h1>Research, not a recommendation.</h1>
    <p class="standfirst">{count} issuers. Two documents each: a report that asks what the company is
    and what it is worth, and a calendar that asks what could move it and when. Every material claim
    carries a source tag. No buy, sell or hold is issued.</p>
    <div class="stats">
      <div class="stat"><b>{count}</b><span>Issuers covered</span></div>
      <div class="stat"><b>{docs}</b><span>Live documents</span></div>
      <div class="stat"><b>6</b><span>Source classes</span></div>
      <div class="stat date"><b>{built}</b><span>Index rebuilt</span></div>
    </div>
  </div>
</section>

<div class="tools">
  <div class="search">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><path d="M20 20l-3.2-3.2"></path></svg>
    <label class="visually-hidden" for="q">Search coverage</label>
    <input id="q" type="search" placeholder="Search ticker, company or thesis line" autocomplete="off">
  </div>
  <label class="sort">Sort
    <select id="sort">
      <option value="fresh">Most recently updated</option>
      <option value="ticker">Ticker A-Z</option>
    </select>
  </label>
  <div class="count" id="count">{count} names</div>
</div>

<main class="wrap" id="coverage">
  <div class="universe" id="universe">

{entries}

  </div>
</main>

<footer>
  <div class="foot">
    <div>
      <h3>Important</h3>
      <p>These documents are for research and educational purposes. They are not investment advice.
      No buy, sell or hold recommendation is issued, and no price target is derived. Third-party
      targets and ratings, where shown, are the published views of the firms named. Verify every
      figure against primary filings on <a href="https://www.sec.gov">sec.gov</a> before acting on
      anything here.</p>
    </div>
    <div>
      <h3>Freshness</h3>
      <p>Each file carries its own as-of date. The set is not uniformly current, and a document is
      never restamped merely to make the universe look consistent. This page is generated from the
      documents it lists, and was rebuilt {built} from them. It is regenerated automatically on
      every change, so it cannot describe a set that is not there.</p>
      <p class="legal">&copy; 2026 NTRS_ZIB Research.</p>
    </div>
  </div>
</footer>
<script src="site.js"></script>
</body>
</html>
"""


if __name__ == "__main__":
    rows = collect()
    if not rows:
        raise SystemExit("No ticker files found. Nothing written.")
    out = ROOT / "index.html"
    # LEDGER 4.44's sweep, and this is the site with the most at stake: index.html is a
    # PUBLISHED artefact that gets committed and pushed. A write that returns success without
    # landing leaves the previous index in place, and because git reads the same filesystem it
    # reports the tree clean, so the stale page is published by being silently left alone.
    # Nothing else in the chain would notice: T2 checks the index's date FORM, never whether
    # its content is current.
    #
    # On this OneDrive-synced tree a successful write is not yet a file another reader gets,
    # so the page is read back and compared before anything is announced.
    text = build(rows)
    out.write_text(text, encoding="utf-8")
    back = out.read_text(encoding="utf-8")
    if back != text:
        raise SystemExit(
            "INDEX WRITE FAILED: %s read back as %d character(s) against the %d written. The "
            "write returned success and the file on disk is not what was built. Do not commit: "
            "git compares against this same file and would report the tree clean while the "
            "published page stayed stale." % (out.name, len(back), len(text)))
    print("Wrote and READ BACK %s with %d companies:" % (out.name, len(rows)))
    for ticker in sorted(rows):
        have = "+".join(sorted(rows[ticker]))
        print("  %-6s %s" % (ticker, have))

    if WARNINGS:
        print("%d warning(s), each naming the document it came from:"
              % len(WARNINGS))
        for message in WARNINGS:
            print("  " + message)
    else:
        print("No warnings.")
