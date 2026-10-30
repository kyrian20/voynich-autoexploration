# Cabeceras IVTFF repetidas: preflight aditivo y conservación de EXP-173 — 27-10-2026

**Estado:** reparación propuesta en PR #100; nueva CI y comprobación posterior a integración pendientes. No es un EXP, ni una prueba de significado o desciframiento. Base de la rama: `master` `03a069ff3818440510c28d8a597353e3146cf306`.

## Defecto acotado

El auditor histórico `scripts/audit_ivtff_metadata.py` construye `pages[folio] = lang`, de modo que una segunda cabecera de folio con otro `$L` puede sustituir la clasificación anterior. Existe además el auditor aditivo `audit_ivtff_metadata_strict.py`, que ya rechaza **asignaciones contradictorias** de `$L`, pero permite expresamente cabeceras repetidas con `$L` igual o con la primera asignación ausente. Por tanto, no se presenta la contradicción de `$L` como una vulnerabilidad sin protección en CI. El nuevo alcance es más estrecho: **la identidad de cabecera física debe ser única** en el corpus congelado, incluso si la repetición es coherente en el valor de `$L`.

El control nuevo `scripts/audit_ivtff_unique_page_headers.py` detecta toda repetición bajo el patrón de cabeceras existente. Los casos sintéticos comprueban duplicados iguales/contradictorios, primera cabecera sin `$L`, panel `f67r1` y página `fRos`. El control válido con tres páginas distintas pasa. El corpus ZL3b original contiene 227 cabeceras reconocidas y 227 identificadores únicos; IT2a tiene 225 y 225, según lectura de los archivos de `master` antes de editar. **No se observó este defecto en los datos congelados**.

## Fallo detectado y rectificación preservada

La primera implementación de esta PR modificó el auditor histórico y `tests/test_ivtff_metadata.py`. La CI del head `d27f0bf8718d2f7630be26f38ad0339cb2225b76` falló: [run 40492825594](https://github.com/kyrian20/voynich-autoexploration/actions/runs/40492825594), paso **Reproducir auditorías acotadas de EXP-173**, con `Snapshot mismatch: results.json` en `audit_exp173_reader_bridge.py --check`. Causa concreta: ese snapshot congela el **SHA-256 del archivo** `scripts/audit_ivtff_metadata.py` como dependencia. Cambiar el lector invalida su identidad histórica aunque la estadística no cambie. Las pruebas nuevas aún no se habían ejecutado porque el workflow abortó antes de alcanzarlas.

**Rectificación:** se restauraron exactamente los blobs históricos de `scripts/audit_ivtff_metadata.py` (Git blob `6458f89ebd1ea5fe78dba15881fc9e81b2b8778b`) y `tests/test_ivtff_metadata.py` (Git blob `45da02bfbba6c1437e3c0552c15df87cce71db14`). Se añadieron script y pruebas **separados** y una etapa CI específica posterior a los auditores congelados. No se actualizó el snapshot histórico para hacerlo pasar, ni se sustituyeron resultados antiguos. El fallo inicial queda registrado y no se cuenta como éxito.

## Archivos finales y reproducción

- `scripts/audit_ivtff_unique_page_headers.py`: preflight aditivo; imprime censo, estado limitado y SHA-256 real de la entrada.
- `tests/test_ivtff_unique_page_headers.py`: control válido, 12 combinaciones adversariales y comprobación de 227 cabeceras archivadas.
- `.github/workflows/voynich-check.yml`: ejecuta las pruebas y el preflight después de los controles Currier históricos.
- Este informe: alcance, error de integración detectado y corrección.

```sh
python tests/test_ivtff_metadata.py
python scripts/audit_ivtff_metadata.py
python tests/test_ivtff_metadata_strict.py
python scripts/audit_ivtff_metadata_strict.py
python -m unittest discover -s tests -p 'test_ivtff_unique_page_headers.py' -v
python scripts/audit_ivtff_unique_page_headers.py
python scripts/audit_exp173_reader_bridge.py --check research/maintenance/2026-10-23-exp173-reader-bridge
```

El SHA-256 archivado de `data/transcriptions/eva_zl3b.txt` es `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc` (procedencia histórica; el nuevo preflight lo recalcula al ejecutarse). No hay semilla ni parámetro estocástico: son controles deterministas. Se conservan corpus, resultados negativos, manifiestos, hashes históricos y `state/committed_claims.md`.

## Puerta de cierre y límites

Exigir CI satisfactoria **del último commit de la PR**, evidencia del preflight y del snapshot EXP-173, y posteriormente CI del SHA fusionado de `master`. Hasta entonces el estado es **PROPUESTO**, no integrado/verificado. La unicidad bajo este regex no certifica cabeceras malformadas omitidas, conformidad IVTFF integral, independencia de las ediciones, correspondencia texto-imagen ni semántica. La partición de folios está históricamente expuesta. PR #5/#7/#13/#66/#82 continúan pendientes de revisión científica/documental.
