# LIB-EXP-624 — identidad de los dos tokenizadores globales en el auditor de archivo

Fecha: 2026-10-30. Estado: **corrección de contrato de auditoría; verificación CI pendiente**. No se ejecuta un modelo, no se reabre un experimento ni se afirma reproducción histórica.

## Incidencia concreta

`scripts/audit_library_exp624_archive_format.py::validate_summary` comprobaba que cada edición tuviera exactamente dos filas globales, pero no verificaba los identificadores de tokenizador. Una entrada sintética con dos filas etiquetadas `raw EVA letters` pasaba la comprobación de identidad de vistas siempre que las cifras fueran coherentes. Por tanto, el auditor podía presentar dos filas duplicadas como si cubrieran dos normalizaciones distintas. Es un defecto del **contrato de verificación**, no evidencia de que el archivo original contenga duplicados.

La reparación exige, en ZL3b e IT2a, exactamente una fila `raw EVA letters` y una `EVA units with ch/sh collapsed`, sin imponer orden. Son los nombres registrados en el recibo congelado `research/maintenance/2026-10-30-lib-exp624-percentage-evidence.json`, procedente de los ocho renglones de la copia archivada. Las cuatro filas de estratos Currier ya tenían una comprobación separada y no se modifican.

## Regresión y alcance

`tests/test_library_exp624_archive_format.py::test_overall_tokenizer_identities_cannot_be_duplicated_or_relabelled` comprueba por edición los duplicados, etiquetas desconocidas y ausentes, y acepta el orden invertido de ambas vistas. Comandos de reproducción desde raíz:

```sh
python -m unittest discover -s tests -p 'test_library_exp624_archive_format.py' -v
python -O -m unittest discover -s tests -p 'test_library_exp624_archive_format.py' -v
```

No se usa aleatoriedad ni semilla. El control es sintético y deliberadamente adversarial; se espera rechazo de las seis variantes inválidas y aceptación de las vistas legítimas en orden invertido. Los corpus, artefactos originales, resultados negativos, recibos congelados, folios reservados y `state/committed_claims.md` no se modifican.

## Autoauditoría de alcance

- **Conciencia del objetivo:** las dos etiquetas proceden del esquema histórico archivado, no de una métrica Voynich optimizada.
- **Destrucción de rasgos:** no se tokeniza ni se transforma texto.
- **Extrapolación:** se corrige únicamente la identidad de filas del resumen curado LIB-EXP-624; no se certifica su contenido numérico ni la procedencia del JSON nativo.
- **Resultado negativo:** un duplicado sintético se rechaza; no demuestra duplicados en la fuente real.
- **Control:** se espera que intercambiar el orden de dos filas válidas mantenga la aceptación; el nuevo test comprueba esa invariancia.

## Bloqueos que permanecen

El archivo privado original de Biblioteca no está incluido en GitHub; la CI solo comprueba pruebas sintéticas y recibos derivados con hashes publicados. La auditoría previa identificó fuga entre hojas físicas en las 28 particiones históricas; las métricas antiguas siguen inválidas para afirmar evaluación sobre hojas independientes. No se rehabilitan puntuaciones, no se ejecuta ningún ciclo confirmatorio y no existe traducción validada. Siguen pendientes la adjudicación IVTFF completa, EXP-170 exacto y la conciliación general de artefactos.

Para cerrar esta reparación operativa se debe verificar la CI de la PR y, si se integra, la CI del commit posterior de `master`. No confundir esta prueba de contrato con una reproducción del experimento histórico.
