# Harness baseline

A hash-only record of the shared verification harness. **This file carries no code**, only enough
to detect that an instrument changed between passes.

`harness/` is excluded from this repository by `.gitignore`, on the reasoning stated there: it is
working apparatus and not published research. This record is tracked instead, for the same reason
`SPEC_VERSIONS.md` is tracked for the specification. Detecting that something moved needs a hash,
not the contents.

## Why this exists

The correction pass of 5 August 2026 rebound four checks and stated that none of them belonged to
the shared check table. That was the right distinction, but its closing checksum block covered three
files and did not extend to the harness, so the claim was asserted rather than proved. No hash record
of the harness predating that pass exists anywhere in the tree, so it cannot be proved retroactively.
This record is the baseline so the next pass does not inherit the same gap.

## Current baseline, at 2026-08-05T19:40Z

### The shared check chain

| File | What it holds | Bytes | sha256 |
|---|---|---|---|
| `20_checks.ps1` | check table, 30 checks | 43,338 | `1deb9a0c1d1c257ebbce836516ec2bc903c758a459a465462773cd21fb48f3b8` |
| `80_checks_ext.ps1` | check table, 8 checks, C30 to C37 | 15,321 | `21373ea4deaabb83a4e6d887a5dc034c5fc16d2115d88cd162ab8befae59bed8` |
| `A8_checks_v175.ps1` | check table, 2 checks, C38 and C39 | 7,660 | `1422cb8f714d056cc7dabf30aed1ac50a41132c6e8453dffea525acf11d770fb` |
| `D1_checks_v176.ps1` | check table, 1 check, assembles the 40 | 5,376 | `ebdaea79113b3f0d9c4b70517bdbd3289f2c4242b2b367feee01ac7bd4fc3b67` |
| `D2_run_v176.ps1` | delivery runner for an update pass | 6,264 | `8e3ef8f548ff78e85e2acc71f86635bf779c287bb7a2c5224a5495103b8faf17` |
| `82_mutate.ps1` | mutation table, groups A and C | 23,120 | `5e9fdf66e757380fb5cfe31e2c38e3aa99d95dc639e3c168cbeffef7173458e0` |
| `D3_mutate_B.ps1` | mutation table, group B | 8,094 | `65ce9d417b1e54e5cadee5d114678a514680909eb85496002b17a374dd2834f6` |
| `A9_counterexamples.ps1` | counter-example table | 7,313 | `4af32fb87ed3df039bd22124ac559aa8968d3ba7af5de3c62b600a39a4827cf9` |

### The tree-scope check and its resolver

Added 5 August 2026. These bind the tree rather than a delivered file, so they are listed
separately from the per-file chain above.

| File | What it holds | Bytes | sha256 |
|---|---|---|---|
| `G1_passdoc_guard.py` | tree-scope check T1, no pass document written to the repository root | 11,384 | `a9af99650c50b626dedbb0e752e2e7cab92346fe3d7670b68fd5ea7370f2229e` |
| `G2_passdoc_mutate.py` | mutation table for T1, 10 cases | 7,196 | `875abf2091331c02f8ae41996623ea1cb859ae06ba313a55df0bf6eb8d5df752` |
| `passdoc.py` | pass documentation resolver, Python | 3,090 | `57133af78c2bf11e0aa1d6d25b7a18d484d203ced8fbb8a9ab2bc78aecab815e` |
| `PassDoc.ps1` | pass documentation resolver, PowerShell | 2,196 | `6c9708614f6a9a5ae750b7c844e036c57880b9046415e0c0e22bd53b42165836` |

### The runners and the structure they share

Added 5 August 2026 by the runner repair pass. Listed separately from the check chain
because a runner decides which verdicts are reported, not what any verdict is.

| File | What it holds | Bytes | sha256 |
|---|---|---|---|
| `AE_runner_shared.ps1` | applicability for all three pass types, the three-outcome classifier, the tree-scope block, the discovered-anchor control | 13,209 | `4881ebb70053b8d6150eb49dbe6b60a9687a5cde8765e7e5b0e666b6ddcc7a2d` |
| `T2_run_conform.ps1` | conformance runner | 9,880 | `65e6b5ff642f41fcfb35eac2de104fc892cf4a07ad7102496c6af7bf1194581f` |
| `AC_run_original.ps1` | original-build runner | 9,570 | `8873b1e5c27f3cb437330a8cb9bed0eac2398f37618e46f1ee75a3fdbb91c59b` |

