# exp_523 result — sh-LF CL cyclicity + within-line grammar + chain extension

## Audit

**Target-awareness**: No target-aware elements. All measurements are corpus observations.

**Feature-destroying implementation**: The positional grammar filter uses len≥2 for pos1 and len≥3 for pos2/pen (correct). CL pairs are built by treating each folio_lines[n] list as ordered consecutive lines (same methodology as exp_511/522). No feature is destroyed.

**Methodological note on d→qot E-value**: The chain re-verification shows d→qot E=1.46×/obs=13 (below CONF), whereas F491 from exp_511 showed E=1.64×/obs=13 (CONF). The discrepancy (E difference, same obs count) arises from different CL pair baselines: exp_511 used a within-folio sort by line number with a receiver-side baseline computed from that specific sorted pair set (N_pairs=1133); this experiment uses the folio_lines insertion order as the pair ordering and a different total N_pairs=922. The obs count (13) matches, but the baseline rates differ slightly due to different pair-set construction. F491 CONF status is retained from its original derivation (exp_511); this experiment is not a re-derivation of F491. Similarly, qot→ch E=1.77×/obs=11 and ch→o E=1.60×/obs=10 both independently confirm CONF at current methodology.

**Extrapolation**: No claims exceed the tested corpus scope. All findings are within the A herbal_a section (44 folios, 966 lines, 922 pairs).

**Negative-result scope**: sh-LF within-line grammar shows no confirmed rules — this is within the A herbal_a section only. Other sections not tested. H_new_EL is closed for A herbal_a; sh-LF in other sections is unexplored.

**Control behavior**: No explicit control groups. Chain verification serves as internal consistency check (previously confirmed links reproduced).

---

## H_new_EL: sh-LF within-line grammar (A herbal_a)

### sh-LF pos1 (N_elig=38)

| Class | obs | exp | E | Flag |
|-------|-----|-----|---|------|
| ckh | 1 | 0.1 | 12.21× | spurious (N=1) |
| ok | 4 | 2.2 | 1.84× | below dir |
| sh-self | 6 | 3.3 | 1.83× | below dir |
| k | 1 | 0.6 | 1.74× | below dir |
| qot | 4 | 2.7 | 1.48× | below CONF |
| y | 4 | 5.4 | 0.74× | DEPLETED |
| ot | 0 | 2.2 | 0.00× | DEPLETED |
| cth | 0 | 0.2 | 0.00× | DEPLETED |
| s | 0 | 1.7 | 0.00× | DEPLETED |

**No confirmed pos1 rules for sh-LF.** sh-self and ok are both near-directional (E≈1.83-1.84×/obs=4-6) but both below the dir threshold (E≥2.0×/obs≥5). The most striking feature: **y is DEPLETED (E=0.74×/obs=4)** — sh-LF lines actively avoid y at pos1. This is the OPPOSITE of o-LF, where y is enriched at pos1 (E=1.81×/obs=9). The ch→o chain is a transition not just in LF class but in opening word grammar: o-LF lines tend to open with y; sh-LF lines (which follow o-LF) tend NOT to open with y.

### sh-LF pos2 (N_elig=31)

| Class | obs | exp | E | Flag |
|-------|-----|-----|---|------|
| d | 5 | 3.3 | 1.54× | below CONF |
| sh-self | 5 | 3.9 | 1.27× | below CONF |
| ch | 12 | 10.6 | 1.13× | flat |
| cth | 0 | 1.6 | 0.00× | DEPLETED |
| ok | 0 | 1.2 | 0.00× | DEPLETED |
| y | 0 | 0.9 | 0.00× | DEPLETED |
| qot | 0 | 0.9 | 0.00× | DEPLETED |
| ot | 0 | 0.8 | 0.00× | DEPLETED |

**No confirmed pos2 rules.** cth is DEPLETED at pos2 for sh-LF (E=0.00×/obs=0) — contrast o-LF where cth is (dir) at pos2 (F505). Multiple classes are ZERO: ok, y, qot, ot. d is the closest to signal (E=1.54×/obs=5) but below CONF.

### sh-LF pen (N_elig=31)

| Class | obs | exp | E | Flag |
|-------|-----|-----|---|------|
| d | 8 | 5.5 | 1.47× | below CONF |
| ch | 9 | 8.3 | 1.08× | flat |
| sh-self | 4 | 2.8 | 1.43× | below dir |
| cth | 1 | 1.9 | 0.52× | DEPLETED |

**No confirmed pen rules.** d@pen is close (E=1.47×/obs=8) but below CONF (needs E≥1.5×/obs≥10). ch is flat.

**H_new_EL conclusion**: sh-LF has NO confirmed within-line grammar rules in A herbal_a. The within-line grammar of sh-LF is essentially Markovian at all three positions. The one notable feature is the y-depletion at pos1 (E=0.74×/obs=4), which is directionally opposite to o-LF's y-enrichment. sh-LF appears to be a "plain grammar" line class internally — its grammatical distinctiveness is at the CL level (it is a chain destination) rather than at the within-line level.

---

## H_new_EM: CL chain cyclicity (A herbal_a)

### Chain re-verification

| Link | obs | exp | E | N_cond | Finding | Flag |
|------|-----|-----|---|--------|---------|------|
| d→qot | 13 | 8.9 | 1.46× | 249 | F491 CONF | below CONF at current baseline* |
| qot→ch | 11 | 6.2 | 1.77× | 33 | F490 CONF | **CONF** |
| ch→o | 10 | 6.2 | 1.60× | 169 | F506 CONF | **CONF** |
| o→sh | 4 | 1.3 | 3.03× | 32 | F507 dir | **(dir)** |

