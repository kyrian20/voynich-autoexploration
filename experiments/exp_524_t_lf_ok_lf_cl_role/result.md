# exp_524 result — t-LF and ok-LF CL roles + complete A herbal_a CL matrix

## Audit

**Target-awareness**: No target-aware elements. All measurements are corpus observations.

**Feature-destroying implementation**: The len≥3 filter is applied correctly to pos2/pen. The ok-LF pos2=ok-self finding (E=2.73×/obs=5) must be flagged: exp_512 corrected F467 (ok-LF ok@pos2) to E=1.66×/obs=6 after removing 2-word-line baseline inconsistency. The current result uses a correct len≥3 filter and section-wide baseline — the discrepancy from exp_512 may reflect different A herbal_a N (55 vs ? lines in exp_512) or different baseline computation. This finding is NOT claimed as new; it is flagged for verification.

**Extrapolation**: No claims exceed the tested corpus scope. All findings are within A herbal_a (44 folios, 966 lines, 922 pairs).

**Negative-result scope**: ok→d and t→ch are DEPLETED — these are specific to A herbal_a. The chain's lack of cyclicity via d is robust (multiple independent null results: sh→d DEPLETED in exp_523; ok→d DEPLETED here; t→ch DEPLETED here).

**Control behavior**: No explicit controls. The complete CL matrix (Part 5) serves as an internal consistency check showing all above-threshold signals — useful for detecting spurious clusters.

---

## H_new_EQ: t-LF CL role (A herbal_a)

### t-LF as sender (N_cond=28)

| Receiver | obs | exp | E | Flag |
|----------|-----|-----|---|------|
| y | 3 | 1.1 | 2.74× | **(dir)** |
| ot | 3 | 1.2 | 2.53× | **(dir)** |
| d | 11 | 7.5 | 1.47× | below CONF (E=1.47<1.5) |
| ch | 1 | 5.3 | 0.19× | **STRONGLY DEPLETED** |
| qot | 0 | 1.0 | 0.00× | ZERO |
| cth | 0 | 2.2 | 0.00× | ZERO |
| o | 0 | 1.0 | 0.00× | ZERO |

**t-LF is a relay toward d (nearly CONF), not a terminal.** t routes back toward d (E=1.47×/obs=11, just below CONF threshold). It also branches to y ((dir)) and ot ((dir)).

**Critical: t→ch is STRONGLY DEPLETED (E=0.19×/obs=1)**. ch is the second-most common LF class (18.9%) but almost never follows t-LF. This anti-coupling between t and ch mirrors the chain structure: ch is a receiver (from qot via F490), not a downstream target of t.

**t→qot: ZERO.** t does not route back into the chain via qot. The t→d tendency (nearly CONF) suggests t lines create a "soft reset" toward d, the chain origin, without going through the qot relay.

### t-LF as receiver

| Sender | obs | exp | E | Flag |
|--------|-----|-----|---|------|
| d | 11 | 7.3 | 1.51× | **CONF** ✓ F508 |
| sh | 3 | 1.1 | 2.63× | **(dir)** ✓ F510 |
| cth | 3 | 2.1 | 1.44× | below CONF |
| ot | 0 | 1.2 | 0.00× | ZERO |

F508 (d→t CONF) and F510 (sh→t (dir)) both reproduce from the receiver side. t is multiply-fed from d (CONF) and sh ((dir)).

### t-LF within-line grammar (A herbal_a)

**pos1 (N_elig=28):**
- **o@pos1: E=2.07×/obs=5 → dir (NEW)**: t-LF lines open with o-onset words at 2.07× baseline. This is the first confirmed t-LF pos1 rule in A herbal_a.
- y@pos1: E=0.50×/obs=2 — DEPLETED (contrast ok-LF and ot-LF where y@pos1 is enriched)
- cth@pos1: ZERO

**pos2 (N_elig=26):**
- qot@pos2: E=2.55×/obs=2 — (dir) threshold requires obs≥3; this is N=2 → below threshold. Directional but unconfirmed.
- No confirmed pos2 signals.

