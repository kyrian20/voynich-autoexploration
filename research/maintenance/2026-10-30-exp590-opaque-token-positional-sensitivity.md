# EXP-590 — sensibilidad de posición final al conservar códigos high-ASCII como unidades opacas

**Fecha:** 2026-10-30. **Tipo:** reparación de alcance interpretativo sobre una entrada real; no EXP nuevo. **Estado:** pendiente de verificación CI de esta rama y posterior a integración. No se ha ejecutado ninguna permutación ni un predictor.

## Incidencia concreta y antecedentes

El lector histórico de `scripts/exp590_daiin_position.py` elimina anotaciones IVTFF y reconoce solo `[a-z]+`. El inventario de [PR #177](2026-10-30-ivtff-high-ascii-unreadable-record-reconciliation.md) documentó códigos `@NNN;` que no son espacios vacíos; la [PR #178](2026-10-30-exp590-high-ascii-adjacency.md) cuantificó su contacto con letras ASCII y distinguió ligaduras. **Esta auditoría no repite esos censos**: mide cuánto cambia el conteo posicional exacto de `daiin` al conservar los códigos como unidades opacas, sin atribuirles letras ni significados.

Pregunta falsable: ¿los 134 registros de `daiin` en posición final de la vista ASCII ZL3b siguen siendo finales si se conserva un código high-ASCII como unidad desconocida? Se fija de antemano el criterio: comparar exactamente las mismas filas físicas y los mismos delimitadores, sustituir únicamente `@128;`–`@255;` por `¤` antes del filtrado histórico de `<...>`, `{...}` y `[...]`, y tokenizar `[a-z¤]+`. Las letras contiguas a un código permanecen unidas a la unidad opaca; la puntuación sigue separando. No se reconstruye un glifo ni se modifica el corpus.

## Cotejo independiente preliminar de las tres fuentes

Un recorrido independiente sobre las fuentes congeladas, usando la misma expresión de filas y la política explícita anterior, produjo esta tabla. **La reproducción por el script Python y la CI deben confirmarse antes de considerarla cerrada**.

| Edición | Filas físicas | Filas ASCII / opacas | Tokens ASCII / opacos | `daiin` exactos | Iniciales ASCII / opacas | Finales ASCII / opacas | Filas con tokens diferentes |
|---|---:|---:|---:|---:|---:|---:|---:|
| ZL3b | 5.385 | 5.376 / 5.385 | 39.594 / 39.610 | 853 / 853 | 161 / 161 | **134 / 133** | 85 |
| ZL3a | 5.389 | 5.380 / 5.388 | 39.596 / 39.614 | 853 / 853 | 161 / 161 | **134 / 133** | 81 |
| IT2a | 5.215 | 5.207 / 5.207 | 37.945 / 37.945 | 865 / 865 | 157 / 157 | 134 / 134 | 0 |

La discrepancia posicional identificable está en **`f19r.5`** de ZL3b y ZL3a: `otchy.tchy.qoky.daiin.@243;`. El lector ASCII cuenta `daiin` como último token porque descarta `@243;`; la política opaca conserva un último token desconocido y deja `daiin` en penúltima posición. Es una discrepancia **real de selección/definición de unidad**, no una corrección de la lectura paleográfica. La cantidad de `daiin` exactos y su número de inicios no cambian bajo esta única política. Los totales de tokens no son directamente comparables como si ambas vistas tuvieran idéntico vocabulario; incluyen marcadores opacos en la alternativa.

## Código, entradas y criterio de cierre

- Script: `scripts/audit_exp590_opaque_token_sensitivity.py`, sin efectos sobre los originales. Reutiliza el auditor de la PR #178 para comprobar hashes, inventario y estructura; coteja **todas las listas históricas ZL3b** con el lector productivo `load_lines`.
- Regresiones: `tests/test_exp590_opaque_token_sensitivity.py`; cubren fragmentación de letras, código final, comentarios/alternativas/ligaduras excluidos, fila ASCII vacía, separadores físicos inválidos y los tres corpus congelados.
- Fuente ZL3b: `data/transcriptions/eva_zl3b.txt`, SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- Fuente ZL3a: `data/transcriptions/zl3a.txt`, SHA-256 `56419297682d338ff1a0a17f5ae251e3ee3e2c5bf05a62db04c5385ef30b36a2`.
- Fuente IT2a: `data/transcriptions/eva_it2a.txt`, SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.
- Sin aleatoriedad ni semilla; no se asigna EXP ni se usan folios prospectivos reservados.

Comandos desde la raíz (Python 3.12):

```sh
python -m unittest discover -s tests -p 'test_exp590_opaque_token_sensitivity.py' -v
python -O -m unittest discover -s tests -p 'test_exp590_opaque_token_sensitivity.py' -v
python scripts/audit_exp590_opaque_token_sensitivity.py --out /ruta/nueva/exp590-opaque-token-sensitivity.json
sha256sum /ruta/nueva/exp590-opaque-token-sensitivity.json
```

La salida incluye para cada fila modificada el locus, línea física, cuerpo crudo, SHA-256 del cuerpo, listas de tokens de ambas políticas y deltas; la creación es exclusiva (`x`) para impedir sobrescritura. CI archiva JSON y SHA-256 durante 90 días. La CI de software no equivale a una validación de IVTFF ni a una reproducción de las 5.000 permutaciones de EXP-590.

## Decisión científica y autoauditoría

**Clasificación:** la cifra histórica 134 sigue siendo correcta **para la vista ASCII histórica**, pero no puede citarse como recuento inequívoco de finales de línea del manuscrito sin fijar una política para los códigos opacos. La alternativa da 133, bajo un supuesto de tokenización explícito y refutable. No se retira la cifra de su contexto original ni se reemplazan resultados históricos. Los resultados del test de permutación, que usa solo inicios, **no se han recalculado ni validado** con esta auditoría; su validez científica sigue condicionada por las demás incidencias.

**Conciencia del objetivo:** la política de marcador opaco se fija por sintaxis, no se calibra al número de finales de `daiin`. **Implementación:** no se destruye el código high-ASCII; se preserva como marcador desconocido, pero no se adjudican ligaduras ni `?`. **Extrapolación:** únicamente estas tres ediciones y esta política. **Resultado negativo:** la invariancia de los 853 `daiin` exactos y los 161 inicios no demuestra invariancia bajo otras lecturas. **Control:** en IT2a se esperan cero cambios porque carece de códigos high-ASCII visibles; el cotejo independiente observa cero. Un control sintético `daiin.@140;` debe perder la clasificación final y `a@140;b` debe ser una unidad opaca, no dos palabras claras.

**Pendientes independientes:** adjudicación IVTFF completa, reconstrucción histórica exacta EXP-170, conciliación de artefactos y revisión científica de las PR en borrador. No se ha obtenido traducción ni ancla semántica. Evaluación general prevista para el 22-11-2026 sin prometer descifrado.
