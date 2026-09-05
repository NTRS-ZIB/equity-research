#!/usr/bin/env bash
# Assemble the deployable site into dist/ for Cloudflare Pages.
#
# WHY THIS EXISTS. GitHub Pages served the whole repository root, so the working record was
# public: HARNESS_BASELINE.md, SPEC_VERSIONS.md, build_index.py, README.md and scripts/ all
# returned 200. Cloudflare Pages deploys the build output directory and nothing else, so the
# deployable set is chosen here, explicitly, rather than by whatever happens to sit at the root.
#
# THIS SCRIPT DOES NOT BUILD THE INDEX, AND THAT IS DELIBERATE. build_index.py runs in GitHub
# Actions and commits index.html. T3-index-current checks that the COMMITTED index matches what
# the builder produces. If the index were regenerated at deploy time the served page could
# differ from the checked one, and T3 would stop guarding what is actually published. This
# copies the committed index; it never regenerates it.
#
# IT COUNTS BUT DOES NOT PIN. A floor of "at least one deliverable" catches the failure that
# matters, which is a glob matching nothing and Pages cheerfully serving an empty site. It does
# NOT assert 36, because the set grows when a ticker is added and a pinned count would report a
# correct tree as broken. Ledger 3.1: Q1_push_preconditions.py was declared spent for exactly
# that, having pinned a version and called 36 correct files defective.

set -euo pipefail

OUT="${1:-dist}"
rm -rf "$OUT"
mkdir -p "$OUT"

# The site shell. Each is required: a missing one is a broken page, not a smaller one.
# _headers is parsed by Workers and is never served as an asset. It is required rather
# than optional: losing it would silently drop the framing and referrer policies, and
# nothing downstream would notice, because the site would still serve perfectly.
#
# favicon.ico and apple-touch-icon.png are requested by browsers AT THE ROOT for every
# page on the domain, the 36 deliverables included, without any of them linking to one.
# That is why adding an icon required no edit to a single research document, and it is
# the reason these two must sit at the root of the deploy rather than in a subfolder.
SITE="index.html method.html about.html styles.css site.js _headers favicon.ico icon.svg apple-touch-icon.png"
for f in $SITE; do
  if [ ! -f "$f" ]; then
    echo "PUBLISH FAILED: required site file '$f' is not present" >&2
    exit 1
  fi
  cp "$f" "$OUT/"
done

# The research. TEMPLATE_*.html carry the same two suffixes and are gitignored, so they are
# absent from a clean checkout and present in a working tree. They are excluded BY NAME rather
# than by trusting the checkout, because shipping one would publish the house style scaffolding.
copied=0
for f in *_Research_Report.html *_Catalyst_Calendar.html; do
  [ -e "$f" ] || continue
  case "$f" in
    TEMPLATE_*) continue ;;
  esac
  cp "$f" "$OUT/"
  copied=$((copied + 1))
done

if [ "$copied" -eq 0 ]; then
  echo "PUBLISH FAILED: no deliverable matched. An empty site deploys as a 404 and reports success." >&2
  exit 1
fi

# Refuse to ship anything the migration decided not to serve, however it got here.
for bad in HARNESS_BASELINE.md SPEC_VERSIONS.md build_index.py README.md; do
  if [ -e "$OUT/$bad" ]; then
    echo "PUBLISH FAILED: '$bad' reached the deploy directory and must not be served" >&2
    exit 1
  fi
done
if ls "$OUT"/TEMPLATE_* >/dev/null 2>&1; then
  echo "PUBLISH FAILED: a TEMPLATE file reached the deploy directory" >&2
  exit 1
fi

total=$(find "$OUT" -type f | wc -l)
site_count=0
for f in $SITE; do site_count=$((site_count + 1)); done
echo "publish: $OUT holds $total file(s): $copied deliverable(s) and $site_count site file(s)"
echo "publish: excluded from the deploy by design: the build log, the specification version"
echo "publish: record, the index builder, the README and scripts/"