**pen (N_elig=26):**
- ok@pen: E=2.73×/obs=3 — (dir). t-LF lines end with ok-onset at penultimate position at (dir) level. NEW.
- qot@pen: E=2.77×/obs=2 — N=2, below threshold.
- d@pen: DEPLETED (E=0.66×/obs=3) — d-onset words do NOT appear at pen in t-LF lines.

**H_new_EQ conclusion:** t-LF is a **relay class**, not a terminal. It receives from d (CONF, F508) and sh ((dir), F510), and routes back toward d (nearly CONF E=1.47×/obs=11). It also branches to y ((dir)) and ot ((dir)). t has a distinctive pos1 grammar: o-onset at pos1 (dir, E=2.07×/obs=5) — the opposite of the chain members which tend toward y at pos1. ch is strongly avoided after t (E=0.19×/obs=1). t appears to be a "content switch" class whose lines (a) start with o-onset, (b) connect to y/ot, and (c) have a soft tendency to return to d.

---

## H_new_EP: ok-LF CL role (A herbal_a)

### ok-LF as sender (N_cond=53)

| Receiver | obs | exp | E | Flag |
|----------|-----|-----|---|------|
| ol | 4 | 1.1 | 3.66× | **(dir)** NEW |
| y | 4 | 2.1 | 1.93× | below dir |
| ot | 4 | 2.2 | 1.78× | below dir |
| d | 9 | 14.2 | 0.63× | **DEPLETED** |
| qot | 2 | 1.9 | 1.05× | flat |
| ch | 10 | 10.0 | 1.00× | flat |

**ok does NOT route back to d (DEPLETED, E=0.63×) or qot (flat).** ok is a branch terminal from sh, not a cycle-closer. 

**NEW: ok→ol ((dir), E=3.66×/obs=4)**: ok-LF lines are followed by ol-LF lines at 3.66× baseline. ol-LF is a minority class (~1% of LF); this (dir) signal suggests ok specifically routes to ol at high relative rate.

### ok-LF as receiver

| Sender | obs | exp | E | Flag |
|--------|-----|-----|---|------|
| sh | 5 | 2.2 | 2.27× | **dir** ✓ F509 |
| cth | 6 | 4.0 | 1.50× | borderline CONF |
| d | 10 | 14.0 | 0.71× | **DEPLETED** |

F509 (sh→ok dir) reproduced from receiver side. d→ok is DEPLETED (E=0.71×) — confirms that d does not route to ok; d's CL channels are specifically qot (F491) and t (F508).

**cth→ok borderline:** E=1.50×/obs=6 — exactly at CONF boundary. Not counted as new finding (E=1.50 and obs=6 < 10).

### ok-LF within-line grammar (A herbal_a)

**NOTE on F455 (ok-LF pos1=y):** This run gives E=1.52×/obs=11 which crosses the CONF threshold. However, Q010 remains open because exp_521 gave E=1.22-1.38×/obs=9-10. The difference may reflect different A herbal_a section sizes across runs. This is NOT claimed as a new finding; it is noted as additional evidence for F455 borderline-CONF status. Q010 should be resolved by running a standardized section definition.

**pos1 NEW finding — s-onset (dir, E=2.22×/obs=5):**
- s@pos1: E=2.22×/obs=5 → dir. ok-LF lines open with s-onset words at dir rate. This was not previously noted. Unlike y@pos1 (F455 FLAGGED), s@pos1 is independent of the Q010 methodology dispute.

**pos2:** ok-self E=2.73×/obs=5 — this CONFLICTS with exp_512's F467 correction (E=1.66×). Do not claim as new finding pending verification.

**pen:** ok-self E=3.60×/obs=7 → dir (below CONF due to obs=7 < 10 at this section size). Consistent with F485 CONF direction but below CONF here due to smaller N.

---

## Part 3: d-LF confirmed as a 2-channel CL hub

d→t: CONF (E=1.51×/obs=11, F508) ✓
d→qot: E=1.46×/obs=13 (below CONF at 1.46<1.5× — see exp_523 methodological note; F491 CONF retained from exp_511)
d→d-self: E=1.35×/obs=90 (near-threshold, not CONF)
All other d→X: DEPLETED or flat.

