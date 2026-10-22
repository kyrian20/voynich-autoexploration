# Auditoría limitada de EXP-170 — 22-10-2026

Base: último `master` verificado por el conector GitHub al empezar, `b31492596c3e9a0c3f322c0ece62fa13a84d739d`.
**Estado: cálculos del archivo reproducidos; simulaciones originales no reproducidas.** No se recuperan inputs externos ni se ejecuta Naibbe. Originales en `experiments/` intactos. Esta auditoría no asigna un EXP nuevo.

## Resultado principal

Los 400 vectores archivados (100 por condición, 18 métricas) son legibles y finitos. Se reproducen las 16 referencias VMS publicadas al redondear a tres decimales, las 2.447 líneas y los 2.307 supuestos inicios de párrafo. Las fórmulas métricas y el resumen estadístico se ejecutan aislados por AST: nunca se importa el módulo histórico, que cambiaría de directorio, importaría Naibbe y sobrescribiría su JSON. Un corpus sintético contado a mano prueba las 18 métricas, precedencias del clasificador y ausencia de transiciones entre líneas.

La distancia de `am_ll` e `y_lf` respecto al VMS histórico permanece en las cuatro condiciones, incluso comparando con máximos individuales y percentiles 2,5–97,5. Esto respalda únicamente el resultado negativo **de las salidas archivadas y su baseline histórico**. No valida el origen de esos vectores ni descarta cifrado, lenguaje natural o generación algorítmica como clases.

## Errores confirmados y correcciones separadas

1. **Intervalo mal denominado.** `summarize_distribution` toma índices cero-based `int(.05*n)` e `int(.95*n)`: con n=100 usa los elementos sexto y 96.º. Es una convención discreta para P5/P95, intervalo central nominal del **90 %**, no un IC del 95 % de la media. El estimador poblacional de desviación estándar usa divisor n y está calculado correctamente como descripción de estas salidas; no es la desviación muestral insesgada. Los percentiles interpolados y P2,5/P97,5 se guardan por separado, sin reemplazar el cálculo original. P5/P95 tampoco son extremos: ABOVE/BELOW no implica «stronger/weaker than any cipher output».
2. **Columnas intercambiadas.** Frente a las claves del JSON, Italian-B y Latin-A están intercambiadas en nueve filas: `daiin_cth`, `k_para_start`, `cth_lf`, `qok_ch`, las cuatro self-succession mostradas y `sh_lf`. Son **50 componentes numéricos incorrectos en 18 celdas**, a la precisión publicada. Dos etiquetas cambian: `cth_lf` Italian-B es INSIDE, Latin-A es ABOVE. En `qok_ch` las medias redondeadas coinciden, pero los intervalos están intercambiados. La prosa atribuye correctamente sh=1,414 a Latin-A, mientras su tabla lo coloca en Italian-B. [Tabla corregida íntegra](TABLE.md), generada por código, sin editar el informe original.
3. **Resumen contado incorrectamente.** Usando las 16 métricas y P5/P95 originales:

| Condición | INSIDE | ABOVE | BELOW | Publicado INSIDE/ABOVE/BELOW |
|---|---:|---:|---:|---|
| Italian-A | 4 | 10 | 2 | 3/10/3 |
| Italian-B | 4 | 9 | 3 | 4/8/4 |
| Latin-A | 4 | 10 | 2 | 4/9/3 |
| Latin-B | 5 | 9 | 2 | 4/9/3 |

Son 12/12/12/11 métricas fuera, no 13/12/12/12. Si se excluyen las dos INSIDE ya advertidas (`daiin_cth`, párrafo), quedan 2/2/2/3 INSIDE sobre **14** métricas, no «1–2 de 16». Un recuento agregado no es un contraste estadístico: las métricas están correlacionadas.

4. **Máximos confundidos con medias.** `am_ll` tiene medias 1,062/0,999/0,625/1,008, pero máximos individuales 1,531/1,293/0,919/1,283. C001 dice «maximum ... 1.1×»: ese valor puede resumir la mayor **media de condición**, no el máximo de las simulaciones. La síntesis `working_position.md` §2.1 dice máximo 0,57× para el conjunto Naibbe+Timm; los vectores EXP-170 lo contradicen. Se registra la discrepancia en `state/open_questions.md`; no se edita `committed_claims.md`, no se promueve un hallazgo ni se continúa un ciclo experimental. Ninguna salida archivada cruza los disparadores explícitos de C001: am≥3 o y≥2. El máximo y es 1,687. El resultado negativo y el error en la frase de máximo deben distinguirse.
5. **Probabilidad no estimada por el informe.** «Essentially 0» no es un p-valor calculado. Para am e y hay cero excedencias entre 100 salidas por condición. La estimación Monte Carlo con corrección +1 da **1/101=0,009901**, unilateral y solo si el conjunto simulado representa adecuadamente el nulo y el objetivo fuera intercambiable con él. Con cero de 100, la cota binomial unilateral del 95 % para la probabilidad de excedencia es aproximadamente 0,0295, suponiendo ensayos independientes. No es una cota de probabilidad de que la hipótesis de cifrado sea cierta. No se agrupan condiciones heterogéneas para fabricar n=400; no hay ajuste por las 64 comparaciones ni un contraste confirmatorio predeclarado. Los campos de cola son diagnósticos descriptivos, no significación validada.
6. **Prosa y alcance.** qok LF es BELOW en **4/4**, no en 3/4. `qok_ch` está ABOVE usando P5/P95 en 4/4, pero dentro del intervalo interpolado central del 95 % en Italian-A e Italian-B; además existen salidas individuales superiores al VMS. El título de «fallo en toda métrica estructural» y la exclusión general de la sustitución homofónica exceden estos resultados.

