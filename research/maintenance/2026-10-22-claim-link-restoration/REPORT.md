# Recuperación de auditoría de afirmaciones eliminada por integración — 22-10-2026

**Estado:** mantenimiento documental; sin nuevo EXP, corpus, métrica científica ni traducción.

## Incidencia y causa observable

El commit `3571c9e3a61325598e3c029d98990eedc6d947f3` añadió una auditoría acotada de la relación entre afirmaciones y resultados de EXP-267/288, con los cuatro lectores ya reproducidos. El merge de la PR #3, `dfb660e38523732ec9e00a3959eba33f2139481c`, eliminó **cuatro archivos** de esa auditoría al integrar la batería común. Se constata en la lista de ficheros de la PR #3 y en la comparación de commits; no se presume una causa humana o técnica más específica. La batería común se conserva intacta.

## Corrección exacta

Se restituyen **sin modificar bytes** los cuatro blobs Git de `3571c9e`:

| Ruta | Blob Git SHA-1 |
|---|---|
| `research/maintenance/2026-10-22-claim-link-adjudication/REPORT.md` | `00e1fbf9a5430bdc2347fd20d0f704cf0bd13759` |
| `research/maintenance/2026-10-22-claim-link-adjudication/results.json` | `70927b018bf14b0d2189ad223b33bb40ac8fdb25` |
| `scripts/audit_reference_claim_links.py` | `3d0236b38535440c71f31e8d774b283e87fb8ab9` |
| `tests/test_reference_claim_links.py` | `7c45cd0ae94a8d8021b936d3dc911303c235b48c` |

Antes de la restitución se cotejaron los SHA de blobs en master y `3571c9e` de los cuatro scripts históricos, los dos informes históricos, el snapshot de lectores, el manifiesto de identidad y ambos corpus; **todos coincidieron**. El snapshot original documenta los SHA-256 de los scripts y corpus; no se cambian ni se recalculan salidas experimentales.

## Alcance y verificación

Las cuatro pruebas puras y la comprobación de integridad del auditor se encuentran en los archivos restituidos. El commit anterior `3571c9e` tuvo CI `39842201175` con resultado `success`, pero esa CI **no ejecutaba necesariamente el auditor integral**; no se interpreta como validación científica. La restitución no modifica `.github/workflows/voynich-check.yml`, porque la PR #2 abierta edita ese archivo. Comandos para ejecución futura en checkout completo:

```sh
python tests/test_reference_claim_links.py
python scripts/audit_reference_claim_links.py --check research/maintenance/2026-10-22-claim-link-adjudication/results.json
```

Las decisiones de la auditoría son específicas de afirmaciones históricas, no de los experimentos enteros. No se edita `state/committed_claims.md` ni se cambia numeración. Las PR #2 y #5 abiertas no editaban estas cinco rutas en la inspección previa. **Pendiente:** incorporar comprobación integral en CI tras resolver el solapamiento con PR #2, sin duplicar simulaciones. No se atribuye desciframiento ni validación global.