### Aggregate digest over the instruments in `harness/`

Computed over the sorted list of path, null byte, sha256 and newline for every file outside
`__pycache__` **and outside the results artefacts**, so a change to any instrument, an
addition or a deletion all move it.

**The recipe changed on 5 August 2026 and the figure below is not comparable with the one
before it.** See "Recipe change" at the end of this file before comparing against any earlier
aggregate.

| | Files covered | Aggregate sha256 |
|---|---|---|
| **Instruments**, the figure a pass gates on | **467** | `70ae6c42242053531d8e9f2b8055c2bdf685bfddc21df95640132c281b3b29c5` |
| Whole directory, excluding `__pycache__` only | 485 | `ff4345f33809e5166421a37cd3869526b6ac824e2703296d7c0ceade3f6b1ed9` |

**Both are recorded, and only the first is a gate.** The second moves whenever any runner is
run, because running one writes a results file. It is kept so that an addition to `harness/`
is still visible: a file that is neither an instrument nor a results artefact would move the
second figure and not the first, and that is a thing worth seeing.

**A results artefact** is a file a runner writes as the record of a run. In this harness that
is a `.csv` whose name begins `_results_`, and there are eighteen of them.

**The encoding, stated so it need not be recovered again.** Sorted over
`harness/<relative path, forward slashes>`, then a null byte, then the lowercase hex
sha256, then a newline; the concatenation is hashed. The repair pass of 5 August recovered
this by computing six candidate encodings and finding that exactly one reproduced the
recorded value, which cost more than writing it down here would have.

## How to use it

Before a pass edits or relies on any instrument, hash the files above and recompute the aggregate.
A row that differs means that instrument changed since this baseline. The aggregate differing while
every row matches means something else under `harness/` changed. Record the new values here with the
date, so the next pass can prove what this one could only assert.

## Recipe change, 5 August 2026, the amendment pass

**This is a discontinuity. A pass comparing against the figure recorded before this date will
not reproduce it, and that is expected rather than a defect.**

| | Files | Aggregate |
|---|---|---|
| Old recipe, everything outside `__pycache__` | 484 at the time it was recorded, 485 by the time it was next read | `5987d4e18a85e8a7d637a9035f8fa0936ef64a6b2b422a598bd7a71e69d10c96` |
| New recipe, instruments only | **467** | `70ae6c42242053531d8e9f2b8055c2bdf685bfddc21df95640132c281b3b29c5` |

**What happened.** Running the update runner wrote `_results_v176_GLXY-APLD-BTDR.csv`, and
the aggregate moved from 484 files to 485. The drift was confirmed to be exactly that one
file: removing it and nothing else returns the aggregate to the recorded value exactly, which
no other set of removals could do.

**Why the recipe changed rather than the figure.** This record exists to detect that an
**instrument** changed. Under the old recipe, running an instrument moved the aggregate, so
the ordinary act of verifying a delivery invalidated the baseline. A gate that fires on
legitimate use is a gate that gets ignored, and the previous pass had already declined to
re-derive on the reasoning that an output is not an instrument. That reasoning is adopted here
rather than overruled, and it is the same reasoning that already excludes `__pycache__`.

**The cost, stated because it is real.** The exclusion is by name, `_results_*.csv`, and this
project has repeatedly found name-based rules brittle: the pass documentation guard exists
because six accreted filename patterns could not catch a seventh document type. A runner that
writes its output under a different name would fall inside the instrument digest and move it.
The whole-directory figure above is the mitigation: it covers everything, so such a file is
visible there even while the gate stays stable.

**Verified.** All fifteen individually listed rows below sit inside the instrument set and
none was excluded. The instrument digest was shown to move when one byte of `20_checks.ps1`
is changed, so the exclusion has not made it blind.

## Movement recorded on 5 August 2026, the runner repair pass

The previous baseline was taken at 18:05Z and **reproduced exactly at the start of this
pass**, 483 files and `d6b5b5f2d892a8d385379da2ee35eaae79d229a4010447100e52e193f5190c5b`,
with all twelve individually listed rows matching. That is what makes the movement below
attributable rather than merely observed.

