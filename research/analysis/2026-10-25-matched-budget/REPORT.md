# Sensibilidad a cantidades iguales de texto

Diagnóstico exploratorio, 25-10-2026 (UTC de ejecución; 26-10 en Madrid al finalizar). No se asigna EXP ni se reclama novedad académica.

## Resultado acotado

Con 10653/3761/3590 transiciones de entrenamiento/desarrollo/evaluación por fuente, la ganancia de identidad del predictor V2 sigue siendo descriptivamente menor en Voynich que en los dos textos naturales en las cinco selecciones prefijadas. La cantidad de transiciones por sí sola no elimina esta diferencia en estas ejecuciones. Esto no identifica un mecanismo, lengua, cifrado ni significado.

| Fuente | Mínimo EL-W | Máximo EL-W |
|---|---:|---:|
| ZL3b split | 0.000875 | 0.003308 |
| ZL3b join | -0.000575 | 0.004283 |
| IT2a split | 0.001610 | 0.004893 |
| IT2a join (idéntico) | 0.001610 | 0.004893 |
| César latino | 0.020608 | 0.020608 |
| Dante italiano | 0.009387 | 0.014795 |

Unidades: bits/transición, diferencia de pérdida EL menos W, no pérdida absoluta entre lenguas. Rangos de sensibilidad entre selecciones solapadas, no intervalos de confianza. César determina los tres mínimos y conserva todo su material elegible; las cinco semillas solo reordenan sus registros y no son cinco muestras distintas. IT2a split/join son idénticos. Treinta ajustes no equivalen a treinta réplicas independientes.

## Ejecución y reproducción

Se conserva el modelo V2 de research/analysis/2026-10-22-residual-order, con cap 2000+UNK. Se verificó el hash esperado de inputs.json, cantidades exactas y ausencia de grupos compartidos entre train/dev/test en las treinta ejecuciones. El vocabulario se obtiene solo de entrenamiento y los pesos solo de desarrollo. No se han realizado bootstrap, p, pruebas de equivalencia ni simulaciones nuevas de recuperación de contenido. No se ha regenerado la extracción original.

Desde la raíz del repositorio, con Python 3.12:

```sh
python research/analysis/2026-10-25-matched-budget/run.py --model-dir research/analysis/2026-10-22-residual-order --output /tmp/matched-budget-full.json
```

El destino debe ser inexistente. results.json conserva todos los resultados, pesos, UNK, grupos y hashes de selección; omite únicamente las listas de índices `manifest` del JSON completo. Estas se regeneran con el comando y sus hashes se conservan. El código y entradas quedan identificados por SHA256 en la salida. Se verificó que la proyección archivada conserva las treinta métricas y los noventa hashes de selección del resultado completo.

Base consultada: 0d64c5db4114824647d987151d7296fa2ef0ab35. Su CI 40236927215 terminó success; no certifica este análisis añadido. La comprobación específica aquí es local, con invariantes durante la ejecución, no una suite global nueva.

## Antecedentes y uso de Gemini

Se cotejaron REPORT.md residual V2, PROTOCOL.md de dos predecesores, REPORT.md de soporte efectivo de identidad y state/hypothesis_backlog.md. La búsqueda de antecedentes es interna y limitada; no es revisión bibliográfica exhaustiva. Es una sensibilidad de un predictor existente, no un nuevo método de desciframiento.

La revisión externa archivada en research/external-reviews/2026-10-25-gemini-v2/REVIEW.md se usa como propuesta sometida a crítica. No se realizó una nueva llamada a Gemini en este diagnóstico ni se adoptó su contraste ch/sh, que se solapa con EXP-622/623. Se separa disponibilidad técnica de calidad de sus propuestas.

## Autoauditoría — skills/audit_experiment.md

**Conciencia del objetivo:** análisis elegido después de conocer V2; semillas, presupuestos y modelo quedaron fijados antes de la nueva ejecución. Presupuestos dependen de tamaños observados, no de optimización de ganancias. No es confirmatorio.

**Destrucción de características:** quitar líneas y truncar la última reduce información y puede degradar dependencias. No se cruzan líneas. Igualar transiciones no iguala vocabulario, género, diversidad ni unidades físicas; no es una prueba justa para excluir una lengua o mecanismo. Un muestreo distinto o mayor cantidad puede cambiar los resultados.

**Extrapolación:** seis vistas relacionadas, cinco órdenes de selección, un cap y la misma jerarquía. No se afirma potencia, universalidad, significación o independencia de todas las selecciones.

**Alcance negativo:** solo persiste una diferencia predictiva bajo estas condiciones. No se concluye que el manuscrito carezca de dependencia léxica, ni que un modelo alternativo vaya a descifrarlo.

**Controles:** se esperaba ganancia positiva, aproximadamente 0.0206 en César, que mantiene todo el material, y posible reducción de Dante respecto al 0.02035 histórico tras perder texto. César produce 0.020608 y Dante 0.009387–0.014795. La reducción de Dante confirma sensibilidad a selección/cantidad; no es una estimación de potencia. Los controles superan Voynich; se investigó la explicación por cantidad igualando transiciones, pero siguen sin controlarse género, distribución y representación. Por ello se bloquea toda lectura lingüística negativa de la diferencia.

## Decisión

Cerrar la comprobación limitada de cantidades iguales: no repetirla con más semillas para buscar separación favorable. Mantener abierta la selección del siguiente experimento de desciframiento. El siguiente diseño requiere una representación reutilizable y demostrar sensibilidad en problemas de verdad conocida; este diagnóstico todavía no satisface ese objetivo. No se modifican afirmaciones científicas comprometidas.
