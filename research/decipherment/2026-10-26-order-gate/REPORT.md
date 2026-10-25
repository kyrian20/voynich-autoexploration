# Un filtro de orden rechaza barajados pero admite reglas incorrectas

26-10-2026, Madrid. **Estado: NEGATIVE** respecto al requisito de rechazar una familia de cifrado ausente y respecto al uso como validador de lectura. Las salidas numéricas fueron reproducidas byte a byte; eso no cambia el resultado negativo. No se evaluó Voynich ni se obtuvo traducción.

## Resultado y decisión

La selección conjunta de 624 candidatos recupera el idioma y la clave correctos en los dos positivos, con 100 % de tokens reservados. El filtro de orden rechaza los32 barajados y la prueba de empate se abstiene. Sin embargo, acepta una clave incorrecta en ambos desafíos con periodo fuera de la búsqueda, y acepta ambos mensajes generados con pares de palabras. **No admite una validación de contenido ni de reglas exactas.** No se ajustan umbrales ni se amplía la búsqueda después del fallo para presentar esta versión como exitosa.

| Desafío | César | Dante | Lectura permitida |
|---|---:|---:|---|
| Positivo, periodo7 | 100 % tokens exactos | 100 % | Recuperación bajo esta familia conocida y dos idiomas candidatos |
| Barajados admitidos | 0/16 | 0/16 | Rechazo de esos órdenes, no de todas las alternativas |
| Periodo13 ausente: clave elegida | periodo12, offset11 | periodo12, offset11 | Regla incorrecta admitida |
| Palabras erróneas con esa regla | 19/4115 | 79/7925 | 99.54 % y99.00 % globales ocultan errores sistemáticos |
| Generador de pares admitido | sí | sí | El rasgo de orden local no certifica mensaje o semántica |
| Control de empate | NO_IDENTIFICABLE | conjunto de ambos modelos | Abstención solo ante ambigüedad prevista dentro del conjunto |

La etiqueta del selector ORDEN_DETECTADO describe su puerta operacional y no se renombra como «descifrado». Los32 negativos relacionados no permiten estimar una tasa universal de falsos positivos. La corrección de selección de idioma solo cubre latín e italiano con alfabeto/familia/reinicios conocidos; no identificación de idioma desconocido en general.

## Cuánto orden detecta y por qué el adversario lo supera

| Fuente | lambda elegida en dev | Umbral dev | S positivo | S periodo13 mal decodificado | S generado por pares |
|---|---:|---:|---:|---:|---:|
| César | 0.5 | 0.01 | 0.327780 | 0.326179 | 0.927361 |
| Dante | 0.75 | 0.01 | 0.574142 | 0.566825 | 1.257301 |

S es pérdida unigramática menos pérdida del modelo de pares centrado, en bits/transición. Los barajados dan S entre−0.099356 y−0.052387 en César y entre−0.365439 y−0.335833 en Dante. El generador supera a los originales en esta métrica: se investiga antes de interpretar nada y se explica por sus transiciones tomadas del mismo entrenamiento del evaluador y mayor cobertura de vocabulario (83.04 % frente a70.58 % en César;86.03 % frente a78.74 % en Dante). Esto es un adversario favorable al rasgo medido, no evidencia de superioridad lingüística o significado.

Contraste pareado del original frente a media de16 barajados: César0.412222 bits [0.373085,0.452027], Dante0.923113 [0.870563,0.974102]. Intervalos percentiles de2000 remuestreos de21 y37 bloques fuente de evaluación, con modelos fijados. Son incertidumbre exploratoria de ese contraste, no de la recuperación exacta, del proceso histórico ni de significado. No se usaron para escoger clave, mezcla o umbral. El origen son bloques de25 líneas de las vistas existentes, no manuscritos independientes.

## Diagnóstico exacto del fallo de familia

Periodos12 y13, con el mismo offset11 y fase reiniciada por línea, aplican el mismo desplazamiento a las posiciones0..11. Solo a partir de la decimotercera palabra pueden distinguirse. En las evaluaciones reservadas hay19 posiciones de este tipo en César y79 en Dante; coinciden exactamente con sus19 y79 errores. En desarrollo solo había26 y72 posiciones; la gran mayoría de la pérdida agregada no discrimina esos periodos. No es un defecto de cómputo: el conjunto candidato no contiene la regla verdadera y el umbral de orden global acepta una aproximación.

absent-family-diagnostic.json conserva posiciones, grupos y hashes de palabras erróneas sin distribuir texto íntegro. support.json verifica independientemente los recuentos por geometría del cifrado, sin consultar probabilidades o claro. Las cantidades son soporte de posiciones, **no una estimación de potencia estadística**.

Hay una no identificabilidad exacta en esta familia: si todas las líneas tienen como máximo M tokens, cualquier periodo p>=M da j mod p=j para cada posición observada j=0..M−1. Dos de esos periodos con el mismo offset producen el mismo ciphertext en todos los datos. Ningún criterio sobre esos datos puede distinguirlos; requeriría posiciones adicionales o información externa. En César M=18: periodos18/19 coinciden; en Dante M=26:26/27 coinciden. Esta afirmación está limitada a la regla artificial definida aquí; no se traslada al sistema de escritura Voynich.

