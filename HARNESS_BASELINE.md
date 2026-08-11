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


---

## The allowlist record, so a fourth pass does not halt here

**`HARNESS_BASELINE.md` is the single legitimate tracked path matching an unanchored search for
`harness`.** `git ls-tree -r HEAD --name-only | grep -i harness` returns this file and nothing
else, because `harness/` itself is excluded by `.gitignore` and holds no tracked file at all:
`git ls-files harness/` returns zero.

Three passes have halted on that match, each concluding that the ignore rule had failed. It had
not. **Anchor the directory test as `^harness/`, and allow exactly this one line for the name
test.** A second match is a real finding and means an apparatus file has become tracked.

This note is here rather than in the ledger because a reader who clones the repository has no
`harness/` directory and no ledger, so this file is the only place the exception can be found.

---

## Movement recorded on 10 August 2026, the v1.98 language pass and the state verifier

### Removed

| File | Why |
|---|---|
| `Q1_push_preconditions.py` | **Declared spent.** It pinned `EXP_DIGEST`, `EXP_SENTINEL` and `EXP_LOGS` as literals across ten references. When the specification moved to v1.98 it reported all 36 carrier files as defective while every one of them was correct, because it compared them to the value of its own day rather than to any rule. Its function is absorbed into `R1_pass_state.ps1`. Preserved at `preserve/2026-08-10-R1/Q1_push_preconditions.py`, sha256 `2b1defd617573d886efc501c7227569e546235517e7a5523fcbaa4a3fe966087` |

**What replaced it, and how the replacement differs.** `Test-PushPreconditions` enforces as rules,
needing no stored value: one BEGIN and one END sentinel per carrier, one sentinel version across
the tree matching the specification, and exactly one distinct shared-block digest. It compares
`Head`, `GroupHash`, `TrackedCount`, `SpecVersion`, `LogEntryTotal` and `SharedBlockDigest` only
when a caller supplies them, and stores none of them.

### Added

| File | What it holds | Bytes | sha256 |
|---|---|---|---|
| `R1_pass_state.ps1` | repository and roster state, the three assertions, publish preconditions. Carries no expected value | 21,294 | `b42015e526f8d4bf9368d24294609698e39f2c7275437d418a5c5e676c0e1aea` |
| `R1_roster.py` | ticker roster as JSON, from `build_index.collect()`. Computes nothing itself | 1,442 | `a30555e617ec3aa2ed7060b4b5bcc2d45e4e452093179f3437d1649056da4e47` |
| `R1_tests.ps1` | the arm suite for the above | 13,194 | `1257519288c21cdb8cd519aab5fc157e6aec469a7e41937096d07663d04fc2b3` |
| `V1_language_convert.py` | the v1.98 British to American conversion, with three controls | 7,999 | `0f4d3dc4260559dd7807365ef467c4f4b1ed0b83f0cb3c50c3eb40e2bfbe6f8e` |
| `V2_run_after_language.ps1` | read-only run of the full chain after that conversion | 2,015 | `3f29c4b933c619e847ea33104890bb9c20c684e75ac0e4e9a1ea72c2e049a81d` |

### Edited, for the v1.98 date rule

Section 12.9 sets the date form as month, day, year. **Eight date bindings were rebound**, one more
than the seven predicted. The eighth was `A24`, which already carried the month-first form beside
the day-first one and so would have kept passing either way. It was found by a grep control, not by
a failing test, and removed because an arm no conforming file can satisfy is an arm that accepts a
file nobody converted.

| File | Bytes | sha256 |
|---|---|---|
| `20_checks.ps1` | 46,338 | `0e4d4059dc86ffb05f3963c15c4676ca02e2d2c61033f91d444282b7023eed9e` |
| `D1_checks_v176.ps1` | 5,377 | `3049ebf55eeffec7b53bb88852ccd43d6ff7858677950e4595815950f97654ed` |
| `build_index.py`, tracked, not in `harness/` | 14,953 | `b2908c24a51594fc55ea27f5a2aa000b30ecc7306736d5500b7e6c99026eb24a` |

