# exp_607 — Held-out next-token prediction

## Question
Does the immediately previous token improve next-token prediction on unseen folios beyond unigram frequencies? This is a modest test of local sequential structure, not an attempt to assign meanings.

## Preregistered method
- Split by folio using SHA-256 of folio label, modulo 5; bucket 0 is test. The same split rule is applied independently within each transcription.
- Train a unigram baseline and an interpolated bigram model (50% unigram + 50% smoothed bigram; additive alpha=0.1). Score only within-line transitions, never across line boundaries.
- Negative control: shuffle token order within every training line using a fixed random seed, preserving each training line's token inventory but destroying its original order.
- Metric: held-out bits per next token. Positive gain versus unigram means lower log loss. Compare real-order gain with shuffled-control gain.
- Limitations: simple regex tokenization may include transliteration artefacts; repeated/related transcriptions are not independent witnesses; no semantic interpretation is tested.

## ZL3b

- Source SHA-256: bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc
- Train/test folios: 152 / 32; lines: 3139 / 600; scored transitions: 4620.
- Real order: unigram 10.56074 bits/token; interpolated bigram 10.29395; gain 0.26679.
- Shuffled-training control: interpolated 10.34986; gain vs unigram 0.21088.
- Real-minus-shuffled gain: 0.05591 bits/token.

## IT2a

- Source SHA-256: 7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5
- Train/test folios: 151 / 32; lines: 3138 / 597; scored transitions: 4613.
- Real order: unigram 10.74633 bits/token; interpolated bigram 10.40536; gain 0.34096.
- Shuffled-training control: interpolated 10.46035; gain vs unigram 0.28598.
- Real-minus-shuffled gain: 0.05498 bits/token.

## Interpretation rule

A positive gain indicates local token order helps prediction on held-out folios under this tokenizer/model; it does not establish that the text is natural language or that any token has a known meaning. A gain similar to the shuffled control is weak evidence because token inventories and model smoothing can produce apparent improvements. A negative gain means this fixed bigram model did not beat the unigram baseline. Do not tune on the held-out folios; any follow-up must be a new preregistered test.
