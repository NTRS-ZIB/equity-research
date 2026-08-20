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

### Settled 11 August 2026: T1 narrowed to what section 11.1 actually says

> The section below framed this as an open decision. It was taken: script-driven spec
> rollout is legitimate, so the rule's premise was the thing that was wrong. What follows
> is left standing because it states the question the narrowing answers.

### The question it answered: five violations T1 could suddenly see

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

### What changed, and what did not

**The specification did not change, and there is no v1.99.** Section 11.1 already binds
*"every document a pass writes about its own work, whatever it is called"*. The specification
and its version register are not documents about a pass's work and never fell under it. It was
T1 that had drifted: the sentence *"are maintained by hand and no script writes any of them"*
was the check's own invention, appears nowhere in the specification, and had been false since
5 August. **The check moved to the rule, not the rule to the check.**

**The exemption is four FILES, not a class of document**, and the asymmetry is the whole point.
T1 exists because every previous attempt at this was a name list that grew one entry per
document type; `.gitignore` still carries six such patterns. The forbidden side stays
open-ended, so a document type nobody has thought of is caught on the day it is first written.
Only the exempt side is enumerated, and it is four names the specification already fixes.

Three cases hold that line, because an exemption like this usually leaks by name:

| Case | Verdict |
|---|---|
| `SPEC_VERSIONS_DRAFT.md`, bare | violation — the match is on the exact filename, not a prefix |
| `HOUSE_STYLE_NOTES.md`, joined to the root | violation — a working note about the spec is still about the work |
| one statement naming `HOUSE_STYLE.md` *and* a findings document | violation — every name must be sanctioned, not any |

M11 changed its declared verdict in this pass, which is worth stating plainly rather than
burying: it was written against `HOUSE_STYLE.md`, so under the narrowed rule its old answer was
wrong. It kept its subject, the computed-root resolution, and gave up the filename. **M11 and
M17 are now the same case character for character except for the destination**, which is the
narrowing reduced to a single pair.

G2 stands at 20 cases: 12 killed, 0 missed, 8 clean, 0 false positives. T1 reports PASS on the
live tree under both a relative and an absolute root, and the full chain now runs with tree-scope
checks live rather than skipped: T1 and T2 both pass, 40 checks, 1,120 rows.

**That PASS is only worth the table behind it.** T1 reported a clean tree for its whole existence
while blind to four live violations, and the reason a zero is now believable is that twelve
things still make it fire.

### Full chain, 11 August 2026: the first run with tree-scope checks live

Run over the whole published set, 17 tickers, with the roster taken from
`build_index.collect()` rather than the runner's 14-ticker default. Both other runners
default to a subset, and a chain run that silently covers 28 of 34 files is the kind of
partial reading this file exists to record.

```
T1-passdoc-not-at-root     RESULT : PASS, 0 violations
T2-index-date-form         RESULT : PASS, 0 violations
2 of 2 tree-scope checks ran, 0 failing

control 1: C37 on a mutated sentinel -> Pass=False (must be False); as built -> Pass=True
control 2: A10 on an em dash         -> Pass=False (must be False); as built -> Pass=True
control 3: fired on 17 of 34 files

results: 1360 = 1047 on evidence + 24 vacuous + 289 out of scope + 0 failed
```

40 checks over 34 deliverables is 1,360, and 1,047 + 24 + 289 accounts for every row. No
exceptions, exit 0. Control 3 fired on all 17 research reports and on none of the 17
calendars, which carry no computed-figure row.

**The three controls are why the 1,360 passing rows are readings.** Each fails on a mutated
file and passes the file as built, so the chain is discriminating rather than reporting.
The same standard applies to the two tree-scope zeros: G2's 20 cases and G4's 6 are what
they rest on. T1 reported a clean tree over this same repository while blind to four live
violations, and T2 did not exist while the front page contradicted all 34 documents below
it, so neither zero would have been worth anything this morning.

### Added 11 August 2026: the open state outlives the shell

Ledger 4.13. The protocol told a pass to keep `$zzOpen.FileHashes` in a variable for the close.
**Every tool invocation is a fresh shell**, so the variable was gone and the assertion received
nothing. It refused, correctly, but the instruction it enforced was not executable: every pass
following the protocol literally halted at step 5.

An open stamp now persists itself to `harness/R1_open_state.json`, and
`Assert-PublishedSetUnchanged` with no `-IgnoredHashes` reads that baseline. Persisting inside a
read function is normally a smell and is deliberate: the alternative is an instruction the
operator must carry across a shell boundary, and a step that can be forgotten will be.

**Creating a bare form is only safe if it cannot silently degrade**, which was the whole reason
the old design forbade one. `Restore-PassState` throws on a baseline that is missing, partial, or
saved at a different `HEAD`. An empty map is still refused and is still a different thing from an
absent one. An explicit map still overrides the file. A narrowed `-HashPaths` capture is not saved
at all, with a warning, because a partial baseline would let the close certify what it never
watched. `ConvertFrom-Json` returns a `PSCustomObject` whose map indexing yields `$null` SILENTLY,
so the map is rebuilt as a real `Hashtable` and an arm asserts the restored type.

`R4_open_state_arms.ps1` carries nine arms. Arm 6 is the one that separates a real mechanism from
theatre: it corrupts one saved hash and requires the close to halt naming that file. Arm 1 is the
negative control. The end-to-end proof is two separate shells, the second confirming `$zzOpen` is
null and then completing the bare close from disk.

**Two existing arms failed on the first run and were updated, which is recorded rather than done
quietly.** `R1_tests.ps1` and `R1_halt_test.ps1` both matched on the old refusal message for an
absent map. The reason for the refusal changed; the property did not, and the empty-map arm was
not touched because `@{}` is not `$null`. Both were strengthened at the same time, because neither
had checked that the bare form can SUCCEED, and an arm that only ever sees a refusal would be
satisfied by a call that could never work. `-OpenStatePath` was added so those arms point at a
location they control rather than depending on whether an earlier pass left a state file on disk.

Two further defects surfaced from running rather than reading. **The restored state was a
lookalike, not a drop-in**: it carried `Head` at the top level and no `Repo`, and
`Compare-PassState` reported "no Repo property, so nothing was read", which was that instrument
refusing to certify an object it could not read. `TrackedCount` and the repo error now travel with
the saved state, and arm 5b checks both directions, since an arm that only observes silence proves
nothing. **And three arms depended on ambient state**, which is this pass's own defect one layer
out: `R4`'s claimed nothing and failed once the tree was dirty, and `R1_tests.ps1`'s absent-map arm
read whatever baseline a real pass had left on disk, so it refused on a clean machine and was
ACCEPTED mid-pass. All three now use paths and claims they control, and all three suites pass with
the baseline present, absent, and with a dirty tracked path.

That last one was nearly missed. An earlier check of `R1_tests.ps1` reported a blank final line
that reads like success; it was caught only by asserting on the exit code rather than on the last
line of output.

## Movement recorded on 16 August 2026: the v2.00 accent rebind, and a check that forbade compliance

**HOUSE_STYLE reached v2.00 and retired the per-ticker accent.** This pass moved the instruments
to match, and the standing order was kept: specification, then instruments, then files. The 34
deliverables are untouched and are the next pass.

### A14 had inverted, and it was wrong on the day the spec changed rather than at some later drift

`A14` asserted `accent != #1F5993`, because that literal was the template PLACEHOLDER. Section
3.3 now makes the same literal **the standard and the only conformant value**, so the check did
not merely go stale, **it forbade compliance**. Both templates already carry the standard, so the
next original build would have been the first casualty, and the failure would have looked like a
defective build rather than a defective check.

**The check now reads the standard from the specification rather than holding a copy.** The old
form hardcoded the hex, which is exactly what `20_checks.ps1` forbids in its opening line: bind to
a rule, never to a current value.

