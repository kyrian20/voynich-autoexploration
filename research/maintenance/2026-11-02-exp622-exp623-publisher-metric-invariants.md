# EXP-622/623 — invariantes del publicador para contrastes y permutaciones

**Fecha:** 2026-11-02. **Base verificada:** `c99b70b4c668321ebe1c37305221573b5f7f4fc2` (`master`, posterior a PR #254).
**Estado:** reparación de integridad operativa propuesta; no es reproducción de simulaciones, nueva hipótesis ni traducción.

## Defecto y criterio de cierre

El guardia `scripts/check_publisher_source_drift.py` ya comprobaba que algunos campos fueran numéricos y que el p estuviera entre 0 y 1, pero podía eximir del rechazo de deriva un JSON nuevo de EXP-622 o EXP-623 con: más estratos emparejados que la mitad de observaciones, más folios que estratos, contrastes de tasas fuera de [-1,1], interacción distinta de la diferencia entre contrastes o p de Monte Carlo incompatible con sus excedencias y réplicas. Son contradicciones internas del esquema publicado, no evidencia de que los archivos históricos tengan estos defectos.

**Criterio falsable:** los ocho fixtures adversariales deterministas deben ser rechazados por `assert_no_source_drift` al leer el blob del commit candidato; los cuatro JSON publicados, incluidos los originales EXP-622 y EXP-623, deben seguir aceptándose.

## Cambios y regresiones

- `scripts/check_publisher_source_drift.py`: comprobar `2*matched_strata <= occurrences_with_two_neighbors`, `folios_in_matched_strata <= matched_strata`, límites de los dos contrastes, `interaction_next_minus_prev = next - prev` y `p = (permutation_exceedances+1)/(permutation_replicates+1)`, con tolerancia absoluta `1e-12` para operaciones en coma flotante.
- `tests/test_publisher_source_drift.py`: ocho regresiones negativas; control positivo existente con los cuatro JSON originales. No se tocan los scripts generadores ni sus resultados.

## Procedencia y conservación

EXP-622: `research/experiments/exp_622_ch_sh_specificity_interaction/results.json`, SHA Git blob `ae026d6569ddc2e064e42e1d1b831a41c94673d9`; ZL3b SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`; 5.162 observaciones, 472 estratos, 144 folios, 10.000 permutaciones, 8.234 excedencias, p=0,8234176582341766; semilla 6222026 en el script original.

EXP-623: `research/experiments/exp_623_it2a_ch_sh_specificity_replication/results.json`, SHA Git blob `2c10aa645115bf228b425ba840d546a1cf0958b8`; IT2a SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`; 5.374 observaciones, 485 estratos, 149 folios, 10.000 permutaciones, 6.900 excedencias, p=0,69003099690031; semilla 6232026 en el script original.

No se modifican corpus, JSON/MD históricos, semillas, particiones reservadas ni `state/committed_claims.md`. Las ocho mutaciones son deterministas, sin nuevas semillas ni simulaciones.

## Verificación exigida

```sh
python -m unittest discover -s tests -p 'test_publisher_source_drift.py' -v
python -O -m unittest discover -s tests -p 'test_publisher_source_drift.py' -v
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

La ejecución y el SHA de la PR, y después de `master` si se fusiona, deben comprobarse en GitHub Actions. Esta nota no certifica por sí misma una CI verde.

## Límites y siguiente paso

La comprobación de coherencia aritmética no reproduce 10.000 permutaciones, no acredita la validez del parser IVTFF ni prueba semántica. La réplica IT2a es otra transcripción del mismo manuscrito, no un testigo independiente. EXP-170 sigue bloqueado por falta de recibo histórico de sus entradas externas. Continuar la adjudicación de procedencia y la conciliación de artefactos sin ciclos científicos prohibidos.
