# Guardia contra registros IVTFF duplicados — 24-10-2026

**Tipo:** reparación operativa acotada, sin experimento nuevo ni traducción. **Base:** `310a3e6cddbe5d7d6cd5b1a9b9fd2dc50c3e335f`. **Estado:** pendiente de CI remota y revisión.

## Defecto

`experiments/exp_602_independent_ivtff_parser_audit/script.py` construía mapas mediante `{r['id']: r for r in ...}`. Si aparecían dos registros con el mismo ID, el segundo sobrescribía silenciosamente el primero. Los dos parsers podían parecer concordar aun habiendo perdido filas. El auditor `scripts/audit_ivtff_page_locus_ids.py` contaba registros pero no advertía de tags completos repetidos.

## Evidencia de entrada (solo lectura)

Se inspeccionaron los tags crudos de las tres transcripciones originales en `master` antes del cambio: ZL3b: 5.385 tags distintos y 0 duplicados; ZL3a: 5.389 y 0; IT2a: 5.215 y 0. Los recuentos ZL3b/ZL3a concuerdan con `experiments/exp_602_independent_ivtff_parser_audit/results_v7.json`. SHA-256 histórico ZL3b: `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`; ZL3a: `56419297682d338ff1a0a17f5ae251e3ee3e2c5bf05a62db04c5385ef30b36a2`. No se han modificado esos corpus ni el resultado v7.

## Reparación

- El auditor estructural conserva todas las filas, cuenta tags exactos repetidos, registra primera y siguiente línea (máximo 50 ejemplos) y devuelve código de error si encuentra alguno.
- La comparación independiente de EXP-602 ahora rechaza IDs repetidos en cualquiera de los dos parsers antes de construir los mapas. Muestra hasta diez IDs y las líneas implicadas. No modifica reglas de tokenización.
- La regresión `tests/test_ivtff_page_locus_ids.py`, ejecutada por `Voynich Check`, prueba un duplicado sintético (rechazo), dos IDs distintos (aceptación) y los tres corpus reales (ausencia de tags exactos duplicados). Fixture determinista, sin aleatoriedad ni semilla.

## Comandos de verificación

```sh
python tests/test_ivtff_page_locus_ids.py
python scripts/audit_ivtff_page_locus_ids.py > /tmp/ivtff-locus-audit.json
python -m unittest discover -s tests -v
```

Estos comandos deben ejecutarse en CI antes de certificar el cambio. No se ha reproducido EXP-602 completo, ni validado la conformidad IVTFF, ni adjudicado ligaduras/alternativas. Los originales v1–v7 y los resultados negativos permanecen congelados. No asignar EXP nuevo. No fusionar sin CI y revisión del SHA final.