| | Before | After |
|---|---|---|
| `A14` rule | accent must NOT be `#1F5993` | accent MUST equal the standard read from §3.3 |
| where the value lives | written into the check body | `Get-StandardAccent`, read from the spec |
| `A14` mutation | sets accent TO `#1F5993` | sets accent to `#1F5994`, one unit off |
| `A14` inverse control | none | supplies the standard, verdict must flip |
| in-scope fails | 0 | **34, being the unmigrated set** |

**The 34 in-scope fails are the honest state and not a regression.** Every delivered file carries
an accent derived under the retired rule. `C37` was already reporting the same thing out of scope.

### One definition of where the specification is

`C37` read `HOUSE_STYLE.md` through an **absolute path written into the check body**, which bound
the whole chain to one machine's directory layout. `A14` needed the same document. Two copies of a
location is the shape of ledger 4.62: the fault there was never holding the wrong header policy,
it was holding a second copy of it that nothing compared. Both now read `Get-SpecText`, resolved
from `20_checks.ps1`'s own directory, and an arm asserts no check body carries such a path.

### A17 had never been tested, on any file, and this pass found it by accident

The mutation for `A17-stamp-vs-close` looked for `3 Aug 2026`. The check and all 34 documents use
`Aug 3, 2026`. **It therefore never matched and was scored `N/A` rather than `NO-OP`**, so it did
not appear in the no-op report either; it was visible only as `A17` sitting in the
`NEVER-EXERCISED` list. A mutation that cannot find its anchor is indistinguishable from a rule
that does not apply to the document.

**Repaired by giving the mutation the check's own pattern, character for character.**

```
mutation suite    before          after
  KILLED          1316            1350      +34, exactly A17
  N/A              282             248      -34
  INVERSE-OK        68              68      A14 34, C37 34
  SURVIVED           0               0
  NEVER-EXERCISED  A17 (N/A=34)    none
```

**Every registered check now has a working mutation or inverse control.** That has not previously
been true.

### The aggregate digest, recomputed, and it cannot serve as the gate it is called

`VV_harness_aggregate.py` implements the recipe this file states. Recomputed today:

| | Files | Aggregate sha256 |
|---|---|---|
| Instruments, by the recorded recipe | 838 | `1c1a7d3c96dd5125bf25d4d2953c032c7f2c31540ff1fb2ea4d2a32529b3bf9c` |
| Whole directory, `__pycache__` excluded | 862 | `ce1de2025387e1e4d5300402f8104fa2e2f033dd2d8357aeb0846f66e312a9f9` |

**It does not reproduce the 5 August figure of 467 files and `70ae6c42`, and could not.** Many
passes have added instruments since without updating this file, so the recorded figure is stale
rather than contradicted, and **this implementation is therefore unvalidated by reproduction.**

**The larger finding is that the recipe cannot do the job the file assigns it.** It excludes
`__pycache__` and the results artefacts and nothing else, so every document fetched from EDGAR or
an issuer newsroom counts as an instrument. Measured today, **580 of the 838, being 69%, are not
authored code.** Those arrive by the hundred and change on every research pass, so the figure
called "the figure a pass gates on" moves for reasons unconnected to any instrument changing, and
a gate that always moves cannot report that something moved.

**Authored code alone**, being `.ps1` and `.py`, is **258 files** at
`619be651e16419997a31f402b16111190129a376cb99854183c8dd6c56c61f6a`. That is offered as the figure
a corrected recipe would use and **is not comparable with anything above it**. Correcting the
recipe is a discontinuity of the kind this file records under "Recipe change" and is left for a
pass that decides it deliberately.

Note also that the digest includes the script that computes it, so it moves when that script is
edited. That is correct, and it means a figure recorded here is only meaningful alongside the
state of `VV_harness_aggregate.py`.

### Instruments added

| File | Purpose |
|---|---|
| `VT_accent_state.py` | the control: what A14 and A16 say about all 34 files, under both rules |
| `VU_accent_rebind_arms.ps1` | 16 arms over the rebind, arm 1 the negative control |
| `VV_harness_aggregate.py` | the aggregate recipe, made executable |

### What the arms caught, in themselves

`VU` was first written with the standard colour in `$STD` and the standard-carrying document in
`$std`. **PowerShell variable names are case-insensitive, so those are one variable**: arm 1
overwrote the colour with a 137KB HTML document. Arms 1, 4 and 6 stayed correct only because the
right-hand side of an assignment is evaluated before the assignment lands. The one arm that read
the colour afterwards failed, **and reported it as the spec resolver failing to restore**, which
it had not. An arm can lie about the thing it is testing. Distinct names, not distinct casing.

## Movement recorded on 16 August 2026: the A14 rename, and a runner that could not start

**`A14-accent-not-placeholder` is now `A14-accent-is-standard`.** The old name did not merely go
stale with the v2.00 amendment, it became **backwards**: it named a check that requires the value
the name says is forbidden.

### The rename found a fifth table, and the fifth one was broken

The rebind pass at 4.116 named three tables the key joins. **Searching for the key found five**,
and the two extra were the ones that mattered.

| File | What it holds |
|---|---|
| `20_checks.ps1` | the check itself |
| `82_mutate.ps1` | the mutation and the inverse control |
| `AE_runner_shared.ps1` | the applicability table, which decides in-scope |
| **`AC_run_original.ps1`** | **a startup control, and it was dead** |
| `VU_accent_rebind_arms.ps1` | the arms |

**`AC_run_original.ps1` has been unable to start since the rebind.** It runs a startup control
that mutates the accent **to** `#1F5993` and throws unless A14 fails it. Section 3.3 makes that
the standard, so A14 passed the mutated file and the runner threw
`CONTROL FAILED: A14 passed a file whose accent was mutated to the placeholder` **before doing any
work on any ticker**.

**Its own no-op guard did not catch it, and the reason is worth keeping.** The old replacement
wrote `--accent-light: #1F5993` with single spacing while the files carry aligned spacing, so the
text **did** change, the guard was satisfied, and the control failed on the following line
instead. **A guard that only asks whether anything changed cannot tell a meaningful change from a
whitespace one.**

Repaired to mutate to `#1F5994`, one unit off the standard in the blue channel, matching the
mutation in `82_mutate.ps1`. Verified directly: `ctlDirty.Pass=False`, `ctlClean.Pass=True`.

**Why the rebind pass missed it.** Arm 8 asserted that no check body carries an absolute path to
the specification, and it was given three files to look at. **The runners were not among them**,
and no arm asked the broader question: which live instruments hold an accent literal at all.

### Done as one operation, because the property is all-or-nothing

`WA_rename_a14.py` rewrites all five files in one run with one read-back. 4.116a recorded why:
a rename landing in some tables and not others **drops the check out of scope silently**, because
the runner would report 40 checks and nothing enumerates which one is missing.

Verified after: **41 checks per file, 1394 rows, A14 present as `in-scope` on all 34, 18 arms
passing, 1418 mutants killed, none survived, nothing unexercised.**

### Two of the applier's own assertions were wrong, and both accused correct work

- **`length plausible`** read `len(back) >= len(s) - 5` and failed on three files. The new key is
  **four characters shorter** than the old, so a file with twelve occurrences legitimately loses
  forty eight bytes. Replaced with an exact expected delta. A loose bound that does not know what
  the delta should be cannot tell a correct shrink from a truncation.
- **The straggler sweep** walked the whole tree and reported thirteen files still holding the old
  key. **Every one of them must keep it**: results files in `pass_documentation/`, the ledger in
  `scratch/`, and the frozen snapshots under `preserve/` and `preserved/`. Those record what was
  true when they were written, and renaming inside them would falsify the record. The sweep is now
  over live instruments in `harness/` only.

**That is twice in two passes that an assertion of mine failed against work that was correct**,
after 4.117d recorded the same shape in an arm. The pattern is specific: an assertion written
against an expected state rather than against the rule.

