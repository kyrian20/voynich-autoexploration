# Rechazo de identidades duplicadas en la adjudicación de afirmaciones históricas

Fecha: 2026-10-24. Estado: **reparación propuesta en rama; pendiente de CI y revisión**.
Base inspeccionada: `master` `125f431a466121fb0d4e27787a7c0c0e2f51f5c1`.

## Defecto reproducible por inspección de código

`scripts/audit_reference_claim_links.py` convertía `readers['cases']` y
`identities['excluded_from_new_language_baselines']` en diccionarios mediante
comprensiones. Dos registros con el mismo `experiment_path` o `path` se
reducían a uno: el último sobrescribía al anterior sin error. Por ejemplo,
dos entradas `{'experiment_path':'a','selected_units':1}` y
`{'experiment_path':'a','selected_units':999}` producían una única clave
`a` con valor 999. Un duplicado podía quedar invisible si la última entrada
coincidía con el snapshot esperado. Esto afecta a la integridad de la
adjudicación de EXP-001/170/267/288, no demuestra que los snapshots
congelados tengan duplicados.

## Corrección y criterio de aceptación

La función `unique_index` rechaza estructuras que no sean listas, filas que
no sean objetos, claves ausentes/vacías/no textuales y duplicados idénticos o
contradictorios. Se utiliza **antes de leer corpus o scripts históricos**,
tanto para lectores como para el manifiesto de identidad. Cuatro regresiones
nuevas comprueban índices válidos, identificadores malformados, lectores
duplicados idénticos y adjudicaciones de idioma contradictorias; las dos
últimas recorren `audit(root)` con metadatos sintéticos en un directorio
temporal.

Reproducción solicitada en Python 3.12:

```sh
python tests/test_reference_claim_links.py
python scripts/audit_reference_claim_links.py --check research/maintenance/2026-10-22-claim-link-adjudication/results.json
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

El snapshot de 2026-10-22, sus resultados negativos y las fuentes originales
**no se modifican**. No se ejecuta experimento, no se asigna EXP, no hay
parámetros estocásticos ni semilla. Los corpus y sus SHA-256 permanecen en
`research/CORPUS_INPUT_MANIFEST.json` y
`research/CORPUS_IDENTITY_REVIEW.json`. Los hashes Git de los archivos
modificados quedan identificados por el commit de la PR; los resultados de
CI deberán citar el SHA exacto del head que ejecutaron.

## Alcance y concurrencia

Revisadas las PR abiertas #5, #6, #7, #13 y #24; ninguna modifica los dos
archivos reparados. La PR #24 trata la selección de nueve loci de EXP-590:
no se repite ese trabajo ni se ejecutan nuevas pruebas lingüísticas.
El control solo detecta duplicados y estructura inválida de los registros
de entrada; no adjudica idiomas por sí mismo, no prueba que una ejecución
histórica usara esos bytes y no certifica todas las afirmaciones de EXP.
Se mantienen como `INVALID_FOR_CLAIM` las comparaciones monolingües
afectadas por Cicero bilingüe y Douay-Rheims inglés. Tampoco se interpreta
ningún patrón estadístico como traducción.

## Cierre exigido

1. Confirmar que las cuatro regresiones y la comparación completa del
   snapshot pasan en la CI de esta rama.
2. Comprobar que el commit verificado corresponde al head de la PR.
3. Solo después, revisar integración y comprobar CI posterior de `master`.
4. Si falla una comprobación, conservar el fallo y corregir sin alterar
   entradas congeladas ni afirmar cierre.