## Fallo previo de implementación conservado

V1 eligió lambda1 en el sintético independiente, donde se exigía0. El suavizado condicional alteraba la distribución aun sin dependencia de pares. El fallo se detectó antes de ejecutar corpus reales. v1-failed/ conserva código, protocolo y log, con estado INVALID_FOR_CLAIM. V2 usa una corrección multiplicativa centrada respecto a la distribución global y normalización explícita; si condicional=global, la corrección es neutra. Se conserva el umbral sintético; no se relajó para admitir el código.

Siete pruebas V2 pasan: normalización sobre vocabulario/UNK visto y no visto, independencia nula, positivo sintético, ausencia de fuga de vocabulario, transformación reversible, inventario de barajados, empate y soporte exacto. Algunas pruebas cubren varias propiedades. Dos ejecuciones completas producen results.json y candidates.json.gz idénticos. Los39 desafíos conservan los624 candidatos cada uno (24336 costes), incluso los desfavorables. La repetición verifica reproducción, no añade muestras independientes. La suite global del repositorio no se volvió a ejecutar localmente.

## Reproducción y archivos

Desde la raíz del repositorio, Python3.12 y biblioteca estándar:

```sh
python -m unittest discover -s research/decipherment/2026-10-26-order-gate -p 'test_run.py' -v
python research/decipherment/2026-10-26-order-gate/run.py --inputs research/analysis/2026-10-22-residual-order/inputs.json --out-dir /tmp/order-gate-new
python research/decipherment/2026-10-26-order-gate/support.py --inputs research/analysis/2026-10-22-residual-order/inputs.json --output /tmp/order-support-new.json
```

Los destinos deben ser inexistentes. results.json.gz conserva la salida completa; SUMMARY.json permite inspeccionar decisiones sin descomprimir. candidates.json.gz conserva la rejilla completa; VERIFICATION.json fija hashes comprimidos/descomprimidos. No se redistribuyen los textos completos ni se ocultan candidatos. Las entradas preparadas y fuentes/avisos están en el bloque residual, cuya extracción no se regeneró aquí. El diagnóstico posterior de errores es descriptivo y se separa de los criterios previos.

Antecedentes: calibración de recuperación conocida, residual V2, BC-2026-10-22, soporte y sensibilidad de cantidades iguales. KB histórica no disponible; cotejo interno limitado, sin reclamar originalidad externa. Gemini no ha revisado este paquete ni se ha hecho nueva llamada. El prompt de revisión preparado es una solicitud pendiente y no evidencia de revisión independiente.

## Autoauditoría — skills/audit_experiment.md

**Conciencia del objetivo:** códigos y claves no ajustados a EVA. El filtro fue elegido después de detectar un fallo de unigramas; es desarrollo exploratorio del instrumento. El generador comparte pares train con el evaluador y es deliberadamente favorable a S; su aceptación es condicional a esa construcción. No representa todos los generadores.

**Destrucción de rasgos:** barajar destruye orden de palabras pero conserva su inventario e interior; su rechazo solo acredita sensibilidad a ese orden. La familia candidata excluye intencionalmente el periodo13 y fuerza una aproximación. No es un ensayo justo para negar recuperabilidad de ese código: el fallo concierne a la abstención de este buscador. El predictor no modela semántica ni dependencias largas.

**Extrapolación:** dos textos,312 claves por modelo de idioma, dos modelos,32 barajados, un generador por texto y un código ausente. No se declara tasa universal, dominio de todos los cifrados, ni desciframiento. La no identificabilidad de periodos>=M tiene una demostración exacta restringida a esta regla; no deriva de una rejilla finita ni del manuscrito.

**Alcance negativo:** la puerta no rechaza las dos reglas aproximadas ni los dos generadores ensayados. Esto invalida su uso como certificador de lectura exacta bajo estas condiciones, no la búsqueda de claves ni la existencia de contenido del manuscrito.

**Comportamiento de controles:** se esperaban dos recuperaciones exactas positivas,32 rechazos de barajados y abstención ante empate: observados. Se esperaba rechazar periodo13 ausente: falló en ambos textos; se investigó soporte y localización exacta de errores, sin adaptar reglas. Se esperaba que el generador pudiera pasar por compartir el rasgo: ambos pasan, con S superior al original; cobertura y dependencia de entrenamiento explican la ventaja y bloquean interpretación semántica. Se conserva la prueba sintética fallida deV1 y su reparación anterior a los corpus.

## Decisión de investigación

Cerrar esta puerta como filtro de orden local, **no admitido como validador de lectura**. Detener la cadena de ajustes sobre estos mismos tests: elevar umbrales para excluir los fallos o añadir periodo13 después de conocerlos sería otra variante exploratoria, no validación de esta.

La exigencia siguiente es una evidencia que distinga contenido y reglas en las posiciones donde difieren, con origen independiente y exposición declarada. Los recursos de anclas existentes siguen sin equivalencia semántica establecida. No se inventará esa equivalencia ni se aplicará el filtro a Voynich para producir una lectura favorable. El trabajo aporta un control negativo documentado del método; no una contribución lingüística original demostrada ni desciframiento.