## Movement recorded on 16 August 2026: the population arm, which derives its own population

**4.118b left one item owed: an arm that enumerates what it should check rather than being handed
a list.** `VU` arm 8 was given three filenames, the runners were not among them, and a dead
runner sat undetected for two passes. `WB_live_instrument_arms.ps1` removes that.

### The population is computed from the dot-source and import graph

```
  instruments in harness/   264
  LIVE, in the graph        104    at either end of an edge: loads something, or is loaded
  one-shot, in no edge      160    reported, never failed
```

**A hand-written list of "the files that matter" is the same defect wearing a different hat**:
correct the day it is written, silently incomplete afterwards. A new shared instrument now joins
the population **by being loaded**, with nobody remembering to add it.

The distinction is not a judgement about importance. It is a property of the tree.

### The six arms

| Arm | What it asserts |
|---|---|
| 1 | negative control: each detector fires on a violation and stays silent on a clean form |
| 2 | no live instrument names a check key the table does not define |
| 3 | no live instrument holds an absolute path to the specification |
| 4 | a live instrument holding the standard accent also reads it from the specification |
| 4b | the comment stripper keeps operative literals and removes commented ones |
| 4c | every exemption still applies |
| 5 | the census scanned a non-empty population and the counts add up |
| 6 | the graph reaches the known shared apparatus |

**Arm 2 is the general form of the A14 near-miss.** A rename landing in some tables and not others
leaves a reference to a key nothing defines, and the only symptom is a check quietly not running.
130 key references checked against 41 registered checks, 0 dangling.

**Arm 6 is a floor under the edge parser.** If the parser silently matched nothing, every file
would be classified one-shot and arms 2 to 4 would scan an empty set while reporting success.

### Two defects in the arms, both caught by the arms

**Arm 3 found its own negative control.** The violating sample was written as a literal absolute
path, this file is live, so the file violated the rule it tests. Excluding the file from its own
scan would have fixed the symptom by creating a blind spot in the very instrument meant to remove
one. The sample is now assembled at runtime from fragments.

**The comment stripper deleted every hex literal in the tree.** A hex colour begins with the same
character as a comment, and the first version cut from the first `#` on every line. Arm 4 then
reported **`holders=0`**, a perfectly clean result produced by an instrument that had deleted its
own evidence. **Arm 4b caught it, which is the entire reason arm 4b exists.** The comment now
starts at the first `#` that is not the start of a six-digit hex token.

### What arm 4 found

```
  holders=7   exempt=6   offenders=0
```

**`AB_engine.py` held the eight standard literals as a hardcoded tuple**, and every builder
imports it, so it was the most widely shared duplicate of the standard in the tree. It now reads
them from section 3.3. The values are deduped, because wash and line share one `rgba` prefix and
the old tuple held six for that reason.

**Six per-ticker builders are exempted, named, with the reason recorded**, and arm 4c fails if an
exemption stops applying. They hold the standard as the **before** text of a palette edit whose
after is a derived accent.

**The risk is smaller than it looks, and it is measured rather than assumed.**
`VP_engine_anchor_dryrun.py` reports those six builders' `palette` anchors as
`declared 1, live template has 0`: **111 of 117 anchors match the live templates and the 6 that do
not are all `palette`.** A re-run would therefore **abort on the anchor** rather than quietly
write a derived accent over the standard. The builders are records of how APLD, BTDR and GLXY were
built, and they are already incompatible with the eight-token template.

### State after

```
  CHECKS RUN 1394   IN-SCOPE FAILS 0   group C 0
  WB arms 11/11     VU arms 18/18     VQ engine arms 5/5
```

## Movement recorded on 16 August 2026: section 3.4 gets an instrument, and the dark accent gets measured

**Two colour rules the specification states and nothing tested.** Section 3.4 was enforced by
nothing before or after it was rescued from the retired derivation procedure, which is how it came
so close to being deleted without any instrument objecting. `--accent-dark` was stated by section
3.3 and read by no check.

```
  CHECKS RUN 1428   files 34   per file 42   IN-SCOPE FAILS 0   group C 0
  mutations  KILLED 1452, SURVIVED 0, NEVER-EXERCISED none
  WD arms 17/17   WB arms 11/11   VU arms 18/18
```

### The measurement came before the check, deliberately

4.117a left "run the chain against proposed output before writing" owed. The mirror of that
applies to a new check: **if A30 had gone straight into the chain and failed on 34 files, the
result could not distinguish wrong files from a wrong check.** `WC_tint_probe.py` measured the set
first:

```
  1360 comparisons, being 34 files x 40   0 below the floor
```

**The set already satisfied section 3.4.** The check was then written to agree with a known
answer, and the two arrived at the same number independently.

### `A30-semantic-tints`

Per mode: four foregrounds against paper, canvas, panel-2 and their own tint, plus `--ink` against
the four semantic tints. Twenty comparisons per mode, forty per file.

**Both modes, and the specification says why the dark half is the half that matters**: in light
mode every tint sits within a few percent of white, so clearing paper clears the tint as a
by-product; in dark mode the tints are materially darker and that no longer follows.

**Tokens are located by selector, never by position.** Five blocks declare them: the bare `:root`,
two dark variants, and a print block that forces the light values back. A positional reader would
take whichever the author happened to put first.

### THE FINDING: the standard dark accent clears its floor by 0.086

A16 now measures `--accent-dark` against dark paper, using the pair form rather than
`Get-Contrast`, which measures against white and would have reported the dark accent's contrast
against a ground no reader in dark mode ever sees.

```
  #3987D5 on #141C24 = 4.586:1     floor 4.5     margin 0.086
```

**Section 3.3 states 7.22:1 on paper and 6.71:1 on canvas and states no dark figure at all**,
because when the standard was chosen at v2.00 nothing measured the dark half. It passes, and it
passes by less than a tenth. That is worth knowing before anyone adjusts the dark palette.

### The first mutation was not isolating, and the arm caught it

`#1A4636` was chosen because it sits near the dark `--pos-bg`. **In dark mode a foreground must be
LIGHT to clear anything**, so it failed all four grounds at once: paper 1.62, canvas 1.71,
panel-2 1.77, own tint 1.17. It killed A30, so the mutation report looked correct, **while proving
nothing about the limb section 3.4 actually adds** and only re-testing the general contrast limb
A16 already covers.

**An isolating window exists, and the reason is measurable**: the dark `--pos-bg` is LIGHTER than
dark paper, luminance 0.03422 against 0.01107. So a foreground can clear the three surfaces and
still fail its own tint, which is precisely the case the rule was written for.

```
  #36986D   paper 4.81   canvas 5.08   panel-2 5.26   own tint 3.48
```

Arm 4 asserts that isolation rather than trusting the comment.

### The arithmetic is checked against figures nobody here wrote

The specification states `--ink` at 16.9:1 on paper and `--ink-dim` at 7.25:1, derived without
reference to this harness. `Get-ContrastPair` reproduces both, at 16.92 and 7.25. **That is the
one place the contrast arithmetic can be validated against an independent source**, and every
threshold in A30 rests on it.

### The population arm caught the next file written

`WB_live_instrument_arms.ps1` was built one pass earlier to find live instruments holding the
standard accent without reading it from the specification. **The first thing it caught was
`WD_tint_arms.ps1`**, written this pass, whose arm 7 hardcoded `#1F5993`. Fixed to read the
resolver.

## Movement recorded on 16 August 2026: the first-build declaration, and the templates are stuck at v1.99

**The write scope was revision-only and nothing could add a 35th deliverable.** `-RevisedPaths`
refuses a path that does not exist, and an undeclared deliverable lands in `published` and halts.
Both are correct for the files that exist, and together they refused every new ticker by mechanism
rather than by rule.

### `-BuiltPaths`, the mirror of `-RevisedPaths`

```
  -RevisedPaths    the path MUST exist at the open      and may change by the close
  -BuiltPaths      the path MUST NOT exist at the open  and MUST exist by the close
```

