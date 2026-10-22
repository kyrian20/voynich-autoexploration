# Adjudicación reproducibilidad y alcance de EXP-177 / EXP-177-verify — 22-10-2026

**Estado:** diagnóstico estático **INVALID_FOR_CLAIM** solo para reproducibilidad exacta sin entorno congelado y para extrapolaciones universales de C002; no es una refutación numérica de EXP-177 ni un EXP nuevo. Fuente canónica inspeccionada: `75f126df8a358f9d048ec8c1065b8ede82b99c5e`. Se conservan intactos los scripts y JSON históricos. Esta revisión sigue la adjudicación de lectores y afirmaciones de EXP-267/288; no repite ninguno de ellos.

## Entradas y hallazgos verificables

El auditor [scripts/audit_exp177_rng_provenance.py](../../../scripts/audit_exp177_rng_provenance.py) inspecciona mediante AST **sin importar ni ejecutar** los dos scripts y calcula SHA-256 de esos scripts y sus dos JSON archivados. El [snapshot](results.json) contiene los cuatro hashes, el commit de partida y las detecciones. La fuente del corpus del experimento es `data/reference_corpora/latin/cicero_de_officiis_latin.txt`, previamente adjudicada como **edición bilingüe latín+inglés**: su filtro de párrafos deja pasar encabezados, bibliografía e índice; los 34.977 tokens reportados no constituyen un cuerpo latino adjudicado. Véase [auditoría previa de lectores](../2026-10-22-loader-audit/REPORT.md). **No se ha reabierto ni sustituido el corpus en este bloque.**

1. **Semilla no congelada (EXP-177):** `random.Random(sim_i * 1000 + hash(cal) % 1000)` usa `hash()` de una cadena; por defecto Python aleatoriza su valor entre procesos. El JSON histórico no conserva `PYTHONHASHSEED` ni las semillas efectivas. En una demostración local, `PYTHONHASHSEED=1` dio offsets `[341, 852, 635]` para `strong/moderate/weak`, frente a `[711, 445, 287]` con `PYTHONHASHSEED=2`. Estos números son una demostración del entorno de auditoría, **no** resultados del experimento histórico ni valores portables entre versiones de Python. El script de verificación usa otra semilla fija (`999999 + sim_i`), por lo que no reproduce los mismos sorteos de EXP-177.
2. **Estado aleatorio compartido (ambos scripts):** `make_word()` elige el núcleo mediante `random.choice(cores)` global, no mediante el objeto local `rng` que controla onset/sufijo y barajado. `random.seed(42)` global existe, pero los sorteos de distintas simulaciones comparten ese estado y el resultado de una simulación depende de cuántas llamadas globales realizaron las anteriores. No equivale a un RNG independiente por réplica. No se ha medido aquí cuánto cambian las métricas.
3. **Destrucción de dependencia secuencial (ambos scripts):** `rng.shuffle(all_words)` reordena las palabras del supuesto texto de origen **antes** del cifrado; el mapeo de MID además genera palabras EVA aleatorias independientes de la identidad léxica de origen. Por tanto, el `ss_mean≈1` observado solo caracteriza **este** generador barajado y su codificación. No justifica que *todo* cifrado de sustitución sin copia carezca de dependencia entre palabras. C002 permanece en `state/committed_claims.md` sin editar; requiere decisión humana si se reutiliza públicamente su formulación general.

La afirmación específica de EXP-177 de que su implementación target-aware reproduce parcialmente el enriquecimiento posicional no queda refutada por este diagnóstico, pero su comparación con un «latín» monolingüe y la reproducibilidad bit a bit quedan sin certificar. La etiqueta `95% CI` de percentiles empíricos debe tratarse como intervalo de simulaciones, no automáticamente como intervalo de confianza para una media.

## Pruebas, parámetros y límites

Comandos desde el repositorio:

```sh
python tests/test_exp177_rng_provenance.py
python scripts/audit_exp177_rng_provenance.py --check research/maintenance/2026-10-22-exp177-rng-adjudication/results.json
```

Cuatro pruebas unitarias puras comprueban detección de los tres patrones, ausencia de falsos positivos en un fixture limpio, exclusión de patrones irrelevantes y fallo ante funciones faltantes. **Ejecutadas localmente: 4/4 correctas.** La detección de los patrones en los archivos reales y sus hashes se cotejó mediante lectura directa del repositorio; **no se ha ejecutado el auditor integral en un checkout completo local**, porque el acceso a la copia completa no estaba disponible. La CI actual comprueba sintaxis Python, pero no invoca aún este auditor; no se edita el workflow por solapamiento con PR #2. La confirmación del CI del commit nuevo debe registrarse después de publicarlo.

Fuente primaria técnica: [documentación de `PYTHONHASHSEED`](https://docs.python.org/3.12/using/cmdline.html#envvar-PYTHONHASHSEED) y [módulo `random`](https://docs.python.org/3.12/library/random.html). No se ejecutaron simulaciones, ni se recalcularon medias, intervalos, tasas o métricas del Voynich. No se infiere que el manuscrito carezca de significado.

## Autoauditoría según `skills/audit_experiment.md`

- **Target-awareness:** el diseño histórico de EXP-177 usa correspondencias EVA ajustadas a métricas objetivo; el diagnóstico no recalibra nada y no acepta sus métricas como prueba independiente de teoría.
- **Feature-destroying:** el barajado previo destruye las dependencias léxicas del orden original; el generador MID tampoco las conserva. La inferencia sobre la clase general de sustitución es injusta; una codificación que preserve la dependencia del texto de origen **no está probada** por este diagnóstico.
- **Extrapolación:** solo dos scripts, dos JSON y la semántica documentada de Python. No se deduce magnitud de sesgo ni invalidación global.
- **Alcance negativo:** no se declara imposible el cifrado, la lengua ni el descifrado. La evidencia específica de `ss_mean≈1` sigue siendo histórica, condicionada a esta implementación.
- **Controles:** se espera que un fixture con `hash(cal)`, `random.choice` global y `rng.shuffle(all_words)` active los tres detectores; ocurre. Se espera que un fixture con RNG local y sin barajado no los active; ocurre. No hay control de métricas del manuscrito en este diagnóstico.

## Próxima acción concreta

Primero ejecutar `--check` en CI cuando la PR #2 libere el workflow. Después, sin sobrescribir originales, registrar una versión nueva del mecanismo con semillas enteras explícitas, un solo RNG por réplica, corpus monolingüe adjudicado y **dos brazos predefinidos**: orden de origen conservado frente a barajado. Congelar hashes de corpus, política IVTFF y división por folios; comparar dependencia secuencial fuera de muestra y controles positivos/negativos. Solo asignar EXP tras consultar registro y duplicados. Si el brazo con orden conservado no mejora frente al barajado, el mecanismo ensayado no apoya dependencia adicional; si mejora, no constituye traducción.
