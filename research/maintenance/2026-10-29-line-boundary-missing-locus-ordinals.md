# Incidencia acotada: salto de ordinal IVTFF entre dos loci P

**Fecha:** 2026-10-29. **Estado:** propuesta de corrección de código; CI e integración pendientes de comprobar. **Sin EXP nuevo.**

**Base fijada:** PR #138, rama `codex/line-boundary-leaf-replication-20261028`, commit `01921a61a7939f4562260b9097e553176a8bf3d9`. El `master` comprobado antes de abrir esta corrección era `1bce529f2dd4f572f05489443c7a4579e9c0894f`. Las PR #5, #7, #13, #66, #82 y #138 estaban abiertas; no se ha intervenido en ellas.

## Defecto y contrafactual

El lector retenía el orden físico de filas P, pero no el **número de locus** de cada registro. Si una transcripción omitía un locus entero, el constructor podía contar la transición entre dos P observados como límite positivo, aun cuando sus identificadores saltaran, por ejemplo, de `<f11v.4,+P0>` a `<f11v.6,=P0>` en IT2a. No es lícito asumir que no existe la línea 5 por el hecho de que no esté transcrita.

La reparación conserva el ordinal fuente en cada fila y solo construye el candidato positivo entre dos P consecutivos cuando el número siguiente es exactamente el anterior más uno. Los loci no-P interpuestos, los marcadores de párrafo y las barreras de incertidumbre conservan sus comprobaciones independientes. No se cambian los pares intralínea, los textos brutos ni las particiones.

## Preinscripción del diagnóstico

- **Hipótesis falsable:** en las fuentes congeladas, la nueva condición suprime candidatos positivos que antes atravesaban saltos de ordinal no cubiertos por las barreras ya existentes.
- **Control negativo:** cuando los ordinales son consecutivos y no hay otras barreras, el candidato positivo debe permanecer; los negativos intralínea no deben cambiar.
- **Contrafactual histórico limitado:** retirar únicamente el campo `locus_number` de la estructura de filas, conservando las reparaciones anteriores (loci no-P y párrafos), y comparar las listas de candidatos. **No** es una reproducción del `results.json` antiguo.
- **Criterio previo:** regresiones sintéticas en ambas políticas, SHA-256 de las fuentes fijadas, y diferencias de candidatos iguales a las observadas en la auditoría previa de lectura de los registros fuente. No ajustar las expectativas tras observar CI sin documentar la discrepancia.
- **Población:** todos los loci P admitidos por el lector en ZL3b e IT2a, no un nuevo conjunto de entrenamiento/prueba. Semilla: no aplicable (censo determinista).
- **Fuentes inmutables:** ZL3b SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`; IT2a SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.
- **Censo previo, aún pendiente de prueba Python/CI:** 76 transiciones P con salto de ordinal en cada transcripción. En ZL3b todas tienen loci no-P interpuestos; en IT2a tres no presentan locus no-P interpuesto (f11v.4→6, f102r2.6→8 y f106r.28→30). La transición f102r2.6→8 ya queda bloqueada por los marcadores explícitos de párrafo; se esperan **0** candidatos positivos adicionales retirados en ZL3b y **2** en IT2a por política. Estas expectativas se deben verificar con la regresión Python y los logs de CI antes de presentarlas como resultados cerrados.

## Verificación exigida

```sh
python -m unittest discover -s tests -p 'test_line_boundary_locus_ordinal_gaps.py' -v
python -O -m unittest discover -s tests -p 'test_line_boundary_locus_ordinal_gaps.py' -v
python -m unittest discover -s tests -p 'test_line_boundary_interposed_loci.py' -v
python -m unittest discover -s tests -p 'test_line_boundary_paragraph_markers.py' -v
```

El workflow `.github/workflows/voynich-check.yml` ejecuta las dos primeras órdenes, junto a las regresiones existentes. La ejecución posterior a una eventual fusión requiere verificación separada. No se declara CI verde ni integración sin consultar la ejecución y el SHA concretos.

## Integridad y autoauditoría

No se modifica `results.json`, ni las fuentes, los manifiestos reservados, las semillas ni los informes históricos. El resultado es una **corrección de selección de candidatos**, no un cambio de AUC demostrado ni un descifrado. Las métricas históricas continúan `INVALID_FOR_CLAIM` para la política de lector reparada por múltiples defectos previos.

- **Target-awareness:** la condición se basa en la secuencia de identificadores IVTFF, no en AUC, una palabra objetivo ni un resultado Voynich.
- **Feature-destroying:** retirar candidatos de continuidad no demostrada reduce cobertura; no prueba ausencia de dependencia y no autoriza comparar puntuaciones sin reestimar el modelo.
- **Extrapolación:** el alcance es exclusivamente el constructor de candidatos y las dos fuentes comprobadas; no se certifica conformidad IVTFF ni disposición visual.
- **Resultado negativo:** un delta cero en una fuente significa ausencia de impacto adicional bajo los filtros presentes, no ausencia de errores.
- **Control:** una pareja de ordinales consecutivos debe conservar su candidato; una pareja con ordinal omitido debe perderlo. Los controles sintéticos se ejecutan antes de interpretar el censo.

**Siguiente paso:** comprobar CI y logs de esta rama; si todo pasa, integrar solo en la rama de PR #138 tras verificar que su cabeza no se ha movido, comprobar CI posterior y archivar los identificadores. No abrir las hojas reservadas ni repetir el predictor mientras persistan contradicciones IVTFF.
