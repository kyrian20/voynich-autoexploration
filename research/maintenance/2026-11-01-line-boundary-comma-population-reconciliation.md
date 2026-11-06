# Conciliación acotada de población: política de comas en la réplica de límites de línea

**Fecha:** 2026-11-01. **Base científica:** PR #138, head inicial `2ed2ecf26b3c6db90fa9c09324b2f1361c9106d0`. **Clase:** auditoría descriptiva de población, sin entrenar ni evaluar modelos, sin EXP nuevo. **Estado de la reproducción exacta del artículo:** BLOCKED.

## Incidencia y pregunta falsable

La PR #138 documenta una población ZL3b histórica de **35.318** unidades frente a **29.906** en la reejecución corregida, y una población IT2a de **34.510** frente a **34.411**. ¿Cuántas unidades cambiarían *dentro del lector corregido actual*, manteniendo idénticas fuentes, filas P y políticas restantes, si únicamente la coma IVTFF pasara de espacio incierto en cuarentena a la sensibilidad `split`? La comparación no intenta reconstruir la implementación histórica.

## Censo determinista de las fuentes congeladas

| Fuente | Filas P | Filas con coma cruda | Filas cuya cuenta cambia | Vista cuarentena (aceptadas/barreras) | Vista split (aceptadas/barreras) | Incremento split |
|---|---:|---:|---:|---:|---:|---:|
| ZL3b | 4.130 | 1.700 | 1.697 | 29.906 / 4.186 | 34.509 / 2.046 | **4.603** |
| IT2a | 4.118 | 0 | 0 | 34.411 / 1.624 | 34.411 / 1.624 | **0** |

Las **ranuras** de la vista cuarentena suman 34.092 en ZL3b y 36.035 en IT2a; las de la vista split, 36.555 y 36.035. La suma de aceptadas y barreras es exacta en cada vista. Los conteos se derivaron primero mediante un lector independiente de las fuentes completas y se han incorporado como expectativas de regresión para el lector Python real; **su ejecución y artefactos en GitHub Actions deben comprobarse por separado**.

La diferencia publicada de ZL3b es 35.318 − 29.906 = **5.412**. El contraste *contrafactual* de la política de comas en el lector corregido es **4.603**, numéricamente un 85,05 % de esa brecha; quedan **809** unidades entre la cifra histórica y la sensibilidad split. En IT2a quedan **99**. **No se atribuye causalmente el 85,05 % a la ejecución histórica:** la cifra anterior procede de otro lector y no se ha ejecutado aquí. Solo se ha aislado el efecto de una decisión concreta dentro del lector corregido. La sensibilidad split no es la política recomendada ni una lectura segura del manuscrito.

Fuentes fijadas:
- ZL3b: `data/transcriptions/eva_zl3b.txt`, SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- IT2a: `data/transcriptions/eva_it2a.txt`, SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.

## Código, regresiones y archivo

El script `research/analysis/2026-10-28-line-boundary-reproduction/audit_comma_population.py` importa directamente `parse()` del lector corregido en PR #138, comprueba SHA-256 antes de analizar, alinea filas por página y número de línea, compara únicamente `uncertain_space_policy=quarantine` y `split` y emite JSON determinista. La prueba `tests/test_line_boundary_comma_population.py` cubre un ejemplo de coma, el censo congelado y el rechazo de una fuente modificada.

Comandos exactos, sin aleatoriedad ni semillas:

```sh
python -m unittest discover -s tests -p 'test_line_boundary_comma_population.py' -v
python -O -m unittest discover -s tests -p 'test_line_boundary_comma_population.py' -v
python research/analysis/2026-10-28-line-boundary-reproduction/audit_comma_population.py --check > line-boundary-comma-population.json
sha256sum line-boundary-comma-population.json
```

El workflow archiva JSON, logs de ambos modos y SHA-256. No se modifican fuentes, resultados originales, particiones, semillas, ni el `results.json` histórico de PR #138. No se usan las etiquetas ni los resultados de los folios prospectivos reservados; solo se censan tokens/filas de las transcripciones congeladas.

## Decisión y límites

**Resuelta de forma acotada la sensibilidad a la coma del lector actual:** 4.603 unidades ZL3b y cero IT2a. **No resuelta la reproducción histórica exacta:** las 809/99 unidades residuales requieren recuperar el lector y las reglas de inclusión exactos de la ejecución inicial; no sustituirlos por `split` ni denominarlo reproducción. La cobertura IVTFF integral, la validación del predictor y la traducción permanecen pendientes. Este censo no mide AUC, log-loss, significación ni significado. El 22-11-2026 sigue siendo fecha de evaluación, no promesa de descifrado.
