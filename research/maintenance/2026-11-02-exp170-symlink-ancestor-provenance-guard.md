# EXP-170 — cierre de rutas de entrada con ancestros simbólicos (02-11-2026)

**Clase:** reparación de integridad de procedencia y aislamiento; no experimento científico nuevo. **Reproducción histórica exacta: BLOCKED.** No se ejecuta Naibbe ni se cambia ningún dato histórico.

## Incidencia y criterio falsable

En `scripts/audit_exp170_archive.py`, `verify_frozen_inputs()` rechazaba únicamente un enlace simbólico en el archivo final. En `scripts/run_exp170_isolated_reconstruction.py`, `checked_source()` y la comprobación del archivo mal etiquetado como Latin tenían el mismo límite. Una ruta cuyo **directorio padre** fuera un symlink pasaba estas puertas si el archivo de destino era regular y su SHA-256 coincidía. La verificación de bytes seguía funcionando, pero la garantía de ruta de origen sin redirección era falsa. Este fallo no acredita ninguna alteración del archivo histórico.

**Falsación sintética:** un checkout temporal con `experiments/exp_170_naibbe_simulation` enlazado al directorio original, y un corpus regular con SHA válido, debe ser rechazado *antes* de cargar o ejecutar el AST histórico. Para la reconstrucción, tanto un directorio Naibbe enlazado como un directorio padre del input italiano enlazado deben ser rechazados *antes* de reservar salida o lanzar subprocess. Los archivos regulares con padres reales deben seguir aceptándose.

## Reparación

- `scripts/audit_exp170_archive.py`: `has_symlink_component()` comprueba el archivo y cada ancestro; el candado de entradas congeladas lo utiliza antes de leer bytes.
- `scripts/run_exp170_isolated_reconstruction.py`: reutiliza el mismo candado para código Naibbe, tablas, italiano y archivo históricamente etiquetado Latin.
- `tests/test_exp170_archive.py` y `tests/test_exp170_isolated_reconstruction.py`: dos métodos nuevos de regresión adversarial, el segundo con dos variantes; sin cifrado real. La CI ya ejecuta ambas suites con Python normal y `-O`.

No se cambia el algoritmo criptográfico, la fórmula de semillas, la salida del auditor, los scripts originales congelados ni el contrato de los 400 vectores. Las rutas externas mediante symlink quedan expresamente excluidas incluso si su contenido coincide en SHA-256: es una política de procedencia, no una inferencia de manipulación.

## Entradas históricas conservadas

- `experiments/exp_170_naibbe_simulation/script.py`: SHA-256 `8fe0f7d153211b320b34ca8543dac1ba029e629c4413c203fb2df0031063721c`.
- `experiments/exp_170_naibbe_simulation/result.md`: SHA-256 `740e9997559a43529391ba29e339bbf955722aa0a1b8302efb451cb66706f354`.
- `experiments/exp_170_naibbe_simulation/data/simulation_results.json`: SHA-256 `c71f7161eb69c6cefa7b7fb6a72c000b6647137200166f331ca920042159e874`.
- `data/transcriptions/eva_zl3b.txt`: SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.

Estos valores son candados históricos preexistentes, **no** una reproducción de Naibbe ni hashes calculados de nuevas simulaciones.

## Comprobaciones exigidas

```sh
python tests/test_exp170_archive.py
python -O tests/test_exp170_archive.py
python -m unittest discover -s tests -p 'test_exp170_isolated_reconstruction.py' -v
python -O -m unittest discover -s tests -p 'test_exp170_isolated_reconstruction.py' -v
python scripts/audit_exp170_archive.py --check research/maintenance/2026-10-22-exp170-audit/results.json
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

La aceptación de la corrección requiere consultar el resultado de la CI de la PR y de `master` después de integrarla; la mera presencia de este informe no demuestra ejecución.

## Alcance y bloqueos

No se han recuperado recibos de la ejecución de abril que identifiquen de forma inequívoca el commit de Naibbe y los bytes del texto italiano utilizados para los 400 vectores. El proyecto **no** debe declarar EXP-170 reproducido ni reutilizar afirmaciones invalidadas por la auditoría. No se ha modificado `state/committed_claims.md`, los manifiestos prospectivos, los corpus ni las salidas archivadas. Siguen pendientes la adjudicación IVTFF completa y la conciliación global de artefactos.

Esta corrección no demuestra estructura semántica ni traducción del manuscrito. Evaluación final prevista: 22-11-2026, sin promesa de descifrado.
