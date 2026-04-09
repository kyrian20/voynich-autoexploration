# Iteration Log
# Cryptanalyst — Voynich Manuscript Investigation
# One-line entries: timestamp | experiment ID | brief summary of what was learned

---

2026-04-09 | INIT | Phase initialized — directory structure, SOUL.md, skill files, seed hypotheses H001-H009, transcription data, reference corpora, and Python environment established. No experiments run yet.
2026-04-09 | exp_001_word_initial_entropy | H003 tested: Voynich H_initial=3.137 > H2=2.341 (rules out pure glossographic); but H_initial still 0.9 bits below natural languages and 0.73 below shuffled control (onset slot is constrained). q-initial (15.5%) is extreme. Latin reference corpus was wrong (English Bible) — fixed. Labels not extracted (parser bug — fix in exp_003).
2026-04-09 | exp_002_positional_entropy | H001/H002/H010 tested. U-shaped positional bias (outer slots constrained, inner free) confirms slot grammar. H(-1)=2.456 is most constrained position. H2 flat by word length (no info rise with length). Q-initial removal LOWERS H_initial (H010 refuted). Added H012, H013 to backlog.
2026-04-09 | exp_003_label_body_entropy | H009/H012/H013 tested. Labels h2=2.575 > body h2=2.302 (+0.273 bits). 55.3% label vocabulary exclusive. qo-words absent from labels. daiin absent from label top vocab. H013 refuted (qo-stripping negligible). Added H014, H015 to backlog.
2026-04-09 | exp_004_daiin_distribution | H014/H012 tested. daiin concentrates in Currier A/Herbal A (4.58% vs 1.41% in B; 0.09% in labels). A/B vocabularies dramatically different — qo-words dominate B, daiin dominates A. Inner-slot chars differ: A=balanced e/o, B='e' dominant (29.3%). Section vocabularies confirmed strongly distinct.
2026-04-09 | exp_005_currier_ab_comparison | H004 partial. KL(char)=0.069 (same char pool). MI(word;currier)=4.2%. But: qokeedy 14697x more in B than A; positional entropy diverges sharply at positions 5-8 (A stays ~3.6, B drops to ~3.0). A/B are NOT dialects — different suffix templates. Full embedding alignment deferred to H004-followup.