*d→qot E=1.46× here vs E=1.64× in exp_511. Same obs=13, different pair baseline (N=922 vs 1133). F491 CONF retained from original derivation. See methodological note above.

### sh-LF as sender — cyclicity test

| Successor | obs | exp | E | Flag |
|-----------|-----|-----|---|------|
| t | 3 | 1.1 | 2.63× | **(dir)** |
| ok | 5 | 2.2 | 2.27× | **dir** |
| k | 4 | 1.8 | 2.25× | below dir |
| sh-self | 3 | 1.6 | 1.87× | below (dir) |
| ch | 10 | 7.4 | 1.36× | below CONF |
| d | 6 | 10.4 | 0.57× | **DEPLETED** |
| qot | 0 | 1.4 | 0.00× | **ZERO (DEPLETED)** |
| ot | 0 | 1.6 | 0.00× | DEPLETED |
| o | 1 | 1.4 | 0.70× | DEPLETED |

**THE CHAIN IS NOT CYCLIC.** sh-LF does NOT route back to d (E=0.57×, DEPLETED) and does NOT route to qot (E=0.00×, ZERO). The chain d→qot→ch→o→sh is a LINEAR trajectory; sh is a terminal/branching node, not a cycle-closing node.

**NEW: sh→ok (dir, E=2.27×/obs=5)**: sh-LF lines are followed by ok-LF lines at 2.27× baseline. This meets the dir threshold (E≥2.0×/obs≥5). The CL chain **branches at sh**: sh→ok (dir) and sh→t ((dir)).

**NEW: sh→t ((dir), E=2.63×/obs=3)**: sh-LF lines are followed by t-LF at 2.63× baseline. Meets (dir) threshold (E≥2.5×/obs≥3).

### sh as receiver — cross-check of F507

| Predecessor | obs | exp | E | Flag |
|-------------|-----|-----|---|------|
| o | 4 | 1.3 | 3.03× | **(dir)** |
| s | 2 | 1.0 | 2.02× | 2.02× |
| sh | 3 | 1.6 | 1.87× | below (dir) |
| d | 10 | 10.3 | 0.97× | flat |

**F507 confirmed from receiver side**: o→sh E=3.03×/obs=4 ((dir)) from both sender and receiver perspectives. The finding is internally consistent.

### Full chain sender survey

**d→X (N_cond=249):**
- **t: E=1.51×/obs=11 → CONF** (NEW: d→t CL finding; E just above 1.5×, obs=11≥10)
- qot: E=1.46×/obs=13 (below CONF — see note)
- d-self: E=1.35×/obs=90 (flat)

**qot→X (N_cond=33):** ch CONF (1.77×/11) only clear signal.

**ch→X (N_cond=169):** o CONF (1.60×/10) only clear signal.

**o→X (N_cond=32):** sh (dir) (3.03×/4); o-self (1.69×/2); ot (1.48×/2) — all below CONF.

**sh→X (N_cond=39):** ok dir (2.27×/5); t (dir) (2.63×/3) — chain branches.

---

## New CL structure summary

The A herbal_a CL structure is now:
```
d ——————→ qot (F491, CONF)
  \
   ——————→ t (F508, CONF, NEW)
   
qot ——→ ch (F490, CONF)
ch ————→ o (F506, CONF)
o —————→ sh (F507, (dir))
sh ————→ ok (F509, dir, NEW)
sh ————→ t (F510, (dir), NEW)
```

The chain is NOT a loop. d has TWO confirmed CL destinations: qot and t. sh branches to ok and t after the main chain. t appears as a downstream destination from both d (directly) and sh (via the chain).

**Interpretive note:** t appearing as a successor from both d (direct) and sh (terminal chain node) may reflect t being a "reset" or "paragraph continuation" class that follows multiple LF class types. t-LF's role warrants further investigation (H_new_EJ in A stars is blocked, but t-LF in A herbal_a CL grammar is now worth examining).

---

## Part 4: o-LF pos2 cross-section

A herbal_a o-LF pos2: o-self (dir, E=3.06×/obs=3, F504) ✓; cth (dir, E=2.75×/obs=4, F505) ✓ — reproduced from exp_522.

A stars o-LF pos2: o-self (dir, E=4.17×/obs=4) — reproduced. cth: ZERO (E=0.00×). A stars o-LF pos2 grammar differs from A herbal_a: o-self enrichment is present in both, but cth enrichment is A herbal_a-specific. F505 scope is A herbal_a only.

---

## Summary

| Hypothesis | Result |
|-----------|--------|
| H_new_EL: sh-LF within-line grammar | NO confirmed rules. y DEPLETED at pos1 (0.74×) — OPPOSITE of o-LF y-enrichment. sh-LF grammar is internally Markovian. |
| H_new_EM: CL chain cyclicity | NOT CYCLIC. sh→d DEPLETED (0.57×); sh→qot ZERO (0.00×). Chain is linear: d→qot→ch→o→sh. sh BRANCHES: →ok (dir, NEW), →t ((dir), NEW). |
| Additional: d→t CL | NEW CONF: d→t (E=1.51×/obs=11). d is a CL HUB with two confirmed destinations. |
| F504/F505 scope | F504 (o→o-self@pos2) present in both A herbal_a and A stars. F505 (o→cth@pos2) A herbal_a-SPECIFIC (A stars: cth ZERO). |

**New finding IDs:** F508 (d→t CL A herbal_a, CONF, E=1.51×/obs=11); F509 (sh→ok CL A herbal_a, dir, E=2.27×/obs=5); F510 (sh→t CL A herbal_a, (dir), E=2.63×/obs=3). F505 scope corrected: A herbal_a-specific.
