# EXP-616 — corrección de esquema del campo `removed` (28-10-2026)

**Alcance:** corrección de atribución del JSON histórico, no reproducción de EXP-616 ni experimento nuevo. El original se conserva congelado en `experiments/exp_616_folio_block_holdout_sensitivity/results.json`.

## Defecto demostrado

En los ocho registros `results.{ZL3b,IT2a}.leave_out[*]`, la propiedad `removed` contiene las **observaciones que permanecen** tras excluir el bloque, no las observaciones retiradas. Ejemplo ZL3b 103–106: total 280 celdas; `removed.cells=171`; `group_contributions.summary.cells=109`; 171+109=280. IT2a: 283=173+110. El texto del informe histórico ya describe correctamente las celdas restantes. La ambigüedad afecta a consumidores programáticos del JSON.\n\n**Segundo defecto revelado por la regresión inicial:** el campo histórico `folios` tampoco es el número de hojas físicas: registra 23 unidades para los cuatro bloques, que solo contienen 12 números de hoja (4+2+3+3). En 103–106 figuran 8 `folios` para 4 hojas numéricas, coherente con contar las dos caras. Sin las filas y el script originales no se certifica la unidad exacta; el JSON derivado distingue el recuento histórico de los números nominales de hoja y no los equipara.

## Reparación verificable

`scripts/audit_exp616_legacy_schema.py` lee el JSON congelado, verifica su Git blob SHA-1 `03b8316b10abd511d7bd55546ef7ac051ed97254`, y las identidades Git blob SHA-1 **y** SHA-256 de ZL3b e IT2a. Comprueba partición de bloques, suma de recuentos, coherencia de tasas ponderadas y `sh−ch`. Produce un JSON derivado con campos explícitos `remaining` y `excluded` (creación exclusiva, sin sobrescritura). La CI ejecuta ocho regresiones normales y optimizadas y publica el JSON como artefacto.

Comandos de comprobación:

```sh
python -m unittest discover -s tests -p 'test_exp616_legacy_schema.py' -v
python -O -m unittest discover -s tests -p 'test_exp616_legacy_schema.py' -v
python scripts/audit_exp616_legacy_schema.py --out exp616-schema-correction.json
```

## Limitaciones y autoauditoría

La primera CI de esta rama ([run 40750127958](https://github.com/kyrian20/voynich-autoexploration/actions/runs/40750127958)) falló porque el auditor equiparó indebidamente las 8 unidades `folios` del bloque 103–106 con sus 4 hojas numéricas. Se conserva el fallo y se corrigió el supuesto, añadiendo regresión explícita. La CI del nuevo commit debe comprobarse por separado.\n\nNo existe `script.py` dentro del directorio histórico EXP-616: se verifica **aritmética interna y procedencia**, no la reproducción de las tasas desde las líneas IVTFF. Los bloques 103–106, 107–108, 111–113 y 114–116 son heurísticos, no secciones codicológicas confirmadas. ZL3b e IT2a no son testigos independientes. No se calculan nuevos p-valores ni se interpreta significado lingüístico.

**Target-awareness:** ninguna selección o parámetro se calibra sobre un objetivo Voynich; se conserva la partición histórica. **Feature destruction:** no se altera texto, tokenización ni resultados. **Extrapolación:** únicamente se corrige el nombre semántico de un campo. **Resultado negativo:** no se modifica ninguna conclusión histórica. **Controles:** se exige que las contribuciones excluidas más las restantes reconstruyan exactamente los totales y tasas; las mutaciones sintéticas deben ser rechazadas. No hay inferencia sobre controles de lenguaje.

**Estado:** reparación propuesta hasta comprobar CI y artefacto; no implica limpieza global. **Siguiente paso:** recuperar script y parámetros exactos de EXP-616, si existen en la historia verificable, antes de intentar reproducir sus tasas. No usar los folios reservados para ajustar una regla. Evaluación global 22-11-2026.
