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

    Repeats are collapsed: sort_key runs more than once per document, and a
    warning counted twice would misstate how many files were affected.
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


def sort_key(asof):
    """Newest first; anything unparseable sorts last."""
    m = re.match(r'(\d{1,2})\s+(\w+)\s+(\d{4})', asof or "")
    if not m:
        warn("date %r does not parse as 'D Month YYYY', sorting last" % (asof,))
        return datetime.date.min
    day, month_name, year = m.group(1), m.group(2), m.group(3)
    month = MONTH_LOOKUP.get(month_name.lower())
    if month is None:
        warn("unrecognised month %r in date %r, sorting last" % (month_name, asof))
        return datetime.date.min
    try:
        return datetime.date(int(year), month, int(day))
    except ValueError:
        # The regex admits any one or two digit day, so 31 February reaches
        # here. The docstring promises this sorts last rather than raising.
        warn("impossible date %r, sorting last" % (asof,))
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
        return max((sort_key(v["asof"]) for v in entry.values()), default=datetime.date.min)

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
                    '<div class="doc"><a href="{f}">{l}</a>'
                    '<span class="asof">as of {a}</span></div>'.format(
                        f=html.escape(urllib.parse.quote(d["file"])), l=label,
                        a=html.escape(d["asof"])))
            else:
                links.append(
                    '<div class="doc"><span class="none">{l}</span>'
                    '<span class="asof">not published</span></div>'.format(l=label))

        cells.append(
            '  <article class="entry">\n'
            '    <div class="head"><span class="tkr">{t}</span>'
            '<span class="co">{c}</span></div>\n'
            '    <p class="tension">{h}</p>\n'
            '    <div class="docs">{d}</div>\n'
            '  </article>'.format(t=html.escape(ticker), c=company, h=headline,
                                  d="".join(links)))

    today = datetime.date.today()
    built = "%d %s %d" % (today.day, today.strftime("%B"), today.year)

    return TEMPLATE.format(entries="\n".join(cells), count=len(ordered), built=built)


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light only">
<title>Equity research &middot; index</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600&family=IBM+Plex+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{{
  color-scheme: light only;
  --paper:#FFFFFF;  --canvas:#F4F7F9;  --panel-2:#EDF2F6;
  --line:#DEE6EC;   --line-hard:#C0CDD7;
  --ink:#0F1E2B;    --ink-dim:#46596A; --ink-faint:#5C6E80;
  --display:'Archivo',ui-sans-serif,system-ui,'Helvetica Neue',Arial,sans-serif;
  --body:'Source Serif 4',Georgia,'Times New Roman',serif;
  --mono:'IBM Plex Mono',ui-monospace,'SFMono-Regular',Menlo,monospace;
  --col:760px;
}}
*{{box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%}}
html,body{{background:var(--canvas) !important}}
body{{margin:0;color:var(--ink);font-family:var(--body);font-size:16.5px;line-height:1.62;
     -webkit-font-smoothing:antialiased}}
.wrap{{max-width:var(--col);margin:0 auto;padding:0 22px 96px;background:var(--paper);
      border-left:1px solid var(--line);border-right:1px solid var(--line)}}
header{{padding:44px 0 26px;border-bottom:2px solid var(--line-hard);margin-bottom:8px;
      position:relative;padding-left:20px}}
header::before{{content:"";position:absolute;left:0;top:44px;bottom:26px;width:4px;
      background:var(--ink-dim)}}
h1{{font-family:var(--display);font-size:30px;font-weight:700;line-height:1.22;margin:0}}
.functional{{font-family:var(--mono);font-size:12.5px;font-weight:500;letter-spacing:.14em;
      text-transform:uppercase;color:var(--ink-faint);margin:18px 0 0}}
.lede{{margin:22px 0 0;max-width:68ch}}
.entry{{border:1px solid var(--line);background:var(--paper);padding:18px 22px;
      margin-top:14px;border-left:4px solid var(--line-hard)}}
.head{{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}}
.tkr{{font-family:var(--mono);font-size:19px;font-weight:700;letter-spacing:-.5px;
      color:var(--ink)}}
.co{{font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;
      color:var(--ink-faint)}}
.tension{{margin:10px 0 0;font-size:16px}}
.docs{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:14px;padding-top:12px;
      border-top:1px solid var(--line)}}
.doc{{display:flex;flex-direction:column;gap:3px}}
.doc a{{font-family:var(--display);font-size:14.5px;font-weight:600;color:var(--ink);
      text-decoration:none;border-bottom:1px solid var(--line-hard);align-self:flex-start;
      padding-bottom:1px}}
.doc a:hover{{border-bottom-color:var(--ink)}}
.doc .none{{font-family:var(--display);font-size:14.5px;font-weight:600;color:var(--ink-faint)}}
.asof{{font-family:var(--mono);font-size:11.5px;color:var(--ink-faint)}}
footer{{margin-top:44px;padding-top:22px;border-top:2px solid var(--line-hard)}}
footer p{{font-family:var(--mono);font-size:12px;color:var(--ink-faint);margin:0 0 8px}}
.norec{{border:1px solid var(--line-hard);background:var(--canvas);padding:16px 20px;
      font-family:var(--mono);font-size:12.5px;color:var(--ink-dim);line-height:1.55}}
@media (max-width:720px){{
  .wrap{{padding:0 16px 70px;border-left:none;border-right:none}}
  h1{{font-size:23px}}
  .docs{{grid-template-columns:1fr}}
}}
@media print{{ body{{font-size:11pt}} .wrap{{max-width:none;border:none}} }}
</style>
</head>
<body>
<div class="wrap">

<header>
  <h1>Equity research</h1>
  <p class="functional">{count} companies &middot; index &middot; rebuilt {built}</p>
</header>

<p class="lede">Each company carries two documents. The research report asks what the company
is and what it is worth; the catalyst calendar asks what could move it and when. Each is
stamped with its own as-of date, shown below, because they are revised on different days.</p>

{entries}

<footer>
  <div class="norec">
    No buy, sell, or hold recommendation is issued and no price target is derived.
    Third-party targets and ratings, where shown, are the published views of the firms
    named. These documents are for research and educational purposes and are not
    investment advice. Verify against primary filings on sec.gov before acting.
  </div>
  <p style="margin-top:16px">Index rebuilt automatically from the documents it lists.</p>
</footer>

</div>
</body>
</html>
"""


if __name__ == "__main__":
    rows = collect()
    if not rows:
        raise SystemExit("No ticker files found. Nothing written.")
    out = ROOT / "index.html"
    out.write_text(build(rows), encoding="utf-8")
    print("Wrote %s with %d companies:" % (out.name, len(rows)))
    for ticker in sorted(rows):
        have = "+".join(sorted(rows[ticker]))
        print("  %-6s %s" % (ticker, have))

    if WARNINGS:
        print("%d file(s) skipped or warned about:" % len(WARNINGS))
        for message in WARNINGS:
            print("  " + message)
    else:
        print("No files skipped, no warnings.")
