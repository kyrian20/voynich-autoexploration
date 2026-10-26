# Reparación del selector de hojas v2: cabeceras reales, no loci

Fecha: 2026-10-26. Estado: corrección operativa propuesta; verificación remota por CI pendiente en el momento de redactar este registro. Sin EXP nuevo ni inferencia semántica.

## Incidencia reproducible

La expresión anterior `^<f(\\d+)[rv]\\d*(?:[.,][^>]*)?>` de `scripts/prepare_prospective_leaf_holdout_v2.py` aceptaba tanto cabeceras `<f67r1>` como registros `<f67r1.1,@P0>`, paneles inválidos `<f2r7>`, cabeceras con coma `<f3r,>` y cifras Unicode. Un locus huérfano podía crear una hoja elegible aunque faltase su cabecera, contradiciendo la política escrita de selección por cabecera.

## Reparación y criterio

Sustituir por `^<f([0-9]+)[rv][1-6]?>`: únicamente cabeceras de página válidas según el alcance de `audit_ivtff_page_locus_ids.py`, conservando paneles 1–6 y agrupación por hoja. Rechazar loci huérfanos, paneles inválidos, comas y dígitos no ASCII. No alterar el algoritmo de partición, la sal, los manifiestos archivados ni los corpus. La condición de aceptación es: las pruebas sintéticas rechazan los falsos encabezados y el manifiesto v2 generado a partir de los corpus originales sigue siendo **idéntico por bytes** al archivado.

## Procedencia y comprobación previa

Base `master`: `37250ef3b12f1e1979237731228edd08f35f74c2`. Blobs de fuentes inspeccionadas por el conector de GitHub: ZL3b `2a4533ab9bdfa85db9bad602d590978953055df1`, IT2a `4d6d3f2537b1f507a257529b49c94af7d6e03446`. SHA-256 de corpus ya congelados en `manifest-v2.json`: ZL3b `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`, IT2a `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.

Escaneo independiente en memoria de los textos recibidos por GitHub: el lector amplio reconoce 5.451/5.440 etiquetas numéricas, mientras el patrón de **cabeceras estrictas** reconoce 226/225 cabeceras; ambos dan exactamente 102 hojas distintas por edición y ninguna hoja adicional. Esta igualdad de conjuntos **no sustituye** el cotejo byte a byte del JSON por CI. El manifiesto v2 archivado (blob `84f59008a190df7481c4e81a5c84c3916d79a59d`) y el v1 permanecen intactos.

## Pruebas y reproducción exigidas

```sh
python -m unittest discover -s tests -p 'test_prospective_leaf_holdout_v2.py' -v
python scripts/prepare_prospective_leaf_holdout_v2.py --out /tmp/holdout-v2-replay.json
cmp research/decipherment/2026-10-23-prospective-leaf-holdout/manifest-v2.json /tmp/holdout-v2-replay.json
python -m unittest discover -s tests -p 'test_holdout_page_crosswalk.py' -v
python scripts/audit_holdout_page_crosswalk.py --out /tmp/holdout-crosswalk.json
cmp research/maintenance/2026-10-25-holdout-page-crosswalk/results.json /tmp/holdout-crosswalk.json
```

Tres regresiones nuevas: loci huérfanos, cabeceras malformadas y cifras Unicode. Las pruebas anteriores de paneles y partición usan ahora **cabeceras sintéticas reales** en lugar de registros presentados como cabeceras. La CI canónica ejecuta la primera prueba y el `cmp` de manifiesto, además de las auditorías de cobertura; verificar el run específico antes de declarar éxito.

## Límites y siguientes pasos

La reparación corrige la selección de hojas para futuros protocolos, no revalida resultados históricos ni acredita conformidad IVTFF completa. El manifiesto está marcado `PROPOSED_FOR_FUTURE_RULES`: no es una partición históricamente ciega, y no se ha ejecutado ninguna regla sobre folios reservados. La prueba semántica permanece bloqueada por falta de referentes y anotaciones independientes. Revisar CI, diff y concurrencia antes de integrar; si la reproducción no coincide, conservar los originales y abrir adjudicación, no sustituir el manifiesto.
