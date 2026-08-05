# Specification version record

A hash-only record of `HOUSE_STYLE.md`. **This file carries no text from the specification**,
only enough to detect that it moved and to say which snapshot to compare against.

The specification itself is excluded from this repository by `.gitignore`, on the reasoning
stated there: it is the working reference and not part of the published set. The snapshots of
it are excluded for the same reason. This record is tracked instead, because detecting that
the specification changed needs a hash rather than the prose.

Snapshots live in `spec_snapshots\`, which is in the working tree and outside the published
set. A later pass diffs against the snapshot named below.

| Version stated in the file | Snapshot taken | Bytes | Lines | sha256 | Snapshot file |
|---|---|---|---|---|---|
| **Version 1.93 · Effective 5 August 2026** | 2026-08-05T21:30Z | 135,393 | 2,222 | `73afd03a617e831edf7c0eff77a2e6ad383b931612fb852d984d9aff4921bd6e` | `HOUSE_STYLE.v1.93.2026-08-05T2130Z.73afd03a.md` |
| **Version 1.92 · Effective 4 August 2026** | 2026-08-05T15:00Z | 129,462 | 2,137 | `ae769bc54e24509e5f8906c6acce5dae18d6d07d65565428aa020bb3d1145650` | `HOUSE_STYLE.v1.92.2026-08-05T1500Z.ae769bc5.md` |

## What each version changed

**The prose account lives in `spec_snapshots\SPEC_CHANGELOG.md`**, beside the snapshots it
describes. It is not here, and that is deliberate: this file is tracked and published, and it
carries no text from the specification by design. A change record has to quote the
specification to be worth anything, so it belongs where the specification's own copies belong,
in the ignored directory.

The changelog begins at **v1.93**. It does not cover v1.91 or v1.92, because no record of what
those versions changed exists and none can now be produced: no copy of the specification at
v1.90 or v1.91 survives anywhere, established by five independent routes during the
conformance sweep of 5 August 2026. That interval was conformed by confirming every rule in
the live endpoint against every file and saying plainly that per-version attribution was not
possible. The changelog exists so that no later interval has to be handled that way.

## Why this record exists

On 5 August 2026 the specification was modified at 14:15:16Z without its version line moving,
and no copy of the previous state existed anywhere in the tree. The change was recovered by
comparing section boundary positions, not by diffing, because there was nothing to diff
against. A hash recorded here would have made that a one-line answer.

## How to use it

Hash the live `HOUSE_STYLE.md`. If it matches the newest row, the specification is unchanged
since that snapshot. If it does not, the file moved: take a new snapshot into
`spec_snapshots\`, add a row here, and diff the new snapshot against the one named in the
previous row.

A version line that has not moved is not evidence the file has not moved.
