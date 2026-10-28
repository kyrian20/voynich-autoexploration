# Protección contra sobrescritura del manifiesto prospectivo v2 — 28-10-2026

**Clase:** corrección de integridad operativa, no experimento lingüístico ni nuevo EXP. **Base:** `master` `f5d965ef434e4bf5e37b13b49b550f330fac51d0`. **Estado del informe:** propuesta; verificar ejecución y CI antes de declarar integración.

## Defecto concreto

`scripts/prepare_prospective_leaf_holdout_v2.py --out RUTA` utilizaba `Path.write_text()`, que **trunca y sustituye** silenciosamente una ruta existente. El generador tiene acceso a los corpus y a los manifiestos congelados; una ruta de salida equivocada podía destruir evidencia histórica o sobrescribir el manifiesto de particiones reservado. No se ha observado una sobrescritura real de corpus; es un defecto reproducible del comportamiento de escritura.

## Cambio acotado

Se usa `Path.open("x", encoding="utf-8", newline="\\n")` con escritura dentro de un contexto: solo se crea una ruta inexistente. Si existe un archivo o enlace simbólico, se rechaza con `FileExistsError` sin modificar su destino. No se cambia la sal, las particiones, la política de folios, el tokenizador ni las fuentes.

Se añaden dos regresiones a `tests/test_prospective_leaf_holdout_v2.py`: (1) generación nueva con comparación byte a byte contra `manifest-v2.json` congelado; (2) rechazo de archivo preexistente y de enlace simbólico, verificando bytes originales. Las pruebas usan un directorio temporal para no tocar los manifiestos archivados. No hay semillas ni aleatoriedad nuevas.

## Comprobación exigida

```sh
python -m unittest discover -s tests -p 'test_prospective_leaf_holdout_v2.py' -v
python -O -m unittest discover -s tests -p 'test_prospective_leaf_holdout_v2.py' -v
python scripts/prepare_prospective_leaf_holdout_v2.py --out prospective-leaf-holdout-v2.json
cmp research/decipherment/2026-10-23-prospective-leaf-holdout/manifest-v2.json prospective-leaf-holdout-v2.json
```

El workflow existente `Voynich Check` ya ejecuta las regresiones normales y la comparación del manifiesto; no se crea otro workflow ni se relanzan ejecuciones ajenas. Verificar el SHA exacto del commit de PR, los pasos y el run de `master` después de fusionar. Conservar los resultados negativos y los artefactos originales.

**Limitaciones:** esta reparación impide sobrescrituras de la salida v2; no certifica IVTFF completo, procedencia de todos los archivos, independencia histórica de los folios reservados, validez predictiva o traducción. El generador v1 permanece congelado. EXP-170 y la conciliación histórica de artefactos continúan pendientes. Evaluación general: 22-11-2026, sin garantía de desciframiento.
