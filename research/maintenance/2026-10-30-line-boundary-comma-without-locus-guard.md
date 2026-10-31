# Coma sin componente de locus IVTFF: barrera conservadora (30-10-2026)

**Estado al preparar el cambio:** propuesta técnica pendiente de CI, no EXP ni reproducción científica. Base exacta de PR #138: `4ea3d296ca808bf3b2585c3a94b9a8265e4b59da`; master observado: `342b4dd0eaf36e4b2ee94cc2628378b0ae47320b`. PR abiertas observadas: #5, #7, #13, #66, #82, #138. PR #169 fusionada en #138; no se repite su corrección de comas ausentes.

## Incidencia falsable

El lector `parse()` ya bloqueaba filas del mismo folio sin coma o sin cierre, pero seguía descartando silenciosamente una fila con coma y **sin componente de locus**, por ejemplo `<f1r,P0> orphan`. La expresión `ROW` la admite; `ident.split(".")` devuelve una sola parte y el antiguo `if len(parts)<2: continue` la hacía desaparecer. Entre `<f1r.P.1,P0> alpha.beta` y `<f1r.P.2,P0> gamma.delta`, esto podía fabricar un candidato positivo de adyacencia entre dos líneas físicamente separadas por una fila no interpretada.

**Criterio fijado antes de ejecutar:** toda fila con coma cuyo identificador anterior a la coma sea exactamente un nombre de página IVTFF admitida (`fNr`, `fNv`, panel 1–6 o `fRos`), pero carezca del componente `.locus`, debe registrar `UNPARSED_LOCUS` en la última P de esa página. Se conservan los negativos intralínea. Una fila defectuosa de otro folio no debe bloquear. No se inventan palabras, lectura ni ordinal.

## Implementación y verificación prevista

- `research/analysis/2026-10-28-line-boundary-reproduction/line_boundary_replication.py`: sustituye el descarte silencioso por una barrera de continuidad limitada a la misma página. No altera datos, modelos ni política de tokenización.
- `tests/test_line_boundary_interposed_loci.py`: tres variantes adversariales con coma sin locus, control de otra página y censo exacto de ambos corpus autenticados. Los tres casos adversariales **fallaban conceptualmente antes**: se producía un positivo; después deben dejar dos negativos y cero positivos.
- Comandos: `python -m unittest discover -s tests -p 'test_line_boundary_interposed_loci.py' -v` y la misma orden con `python -O`, mediante el workflow ya existente `Voynich Check`. Python 3.12; sin semilla ni aleatoriedad.
- SHA-256 de fuentes exigidos por el test: ZL3b `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`; IT2a `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.
- No se alteran `data/`, `experiments/`, `results.json`, semillas, hashes, estado de afirmaciones ni particiones reservadas. La prueba de censo determinará si existen filas de esta clase en las fuentes congeladas; no se anticipa su resultado.

## Autoauditoría y limitaciones

1. **Target-awareness:** ninguna regla está calibrada con palabras Voynich ni AUC; el objetivo es conservar discontinuidades físicas.
2. **Destrucción de rasgos:** la cuarentena puede descartar una adyacencia genuina cuando una fila es defectuosa; es una decisión conservadora, no una conclusión lingüística.
3. **Extrapolación:** solo esta forma de identificador malformado; no certifica conformidad completa IVTFF ni integridad de todos los registros.
4. **Negativos:** cero filas afectadas, si CI lo confirma, significaría solo ausencia de esta clase en las dos fuentes congeladas; no invalida otros defectos ni demuestra corrección de métricas.
5. **Control:** antes se espera un positivo falso entre P.1 y P.2; después, cero positivos y dos negativos. Con la fila malformada de otro folio, se espera un positivo en ambos lectores.

**Estado científico:** los resultados históricos del predictor PR #138 siguen `INVALID_FOR_CLAIM` para el código combinado corregido. La adjudicación IVTFF, procedencia EXP-170 y conciliación Biblioteca/GitHub siguen abiertas. No se ejecuta un nuevo ciclo científico prohibido ni se afirma traducción.

**Cierre pendiente:** consultar el SHA exacto del run de CI, logs de regresiones y artefactos, y registrar el resultado en la PR. No integrar sin comprobar la cabeza de la rama destino y trabajo concurrente.
