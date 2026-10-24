# EXP-267: rechazo de filas posicionales malformadas (24-10-2026)

**Tipo:** reparación de auditoría histórica; no EXP nuevo. **Base:** `master` `d8f1ac8fd0955c9777cd99eb0a91ab888e3db4cb`. **Estado:** pendiente de CI remota y de revisión para integración.

## Defecto reproducido

`scripts/audit_reference_claim_links.py::parse_position_table` extraía solo las filas que coincidían con un patrón numérico. Si las seis filas A/B × LF/MID/LL eran correctas y se añadía otra fila `| B | LL | 12 | n/a | 5 |` o `| B | LL | ? | 999.0 | 5 |`, la fila malformada no entraba en `re.findall` y el auditor aceptaba el documento como si solo contuviera seis filas. El fallo se reprodujo con ambas entradas sintéticas mediante Python; el código anterior devolvió una tabla de seis claves en los dos casos. **No se ha observado ni se afirma que las tablas históricas originales contengan esos duplicados.**

## Reparación y controles

El parser ahora identifica **todas** las filas candidatas de posición, rechaza las que no tienen cinco columnas válidas, impide duplicados y recuentos de muestra cero, y exige exactamente seis combinaciones. Se añaden dos métodos de regresión (tres entradas adversariales), conservando las pruebas previas de duplicados idénticos y contradictorios.

Prueba sintética local de la nueva lógica: ambas filas malformadas rechazadas, duplicado numérico rechazado, muestra vacía rechazada, seis filas limpias aceptadas. Comandos requeridos para CI:

```sh
python tests/test_reference_claim_links.py
python scripts/audit_reference_claim_links.py --check research/maintenance/2026-10-22-claim-link-adjudication/results.json
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

La CI `.github/workflows/voynich-check.yml` ejecuta los controles específicos de referencia. La prueba local sintética no sustituye la CI ni demuestra reproducción de EXP-267.

## Preservación, procedencia y limitaciones

No se modifica `experiments/exp_267_word_length_position/result.md` (blob Git `92c47d101d35543dabce569f877cbf98176db246`), ninguna transcripción, corpus, script histórico, resultado numérico, ni `state/committed_claims.md`. La adjudicación sigue fijando el resultado original por blob y los lectores por SHA-256. El parche no cambia las métricas archivadas; protege contra aceptación silenciosa de una tabla contradictoria. Prueba determinista: sin semillas, muestreo ni parámetros aleatorios. No valida identidad monolingüe latina, conformidad IVTFF, resultados de EXP-170 ni traducción del Voynich.

Al preparar el parche se comprobaron las PR abiertas #5, #7 y #13 (borradores, sin superposición con el parser). No se fusiona automáticamente sin comprobar el head, los checks remotos y el `master` posterior.
