# Corrección acotada: etiquetas IVTFF ocultas tras una barra de continuación

**Fecha:** 2026-11-02. **Base inspeccionada:** `master` `243d581a06d6a509c5db23d4565bef7cffcb4cbb`. **Clase:** integridad de lector, sin nuevo EXP. **Estado científico:** ninguna traducción validada.

## Defecto verificable y alcance

En `research/maintenance/2026-11-01-zs-wordpair-audit/wordpair_audit.py`, ambos lectores (`read_pages` y `read_pages_legacy`) omiten filas físicas sin una etiqueta `<f...>` al comienzo. El iterador común rechazaba etiquetas con sangría o sin separador, pero no etiquetas de página o locus precedidas por una barra de continuación (`/<f2r>`, `/<f1r.2,@P0>`). Una fila así se descartaba como texto no estructural, dejando la página activa sin advertencia. El auditor estructural canónico `scripts/audit_ivtff_page_locus_ids.py` ya considera estos casos malformados; esta corrección alinea la puerta del lector estadístico con esa política, sin modificar el auditor canónico.

**Fixture adversarial:** una cabecera `<f1r> <! $L=A>`, seguida de `/<f2r> <! $L=B>` y una fila válida de f1r. La versión anterior ignoraba la falsa cabecera sin error. El criterio de aceptación es que ambos lectores lancen `ValueError` antes de contar palabras; se comprueban asimismo un locus tras barra y una variante con sangría. Las continuaciones válidas dentro de registros etiquetados conservan su regresión positiva previa.

## Reparación y comprobaciones requeridas

- `wordpair_audit.py`: `physical_ivtff_rows` detecta una barra inicial opcionalmente sangrada seguida de una etiqueta `<f...` y rechaza la fila; no convierte ni repara la entrada.
- `tests/test_zs_wordpair_source_lock.py`: regresión con tres filas adversariales y los dos lectores, seis casos de rechazo. La prueba de continuación contigua válida preexistente sigue vigente.
- No se cambia `scripts/ivtff_lossless.py`, el cálculo de métricas, el universo P/C/R, las particiones ni el contrato de resultados.

Desde la raíz, ejecutar:

```sh
python -m unittest discover -s tests -p 'test_zs_wordpair_source_lock.py' -v
python -O -m unittest discover -s tests -p 'test_zs_wordpair_source_lock.py' -v
python -m unittest discover -s tests -p 'test_zs_wordpair_archive_contract.py' -v
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

La CI debe comprobarse en el SHA exacto de la PR; si se integra, verificar otra CI posterior de `master`. Este informe por sí solo no demuestra ejecución.

## Integridad, interpretación y pendientes

Los originales `eva_zl3b.txt` (SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`) e `eva_it2a.txt` (SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`) permanecen congelados. También permanecen sin cambios las 54 filas archivadas, las semillas 20261101–20261103, los logs y resultados históricos, los manifiestos de hojas reservadas y `state/committed_claims.md`.

Los casos adversariales son sintéticos: no se afirma que aparezcan en las transcripciones originales ni que hayan alterado correlaciones. Solo dos de las 54 filas archivadas tienen regresión numérica de reproducción; las mitades históricas comparten cuatro hojas físicas y no constituyen holdout independiente. EXP-170 sigue `BLOCKED` para reproducción histórica exacta por falta de recibos de entradas externas; siguen pendientes la conformidad IVTFF integral, la conciliación de artefactos y las PR científicas #7/#138. No ejecutar nuevos ciclos científicos prohibidos por contradicciones pendientes.

**Cierre de esta incidencia:** condicionado a regresiones y CI verificadas. **Evaluación global:** 2026-11-22, sin promesa de descifrado.
