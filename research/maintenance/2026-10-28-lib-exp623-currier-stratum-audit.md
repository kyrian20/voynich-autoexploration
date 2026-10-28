# LIB-ORDER-2026-10-19-B — grupo Currier sin adjudicar (28-10-2026)

**Tipo:** reparación de auditoría de procedencia; no es un EXP nuevo ni reproducción de puntuaciones. **Estado:** corrección propuesta; comprobar CI y commit de integración antes de declarar cierre.

## Incidencia verificable

El piloto histórico B no se dividió exclusivamente entre Currier A y B. El lector `eligible_b` de la reconstrucción preservada en `scripts/audit_library_exp623_leaf_leakage.py` incluye un tercer grupo `?` para páginas con cabecera sin `$L=A/B`. Este grupo no figuraba explícitamente en la evidencia JSON ni estaba protegido por una regresión. Describir su reparto simplemente como «estratificado por Currier A/B» oculta una exclusión de metadatos relevante.

Ambas transcripciones hash-identificadas contienen **203 caras elegibles** para B: **114 A, 81 B y 8 sin `$L`**. Las ocho caras sin clasificación son, en orden de lectura: `f65v`, `f67r1`, `f67r2`, `f68r1`, `f68r2`, `f68v3`, `f68v2`, `f69r`. Sus cabeceras contienen otros metadatos (`$Q`, `$I`, etc.), pero **no** `$L`; no se deduce Currier a partir de esos campos. La observación se obtuvo leyendo las cabeceras y reproduciendo el filtro de elegibilidad sin inspeccionar palabras de test para elegir una regla.

## Procedencia y límites

- ZL3b: `data/transcriptions/eva_zl3b.txt`, SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- IT2a: `data/transcriptions/eva_it2a.txt`, SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.
- Fuente histórica B externa: `exp623_order_null.py`, SHA-256 `ea51e67e6f36b8c651231262cb22ebbb5ef9f98cd31c4673924e33d6a3627010`. Los originales no se copian ni modifican.
- Reconstrucción y alcance previo: `research/maintenance/2026-10-28-lib-exp623-physical-leaf-leakage.md`.
- La existencia de ocho páginas sin `$L` **no demuestra** que el resultado numérico del piloto cambie. Las 60 particiones históricas y su contaminación por hoja física se conservan como evidencia `INVALID_FOR_CLAIM` para holdout físico. Las dos ediciones no son muestras independientes.

## Corrección

El auditor ahora publica `B_currier_group_counts` y `B_unclassified_folios` por transcripción. `--check` rechaza alteraciones de esos recuentos o identidades, además de mantener los SHA-256 previamente fijados para las 60 particiones. Una regresión sintética comprueba que una página sin `$L` queda en `?` y otra que la pérdida de una página no clasificada falla de forma cerrada.

Comandos de verificación desde la raíz:

```sh
python -m unittest discover -s tests -p 'test_library_exp623_leaf_leakage.py' -v
python -O -m unittest discover -s tests -p 'test_library_exp623_leaf_leakage.py' -v
python scripts/audit_library_exp623_leaf_leakage.py --check
```

**Criterio de cierre:** pruebas anteriores y CI de la rama satisfactorias; comprobar los campos nuevos y que los hashes congelados de las 60 particiones no cambian. No afirmar CI verde ni fusión antes de inspeccionarlas.

## Decisión y siguiente paso

Esta reparación protege la atribución de las páginas sin clase y evita presentarlas como Currier A/B. **No valida** el holdout físico de LIB-EXP-623, no reproduce puntuaciones históricas y no aporta traducción. Para un futuro contraste confirmatorio debe fijarse antes del entrenamiento la política de exclusión o tratamiento del grupo `?`, y reservar hojas físicas completas sin escoger reglas a partir de las hojas de test. La evaluación global permanece prevista para el 22-11-2026.