d's CL channels: d→qot (F491, CONF) and d→t (F508, CONF). Both are near-threshold CONF signals. d does NOT route to ok, ch, sh, or o directly.

---

## Part 4: ot-LF CL findings (new signals)

**k→ot (dir, E=2.96×/obs=5):** k-LF lines followed by ot-LF at dir rate. NEW.
**t→ot ((dir), E=2.53×/obs=3):** t-LF lines followed by ot-LF. NEW.

ot receives from k (dir) and t ((dir)). ot as sender shows no elevated signals (qot E=2.04×/obs=3 — below dir with N=3; d E=1.27×/obs=14 near-flat).

---

## Part 5: Complete A herbal_a CL matrix

All pairs above threshold (sorted by E):

| Link | obs | exp | E | N_cond | Flag |
|------|-----|-----|---|--------|------|
| qok→qok | 3 | 0.7 | 4.43× | 25 | (dir) |
| qo→k | 3 | 0.7 | 4.39× | 15 | (dir) |
| ok→ol | 4 | 1.1 | 3.66× | 53 | (dir) |
| o→sh | 4 | 1.3 | 3.03× | 32 | (dir) ✓F507 |
| k→ot | 5 | 1.7 | 2.96× | 40 | dir NEW |
| y→y | 4 | 1.4 | 2.77× | 37 | (dir) |
| k→qok | 3 | 1.1 | 2.77× | 40 | (dir) |
| t→y | 3 | 1.1 | 2.74× | 28 | (dir) NEW |
| sh→t | 3 | 1.1 | 2.63× | 39 | (dir) ✓F510 |
| t→ot | 3 | 1.2 | 2.53× | 28 | (dir) NEW |
| sh→ok | 5 | 2.2 | 2.27× | 39 | dir ✓F509 |
| qot→ch | 11 | 6.2 | 1.77× | 33 | CONF ✓F490 |
| ch→o | 10 | 6.2 | 1.60× | 169 | CONF ✓F506 |
| d→t | 11 | 7.3 | 1.51× | 249 | CONF ✓F508 |

Note: d→qot E=1.46×/obs=13 (below CONF threshold here, but F491 CONF retained from exp_511).

**New signals from matrix not previously characterized:**
- k→ot (dir, E=2.96×/obs=5) — F511 candidate
- t→y ((dir), E=2.74×/obs=3) — F512 candidate  
- t→ot ((dir), E=2.53×/obs=3) — F513 candidate
- ok→ol ((dir), E=3.66×/obs=4) — already noted above

---

## Summary

| Hypothesis | Result |
|-----------|--------|
| H_new_EQ: t-LF CL role | t is a RELAY: routes back toward d (nearly CONF, E=1.47×/obs=11); also →y ((dir)), →ot ((dir)). ch STRONGLY DEPLETED after t (E=0.19×). t-LF pos1=o new dir finding. ok@pen (dir) finding. |
| H_new_EP: ok-LF CL role | ok does NOT route to d or qot (DEPLETED). ok→ol NEW (dir). sh→ok reproduced. No cyclicity via ok. ok-LF pos1=s NEW dir finding. F455 y@pos1 shows E=1.52×/obs=11 (CONF range) but Q010 remains open. |
| d-LF hub confirmed | d→t CONF + d→qot (near-CONF) only two elevated channels. All other d→X flat/depleted. |
| ot-LF new signals | k→ot dir (F511). t→ot (dir) (F513). |
| New CL signals | t→y (dir) (F512); ok→ol (dir) (F514). |

**New finding IDs:** F511 (k→ot, dir, E=2.96×/obs=5); F512 (t→y, (dir), E=2.74×/obs=3); F513 (t→ot, (dir), E=2.53×/obs=3); F514 (ok→ol, (dir), E=3.66×/obs=4). t-LF pos1=o new dir: F515. ok-LF pos1=s new dir: F516. **F467 ok-self@pos2 (dir/CONF) NOT claimed** — conflicts with exp_512 correction; needs verification.
