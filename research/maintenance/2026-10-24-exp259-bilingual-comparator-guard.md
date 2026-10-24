# EXP-259: comparador histórico bilingüe mal presentado como latín (24-10-2026)

**Tipo:** reparación acotada de integridad de afirmaciones, sin EXP nuevo. **Base inspeccionada:** master 3e26ae513a2c30334c14419e1b0979645cc4c93b. **Estado inicial:** pendiente de CI y revisión de PR; no confundir esta propuesta con una integración.

## Defecto identificado

El informe congelado experiments/exp_259_char_positional_entropy/result.md presenta un comparador «Latin Cicero» y concluye que los caracteres Voynich son aproximadamente un bit más predecibles que los del latín. El lector histórico parse_latin de experiments/exp_259_char_positional_entropy/script.py usa una expresión regular para letras ASCII sin discriminar idioma y lee data/reference_corpora/latin/cicero_de_officiis_latin.txt. El registro research/CORPUS_IDENTITY_REVIEW.json adjudica ese mismo archivo como **Latin and English**, con incidencia BILINGUAL_REQUIRES_FILTER_AUDIT y evidencia textual de traducción inglesa.

Por tanto, la **comparación con un control latino monolingüe es INVALID_FOR_CLAIM**. La existencia de un comparador contaminado no demuestra que los números internos de A/B sean erróneos; tampoco permite sustituir la referencia y llamar al resultado una reproducción histórica.

## Reparación ejecutable y criterio falsable

scripts/audit_exp259_latin_claim.py verifica los blobs Git congelados del script y del informe, SHA-256 y longitud de la referencia contra el manifiesto, la adjudicación bilingüe y la evidencia; ejecuta solamente la función histórica parse_latin aislada mediante AST, exige los 112.081 tokens de referencia del informe y emite un recibo con el hash de la secuencia. Las pruebas de tests/test_exp259_latin_claim.py incluyen una lectura sintética de palabras latinas e inglesas, rechazo de cambio de adjudicación, registros duplicados, claves JSON duplicadas y una comprobación de corpus real.

**Predicción falsable:** cualquier cambio de bytes, procedencia, lectura histórica o recuento que rompa las invariantes debe hacer fallar el auditor. El control sintético solo demuestra que el lector admite ambas lenguas, no identifica el idioma de cada token.

**Comandos:** python -m unittest discover -s tests -p 'test_exp259_latin_claim.py' -v ; python scripts/audit_exp259_latin_claim.py --out exp259-scope.json.

## Conservación y límites

- No se modifica ningún corpus, transcripción, script histórico, resultado, registro EXP ni state/committed_claims.md.
- La ejecución es determinista; semilla no aplicable. Se conservan hashes de entrada, script, informe y secuencia de tokens en el recibo de CI.
- No se recalcula entropía, no se aísla latín del inglés, no se valida la asignación de folios A/B ni el formato IVTFF completo. No hay inferencia semántica ni traducción.
- La conclusión sobre morfología natural y la comparación entre alfabetos diferentes necesitan una adjudicación separada.
- **Cierre:** pruebas y CI de la PR en el SHA exacto; tras eventual fusión, CI nueva de master. Conservar logs y artefactos, incluidos fallos.