Loosening `-RevisedPaths` to accept an absent path was the obvious alternative and is worse: that
same refusal is what catches a typo'd filename, which is the error it was written for.

Seventeen arms in `WK_build_mode_arms.ps1`, most of them on what must still be refused, because a
widening that errs on the permissive side does not fail loudly. It accepts work it should have
stopped and every downstream check reports what it always reports.

| Refused | |
|---|---|
| a built path that already exists | use `-RevisedPaths`, which bounds it against its own prior bytes |
| a revised path that does not exist | unchanged |
| a path declared in BOTH modes | opposite preconditions, so declaring both states no scope |
| an untouchable name | the specification and both templates stay unreachable |
| a non-deliverable filename | a typo is a refusal, not a silent non-declaration |
| a declared build absent at the close | `BUILD DECLARATION UNFULFILLED` |

**Classification is tested through `Get-DirtyClass` directly**, not only through `Get-PassState`,
because a guard that holds only at the API boundary is one direct call away from not holding.
A template declared as a build still classifies `published`, and a path declared in both modes
yields `revised`, the class with the stricter precondition.

`R4_open_state_arms.ps1` and `RE_revision_arms.ps1`, which guard this same mechanism, both still
pass.

### THE FINDING: both templates carry v1.99 sentinels

```
  34 deliverables   v2.01
  2 templates       v1.99
  specification     v2.01
```

**Section 11 step 2 builds a new ticker by copying the templates**, so the first build this pass
just enabled would produce v1.99 sentinels and `C37` would fail the new pair on sight.

**`C37` cannot see this**, because it runs over the 34 deliverables and the templates are not
among them. `R1_tests.ps1` does see it, and has been failing on it since v2.00 landed. The
failure is pre-existing and was surfaced here only because a change to the write scope is worth
a full regression run.

The templates are untouchable by every mode, build included, so moving them needs the same
authorisation the specification does.

`W2_protocol_arms.py` also fails, pre-existing, naming three calls the protocol document shows an
operator that no arm makes. None involves the new parameter.

### The regression sweep destroyed this pass's own open state

The close refused with `OPEN STATE FAILED: no saved open state`. **`R1_tests.ps1` and
`W8_two_hop.ps1` open and close their own passes against the same
`harness/R1_open_state.json`**, so running the protocol arm suites as a regression, which is the
careful thing to do after changing the write scope, is what removed the live baseline.

`WK_build_mode_arms.ps1` anticipated this for itself and backs the file up before arm 4 and
restores it after, and its own arm confirms the restore. **The older suites do not**, and there
is no reason they would have: they predate any convention about it.

**Verified independently instead**, against values recorded before this pass began:

```
  group hash        f2bcf472...  matches the value at the v2.01 close
  HOUSE_STYLE.md    5fc7a5f2...  matches
  both templates                 match
  deliverables      34
  dirty             HARNESS_BASELINE.md only
```

That proves no deliverable, no template and no specification moved. **It is weaker than a close
in one specific way**: it compares against figures a human copied forward rather than a baseline
the mechanism saved, so it rests on those figures being right.

**Owed: the arm suites should save and restore the open state, as `WK` does.** Until they do, a
pass that runs them as a regression loses its own baseline, and the more careful the pass, the
more likely it is to hit this.

## Movement recorded on 16 August 2026: both templates moved to v2.01, and the engine repointed

**Written under explicit user authorisation**, on the same footing as the specification edits. The
templates are untouchable by every mode, build included, so the close halted on their hashes and
that is the guard working rather than a defect.

```
  before   34 deliverables v2.01   2 templates v1.99   spec v2.01
  after    36 files at v2.01
```

**Why it became urgent rather than staying inert.** Section 11 builds a new ticker by copying the
templates. Until `-BuiltPaths` landed, nothing could add a ticker at all, so a stale template
sentinel could not reach a delivered file. It was the first thing a first build would have
carried, and `C37` would have failed the new pair on sight.

### Four parts, and the third is the one that was easy to miss

| | |
|---|---|
| 1 | the two live templates, two sentinel tags each |
| 2 | a new preserved snapshot at `templates_v201` |
| 3 | **`AB_engine.py` repointed to it, checksums moved** |
| 4 | `templates_v199` left frozen |

**The engine does not build from the live templates.** It loads preserved copies and verifies them
by checksum, deliberately, so a build cannot drift under a template edit. **Updating only the live
files would have left every future build still emitting v1.99**, and the checksum guard would have
kept passing, because the preserved copies would have been untouched and self-consistent with
their own recorded hashes.

`templates_v199` is not superseded and was not deleted. It is the record of the shape the 34
existing deliverables were built from, and a snapshot that changes is not a record.

The script deliberately does **not** edit `AB_engine.py`. It prints the new checksums and stops,
so the guard is moved by a hand that has seen the values rather than by the same run that
produced them.

### R1_tests.ps1 now passes

It had been failing on sentinel uniformity since v2.00, and was the only instrument that could
see the divergence: `C37` runs over the 34 deliverables and the templates are not among them.

### A CORRECTION to the entry above this one

That entry says `R1_tests.ps1` and `W8_two_hop.ps1` both destroy the live open state. **`R1_tests.ps1`
does not.** It was run again in this pass and the open state survived intact, still carrying the
pre-edit template hash. On that evidence the earlier destruction was `W8_two_hop.ps1` alone.

The correction is made because a wrong entry about which instrument is unsafe is worse than no
entry: it would send a later pass to harden the wrong file and leave the real one alone.

### Added 19 August 2026: the table-order check joins the chain as tree-scope check T4

Three separate passes on 19 August 2026 each left a dated table holding a row against the order
that table itself keeps. WULF's coverage row was restruck from 6 July to 9 July and left where it
sat; NUAI's calendar took three actions of 17 August at position 3 while its own companion report
appended them correctly; IREN's fourth catalyst band ran December, July, May against a rule the
file states about itself twice. **Every one of those passes cleared every control its applier
runs**: the anchor matched once, the replay was byte-identical, the tag balance was derived from
the plan, the line terminator held by count, and thirty read-backs came back from disk. **None of
those can see an ordering.** The first was found by rendering a table and reading the dates down
the column, on the following ticker, after the file had already been written.

`ZZ_table_order_check.py` closes that. It is registered as **T4** in the tree-scope block rather
than as check 43, for the reason recorded there for T1 and T2, and for one more that is specific
to it: **the per-file table holds PowerShell scriptblocks**, and reimplementing the ordering logic
in PowerShell beside the Python that already holds it would be a second copy of one rule that
nothing reconciles, which is the defect ledger 4.62 records. One reading, run once, over the set.

**The per-file arithmetic is unchanged and that was measured, not assumed.** The chain reports
`CHECKS RUN: 1512   files: 36   per file: 42` after the change exactly as before it, and the
tree-scope line moves from `3 of 3` to `4 of 4`.

It keys on markup rather than on a heading. Its first version looked for a heading reading
"Third-party coverage" and found ten tables; measured across the set that heading is one of at
least fourteen wordings, and **it would have missed the very table that produced the next
defect**. The rule is now `td class="when"`, which is 1,057 cells across 73 tables in all 36
deliverables, and it segments on the catalyst identifier so a calendar's D, S and R sequences are
three orderings rather than one.

| File | What it holds | Bytes | sha256 |
|---|---|---|---|
| `ZZ_table_order_check.py` | tree-scope check T4: every dated table holds its own ordering, with its reach reported and pinned | 16,049 | `09ee9c3c7978694f89525668f25862f2984a7aa10798f14c2d8c134bf0d7f7f5` |
| `AE_runner_shared.ps1` | as before, plus the T4 row, the printed check roster and the stderr guard | 23,555 | `8391d073f0d8c1ab49d142a3142164d4bbd12a70a802c222833826d6767e7f7b` |
| `G5_treescope_arms.ps1` | as before, plus arms 6 to 10, arm 5 widened and arm 7 strengthened | 21,239 | `a0244b3155d899222e95595d32214325caefc0665a7a4ef6e2e7c3fb3722a497` |

