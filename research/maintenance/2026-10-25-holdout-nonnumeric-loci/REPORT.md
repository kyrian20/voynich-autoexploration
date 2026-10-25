# Cobertura de loci del holdout físico v2 — 25-10-2026

**Estado:** auditoría operativa de cobertura; no EXP, no regla semántica, no descifrado. Manifiestos v1/v2 y corpus originales intactos.

## Defecto concreto y alcance

La partición v2 reserva hojas **numéricas** compartidas entre ZL3b e IT2a. No asigna los loci con identificador no numérico. Una inspección de las dos transcripciones originales de `master` (SHA base `96b6ba7709f5cfcdfd0660b2fed954aa0b351b46`) encontró 161 registros de encabezado `<fRos...>` en ZL3b y ninguno en IT2a; son loci no elegibles para el holdout numérico. Los recuentos de encabezados numéricos observados fueron 5451 y 5440, respectivamente; cero encabezados numéricos sin reconocer bajo el patrón v2. **No son 161 errores de transcripción** ni se deduce que deban asignarse a hojas 1–102.

El riesgo era evaluar en el futuro una regla con loci no asignados y presentarla como validación en hojas reservadas. La auditoría independiente `scripts/audit_holdout_locus_coverage.py` comprueba encabezados numéricos y nombrados, hashes de ambos corpus frente al manifiesto v2, recuentos de hojas, intersección, exclusiones, particiones disjuntas y cobertura exacta. Rechaza encabezados numéricos mal formados, hojas no positivas, sustitución de fuentes y asignaciones duplicadas o ajenas.

La salida `holdout-locus-coverage.json` se conserva como artefacto de `Voynich Check`. Los tests sintéticos adversariales están en `tests/test_holdout_locus_coverage.py`. El JSON no incluye tokens Voynich ni modifica las fuentes.

## Criterio de cierre

1. CI sobre el SHA de esta PR con siete pruebas de regresión y auditoría real completadas.
2. Artefacto conservado y cotejado: 102 hojas elegibles (68 entrenamiento, 16 desarrollo, 18 prueba), `Ros=161` ZL3b y `Ros=0` IT2a, sin encabezados numéricos malformados.
3. La validación futura debe excluir explícitamente loci nombrados/no asignados; no interpretar `Ros` como hoja numérica ni usar el test para calibración.

## Limitaciones

El lector de encabezados es una auditoría de cobertura, **no** una implementación completa del estándar IVTFF. ZL3b e IT2a son ediciones del mismo manuscrito. El holdout no es históricamente ciego; no se evaluó ninguna hipótesis de traducción. Los resultados de este informe son una inspección de cabeceras; el cierre depende de la evidencia de CI/artefacto, que debe añadirse tras ejecutarse.

## Reproducir

```sh
python -m unittest discover -s tests -p 'test_holdout_locus_coverage.py' -v
python scripts/audit_holdout_locus_coverage.py --out holdout-locus-coverage.json
```
