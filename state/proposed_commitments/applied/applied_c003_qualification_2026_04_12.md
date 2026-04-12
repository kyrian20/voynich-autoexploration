# Proposed Qualification to C003

**Experiment:** exp_579 (2026-04-12)
**Type:** Qualification (not retraction) — C003 stands but scope needs narrowing.

## Proposed text addition to C003

Current C003: "19/19 PASS on B-dialect battery (exp_314, N=30)"

**Proposed qualification to append:**
> "The 19/19 PASS was calibrated on full B-dialect corpus metrics, which are weighted averages across four sections (B_herbal ~14%, B_bio ~33%, B_astro ~15%, B_pharma ~39%) with systematically different positional grammar profiles (am_ll ranges from 0.053 in bio to 0.192 in pharma; qok_lf ranges from 0.032 in astro to 0.148 in bio). Section-level calibration would require different parameter values per section, consistent with the catastrophic First/Second cross-validation failure in exp_576 (17→8/19). C003 is a statement about the full-corpus aggregate. It should not be interpreted as 'the architecture matches all B-dialect text uniformly.' The architecture achieves near-full-corpus coverage on average, but individual sections may score differently under section-specific metrics."

## Basis
exp_579 (2026-04-12): Section composition explains 97–107% of the document-order metric gradient in B-dialect. The four B-dialect sections have systematically different positional grammar profiles. The full-corpus calibration (exp_314) optimizes for the weighted average of these profiles. This is a valid and useful result, but needs the scope qualification above to prevent overinterpretation of C003 as a universal fit claim.

## Action required
Human review. If accepted, append qualification to C003 in state/committed_claims.md.