`AE_runner_shared.ps1` was `9d208d4c04a18789...` before this pass and `G5_treescope_arms.ps1` was
`60dc548cfc0917c1...`. Both prior copies are at `preserve/2026-08-19_zz_into_chain/`.

**ONE GAP IN THAT PRESERVATION, STATED RATHER THAN LEFT TO BE INFERRED.** `ZZ_table_order_check.py`
carries the same hash before and after in that directory, because it was taught the directory
calling convention **before** the pass opened and was preserved afterwards. So no copy of its
pre-wiring state exists. Nothing depends on recovering one: the instrument was written the same
day, the change is described above and in the results file, and the convention it adopted is G4's.
But the checksum row would otherwise read as a file that did not change, and it did.

**What the wiring is protected by, because a row in a table nothing reads is not a check.** That
sentence is `AE_runner_shared.ps1`'s own, written after T2 was registered in a table the delivery
runner was not reading. Three arms in `G5_treescope_arms.ps1` now stand against the same thing:

- **arm 5** requires every tree-scope guard present on disk to be registered. It had to be
  widened: it matched `G<n>_` names against a list of three, and `ZZ_table_order_check.py` is not
  a G-file, so nothing would have required it to be registered. Verified load-bearing by removing
  the T4 row from a copy of the table, at which point the arm names ZZ as unregistered.
- **arm 6** requires T4 to fire **through the runner**, on the real WULF file exactly as it stood
  between the two appliers of 19 August, and requires its id to reach the thrown message.
- **arm 7** requires T4 to **pass** the same file once corrected, so the guard discriminates
  rather than refuses.

`ZZ` keeps its name rather than being renamed into the `G` convention. Three results files and
three ledger entries written the same day name it, and the record is worth more than a tidy
prefix; the standing hazard says an instrument prefix is not a namespace.

**What T4 cannot see, stated so a later pass does not assume otherwise.** It reads an ordering and
nothing else. A table below its 80% threshold is reported `unordered` and passed, because a
grouped table is not a defect and this instrument does not get to impose a sort on one. A row
whose date will not parse is excluded and counted as `unread`. Neither is a fault; both are limits.


#### The same day, one layer out: T4 was registered in a chain of three runners and reached one

Registering the row above was not wiring the check, and this file said so about a different check
three weeks earlier: **a row in a table nothing reads is not a check.** The question never asked
was which runners read it. Three runners score the 36 deliverables against the per-file table. The
answer, with every arm green and the delivery runner reporting `4 of 4 tree-scope checks ran`, was:

| Runner | Calls the tree-scope block | Declared `ExpectChecks` | Live table |
|---|---|---|---|
| `D2_run_v176.ps1` | yes | 42 | 42 |
| `T2_run_conform.ps1` | yes, 21 lines past a throw it could not survive | **40** | 42 |
| `AC_run_original.ps1` | **no, not once** | **40** | 42 |

T4 ran in one runner of three, and **T3, registered on 12 August 2026, had never run in the other
two either.** `AC_run_original.ps1` could score 1,512 file-check pairs, print a complete looking
green result, and have executed none of T1 to T4.

**One defect was concealing the other, and that is the part worth keeping.** A stale
`ExpectChecks` fails CLOSED, which reads as safe. But it throws on guard 1, twenty lines above
where the tree-scope call sits, so the runner never reaches the call and the missing call cannot
be observed to be missing. Correcting the count alone would have converted an accident that failed
loudly into a gap that passed quietly. Both were corrected together, in that knowledge.

**What now holds it shut.** Arms 1 to 8 all prove the *block* behaves. Not one of them could see
whether anything *calls* it, which is precisely the layer the recorded defect has now lived at
twice.

- **arm 9** reads every `*_run_*.ps1` declaring `$ExpectChecks`, requires at least three, and
  requires each both to contain the call and to declare a count equal to `$CHECKS.Keys.Count` as
  loaded from `D1_checks_v176.ps1`. Proved load-bearing against a copy of the harness carrying the
  pre-correction `AC_run_original.ps1`, where it names that file and lists the four checks it
  would have skipped.
- **arm 8** holds the stderr hazard shut. All three runners set `$ErrorActionPreference = 'Stop'`,
  and PowerShell 5.1 wraps every stderr line from a native executable in a `NativeCommandError`
  when `2>&1` merges it into the success stream. Under `Stop` that record **terminates the loop**:
  checks after it never run, and the operator sees a `NativeCommandError` instead of the `OnFail`
  sentence written for the defect. `ZZ_table_order_check.py` is the only check in the table that
  writes to stderr, and it does so on exactly one path, `REFUSED`, the moment its own
  preconditions fail. The newest check could therefore silence the block that runs it, precisely
  when it had something to say. The preference is now lowered for the invocation alone and
  restored on the next line. **This is not theoretical: arm 10 was first written calling `python`
  directly and died on the refusal it had deliberately provoked, within the hour, from outside
  the block.**

**The reach floor, because a clean result on part of the set is not a clean result on the set.**
T4 passes any sequence it did not adjudicate: one with fewer than three dated rows cannot show an
order, and one below the 80% threshold is grouped rather than sorted. Measured on the shipped set
that is **63 of 109 sequences, and 162 of 531 dated rows, passed without being read**, and the
verdict line could not tell them from sequences read and found clean. Reach can therefore fall
silently, and **an in-place restrike, the exact edit T4 exists to catch, is one of the things that
makes it fall.** `EXPECT_ADJUDICATED = 46` pins it the way `$ExpectChecks` pins the check table: a
fall is a refusal, and raising or lowering the number is a deliberate hand edit with a reason.
It binds only on a run that read the full set of 36, and a shorter run says so in its own output
rather than standing the control down in silence. **arm 10** runs a copy of T4 with the floor
raised by one and requires the refusal, then runs the shipped copy and requires the floor to be
reported as applied.

**The registered Id now prints on a green run.** Each check prints its own banner, so a passing
transcript read `ZZ-table-order-check` and never the word `T4`. You could not answer "did T4 run?"
from a green result without knowing which script T4 is, which is the question this block exists to
answer, and the question nobody could answer about T3 for a week. The block now prints its roster
before it starts, then `[Id] -> script` as each one goes.

**Measured after, not assumed.** All three runners exit 0. Each reports `4 of 4 tree-scope checks
ran, 0 failing`, and `CHECKS RUN: 1512   files: 36   per file: 42` is unchanged. G5 passes 10 of 10.

| File | Bytes | sha256 | Was |
|---|---|---|---|
| `AC_run_original.ps1` | 13,877 | `87ced4e8c929b205...` | 12,645 `63a33cf8443f22cc...` |
| `T2_run_conform.ps1` | 9,839 | `48df89b4cdd91140...` | 9,839 `b34792d24e3d5931...` |

`T2_run_conform.ps1` is **the same size before and after**, because `40` and `42` are both two
characters. The row is here so a later reader comparing byte counts alone does not conclude the
file was untouched. Both prior copies are at `preserve/2026-08-19_zz_into_chain/`.

**Not swept, and named rather than left to be found.** This file carries six em dashes and one
section sign from passes predating the no-em-dash rule. They are untouched: this pass rewrites
checksum rows, and quietly rewording historical prose is the same falsification that kept the
rewrite scoped to this section in the first place. A sweep is its own pass.


### Added 20 August 2026: T6, the first check that reads a citation back against the registry

**Of the 46 checks this project shipped, 42 per-file and 4 tree-scope, not one was a
source-coverage check.** `HOUSE_STYLE.md` L250 has required "Cite form and date" throughout, and
nothing had ever read a citation back against the filing index. The first instrument that did
found **five citations, in three files, to filings that were never made**:

