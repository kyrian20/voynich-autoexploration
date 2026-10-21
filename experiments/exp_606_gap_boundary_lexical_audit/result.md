# exp_606 — Lexical boundary audit around known foliation gaps

Exploratory descriptive test; not physical codicology and not a test for unnumbered missing leaves.

Method: compare cleaned token distributions on six predeclared surviving-page transitions with adjacent page transitions sharing the same Currier label. Report Jensen–Shannon divergence (bits; higher means more different) and vocabulary Jaccard overlap (higher means more overlap). Token extraction is deliberately simple and must not be treated as a validated EVA linguistic parser.

## ZL3b

- Source SHA-256: bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc
- Mean gap-edge JSD (only same non-null Currier label; 3 eligible edges): 0.691436927946152
- Mean same-label adjacent control JSD (147 transitions): 0.7019357140814954
- f11v->f13r: JSD=0.6901; Jaccard=0.1494; Currier labels A → A
- f58v->f65r: JSD=0.9519; Jaccard=0.0085; Currier labels A → None
- f73v->f75r: JSD=0.8230; Jaccard=0.0798; Currier labels None → B
- f90v->f93r: not available in this transcription
- f96v->f99r: JSD=0.9130; Jaccard=0.0316; Currier labels A → A
- f108v->f111r: JSD=0.4712; Jaccard=0.1827; Currier labels B → B
- Gap-edge JSD control percentiles: 0.422, 0.973, 0.041

## IT2a

- Source SHA-256: 7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5
- Mean gap-edge JSD (only same non-null Currier label; 3 eligible edges): 0.6733849197915355
- Mean same-label adjacent control JSD (147 transitions): 0.7106775382841305
- f11v->f13r: JSD=0.6786; Jaccard=0.1379; Currier labels A → A
- f58v->f65r: JSD=0.9600; Jaccard=0.0082; Currier labels A → None
- f73v->f75r: JSD=0.8459; Jaccard=0.0690; Currier labels None → B
- f90v->f93r: not available in this transcription
- f96v->f99r: JSD=0.8776; Jaccard=0.0415; Currier labels A → A
- f108v->f111r: JSD=0.4639; Jaccard=0.1956; Currier labels B → B
- Gap-edge JSD control percentiles: 0.361, 0.946, 0.034

## Interpretation limits

Six transitions are a tiny, selected sample. Only gap edges whose two sides both have the same non-null Currier $L label enter the mean and control-percentile comparison; edges with missing/different labels remain descriptive only. Controls are adjacent surviving pages with matching Currier labels, not matched for illustration type, scribal hand, text length, or exact section. Missing leaves may interrupt content, but lexical distance cannot establish that additional pages were lost. The simple token cleanup may include annotation artefacts. No p-value or causal claim is made.