## Qué miden realmente las funciones

- LF/LL: tasa del rasgo en extremos de línea dividida por su tasa en todos los tokens. `am_ll` solo usa sufijo literal `am`; el helper no utilizado `ends_am` incluye `ain`, pero no interviene en esta métrica.
- Bigramas: tasa condicional entre sucesores disponibles **dentro de línea**, dividida por frecuencia global de la clase destino (incluidos tokens sin predecesor). No es el mismo baseline que la frecuencia entre destinos elegibles. Los controles pueden diferir de 1 por posición/segmentación y dependencia del cifrador; no se atribuye automáticamente a «memoria».
- `qok_ch` agrupa `ch`+`ch_e`; `ch_self_succ` solo `ch`, excluye `che/chi`. `qok/qot` se separan antes de `qo`. El `qo` self-succ de 2,047 publicado aparte se reproduce como baseline, pero no integra las 16 comparaciones; `sh_self_succ` también se archiva sin integrarlas.
- `edy_rate` busca subcadena `edy`, y `edy_ol_ratio` divide ese recuento por sufijos literales `ol`; no es un conteo morfológico de sufijos `edy` estrictos. Las tasas con denominador/clase ausentes se codifican 0; párrafo ausente se codifica None, y ausencia de `ol` daría infinito. El archivo real no contiene no-finitos; la auditoría los rechaza.

## Limitaciones y confusores conservados

La [adjudicación previa](../2026-10-22-c001-adjudication/REPORT.md) sigue vigente: «Latin» remite al archivo identificado como inglés Douay-Rheims. No puede atribuirse la diferencia a latín frente a italiano. La procedencia exacta histórica del cifrador y del italiano no se valida aquí. El JSON solo guarda métricas, no tokens cifrados, semillas por registro, denominadores ni recuentos; es imposible recomputar las métricas de esas simulaciones o verificar fallos omitidos. Las semillas son inferibles del script, pero no prueban identidad del entorno ni éxito de la ejecución histórica.

Se reproduce deliberadamente el parser legado: clase B inferida por `edy >= .05` y número de folio (fusiona caras/subpáginas), no por `$L`; tokens con anotaciones no se normalizan según la política actual. Por ello la coincidencia exacta de baseline **no certifica** Currier B ni conformidad IVTFF. La alta tasa de P0 confirma la limitación ya reconocida, no una medición válida de párrafos.

Protocol A preserva cada línea aceptada del input, aunque el informe lo llame sentencia; no divide por puntuación en ese wrapper. Protocol B recorta longitudes a 2–19 y fija un párrafo cada 10 líneas; no replica toda la distribución ni párrafos observados. La exposición del cifrador a las estadísticas Currier B hace que el ajuste léxico sea condicionado a esa calibración. No se puede recuperar aquí cuánto de esa calibración conocía los objetivos.

## Reproducción sin red ni paquetes externos

Desde la raíz del repositorio:

```sh
python tests/test_exp170_archive.py
python scripts/audit_exp170_archive.py --check research/maintenance/2026-10-22-exp170-audit/results.json
python scripts/audit_exp170_archive.py --format markdown
```

`results.json` fija SHA-256 del script, informe, JSON histórico y transcripción. Contiene las 18 métricas × 4 condiciones, media, desviación poblacional, n, rangos, percentiles de dos convenciones, diagnósticos de cola, errores de tabla y recuentos. El workflow de PR verifica snapshot y tests. No se necesitan los archivos externos ausentes ni se escriben salidas en `experiments/`.

## Autoauditoría según skills/audit_experiment.md

- **Target-awareness:** calibración histórica del léxico y longitudes a VMS; el fallo es condicional a esa calibración y selección. La auditoría no ajusta modelos ni elige umbrales.
- **Destrucción de rasgos:** resegmentar con B puede eliminar relaciones de posición del plaintext; A tampoco empareja líneas. No extrapolar a todos los cifrados. El parseo de párrafos no prueba F101.
- **Extrapolación:** solo cuatro conjuntos de 100 vectores, sin verificación de generación. El error máximo/media se señala sin inferir que C001 quede refutada en su núcleo.
- **Alcance negativo:** ningún lenguaje, significado ni clase general de mecanismos descartados.
- **Controles:** esperaba que tasas posicionales sin mecanismo de posición fueran aproximadamente 1 bajo intercambio; las medias am son 0,625–1,062 e y 0,724–1,117. am Latin-A difiere por factor >1,5 de 1 y se bloquea una interpretación de nulo puro: el origen/segmentación puede inducir estructura. sh Latin-A=1,414 supera VMS=0,859; l Italian≈0,07 también supera VMS≈0,058. Se documentan controles inesperados sin atribución causal ni conclusión general. No se generaron controles nuevos.

## Validación local de esta revisión

Siete tests específicos y la suite completa descubierta bajo `tests/` (53 tests, incluidos los siete nuevos) pasan. También pasan la comparación exacta del snapshot, auditoría de contratos operativos/workflows, identidad de 14 corpus, replay de los cuatro lectores restantes y `git diff --check`. La comprobación de identidad mantiene un corpus en cuarentena; no certifica su idioma ni licencia. CI remoto se comprueba después de abrir la PR; no se declara aprobado por anticipado.

[Próximas tres pruebas recomendadas y puertas de dependencia](NEXT_EXPERIMENTS.md). Ninguna se ha ejecutado.