- **WYFI, both files, the same sentence in each.** "Forms 8-K dated August 8, 2025, December 18,
  2025, **March 26, 2026, May 14, 2026**, May 21, 2026, May 27, 2026 and June 10, 2026".
  WhiteFiber's index holds thirteen 8-Ks and none on either of those dates, on the filing date or
  the date of report. **Those two dates are the days it filed its 10-K and its 10-Q**, both cited
  correctly a few clauses earlier in the same sentence, and both also carrying a press release
  named in that same sentence. The likeliest mechanism is that a results date was assumed to
  carry an earnings 8-K. WhiteFiber does not file one.
- **DGXX's calendar.** "Form 10-K/A, April 27, 2026, Part III". Digi Power X filed **nothing at
  all** on 27 April 2026 and holds exactly one 10-K/A, filed 30 April.

`ZF2_citation_exists.py` is registered as **T6**, and the number is not a typo. `T5` is held by
`harness/T5_stamp_collateral.py`, which the ledger names in roughly fourteen places; 4.154e
records it dead and 4.154h carries it as owed, which makes the name **more** spoken for rather
than less. A reader meeting two T5s cannot tell which the record means. Same decision, same
reason, as ZZ keeping its name.

**Four rules, each bought with a measured false positive.** The first version of this scan
returned **228 hits across all 18 tickers**, which measured the extractor and not the set.

| Rule | The false positive that produced it |
|---|---|
| Read **both** dates | An 8-K carries a date of report distinct from its filing date. BGDE's "27 April" resolves only on `reportDate`. Judged on `filingDate` alone it was written up as a phantom filing **in this project's own findings file, wrongly, on the morning of the day this was built** |
| **Attribute** before testing | **5 of 14** candidates were correct citations of a counterparty's filing: CIFR, HUT and WULF citing BGDE's 3 June 8-K, IREN citing **Bakkt's** 8-K, CLSK citing **BGDE's** 10-Q. A check that tests every citation against the covered ticker's index calls all five defects |
| Exclude **period ends** | "Form 10-Q for the quarter ended March 31, 2026" names a period, not a filing. This class alone produced most of the original 228 |
| Match the **form** | Where the entire real yield was. All five confirmed faults are dates on which a filing **does** exist, of a different form or on a neighbouring day |

**The document log is not scanned, and that is a rule rather than an exemption.** §9.2 *requires*
a correction to quote what it corrected. The first run of T6 after its own corrections were
applied reported five faults, and **all five were the log entries recording those very
corrections**. That is ledger 4.176's note that "T5 read its own answer back as a defect",
recurring. The exclusion is **counted and reported**, 63 citations on the shipped set, because a
check that quietly stops reading part of a file is how reach falls unnoticed.

**Measured, not assumed.** 430 citations in filing-date position, **429 adjudicated against a
registry, 1 not**, across 23 cached issuer indexes holding 13,008 filings. G5 passes **12 of 12**.
All three runners exit 0 at `5 of 5 tree-scope checks ran, 0 failing`, and
`CHECKS RUN: 1512   files: 36   per file: 42` is unchanged, since this adds no per-file check.

**Arm 5 had to be widened again, which is the third time and is now a documented cost.** It
matches guard scripts against a hand-kept list, so a newly added guard is not required to be
registered until someone adds it. ZZ sat in that gap until 19 August; ZF2 sat in it for the
length of one pass. The list is explicit rather than a wildcard because "every .py in harness"
would sweep in appliers and probes.

**Arms 11 and 12** put T6 on the T4 pattern: it must fire through the runner on `WYFI`'s report
**exactly as it stood before the correction**, taken from `preserve/2026-08-20_citation_exists/`
rather than from a synthetic string, and it must **pass** the corrected file while adjudicating
at least one citation in it, because a check that read nothing also does not throw.

| File | Bytes | sha256 |
|---|---|---|
| `ZF2_citation_exists.py` | 13,873 | `a2747d1e4ccb61b2...` |
| `ZG2_citation_repair.py` | 13,185 | `aec2634add51835c...` |
| `AE_runner_shared.ps1` | 24,612 | `ef8832c429882c5d...` |
| `G5_treescope_arms.ps1` | 24,844 | `afb9633c1267ec69...` |

**One carried ledger item was discharged as a side effect, and it is named rather than left to be
found.** `WYFI_Catalyst_Calendar.html` carried **one bare LF among 1,850 CRLF**, which is 4.151e.
`ZS_revision_runner` refuses a mixed source outright rather than guessing, and no plan can repair
it through the runner because the refusal is computed from the source before any edit is
considered. So the terminator was repaired first, as its own asserted act, on the bytes, with the
context checked before the write so a stray LF elsewhere could never be silently normalised. It
is **apparatus** and earns no log entry in the file. The file is now uniform CRLF at 1,851.

**What T6 cannot see.** It decides **existence and nothing else**: that a filing of the cited form,
by the cited issuer, exists on the cited date. **A citation can pass T6 and still be the wrong
document for the claim beside it.** It also cannot adjudicate a citation whose issuer it cannot
establish, and it says how many of those there were rather than counting them as clean.


### Corrected 20 August 2026: the push guard rejected the class the close accepts

`Test-PushPreconditions` **could not pass after any declared revision, and had not been able to
since ledger 4.29 introduced the mode.** It was found at the push gate of the T6 pass, refusing a
tree `Assert-PublishedSetUnchanged` had certified one command earlier.

The two answered the same question through different accessors:

| | Accessor | Returns |
|---|---|---|
| `Assert-PublishedSetUnchanged`, L619 | `Get-ProceedableDirtyClasses` | `apparatus, revised, built` |
| `Test-PushPreconditions`, L1581 | `Get-ProceedableDirtyClass` | `apparatus` |

**The comment directly above the defect is the finding.** It says the block goes through
`Get-DirtyList` "so there is one derivation of which dirty paths stop a push and not two". It took
the **classification** from there and then re-implemented the **acceptance** rule inline against
the singular. **That was the second derivation, in the sentence claiming there was not one.**

**It was latent, and latent in the worst way.** A clean tree carries nothing classified `revised`,
so the guard passed on every ordinary day and failed only during a revision, which is the one
moment it was being asked to do its job.

**Adjudicated before being changed, because "the guard is deliberately stricter" was a live
answer.** Three tests: nothing in the instruments or the ledger states that a push is stricter
than a close; the plural accessor exists precisely to carry `revised` and `built`, added with them
at 4.29; and accepting `revised` grants **no permission the close has not already granted**, since
`Assert-PublishedSetUnchanged` proves every **undeclared** deliverable byte-identical by hash and
only paths declared at the open stamp can ever classify `revised`. The third is decisive.

**Four stale sites, not one, and the fourth is why the others could not be left.** The singular has
six call sites. Two are correct: `R1_pass_state.ps1:61` builds the plural from the three singulars,
and `R1_halt_test.ps1:86` asserts a claimed path is `apparatus` **specifically**. The other four all
ask "which dirty paths stop a hop" and all read the singular: the guard itself,
`R1_halt_test.ps1:60`, and `R1_tests.ps1:518` and `:592`.

**`R1_tests.ps1:518` is coupled to the guard.** It computes the bad-path set with the singular and
then requires `Test-PushPreconditions` to have reported. Correcting the guard alone would make that
test compute a fault the guard no longer reports and **throw a false failure during any revision**.
Fixing one and not the others is the partial sweep this project's protocol warns about, in an
instrument rather than a document.

**Arm 12 in `RE_revision_arms.ps1`, and it is the arm the other eleven could not stand in for.**
They all prove the close-out assertion behaves. **Not one had ever called
`Test-PushPreconditions`**, which is why a guard broken for the length of the revision mode's
existence was found by a person at a push gate rather than by the suite.

