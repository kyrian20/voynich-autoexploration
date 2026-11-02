# Reparación acotada: validación de $L Currier en los lectores Zhang–Sheng

**Fecha:** 2026-11-02. **Base inspeccionada:** `master` `02c60bd12597319c283018e2a0e2619e50520f09`. **Tipo:** corrección de integridad de metadatos, sin nuevo EXP.

## Defecto, causa y falsación

Ambos lectores usaban `re.search(r"\\$L=([AB])", ...)`, que aceptaba prefijos de campos malformados: `$L=AB` y `$L=A $L=B` se clasificaban silenciosamente como A. Esto puede contaminar cualquier uso futuro por clase Currier. La métrica actual de pares no utiliza la clase, por lo que **no se afirma que sus puntuaciones hayan cambiado**. No hay evidencia de esas anomalías en los corpus congelados.

Se añade `checked_currier_metadata` para exigir un solo campo `$L=A` o `$L=B` completo, rechazar duplicados, contradicciones, valores parciales y espacios Unicode anómalos. Si falta `$L`, se conserva `None`, nunca se infiere desde `$Q`. Dos regresiones comprueban seis entradas adversariales y cabeceras B y desconocida válidas en ambos lectores.

**Criterio de aceptación:** pasan tests normales y optimizados, corpus ZL3b/IT2a sin cambio de población, las dos filas numéricas congeladas de reproducción acotada y el CI exacto de PR/master.

## Comandos y preservación

```sh
python -m unittest discover -s tests -p 'test_zs_wordpair_source_lock.py' -v
python -O -m unittest discover -s tests -p 'test_zs_wordpair_source_lock.py' -v
python -m unittest discover -s tests -p 'test_zs_wordpair_archive_contract.py' -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

Se conservan intactos `data/transcriptions/`, `results.json` (54 filas), semillas 20261101–20261103, particiones reservadas, resultados negativos y `state/committed_claims.md`. Fuentes SHA-256: ZL3b `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`; IT2a `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.

**Estado al abrir PR:** CI todavía no inspeccionada. No se ha ejecutado un nuevo experimento ni se ha asignado significado a tokens. No certifica conformidad IVTFF completa, reproducción de 52 filas adicionales, independencia física de las mitades históricas ni recuperación de EXP-170. Evaluación general: 22-11-2026.
