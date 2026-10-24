# IVTFF: separación entre ligaduras de registros y llaves editoriales (24-10-2026)

**Clase:** reparación acotada del instrumento de inventario, sin EXP nuevo.  
**Base inspeccionada:** `master` `92b95f5fe2faab882e02472725dda6a5e6230f49`.  
**Estado inicial:** propuesta con regresiones añadidas; comprobar CI remota antes de declarar la corrección integrada.

## Defecto comprobable en el algoritmo anterior

`scripts/audit_ivtff_brace_spans.py` decía cuantificar material de registros de transcripción que podrían perder los tokenizadores, pero `audit_text` recorría **todas** las líneas que no comenzaban con `#`. Una cabecera como `<f1r> <!editorial {header}>`, una línea sin locus `free {prose}` o el comentario en línea `<f1r.1,@P0> a{ch}b<!editorial {comment}>` añadían llaves editoriales al inventario. En la última cadena solo `{ch}` pertenece al cuerpo transliterado. El comportamiento previo es determinista, no una anomalía inferida en los corpus originales.

## Corrección y prueba falsable

La nueva función `mask_non_record_text` conserva longitud, saltos de línea y offsets de caracteres, pero enmascara cabeceras, texto sin identificador de locus y etiquetas `<...>` dentro del cuerpo. El inventario principal se calcula sobre esa vista; **el informe previo completo** permanece en `historical_non_hash_comment_inventory` y se informa el número de spans completos excluidos. Se actualiza la versión de salida a 3; no se reescriben snapshots ni corpus.

Regresión sintética prerevisable: un fixture con siete spans completos no pertenecientes a líneas de comentario `#` debe producir **tres** spans en cuerpos de registros (`ch`, `sh`, `y'`), con offsets originales idénticos. Otros casos comprueban que una cabecera y un comentario en línea no crean ligaduras y que dos llaves mal cerradas en líneas distintas no se emparejan. Sin semilla ni aleatoriedad. Se añaden cuatro tests de `unittest` y su ejecución obligatoria en `Voynich Check`.

## Alcance y cautelas

- La comparación histórica de 446/444/0 spans no se sustituye retroactivamente: la cifra del inventario de 2026-10-22 pertenece a su población anterior. Una diferencia de conteos exige inspección de las filas reales, no una reinterpretación automática.
- Se usa la gramática de locus de la auditoría estructural actual. Una fila malformada no se repara ni se incorpora a la población por conjetura: debe bloquearla el auditor de estructura independiente.
- Los offsets son índices de caracteres del texto UTF-8 decodificado, no offsets de bytes; las llaves dentro de alternativas `[...]` siguen en la población de ligaduras representadas y requieren su política específica de incertidumbre.
- La máscara de etiquetas `<...>` presupone terminadores correctos. La conformidad completa IVTFF, las alternativas inciertas y el análisis semántico siguen pendientes.
- No se cambian transcripciones, referencias, scripts experimentales, resultados negativos, hashes congelados, ni `state/committed_claims.md`. No hay traducción validada.

**Comprobaciones exigidas para cerrar:** tests nuevos, inventario sobre ZL3b/ZL3a/IT2a, auditoría estructural, CI de la PR en su SHA exacto; tras fusión, una CI nueva de `master`. No usar el verde anterior como evidencia del cambio.
