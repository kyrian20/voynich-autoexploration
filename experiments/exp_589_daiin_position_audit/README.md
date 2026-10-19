# exp_589 — daiin positional audit

Question: does EVA `daiin` appear at the beginning of body-text lines more often than expected when conditioning on each line's own token composition and length, and is the direction consistent between ZL3b and ZL3a?

- Primary transcription: `data/transcriptions/eva_zl3b.txt` (manifest in `data/transcriptions/README.md`).
- Sensitivity replication: `data/transcriptions/zl3a.txt`.
- Script: `script.py`; no OpenAI API, credentials, or external downloads required.
- Output: `results.json`, generated in GitHub Actions.
- Randomization: within-line token shuffle, 2,000 replicates, fixed seed; separate all/A/B subsets.
- Treat outcomes as conditional on the conservative parser; positions alone do not provide semantic interpretation.

Motivation sources:
- https://voynich.world/explore/manuscript?word=daiin
- https://voynich.world/explore/sources
- https://www.voynich.nu/data/ZL3b-n.txt
- https://voynichattacks.wordpress.com/2022/12/26/word-positions-on-the-folios/
- https://voynichattacks.wordpress.com/2022/12/30/word-positions-on-the-folios-part-deux/
- https://arxiv.org/abs/2604.25979

No result is claimed until `results.json` has been generated and reviewed.
