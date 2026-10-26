# Corrección acotada: límite posterior de la cabecera IVTFF en holdout v2

Fecha: 2026-10-26. Estado: **propuesta operativa pendiente de CI remota**; sin experimento semántico ni EXP nuevo.

## Problema falsable

Tras la corrección de la PR #84, `HEADER_V2` identificaba la etiqueta `<f67r>` al principio de `<f67r>garbage` y `<f68r>` al principio de `<f68r><!comment>`. El selector interpretaba ambas líneas sintéticas como cabeceras completas y podía incorporar hojas fantasma al manifiesto de futuros folios reservados. No se ha observado este defecto en las transcripciones originales consultadas: es un fallo de aceptación de entrada malformada, no una afirmación de corrupción del corpus.

## Reparación

En `scripts/prepare_prospective_leaf_holdout_v2.py` se exige que después del `>` del identificador de página haya espacio, tabulador o fin de línea. Se mantiene la distinción entre cabeceras y loci y la agrupación de paneles 1–6. Se añade `test_page_tag_requires_boundary_after_closing_bracket` en `tests/test_prospective_leaf_holdout_v2.py`. No se modifica el lector histórico v1, ningún corpus ni manifiesto congelado.

La restricción es **específica del selector de cabeceras para el holdout**, no una certificación de toda la gramática IVTFF.

## Base y fuentes

- Base `master`: `3a4e2801a8e73b68f13ffdbe94b4394705fea7b7`.
- Fuente ZL3b `data/transcriptions/eva_zl3b.txt`: blob Git `2a4533ab9bdfa85db9bad602d590978953055df1`, SHA-256 archivado `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- Fuente IT2a `data/transcriptions/eva_it2a.txt`: blob Git `4d6d3f2537b1f507a257529b49c94af7d6e03446`, SHA-256 archivado `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.
- Exploración de las líneas originales recibidas desde GitHub: el patrón previo y el corregido identifican **102 hojas distintas por fuente**. No se encontró ninguna cabecera cuyo sufijo pegado fuese admitido por el patrón antiguo y rechazado por el nuevo. Esta comprobación de conjuntos no reemplaza el cotejo byte a byte del manifiesto.

## Criterios y pruebas

Entrada sintética previa: `<f67r1>garbage`, `<f68r><! $L=B>`, `<f69r> <! $L=A>`, `<f70r>`, `<f71r.1,@P0>`. Esperado: **solo hojas 69 y 70**; si únicamente hay sufijos pegados, excepción `No folio headers`. El patrón anterior acepta indebidamente 67 y 68. Control: cabecera con espacio y cabecera sin metadatos deben seguir siendo aceptadas; locus huérfano no se acepta. Semilla: no procede (prueba determinista, sin aleatoriedad). Unidad: línea física y hoja numérica; `fRos` se excluye por diseño.

Comprobación local acotada: seis cadenas sintéticas confrontadas con los patrones antiguo y nuevo mediante Python, resultado esperado confirmado. **No equivale a ejecutar toda la suite del repositorio**.

Reproducción exigida en CI, Python 3.12:

```sh
python -m unittest discover -s tests -p 'test_prospective_leaf_holdout_v2.py' -v
python scripts/prepare_prospective_leaf_holdout_v2.py --out /tmp/holdout-v2-replay.json
cmp research/decipherment/2026-10-23-prospective-leaf-holdout/manifest-v2.json /tmp/holdout-v2-replay.json
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

Verificar ejecución y logs de la PR antes de declarar **REPRODUCED**. Si cambia el manifiesto, detener integración y adjudicar; no sustituir el archivo histórico.

## Límites

No se prueba ninguna regla de descifrado, no se asigna significado, no se ha usado el test de folios reservados. Los folios ya inspeccionados no son un holdout históricamente ciego. La adjudicación IVTFF completa y la identidad de corpus históricos siguen pendientes. El piloto semántico continúa bloqueado por referentes y anotadores independientes.