### A caution for the next pass that adds an instrument

**`R1_`, `V1_` and `V2_` were not free prefixes.** `R1_clsk_agents.py`, `V1_closes.py` and
`V2_sweep.py` already existed. Nothing was overwritten because the full names differ, but the
prefix scheme is not a namespace and should not be treated as one. Check the directory before
choosing a name.

**The instrument count is not 468.** `harness/` holds **593** files, and most of the growth is
preserved evidence rather than instruments: a single EDGAR sweep contributed 65. Any figure quoted
for "the harness" needs to say whether it counts evidence, and the older 467 and 468 figures in the
ledger do not.

### Corrected 10 August 2026, after the final review fix wave

**The three digests recorded above describe no file that exists.** The fix wave that closed the
final whole-branch review rewrote all of them, and this table was not updated with it. It is
corrected here rather than edited in place, so a reader can see that a tracked record went stale
against an untracked directory and how long it took to notice.

**That is worth more than the correction.** `harness/` is gitignored, so this table is the only
tracked record of what the harness holds. Nothing verifies it programmatically. It is structurally
the same exposure as the specification being gitignored, which is what the review's first Critical
was about, and it went stale in the same session that fixed the other one.

| File | Bytes | sha256 |
|---|---|---|
| `R1_pass_state.ps1` | 42,693 | `48740487bb21a0cc08adff94c84ce1634373b2b4896216ecbed18fe10d661021` |
| `R1_tests.ps1` | 46,463 | `3cb317e72cfcb75d3334e60dbaad051d2230b7dca8f8e8e376180da281a5ab7a` |
| `R1_roster.py` | 3,572 | `0530cf6e8b265df4a6455b1cfff24f0d3cbccd2fb76a6eb97933064037786a29` |
| `R1_halt_test.ps1` | 9,322 | `4cf91263f5c9901ef72c8bd9fe54f91498cf9777f32d76c96317afce6c3e68c7` |

`R1_halt_test.ps1` was not in the earlier table at all and is recorded here for the first time.

### Added 10 August 2026, after the final review: the protocol-arm check

`W2_protocol_arms.py` requires every call `SKILL.md` shows an operator to be made by at least one
arm, with the same named parameters. It fails in both directions: change the protocol and the
suite goes red, change the suite and the protocol is exposed as stale.

**On its first real run it found the gap a human reviewer had parked as an observation**, that
`Get-PassState -ClaimedPaths -Stamp` is the call the protocol document shows and no arm made it.
An arm was added and the seam now carries the argument.

**Its own control exists because the first, casual version of this check failed exactly the way it
was built to catch.** That version anchored a closing fence at column zero. Two of `SKILL.md`'s
three code blocks are indented inside a numbered list, so it found one block instead of three and
reported "none missing" while reading none of the calls it existed to verify. The control now
proves the extractor sees indented blocks and that the comparison discriminates, before any other
figure is printed.

### Added 10 August 2026: the mutation harness for R1

`W3_mutate_R1.ps1` mutates the module source and requires the arm suite to fail. It follows
`82_mutate.ps1`'s shape and adds what the source-mutation form needs: a restore point written by
the run itself, a hash-verified restore after every mutation, and a cosmetic mutation that must
SURVIVE, which is the control in the awkward direction. A harness that kills a comment change is
measuring its own noise.

**On its first run it found three arms that could not fail**, including the sharpest one available:
`Test-GroupHashControl` could be stubbed to `return $true` and nothing noticed. The positive
control that proves the group-hash reader can see was itself unguarded.

Two were closed by new arms. The deliverable list is now asserted to be ascending, and the group
hash is checked against an **independent recomputation of the recipe**, which stores no value and
is a second statement of the rule.

The third is declared **EQUIVALENT** rather than hidden: no reachable input makes the digest of the
whole list equal the digest of the list with one file withheld, so that expression is always true
and no arm can distinguish it. The harness prints the justification on every run and **fails if a
declared-equivalent mutation is ever killed**, because that means the justification has gone stale.

