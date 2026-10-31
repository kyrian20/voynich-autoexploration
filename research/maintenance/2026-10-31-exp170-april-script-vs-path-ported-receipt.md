# EXP-170 — distinguir el script original de abril de la copia con rutas portables

**Fecha:** 2026-10-31. **Tipo:** corrección de procedencia del recibo de reconstrucción moderna, sin EXP nuevo ni simulaciones. **Base de trabajo:** `master` `2579f1233444dbe8c2e81cb30f0464af4bb60e51`. **Estado científico:** reproducción histórica exacta **BLOCKED**.

## Incidencia verificada en el historial Git

El primer commit que introdujo EXP-170, [`bfa786767d61a2c52bfb7a34a10d8b81ab777230`](https://github.com/kyrian20/voynich-autoexploration/commit/bfa786767d61a2c52bfb7a34a10d8b81ab777230), fechado 2026-04-10, añadió `experiments/exp_170_naibbe_simulation/script.py` con **Git blob SHA-1** `26553a194c67fa82dd02a4d3e39b8f4fb12898ce`. Ese script usaba cinco rutas absolutas bajo `~/voynich-cryptanalyst`. El mismo commit añadió `data/simulation_results.json` (Git blob `836a76195831b2bd6804ef8287056987d5138ee3`), pero **no** incluyó `naibbe_v2.py`, sus tablas ni el `divina_commedia.txt` que importaba desde `data/derived/naibbe-cipher`. Una inspección del árbol completo de ese commit (`truncated=false`) confirmó su ausencia en el repositorio, no en el entorno local histórico.

El commit de portabilidad [`83b0875841b3cbdb83c4ffa661e55abfb5b98fa4`](https://github.com/kyrian20/voynich-autoexploration/commit/83b0875841b3cbdb83c4ffa661e55abfb5b98fa4), de 2026-10-22, cambió el script. Una comparación de los **579/580 renglones** de ambos archivos mostró exactamente seis bloques de diferencia: la importación `Path as _RepositoryPath` y las cinco expresiones de ruta `REPO_DIR`, `VMS_CORPUS`, `ITALIAN_CORPUS`, `LATIN_CORPUS` y `OUT_DIR`. No se detectaron otros cambios textuales en esa comparación. El blob Git de la variante portable en la base era `6db4e51f7b508d07acbd054860c20bdcc5ecede0` y su SHA-256 congelado por el auditor es `8fe0f7d153211b320b34ca8543dac1ba029e629c4413c203fb2df0031063721c`. **Git SHA-1 y SHA-256 son algoritmos distintos**: no comparar sus cadenas como si fueran el mismo hash.

La reconstrucción aislada copia la **variante portable**, no el script original de abril. Su recibo anterior llamaba `historical_script` a esa ruta y podía inducir a confundir la identidad del código original con la identidad del código que se ejecutaría en una reconstrucción moderna. Esto es una imprecisión de procedencia comprobada; **no demuestra** que las métricas históricas sean falsas o que la portabilidad cambiara su cálculo.

## Corrección y prueba falsable

En `scripts/run_exp170_isolated_reconstruction.py` se conserva el campo anterior por compatibilidad y se añade `runtime_provenance.script_lineage`: variante `PATH_PORTED_2026_10_22`, ruta y SHA-256 de la copia portable, commit y blob Git originales, commit de portabilidad, descripción del diff y `april_original_used_for_execution=false`. El recibo se produce también en preflight y se conserva en `receipt.json` cuando se ejecuta una prueba sintética. No se permite concluir que los recursos externos originales se han recuperado.

En `tests/test_exp170_isolated_reconstruction.py`, el caso de preflight comprueba esos campos y compara el SHA-256 declarado con los **bytes reales** de la copia portable fijada en el checkout. La prueba de ejecución sintética existente comprueba la persistencia exacta de `runtime_provenance` en el recibo. Si el recibo omite la distinción o declara un hash portable incorrecto, la regresión falla. Las pruebas no ejecutan el cifrador real.

Comandos de regresión requeridos desde raíz, Python 3.12:

```sh
python -m unittest discover -s tests -p 'test_exp170_isolated_reconstruction.py' -v
python -O -m unittest discover -s tests -p 'test_exp170_isolated_reconstruction.py' -v
python scripts/audit_exp170_archive.py --check research/maintenance/2026-10-22-exp170-audit/results.json
```

**Criterio de cierre operativo:** verificar CI en el SHA exacto de la PR, revisar pasos y artefactos, integrar sin sobrescribir cambios ajenos y verificar CI del nuevo `master`. Hasta entonces, el parche es una propuesta y no se declara integración ni éxito remoto.

## Límites y conservación

El commit de abril acredita el **código y el JSON que quedaron versionados**, no el contenido exacto de la dependencia externa Naibbe, las tablas, el texto italiano ni los 400 recibos individuales. El repositorio conserva un texto italiano diferente en `data/reference_corpora/italian/dante_divina_commedia.txt`; su presencia **no demuestra** que fuera el input usado por EXP-170, cuya ruta histórica apunta al árbol Naibbe. No se lo sustituye. La fuente llamada `latin/vulgate.txt` sigue identificada en auditorías previas como texto inglés Douay-Rheims. La reproducción histórica exacta continúa **BLOCKED**.

No se modifican el script de EXP-170, JSON de 400 vectores, corpus, hashes congelados, semillas, folios reservados, resultados negativos ni `state/committed_claims.md`. No se genera evidencia lingüística ni traducción. Pendientes: recuperar un recibo histórico independiente de Naibbe/italiano, adjudicación IVTFF y conciliación global de artefactos. Fecha de evaluación científica: 2026-11-22, sin garantía de descifrado.
