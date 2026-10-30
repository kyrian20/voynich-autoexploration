# Auditoría IVTFF de ligaduras: rechazar registros falsos y malformados — 28-10-2026

**Tipo:** corrección de integridad de un inventario descriptivo; no es un EXP nuevo ni una traducción. **Base comprobada:** `master` `e5bb2129ea08836e50beabe042e0743519cf439c` (CI push `40670476845`, success). **Estado inicial:** propuesta en rama, no declarar cierre antes de CI y fusión verificadas.

## Defecto reproducible

`scripts/audit_ivtff_ligature_views.py` usa dos lectores descriptivos: `legacy_parser_coverage` y `audit_source`. Ambos separaban filas mediante `str.splitlines()`, que reconoce ocho separadores Unicode/de control adicionales a CR, LF y CRLF. Un registro `<f1r.1,@P0> daiin` escondido detrás de U+2028 en una fila física de comentario podía entrar en los recuentos de palabras. Además, el regex `TEXT_LINE` aceptaba una etiqueta mal delimitada `<f1r.1,@P0>garbage` como si fuera una fila de texto. El auditor imprimía recuentos sin comprobar primero la integridad estructural de los folios/loci. Esto es un **defecto verificable del lector**, no evidencia de corrupción de las transcripciones reales.

## Corrección y criterio de aceptación

- `scripts/audit_ivtff_ligature_views.py`: ambos lectores recorren filas mediante `checked_physical_lines`; `audit_source` exige antes `audit_text` y `structural_errors` sin anomalías. El inventario de ligaduras, su tokenizador y la comparación histórica conservan sus reglas de proyección.
- `tests/test_ivtff_ligature_views.py`: ocho separadores falsos dentro de comentarios (rechazo), etiqueta de locus sin separador (rechazo), CR/LF/CRLF válidos (aceptación). Ficheros temporales sintéticos, sin semilla.
- No se crea otro workflow: `Voynich Check` ya ejecuta el test y el auditor con los tres corpus.

**Criterio previo:** pruebas anteriores y nuevas satisfactorias; tres corpus reales sin errores estructurales; mismo número de filas y mismos conteos `daiin`/ligaduras que en CI `40670476845`; CI en el SHA final de PR, integración y CI `push` posterior sin fallos. No se acepta un estado vacío de checks como éxito.

## Línea base real conservada (CI push 40670476845)

| Edición | SHA-256 fuente | Filas descriptivas | Ligaduras | `daiin` histórico / expandido |
|---|---|---:|---:|---:|
| ZL3b | `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc` | 5385 | 402 | 853 / 852 |
| ZL3a | `56419297682d338ff1a0a17f5ae251e3ee3e2c5bf05a62db04c5385ef30b36a2` | 5389 | 399 | 853 / 852 |
| IT2a | `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5` | 5215 | 0 | 865 / 865 |

La línea base se ha extraído del log de la ejecución previa, no se ha regenerado ni reescrito. La comparación posterior debe hacerse contra el mismo conjunto de campos, sin reajustar parámetros. Se preservan íntegros los corpus, `results_v1`–`results_v7` del parser independiente, los resultados negativos, scripts históricos, hashes, semillas, folios reservados y `state/committed_claims.md`.

## Comandos y límites

```sh
python tests/test_ivtff_ligature_views.py
python scripts/audit_ivtff_ligature_views.py
python scripts/audit_ivtff_page_locus_ids.py
python scripts/audit_repository_operations.py
```

La comparación v7 de dos parsers informa cero discrepancias **bajo su política declarada**; no certifica conformidad IVTFF completa. El presente guardia impide un tipo concreto de recuento espurio, no verifica significado, identidad botánica ni independencia de transcripciones. No se usan folios de test para ajustar reglas ni se ejecuta investigación confirmatoria bloqueada. EXP-170 permanece `BLOCKED` para reproducción histórica exacta; la conciliación de artefactos y los borradores científicos siguen pendientes.
