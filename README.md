# Equity research

Two documents per company, covering power, datacentre and digital-asset
infrastructure businesses.

**[Read them here →](https://ntrs-zib.github.io/equity-research/)**

---

## What is here

| Document | Question it answers |
|---|---|
| **Research report** | What is this company and what is it worth? |
| **Catalyst calendar** | What could move it, and when? |

Each is a single self-contained HTML file. No build step, no JavaScript, no external
dependencies beyond a webfont that degrades to a system stack. Open one in any browser.

The two are separate because they are read differently: a report start to finish, a
calendar scanned and jumped into.

---

## How to read them

**Every material claim says where it came from.** Small tags mark the source of each
figure:

| Tag | Means |
|---|---|
| `FILED` | Stated in an SEC filing or company release, cited by form and date |
| `ESTIMATE` | Derived here, with the arithmetic shown |
| `OPEN` | Expected but unconfirmed, nothing filed either way |
| `MARKET` | Price, volume, float, published targets and ratings, stamped with the close |
| `PRESS` | Reported by a named publication, cited by outlet and date |
| `SOCIAL` | Posted publicly by a named account, cited by handle and date |

`PRESS` and `SOCIAL` assert that something was *said*, never that it is true. Neither is
ever the sole basis for a material claim.

**Inference is separated from evidence.** Where the analysis stops reporting filings and
starts reasoning, a violet-bordered block says so. A reader can tell which parts would
survive if the analyst turned out to be wrong.

**Colour carries fixed meaning.** Green is favourable, red adverse, amber unresolved,
violet an analyst assumption. These mean the same thing in every document. Each company
also has one accent colour taken from its logo, used only for identity: the ticker, the
section numbers, the links. It never marks anything as good or bad.

**Absence is stated, not left blank.** Every document carries a table of categories that
were checked and found empty, so a reader can tell "there is no dividend" from "nobody
looked". A category nobody examined reads *Not established*, not *None*.

**Each document ends with its own revision history**, preserved across updates, including
entries recording what an earlier version got wrong.

---

## Dates

Each file carries its own as-of date and the market close its figures are priced from.
These differ whenever a document is built after the close it uses, and both appear in the
masthead.

Documents are revised on different days, so **the set is not uniformly current**. The
index shows each document's date so you can see how fresh any one of them is. A file is
never restamped to today merely to make the set look consistent.

---

## What these documents do not do

**No buy, sell, or hold recommendation is issued, and no price target is derived.**

Where another firm has published a target or a rating, it is reported as market data:
attributed to that firm, dated, and never adopted as this document's own view. Analysing
where someone else's target came from is in scope. Agreeing with it is not.

These documents are for research and educational purposes.
**They are not investment advice.**
Verify every figure against primary filings on [sec.gov](https://www.sec.gov) before
acting on anything here.

---

## About the set

The documents follow a written house style covering section order, sourcing, colour,
titling and revision history, so that a reader who has learned one document can read any
of them. The style guide itself is not published; the documents are the product.

`index.html` is generated automatically from the files it lists and is not maintained by
hand.
