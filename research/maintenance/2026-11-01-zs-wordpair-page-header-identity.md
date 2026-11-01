# Zhang–Sheng: control de identidad de cabeceras de página

**Fecha:** 2026-11-01. **Tipo:** reparación de integridad de un lector de auditoría parcial; no es un EXP nuevo ni un resultado de descifrado.
**Base revisada:** `master` `3938af4d0d54ff1e8f30e5e70ada982c42aae516` (PR #226 integrada, CI posterior satisfactoria).

## Defecto identificable

En `research/maintenance/2026-11-01-zs-wordpair-audit/wordpair_audit.py`, los dos lectores `read_pages` y `read_pages_legacy` usaban `PAGE_ID.match()` sobre cabeceras y no verificaban identidades de páginas repetidas. Así, `<f1rEXTRA>` podía interpretarse como `f1r`; y `<f1r>` junto con `<f01r>` podían contarse como páginas distintas de un mismo folio físico. Un lector que cuenta páginas incorrectamente puede alterar la partición por bloques de diez y los denominadores de la correlación.

La vulnerabilidad se identifica por inspección del código y se comprueba mediante entradas sintéticas adversariales. **No se afirma que las transcripciones congeladas contengan esas corrupciones.**

## Reparación y criterio

- Función compartida `checked_page_header()` que exige coincidencia completa con la gramática de cabeceras usada por esta auditoría, prohíbe folio cero y rechaza identidades físicas duplicadas (normalizando ceros iniciales).
- Ambos lectores conservan la grafía original de la cabecera para comprobar los loci de sus líneas; la normalización solo se utiliza para detectar duplicados.
- Nuevas regresiones con cabeceras malformadas, duplicados físicos por alias y verificación del número de cabeceras de los dos corpus congelados.
- Criterio de aceptación: las entradas adversariales deben rechazarse y las dos fuentes originales deben seguir produciendo los recuentos 227/225 de cabeceras; las dos filas previamente congeladas de la prueba de contrato deben reproducirse sin cambiar los resultados.

## Comprobaciones reproducibles

```bash
python -m unittest discover -s tests -p 'test_zs_wordpair_source_lock.py' -v
python -m unittest discover -s tests -p 'test_zs_wordpair_archive_contract.py' -v
python -O -m unittest discover -s tests -p 'test_zs_wordpair_source_lock.py' -v
```

La CI canónica añade comprobaciones de integridad, suites y artefactos. Confirmar el run de la PR y el posterior a la integración antes de declarar cierre.

## Fuentes y conservación

ZL3b: SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`; IT2a: `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`. Los recibos Git y la rejilla de 54 filas están congelados en el informe y archivo existentes. No se editan corpus, resultados, semillas, particiones ni afirmaciones comprometidas.

## Limitaciones

El control es específico de los lectores de esta auditoría, no un validador IVTFF completo. Las 52 filas no recalculadas permanecen sin reproducción numérica independiente. Las cifras del preprint Zhang–Sheng no se han reproducido y no hay traducción validada. EXP-170 sigue bloqueado para reproducción histórica exacta por falta de entradas externas acreditadas.

**Próxima prioridad:** continuar la conciliación histórica de entradas y artefactos, especialmente EXP-170, sin ejecutar ciclos científicos prohibidos por contradicciones pendientes. Evaluación general prevista para el 22-11-2026, sin prometer descifrado.
