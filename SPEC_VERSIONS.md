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
| **Version 2.01 · Effective August 16, 2026** | 2026-08-16T2340Z | 146,028 | 2,407 | 5fc7a5f2b037ce9e424a18ee8790485d4ad22368069e4ba4f719f6b4f9159ebc | HOUSE_STYLE.v2.01.2026-08-16T2340Z.5fc7a5f2.md |
| **Version 2.00 · Effective August 16, 2026** | 2026-08-16T2200Z | 144,921 | 2,393 | `d868664332f249b65fd266e844998bcc708650d0c3b2040188b9ae42161c7a0e` | `HOUSE_STYLE.v2.00.2026-08-16T2200Z.d8686643.md` |
| **Version 1.99 · Effective August 12, 2026** | 2026-08-12T2149Z | 153,120 | 2,508 | `2ec6041212e2438f0bc887c08a8d36199426da9537a82caca18a2d73f44191bf` | `HOUSE_STYLE.v1.99.2026-08-12T2149Z.2ec60412.md` |
| **Version 1.98 · Effective August 10, 2026** | 2026-08-12T2149Z | 150,388 | 2,459 | `8a245ec485bc394d03f0114815cfacda50d2bdcf5b734204c4a4678aaf771169` | `HOUSE_STYLE.v1.98.2026-08-12T2149Z.8a245ec4.md` |
| **Version 1.97 · Effective 6 August 2026** | 2026-08-06T00:50Z | 148,936 | 2,432 | `4fcb37bfac3ed90d96b3d04fbf0e517dfb2422f680e57b2282020ad55f4f6d67` | `HOUSE_STYLE.v1.97.2026-08-06T0050Z.4fcb37bf.md` |
| **Version 1.96 · Effective 6 August 2026** | 2026-08-06T00:10Z | 148,065 | 2,419 | `7a358a912d7d953aef5b4a4ef037ba007fc7b6e66b4efda7661e56bd169396e4` | `HOUSE_STYLE.v1.96.2026-08-06T0010Z.7a358a91.md` |
| **Version 1.95 · Effective 5 August 2026** | 2026-08-05T23:20Z | 146,364 | 2,396 | `eb48205e1a2bc3faa0b4a1effe5a96f374f3958429b9d279a6d53075dcae3249` | `HOUSE_STYLE.v1.95.2026-08-05T2320Z.eb48205e.md` |
| **Version 1.94 · Effective 5 August 2026** | 2026-08-05T22:30Z | 144,352 | 2,363 | `2c4b5d643577441a9c49c0f742eb0234676a42eb8e1bb6e4e2bd352671fbe341` | `HOUSE_STYLE.v1.94.2026-08-05T2230Z.2c4b5d64.md` |
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
