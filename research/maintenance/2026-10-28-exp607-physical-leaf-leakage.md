# EXP-607 — adjudicación de contaminación entre caras de una hoja (28-10-2026)

**Tipo:** auditoría retrospectiva, sin EXP nuevo. **Decisión:** INVALID_FOR_CLAIM para la afirmación de evaluación sobre hojas físicas completamente reservadas; conservar los resultados exploratorios originales. **Estado de integración:** propuesta en rama; verificar CI, artefacto y SHA final antes de cerrar.

## Incidencia verificable

El EXP-607 histórico calcula la partición con SHA-256 de `fNNr` / `fNNv` y módulo 5, de modo que **divide por cara**, no por hoja física `NN`. No se impone que ambas caras queden juntas. La prueba de pertenencia al grupo de evaluación, el vocabulario y el control barajado utilizan ese reparto. Por tanto, el resultado no satisface la exigencia de hojas físicas enteramente no vistas. Los lectores posteriores de sensibilidad de EXP-607 reutilizan el mismo criterio de división; no son confirmaciones físicamente independientes.

Se inspeccionaron `experiments/exp_607_heldout_bigram_prediction/script.py`, `results.json`, el registro de EXP, `scripts/audit_exp607_reader_sensitivity.py`, `scripts/audit_exp607_scope_sensitivity.py`, `SOUL.md`, `CLAUDE.md` y la norma de integridad. La búsqueda de PR y ramas no encontró otra corrección específica de EXP-607 sobre este defecto. Las PR #2, #8, #10 y #129 ya estaban integradas; las PR #5, #7, #13, #66 y #82 permanecían abiertas al iniciar este bloque. No se ha reasignado ID ni alterado ninguna transcripción.

## Reconstrucción de asignaciones (solo metadatos)

`scripts/audit_exp607_physical_leaf_holdout.py` reproduce **exclusivamente** la selección de loci elegibles y el reparto SHA-256 de caras del lector original. Utiliza los mismos patrones, lectura Latin-1 y condición de al menos dos tokens ASCII; no calcula pérdidas, ganancias, ni permutaciones nuevas. El programa exige SHA-256 de los dos corpus, del script histórico y del JSON histórico antes de reconstruir.

| Transcripción | Caras train/test | Líneas train/test históricas | Hojas físicas distintas en test | Hojas test también en train | Hojas test completamente no vistas |
|---|---:|---:|---:|---:|---:|
| ZL3b | 152/32 | 3.139/600 | 30 | **28** | **2** |
| IT2a | 151/32 | 3.138/597 | 30 | **27** | **3** |

Identidades compartidas ZL3b: 5, 6, 8, 10, 13, 14, 18, 21, 25, 30, 33, 34, 41, 42, 43, 44, 50, 51, 55, 57, 58, 73, 78, 100, 101, 111, 114, 116.

IT2a coincide salvo la hoja 116, ausente de la intersección. Los recuentos y las identidades se fijan en el auditor y deben cotejarse contra el artefacto generado por CI. La reconstrucción preliminar independiente del reparto, basada en las dos transcripciones recuperadas mediante el conector de GitHub, dio 28/27 hojas compartidas. Hasta ejecutar la auditoría en CI no debe darse por cerrada la comprobación completa de elegibilidad y de los 3.139/600 y 3.138/597 loci.

### Fuentes congeladas

- Script EXP-607 SHA-256: `a991bf0b3a3b209a542b071da1b800d23eeb662990482413b57089ad848cbc97`.
- JSON histórico SHA-256: `d6aa4cb01c066cf3a25bc8c07ce90840a0dde3084bb4178696c94a1ce96b5218`.
- ZL3b SHA-256: `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- IT2a SHA-256: `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.
- Partición histórica: `int(sha256(folio.encode()).hexdigest()[:8], 16) % 5 == 0` para test; sin semilla aleatoria. Control barajado histórico: `6072026`; no se ejecuta aquí.
- Los valores históricos permanecen en `results.json`: ganancia real frente a unigramas 0,26679 bits/token (ZL3b) y 0,34096 (IT2a); diferencia real menos control barajado 0,05591 y 0,05498. **No se reproducen ni reinterpretan en este bloque.**

## Reparación y criterio de cierre

Archivos añadidos: `scripts/audit_exp607_physical_leaf_holdout.py`, `tests/test_exp607_physical_leaf_holdout.py`, `experiments/exp_607_heldout_bigram_prediction/CORRECTION.md` y este informe. El workflow `.github/workflows/voynich-check.yml` ejecuta regresiones normales y `-O`, genera `exp607-physical-leaf-holdout.json` con modo exclusivo (sin sobrescribir) y conserva el artefacto. La CI debe fallar ante deriva de corpus, script, JSON histórico, conteos o identidades de hojas compartidas.

Comandos desde la raíz:

```bash
python -m unittest discover -s tests -p 'test_exp607_physical_leaf_holdout.py' -v
python -O -m unittest discover -s tests -p 'test_exp607_physical_leaf_holdout.py' -v
python scripts/audit_exp607_physical_leaf_holdout.py --out exp607-physical-leaf-holdout.json
```

Las cinco regresiones sintéticas pasaron localmente con Python normal y `-O` (5/5 cada uno). **Pendiente:** cotejar los corpus reales en CI, verificar el JSON y su hash, y confirmar el estado del commit de integración. No llamar `REPRODUCED` al experimento completo.

## Autoauditoría de alcance

**Conocimiento del objetivo:** la auditoría se eligió para revisar una afirmación de holdout; las hojas no se utilizaron para seleccionar una regla semántica. **Rasgos destruidos:** se reconstruye la partición histórica sin modificar tokens, modelo ni control. **Extrapolación:** la invalidación se limita a generalización sobre hojas físicas no vistas; no se niega el patrón de orden local. **Negativo:** el reparto histórico no cumple el criterio físico, pero no se sabe cuánto infló las ganancias. **Control esperado y observado:** en el fixture, `f5r` y `f5v` se reparten y comparten hoja 5; `f1r` y `f1v` permanecen juntas y no generan solapamiento. Este es un control de metadatos, no una prueba de rendimiento predictivo.

## Bloqueos y siguiente acción

La conformidad IVTFF completa y la procedencia de otros artefactos históricos siguen pendientes; EXP-170 carece de las entradas externas exactas para reproducción íntegra. Para evaluar una regla de descifrado, preregistrar una partición nueva por **hoja física**, sin usar los folios ya observados para selección, y demostrar recuperación de información en controles de verdad conocida. No inferir significados a partir de este diagnóstico. Evaluación general: 22-11-2026, sin prometer descifrado.
