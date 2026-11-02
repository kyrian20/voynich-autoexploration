# EXP-170 — cierre de dominios numéricos imposibles en reconstrucciones

**Fecha:** 2026-11-02. **Tipo:** reparación del validador de archivos de 400 vectores; **sin nuevo EXP**, sin ejecución de Naibbe y sin cambio de hipótesis científica. **Reproducción histórica exacta:** BLOCKED.

## Defecto y criterio falsable

El validador `validate_archive()` de `scripts/audit_exp170_archive.py` rechazaba booleanos, nulos no permitidos, NaN, infinitos y esquemas incorrectos, pero aceptaba valores finitos **negativos** para métricas que el `compute_metrics()` histórico calcula exclusivamente como cocientes de recuentos no negativos. También aceptaba `edy_rate > 1` y `l_onset_rate > 1`, aunque ambas tasas son proporciones de palabras sobre el total. Un proceso hijo que terminara con código 0 podía así obtener el estado `MODERN_RECONSTRUCTION_UNVALIDATED` para un archivo matemáticamente imposible. Es un defecto del contrato de aceptación; no se ha demostrado que aparezca en los 400 vectores históricos.

**Criterio previo:** rechazar toda métrica negativa y ambas tasas fuera de [0, 1], incluso si el proceso hijo termina con código 0. Mantener válidos enriquecimientos y razones >1, límites 0 y 1, y el único nulo permitido (`k_para_start_enrichment`). No alterar el archivo histórico.

## Reparación y regresiones

- `scripts/audit_exp170_archive.py`: validación explícita de dominio después de validar tipo y finitud; los errores indican la clave.
- `tests/test_exp170_archive.py`: cinco valores adversariales, controles de enriquecimiento >1 y extremos válidos.
- `tests/test_exp170_isolated_reconstruction.py`: dos procesos hijos sintéticos con salida imposible y código 0; exige error de validación 65, recibo `FAILED`, bytes de salida en cuarentena, ausencia de resultado aceptado y SHA del archivo histórico intacto.

**No se ejecuta el simulador real.** La prueba sintética reutiliza una copia en memoria de los 400 vectores para preservar su estructura y altera exclusivamente una celda. Los hashes y semillas históricas no cambian.

## Comprobaciones y límites

Para verificar en la rama y tras integración:

```sh
python tests/test_exp170_archive.py
python -O tests/test_exp170_archive.py
python -m unittest discover -s tests -p 'test_exp170_isolated_reconstruction.py' -v
python -O -m unittest discover -s tests -p 'test_exp170_isolated_reconstruction.py' -v
python scripts/audit_exp170_archive.py --check research/maintenance/2026-10-22-exp170-audit/results.json
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

La CI de la PR y del `master` posterior deben comprobarse por SHA antes de declarar el cierre. Este cambio **no** demuestra procedencia de Naibbe/italiano en abril de 2026, no rehabilita las inferencias de C001, no resuelve las discrepancias IVTFF ni la conciliación global de artefactos. No se modifican `state/committed_claims.md`, corpus, resultados congelados ni particiones reservadas. Próximo paso: buscar un recibo histórico independiente que vincule bytes y parámetros de EXP-170; sin ello no existe reproducción histórica exacta.
