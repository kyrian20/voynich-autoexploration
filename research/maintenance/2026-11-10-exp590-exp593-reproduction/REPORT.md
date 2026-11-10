# Reproducción independiente local de EXP-590 y EXP-593

Fecha: 2026-11-10

## Alcance

Reejecuté los scripts versionados en el `master` de base `def929347e91f8d68bc71430bb236532d69136da` sobre la transcripción exacta `data/transcriptions/eva_zl3b.txt`. Como esta sesión no tenía un checkout Git local, descargué por la integración de GitHub solo los archivos fuente necesarios y los monté en un directorio temporal aislado; no modifiqué el corpus ni el repositorio local.

- SHA-256 de EVA ZL3b: `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc` (coincide con el registrado en ambos informes).
- Python: `3.12.14`.
- Dependencias auxiliares: `audit_ivtff_metadata.py`, `audit_ivtff_ligature_views.py`, `ivtff_physical_rows.py` y `audit_ivtff_page_locus_ids.py`, obtenidas del mismo estado de `master`.
- Comandos:
  - `python scripts/exp590_daiin_position.py`
  - `python scripts/exp593_daiin_variants.py`

## Resultado

Los dos scripts terminaron correctamente. Los cuatro artefactos generados (JSON y Markdown de cada experimento) son idénticos byte por byte a los archivos versionados en `research/experiments/2026-11-10-*`; `cmp` terminó con código 0 en las cuatro comparaciones.

| Análisis | Cifras reproducidas |
|---|---|
| EXP-590 | 5.376 líneas, 39.594 tokens, 853 `daiin`, 161 líneas iniciales, p unilateral = 0,0001999600 |
| EXP-593 | 4.188 líneas, 32.732 tokens; max-T ajustado: `daiin` = 0,0003999200, `dain` = 0,0003999200, `daiiin` = 0,9886022795 |

SHA-256 de JSON reproducidos:

- EXP-590: `9aa513d9dc7e06a1322b5f44050204578bb327462c6991e92a230f86996ede35`
- EXP-593: `bd9bab3de74379360229a6993d1ab53d07d8d11eeb8cff67ceddddf2c40ca714`

## Interpretación y límites

Esto confirma la reproducción determinista de estas dos salidas desde los scripts y la transcripción preservada. No valida el modelo nulo, la conformidad IVTFF completa ni una hipótesis lingüística. EXP-590 usa la cobertura amplia de identificadores; EXP-593 conserva la cobertura histórica restringida. Sus tamaños de población no son directamente comparables. Los valores p son exploratorios y no acreditan traducción ni descifrado.

No asigné un EXP nuevo, no edité datos ni afirmaciones científicas y no afirmo que CI haya corrido sobre `def929347e91f8d68bc71430bb236532d69136da`: `fetch_commit_workflow_runs` no devolvió ejecuciones asociadas a ese commit. Esta nota deja la reproducción local auditable; hace falta revisar el estado de CI de esta rama para añadir verificación remota.
