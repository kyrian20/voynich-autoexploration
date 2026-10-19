# exp_601 — Results: paired sensitivity of the primary positional statistic

**Execution date:** 2026-10-19  
**Successful workflow:** https://github.com/kyrian20/voynich-autoexploration/actions/runs/39260083190  
**Machine-readable output:** `results.json`

The workflow's analysis and artifact upload succeeded; its automatic commit encountered a concurrent-ref race. I recovered the JSON from the successful Actions artifact, checked the key values, then committed the result through the GitHub connector.

## Source and paired coverage
- ZL3b SHA-256: `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc` (411,671 bytes).
- ZL3a SHA-256: `56419297682d338ff1a0a17f5ae251e3ee3e2c5bf05a62db04c5385ef30b36a2` (411,710 bytes).
- Matched eligible Currier-B/P0 lines with at least two clean tokens in both versions: **2,325**.
- Matched eligible lines with any cleaned-token sequence difference: **10**.
- Two of these 2,325 lines have a different literal first token, but none changes first-position status for any of the six predeclared test forms (`daiin`, `aiin`, `chedy`, `dain`, `saiin`, `qokaiin`).
- The four ZL3a-only line IDs (`f1r.29`, `f1r.30`, `f1r.31`, `f89v2.26`) are not eligible Currier-B/P0 lines.

## Full-version B/P0 statistics

| Token | ZL3b total | ZL3b first | ZL3b expected first | ZL3b ratio | ZL3a total | ZL3a first | ZL3a expected first | ZL3a ratio |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `daiin` | 295 | 88 | 31.279 | 2.813× | 296 | 88 | 31.384 | 2.804× |
| `aiin` | 355 | 1 | 34.199 | 0.029× | 354 | 1 | 34.088 | 0.029× |
| `chedy` | 479 | 6 | 49.337 | 0.122× | 479 | 6 | 49.331 | 0.122× |
| `dain` | 107 | 34 | 10.714 | 3.173× | 107 | 34 | 10.714 | 3.173× |
| `saiin` | 82 | 46 | 9.158 | 5.023× | 82 | 46 | 9.158 | 5.023× |
| `qokaiin` | 240 | 25 | 26.846 | 0.931× | 240 | 25 | 26.846 | 0.931× |

## Interpretation

For `daiin`, the total count differs by one token (295 vs 296), but the observed first count remains 88 in both versions. The expected first count changes from 31.279 to 31.384 and the enrichment only from 2.813× to 2.804×. The other five predeclared forms likewise have unchanged observed first-position counts between versions.

Thus the primary first-position pattern is **insensitive to the observed ZL3a/ZL3b differences** within matched Currier-B/P0 rows and this fixed six-token set. This is a paired sensitivity comparison, not a p-value and not independent-sample replication.

## Limitations
- The audit only tests these six literal EVA strings within matched Currier-B/P0 lines.
- The parser/token cleanup remain operational definitions; independent IVTFF conformance review is still necessary.
- These statistics describe token placement, not word meaning or decipherment.