| File | Bytes | sha256 |
|---|---|---|
| `W2_protocol_arms.py` | 7,774 | `7e89cbcc71666caa09d0bc1ffefcc643f152acba15880a069dd5c9e689626321` |

### Added 10 August 2026: the two-hop test, and what running it found

`W8_two_hop.ps1` exercises spec section 9.2's case, which had never run: hop 2 opening on a tree
hop 1 left dirty, proceeding past what hop 1 declared and halting on what nobody did. It passes,
and it also proves the class follows the claim rather than the path, by swapping the claim and
requiring the classes to swap with it.

**Its first version could not work, and the reason is a property nothing had stated.** It wrote
marker files into `scratch/` and neither ever appeared in the dirty list, because `scratch/`,
`harness/`, `preserve/` and `pass_documentation/` are all gitignored and `git status` never
reports an ignored file.

> **The claim mechanism only engages for TRACKED paths.**

A hop writing only into ignored apparatus produces no dirty path and has nothing to declare.
Declaring those directories looks careful and accomplishes nothing. `SKILL.md`'s own example did
exactly that, naming `harness`, `scratch` and `pass_documentation`, and has been corrected to name
a tracked path instead. The paths the mechanism can ever see today are `HARNESS_BASELINE.md`,
`build_index.py` and `index.html`.

### Added 11 August 2026: the index check joins the chain as tree-scope check T2

The v1.98 date conversion rebound eight date **readers** and missed the one **writer**.
`build_index.py` stamped the front page day-first, so `index.html` carried
"rebuilt 11 August 2026" above 34 documents reading "as of August 4, 2026", and every one
of the per-file rows passed while it did. No check in the chain reads `index.html`.

`G3_index_date_guard.py` closes that. It is registered as **T2**, beside T1, in the
tree-scope block rather than as check 41. `AE_runner_shared.ps1` already recorded the
reasoning for T1 and it applies unchanged: the subject is one artefact, not each
deliverable, so as check 41 it would run once per file on the same evidence and inflate
the row count while proving nothing extra. **The count is still exactly 40**, measured
rather than assumed: the conform runner wrote 1,120 rows over 28 files, and 1,120 / 28 = 40.

It binds two things, because either can be wrong alone. `index.html` must carry no
day-first date **and at least one month-first date**, so a zero is a reading rather than an
empty search. `build_index.py`'s formatter is asserted separately, because a reverted
formatter with no rebuild leaves the generated file passing until the next push rebuilds it.

`G4_index_date_mutate.py` is its mutation table: six cases, five faults plus the clean
negative control, all behaving as required.

### The same day: what registering a second tree-scope check exposed in the runner

`Invoke-TreeScopeChecks` threw on the **first** failing check. With one check registered
that was invisible. With two it means a tree carrying two faults reports one, and worse,
**a newly added check tells you nothing until every check registered before it is already
green** — T2 could not be observed on the live tree at all, because T1 fails there.

The loop now runs every registered check and throws once, listing all of them. Two branches
were added on the same principle: a registered check whose script is absent is reported as
DID NOT RUN rather than passed, and an empty table throws instead of printing a clean
header and falling through. `G5_treescope_arms.ps1` holds five arms over the runner itself,
including the negative control that stops a runner which throws unconditionally from
passing the other four.

### Open, not fixed: T1 fails on this tree, and the rule it states is not the rule it enforces

> **FALSE AS WRITTEN, corrected 11 August 2026.** The rule does state this case: it names
> SPEC_VERSIONS.md among the four root files and says *no script writes any of them*. There
> was no rule/enforcement gap here. The section below is left standing rather than deleted
> because the reasoning it records led to the real gap, which is the opposite defect and
> worse. See the next section.

`scratch/darkmode-stage2b/_rollout7.py:26` writes `SPEC_VERSIONS.md` with a bare filename
and T1 flags it [V3]. But `SPEC_VERSIONS.md` is a **tracked file that belongs at the
repository root**, it is not pass documentation, and the script is a spent one-shot rollout
from 5 August 2026 sitting in gitignored `scratch/`.