It asserts both halves: the guard must **accept** a declared revision, and must still **stop** an
undeclared dirty deliverable, because a guard that accepts everything passes the first half
perfectly. **Proved load-bearing rather than asserted:** run against the preserved pre-correction
`R1_pass_state.ps1`, it fails with `ANY_Catalyst_Calendar.html [revised] against an expectation of:
every dirty path in the apparatus class`, and the instrument was restored hash-identical.

**What is synthetic in that arm and what is not, stated because `Get-DirtyList`'s own comment
records a gate proved only against a fixture shaped to fit.** A clean tree carries nothing
classified `revised`, so the dirty **row** is fabricated. Its **class** is not: it comes from the
real `Get-DirtyClass` against a real declaration. The **state** is a real `Get-PassState` result,
so `Repo.Dirty` sits exactly where the guard looks, which is the difference that produced that
comment.

| File | Bytes | sha256 | Was |
|---|---|---|---|
| `R1_pass_state.ps1` | 92,098 | `8c22c77a1cf326df...` | 90,904 `f225991e333fac24...` |
| `R1_tests.ps1` | 80,914 | `74aa28bd6fc980d8...` | 80,890 `06c0c49d8ab4243c...` |
| `R1_halt_test.ps1` | 12,025 | `1af128dc84fd83cd...` | 12,013 `0ffd0384a1b42fae...` |
| `RE_revision_arms.ps1` | 20,235 | `bf6a8e4f06fa6f99...` | 16,182 `76f491b79d26419e...` |

Prior copies at `preserve/2026-08-20_push_precondition_class/`.

**Measured after.** `RE_revision_arms` **12 of 12**, `R4_open_state_arms` **12 of 12**,
`RV_stamp_basis_arms` **8 of 8**, `G5_treescope_arms` **12 of 12**, `R1_tests` PASS,
`R1_halt_test` PASSED. Chain `5 of 5` tree-scope and
`CHECKS RUN: 1512   files: 36   per file: 42`, unchanged.


#### And the suite destroyed the very baseline this pass was closing against

**`RE_revision_arms.ps1` arm 10 wrote to the LIVE open state path and then deleted it
unconditionally.** So running the revision arms during an open pass destroyed that pass's
baseline. It did exactly that here: the arms were run to prove arm 12 load-bearing, and the close
then refused with `OPEN STATE FAILED: no saved open state`. **The refusal was correct.**
`Restore-PassState` fails safe on a missing baseline, which is the one property that made this
recoverable rather than silent.

**The file's own header already claimed the opposite**, in terms: the arms "drive a SCRATCH
baseline path so they never touch the live session's open state, and so their verdicts do not
depend on whether a real pass happens to have left one." **Arm 10 was the exception, and nothing
compared the claim against the code.**

Arm 10 genuinely needs the live path, which is why it is the outlier: it tests that a close
inherits the open declaration, and `Get-PassState -Stamp 'close'` reads `Get-OpenStatePath` and
**takes no override**. So the correct fix is not a scratch path but **backup and restore**, and
that idiom already existed twice in this harness. `R4_open_state_arms.ps1` keeps a `.armbak`;
`WK_build_mode_arms.ps1` reads the file into `$zzBackup` and writes it back in a `finally`. **Two
of the three suites that touch the live path did it right and the third was never compared with
them.**

**Proved rather than asserted.** A sentinel open state was planted, the suite run, and the file
required to survive: 12 of 12 arms pass **and** the sentinel is byte-identical afterwards.

**How this pass closed, stated plainly rather than papered over.** The first open stamp was gone
before the close, so the published set was established **independently and more strongly**: 0 of
36 tracked deliverables differ from the committed tree at `e99d276`, and the three gitignored
names hash exactly to the values the destroyed stamp had printed. A second stamp pair was then
taken to close the ceremony, and it **reproduced the first stamp's group hash
`7c988a8f67c655b5...` and all three gitignored hashes**, which corroborates the independent
reading rather than replacing it. **No deliverable was written by this pass at any point**, and
the only tracked path it touched is this file.


### Added 20 August 2026: the family that had a registry and nothing watching it

**The specification was amended first, and that ordering is the mechanism rather than good
manners.** `HOUSE_STYLE.md` is gitignored and its hash is carried in the pass baseline, so
amending it mid-pass halts the close on a changed ignored file. It moved **`1c21e0cc` to
`0b14d70f`** before this pass opened, the open stamp recorded the new hash, and the close verified
against it. Ledger 4.176(e).

**Three approved changes, and the second is why the first could not ship alone.**

1. §12.2's registry table gains a row for **Company material outside EDGAR**, naming the issuer's
   events-and-presentations page for decks and webcasts and its news page for operational updates
   and transcripts, requiring the page and the date read, and stating that **a page returning a
   script shell is a recorded gap, not an empty result**. That last clause is not decoration:
   CLSK hit exactly that on 3 August 2026.
2. §5's `FILED` row widened. It read "Stated in an SEC filing or company press release. Cite form
   and date." **A deck posted to an IR site is neither, and has no form**, so even a pass that
   read one had no compliant way to cite it. Naming a registry without this would have sent
   passes to a source they could not then quote.
3. A caution: issuer material is the issuer's own selection, dating it is not optional, and
   comparables and per-megawatt economics the issuer chose for itself are `ESTIMATE` rather than
   `FILED`. **Both halves have already cost this project once each**, in VIP's capital-structure
   slide and SLNH's withdrawn 159 MW.

**The family stays CONDITIONAL**, matching every other family in §12.2. That decision was taken
deliberately and it is what keeps `ZH2_ir_material.py` out of the tree-scope table: a conditional
family cannot fail a build, and registering it would turn the chain red on a set that breaks no
rule.

**Why this is NOT an extension of `ZK_reports_inbox.py`, which is where the work was expected to
go.** ZK's load-bearing sentence is *"Location is the record of what was read, not a date
comparison. A file that has been used is MOVED, deliberately, by the pass that used it."* That
principle is correct and it is why ZK works. **It also does not transfer**: this family has no
files and no inbox, and the question is whether a web page was visited, which can only be an
assertion with a date. Putting a date-comparison model inside ZK would make one instrument assert
two contradictory things about what counts as evidence.

**It ships with a recording verb, and would not have shipped without one.** A tracker nobody can
satisfy reports the same red forever and trains its reader to skip it. `--record` requires the
ticker, the page and the result, and refuses each omission by name; the page is mandatory because
the amendment says "Name the page and the date it was read", and a record without it is the
unverifiable form §12.2 calls a gesture.

**Four states, and each is a different claim.** `NEVER` is no record at all and is **not**
"clean". `STALE` means the ticker has been assessed since the check without it being repeated.
`GAP` means reached and unreadable, counted apart from `CURRENT` because §12.2 says an unavailable
source is a recorded gap and never a completed check. `CURRENT` is checked on or after the last
assessment.

**Measured on the shipped set: `NEVER 18, STALE 0, GAP 0, CURRENT 0`.** That is the true state and
no record was fabricated to soften it. A demonstration record was written to prove the verb works
and then removed, because nothing has actually been checked.

**Arm 1 is the one that matters** and the other ten defend it: an unrecorded ticker must read
`NEVER` and never `CURRENT`, because the failure this instrument exists to catch is a family
nobody checked being reported as though it had been. Arm 5 requires a `GAP` recorded **today**
to stay `GAP` rather than becoming `CURRENT` on recency alone.

| File | Bytes | sha256 |
|---|---|---|
| `ZH2_ir_material.py` | 8,683 | `394c629e829e7c5a...` |
| `ZI2_ir_material_arms.py` | 5,412 | `6a46a69f864f7de3...` |
| `HOUSE_STYLE.md`, amended | 150,072 | `0b14d70fdd12624e...` |

Prior specification at `preserve/2026-08-20_spec_ir_registry/`.