| | Files | Aggregate |
|---|---|---|
| Before | 483 | `d6b5b5f2d892a8d385379da2ee35eaae79d229a4010447100e52e193f5190c5b` |
| After | 484 | `5987d4e18a85e8a7d637a9035f8fa0936ef64a6b2b422a598bd7a71e69d10c96` |

**Three files account for the whole of the move**, and each was a deliberate action of that
pass. **None of the twelve rows above moved: the shared check chain and the tree-scope group
are untouched.** No check was edited, and no deliverable was edited.

| File | Change | Why |
|---|---|---|
| `AE_runner_shared.ps1` | added | one applicability table answering all three pass types, so two runners stop answering the same question two ways. Also holds the three-outcome classifier, the tree-scope block, and the computed-figure control with its anchor discovered from the file under test |
| `T2_run_conform.ps1` | edited | decided scope from the letter at the front of the check key, which counted nine calendar-only items and C36 as in-scope passes on every research report and reported vacuous satisfactions as passes on evidence. Now scopes from the table, resolves document type separately from pass type, reports three outcomes with reasons, runs T1 before the per-file table, and guards the table size, the group C presence, the applicability roster and the per-file count |
| `AC_run_original.ps1` | edited | its control 3 pinned the British spelling of "capitalisation" and was a no-op on `VIP_Research_Report`, which would have aborted a run meeting VIP first. Anchor now discovered. Its inline applicability table and `Get-Applicable` were removed in favour of the shared structure, whose conformance branch it lacked |

The preserved sources sit in `preserved\_preserved_v192_runner_repair_20260805\`, checksummed
before the first edit.

## Movement recorded on 5 August 2026, the write-path pass

The previous baseline was taken at 15:40Z and **reproduced exactly at the start of this pass**,
493 files and `2c1dd72ff4114cfee48d9acf28b0a16a43f057514bc90e38bb12ca8a239c88e1`, which is what makes
the movement below attributable rather than merely observed.

| | Files | Aggregate |
|---|---|---|
| Before | 493 | `2c1dd72ff4114cfee48d9acf28b0a16a43f057514bc90e38bb12ca8a239c88e1` |
| After | 483 | `d6b5b5f2d892a8d385379da2ee35eaae79d229a4010447100e52e193f5190c5b` |

Twenty-one files account for the whole of the move, and each was a deliberate action of that pass.

**Two edited.**

| File | Before | After | Why |
|---|---|---|---|
| `U5_findings.py` | `e010a458...` | `fb9db46a...` | main guard added so the module imports without generating; the findings write path routed through `passdoc.py` |
| `D2_run_v176.ps1` | `a1a39005...` | `8e3ef8f5...` | runs tree-scope check T1 before the per-file table, and throws if it fails |

**Four added.** `passdoc.py`, `PassDoc.ps1`, `G1_passdoc_guard.py`, `G2_passdoc_mutate.py`, listed
with their hashes above.

**Fifteen removed from `harness/`, none deleted.** The `RESULTS_2026-08-*.md` documents were moved
into `pass_documentation/`, where the whole class now lives. The reorganisation pass of the same day
identified them and left them, on the reasoning that moving them belonged to a pass that was already
re-deriving this baseline rather than one that would leave it stale. This was that pass.

`harness/AG_open_hashes.json` records those fifteen at their old paths. It is a point-in-time record
written by an earlier pass and is read by nothing, so it was left as written rather than edited:
correcting a past record to match the present would make it a worse record, not a better one.
## Movement since the previous baseline, 2026-08-05T16:55Z

The aggregate moved from `f307a96de3744e3d80c6cd9f5d6d4b956f32b30961f7ff340b4aed2cb93af160`
over 482 files to the value above over 483. Three files account for the whole difference and
each was edited deliberately by the instrument repair pass of 5 August 2026:

| File | Change | Why |
|---|---|---|
| `CA4_readback.py` | edited | the preserved path at line 17 pointed at a directory renamed out of existence, and two B3 checks were pinned to literal amounts that a legitimate restatement had superseded |
| `CA5_mutate.py` | edited | one mutation anchor carried an amount, so it went no-op once the block was restated; retargeted to the phrase without the amount |
| `CA6_b3_mutations.py` | added | mutation evidence for the rebound B3 checks, including the case that proves the repair is bound to the rule rather than re-pinned |

**None of the nine rows above moved.** The shared check chain is untouched.