So T1 states "pass documentation comes from the resolver" and enforces "no bare-filename
markdown write". Those are different rules, and the gap is the project's own recurring
defect pointing the other way: an instrument firing on something its stated rule does not
forbid.

It is left open deliberately. The repair is a judgment call between narrowing [V3] to
pass-document names, excluding `scratch/`, and deleting the spent script, and those have
different consequences. **Widening an exclusion so that a pass just added goes green is the
move this file exists to catch.**

Note also that `T2_run_conform.ps1`'s `-SkipTreeChecks` is a `[switch]`, so tree-scope checks
run by default and T1 has therefore been aborting that runner on this tree. Any recent clean
per-file table from it was produced with the switch set.

### Corrected 11 August 2026: T1 was blind, and had been since it was written

Reading T1 to repair a supposed over-fire found an under-fire instead. **T1 missed four live
violations** and had reported a clean tree over all four for its whole existence.

```python
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
P = os.path.join(ROOT, 'HOUSE_STYLE.md')
open(P, 'w', encoding='utf-8', newline='').write(s)
```

`_rollout6.py`, `_rollout6b.py`, `_spec195.py` and `_spec196.py` each do exactly that. It is
V1's textbook shape. T1's docstring claimed a root base was recognised *"by resolution, not by
being called ROOT"*, but resolution was **four hand-written expression shapes**, and this was
not one of them: the pattern required a bare `os.path.dirname(__file__)` and exactly one `'..'`.

**The repair could not be more patterns**, and G2 now carries the proof as M13 and M14: an
expression one character different from a root binding that resolves somewhere else, which a
spelling-matched check fires on and must not. Matching harder makes the false positive worse at
the same time as the miss. So T1 now **resolves** the expression — it evaluates the arithmetic
against the scanned file's own location and compares the answer to the root. An identifier that
resolves elsewhere now *suppresses* a finding rather than merely failing to raise one.

Two more defects surfaced while proving it, both found by reading why a case passed rather than
by its passing:

**The write detector could not see past a nested paren.** `PY_WRITE_OPEN_RE`'s character class
stops at the first `)`, so in `open(os.path.join(ROOT, 'X.md'), 'w')` it never reached the mode
argument and did not count the line as a write at all. The plainest possible violation, on one
line. Python writes are now read from the syntax tree. G2 carries it as M16.

**The verdict depended on how the argument was spelled.** The resolver answers in absolute paths,
so a root passed as `.` compared equal to nothing and every resolved finding was discarded
silently. Run as `.` it reported 2 violations; run against the same tree spelled absolutely, 6.
`scan_tree` now takes `os.path.abspath` of its argument. **This was shipped and run for a full
pass before it was caught** — the fix that closed the blindness had a blindness of its own, and
only comparing two spellings of the same tree exposed it.

G2 grew from 10 cases to 16 and now stands at 9 killed, 0 missed, 7 clean, 0 false positives.
Every case before this pass bound the root to an absolute path literal, which is the one form
T1 always handled; the computed root was never exercised, which is how the blindness survived a
mutation harness.

### Open, and a decision rather than a fix: five violations T1 can now see

All five sit in gitignored `scratch/darkmode-stage2b/`, are spent one-shot scripts from 5 and 6
August, and re-running any of them would corrupt what it wrote. Four write `HOUSE_STYLE.md`
through a computed root; `_rollout7.py` writes `SPEC_VERSIONS.md` by bare filename.

They are real violations of the rule **as stated**, and that is the problem worth raising: the
rule asserts the four root markdown files *"are maintained by hand and no script writes any of
them"*, and that assertion has been false since at least 5 August. Spec versions v1.94 through
v1.98 were landed **by script**. So the choice is not about five files:

- if script-driven spec rollout is legitimate, the rule's premise is wrong and 12.x should say
  so, with T1 narrowed to pass documents;
- if it is not, the workflow that produced the last five spec versions needs replacing.

Widening an exclusion, or moving the five into `preserved/` where T1 does not look, would settle
neither question and would put the tree back to reporting clean. Left open deliberately.