**What this does not do.** It does not sweep anything. Nine tickers have never had a deck opened
and all eighteen now read `NEVER`; closing that is a separate decision and a separate pass. It
does not make the check mandatory. It adds no check to the chain, which is unchanged at
`5 of 5` tree-scope and `CHECKS RUN: 1512   files: 36   per file: 42`.


#### Swept 20 August 2026: the family goes from NEVER 18 to CURRENT 18

The registry row landed in the morning and swept nothing. This is the sweep. **Every covered
ticker now carries a dated, evidenced record naming the page that was read**, and 18 of 18 issuers
turn out to publish decks, ten of them dated within 21 days.

**The hypothesis this pass carried was wrong, and it is recorded as wrong.** The brief said that a
set where most pages turned out to be `gap` would be worth more than a thin set of greens, because
it would mean the registry names a source this project cannot reach. That did not happen: 17 of 18
pages were retrieved and read. **The source is reachable.** What the sweep found instead is
narrower and sharper.

**REACHABLE IS NOT REACHABLE BY PLAIN RETRIEVAL. Seven of eighteen hosts defeat a plain fetch, and
three of those fail silently rather than honestly.**

| Failure mode | Tickers |
|---|---|
| Needs a JavaScript-rendering browser | CLSK, NUAI, RIOT, GLXY |
| Needs a desktop User-Agent or another client | BGDE, BKKT, VIP |
| Plain fetch sufficient | ANY, APLD, BTDR, CIFR, DGXX, HUT, IREN, MARA, SLNH, WULF, WYFI |

**CLSK is the one to remember, and it is a false NEGATIVE rather than a false positive.** A plain
fetch returns **HTTP 200 with a 168 KB body containing the literal string "No presentations
available"**, served from an empty-state template. A plain-fetch sweep does not gap there; it
**manufactures a false `none` on a ticker that had posted a deck on 10 August 2026.** That is
exactly what §12.2's last clause was written for. **It is the same host that failed this way on 3
August 2026**, recorded in `CLSK_Build_Findings.md`: the same trap, the same issuer, three weeks
apart.

NUAI returns 200 with 143,973 bytes of headings and `Loading...` placeholders; RIOT returns 200
with a 177,579-byte body whose content region is empty. **A status-or-size heuristic scores all
three as content.** Two further traps return 200 with the wrong content entirely: one issuer's
`/investor-relations/investor-presentations` serves a **27 KB 404 body**, and a superseded
`ciphermining.com` path redirects to a homepage and returns 200 with 55 KB.

**Three structural facts a URL-only registry cannot carry.** The canonical path the row's wording
implies, `/events-and-presentations`, **404s on at least five hosts** (BTDR, GLXY, MARA, RIOT,
DGXX), so the page is discovered per issuer and never guessed. The function is **split across two
URLs on ten issuers**, decks on one page and events on another. And **a URL alone does not
reproduce the read on seven of eighteen**, so the retrieval method is part of the record. It is
carried in the note here because a structured field is a change to `ZH2_ir_material.py` that this
pass's brief did not claim.

**One override of the sweep's own synthesis, and it rests on an independently verified fact.** The
synthesis reclassified DGXX from `none` to `gap`. It is recorded **`read`**. DGXX has no
events-and-presentations page at all: its `sitemap.xml` enumerates every route and contains none,
and four direct probes 404. Its own "Events & Presentations" card is **mis-wired** to a governance
vault holding seven charters and no deck. **But the deck exists**, at a single overwriteable slug,
verified here by its headers: **HTTP 200, `application/pdf`, 57,305,280 bytes**, PDF CreationDate
12 June 2026. `gap` asserts we could not see, and we saw a great deal. `none` asserts there are no
decks, which is false. `read` is the only one of the three that is true.

**Recorded serially in one process**, because nine agents produced the findings concurrently and
`R1_ir_checked.json` is a single file that nine writers would race on.

**What this does NOT establish.** Nothing has been **read** yet, only located. **No deck's
contents have entered any deliverable**, and nine tickers have still never had one opened. A
`CURRENT` here means the page was checked on 20 August, not that the deck's information is in the
files. **ANY's only deck is dated 30 January 2023**, three years stale and predating its pivot, and
is `CURRENT` in exactly that limited sense.


#### Added 20 August 2026: Get-PassState gains the -OpenStatePath its neighbours already had

**The root cause behind 4.179, closed.** `Assert-PublishedSetUnchanged` has carried
`-OpenStatePath` for some time, and its own comment says why: *"it exists so an arm can point at a
location it controls. Without it the absent-map arms would pass or fail according to whether a
real pass had left one on disk, which is ambient state a test must never depend on."* **That
reasoning applied to the assertion and not to `Get-PassState`, which is the other half of the same
mechanism.**

**The cost of not having it was measured, not theoretical.** `RE_revision_arms.ps1` arm 10 must
prove a close INHERITS the open declaration, and `Get-PassState -Stamp 'close'` read
`Get-OpenStatePath` with no override, so the only way to exercise it was to write the LIVE
baseline. Its first version then deleted it, and running that suite during an open pass destroyed
that pass's baseline, which is exactly what happened to the pass correcting
`Test-PushPreconditions`. **Three suites carried a backup-and-restore idiom for want of one
parameter.**

**It weakens nothing, and that was established before it was added rather than assumed.** Three
tests, all from the brief:

- **`Restore-PassState` refuses on four grounds regardless of the path handed to it**: absent,
  unparseable, partial (covering fewer than every gitignored published name), or **taken at a
  different `HEAD`**. The refusals live in the function, not in the path.
- **The default is unchanged**, so no existing caller moved. Arm 13 requires exactly that.
- **A caller able to write a scratch file could already have overwritten the live one.** The
  parameter removes the need to mutate global state; it grants no new capability.

**Threaded to every call site, and a guard in the patch refused to write until that was true.**
`Get-PassState` called `Restore-PassState` twice on the close-inheritance paths and
`Save-PassState` once on the open persist. All three now pass `-Path $OpenStatePath`. (The guard's
first version flagged its own explanatory comment as an unthreaded call site, which is the same
class of error as a check reading its own answer back as a defect.)

**Three arms, and all three fail on the pre-parameter instrument.** Proved by swapping the
preserved copy in and running the suite: arms **10, 13 and 14 all fail**, and the instrument was
restored hash-identical.

- **Arm 10** now uses the scratch path the rest of that file already used, so it no longer touches
  the live open state at all.
- **Arm 13** requires the bare call to still read the live baseline **and** an override to produce
  a different answer through the same call, so the parameter is an addition rather than a silent
  behaviour change.
- **Arm 14 closes 4.179's carried item** that nothing required a suite to leave the live pass
  state as it found it. It plants a sentinel, takes an open stamp aimed at a scratch path, and
  requires the sentinel byte-identical afterwards **and** the scratch path written.

**Deliberately not done.** `R4_open_state_arms.ps1` and `WK_build_mode_arms.ps1` still back up and
restore the live path. Both work unchanged, and `R4` is the open-state suite where exercising the
live path is arguably its job. **Simplifying them is carried**: a change that is merely tidier is
the kind this protocol says to leave alone.

| File | Bytes | sha256 |
|---|---|---|
| `R1_pass_state.ps1` | 93,654 | `35bfc27f6cfa3bac...` |
| `RE_revision_arms.ps1` | 23,106 | `cf19627bc1cf9620...` |

Prior copies at `preserve/2026-08-20_openstatepath/`.

**Measured after.** `RE_revision_arms` **14 of 14**, `R4_open_state_arms` 12 of 12,
`RV_stamp_basis_arms` 8 of 8, `WK_build_mode_arms` 17 of 17, `G5_treescope_arms` 12 of 12,
`ZI2_ir_material_arms` 11 of 11, `R1_tests` PASS, `R1_halt_test` PASSED. Chain `5 of 5` tree-scope
and `CHECKS RUN: 1512   files: 36   per file: 42`, unchanged. **This pass's own baseline survived
its own suite run**, which is the property arm 14 now holds shut.
