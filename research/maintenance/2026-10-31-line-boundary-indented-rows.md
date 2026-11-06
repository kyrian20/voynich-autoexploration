# Reparación acotada: filas estructurales IVTFF indentadas en la PR #138 (31-10-2026)

**Ámbito:** lector experimental de límites de línea en la PR #138 (borrador). Sin EXP nuevo ni puntuaciones científicas nuevas. La PR #138 mantiene `results.json` **INVALID_FOR_CLAIM** para el lector y clasificador corregidos.

## Defecto verificable

`parse()` aplicaba `raw.strip()` antes de identificar las filas `<f...>`. Una fila física malformada como ` <f1r.P.2,P0> beta` o `\t<f2r> page` podía ser aceptada como fila estructural en columna cero. Esto permitiría construir candidatos de frontera a partir de una etiqueta que otros lectores estrictos del repositorio rechazan. Es un defecto de contrato de lectura, no evidencia de corrupción del manuscrito.

## Reparación y falsación

Se rechaza una fila cuyo primer marcador `<f` esté precedido por espacios o tabuladores **antes** de normalizar o crear candidatos. La prueba `test_indented_page_and_locus_are_rejected` contiene dos casos adversariales con la línea física exacta en el mensaje de error. La prueba `test_frozen_sources_have_no_indented_folio_rows` exige hashes SHA-256 fijados y recuenta el alcance sobre ZL3b e IT2a, sin ajustar ningún clasificador.

Comandos de regresión (desde la raíz, en la rama de esta reparación):

```sh
python -m unittest discover -s tests -p 'test_line_boundary_interposed_loci.py' -v
python -O -m unittest discover -s tests -p 'test_line_boundary_interposed_loci.py' -v
```

La CI existente de la PR #138 ya ejecuta ambos comandos. **No afirmar éxito remoto hasta consultar el run del commit exacto.** La aceptación requiere ambos comandos en verde, las fuentes congeladas sin filas afectadas y que la PR de reparación se integre solo en la rama borrador de #138, no en `master` sin revisión científica.

## Preservación y límites

Fuentes autenticadas: `data/transcriptions/eva_zl3b.txt` (SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`) e `eva_it2a.txt` (SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`). La comprobación de impacto usa solo filas físicas y no consulta resultados reservados. No se cambian `results.json`, corpus, particiones, seeds, hashes congelados ni compromisos científicos.

**Autoauditoría:** sin parámetros ajustados a una métrica Voynich; no se altera la extracción de palabras válidas; la conclusión se limita a indentaciones ASCII; el control positivo son etiquetas sin indentación, ya cubiertas por la suite; los casos adversariales deben fallar cerrados. La corrección no resuelve diferencias con el artículo, adjudicación IVTFF global ni procedencia EXP-170. No rehabilita AUC/AP/ganancias históricas ni acredita traducción.
