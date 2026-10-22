# Prioridad científica: qué sabemos y cuál es la siguiente prueba decisiva

Fecha: 2026-10-22  
Estado: síntesis de resultados existentes; no es un experimento nuevo ni un desciframiento.

## Decisión ejecutiva

**No lanzar otra tanda de análisis de `daiin` sin una hipótesis nueva.** La prueba predictiva ya existente en `experiments/exp_602_heldout_predictive_test/` no cumplió su criterio positivo: el modelo global entrenado solo con el conjunto de entrenamiento predijo peor que el baseline condicional a la bolsa de tokens de cada línea reservada. Antes de diseñar otra prueba hay que resolver la colisión del ID EXP-602 con `exp_602_independent_ivtff_parser_audit` y dejar claro qué artefacto corresponde a cada análisis.

## Evidencia existente que debe guiar las decisiones

### 1. Predicción fuera de muestra: criterio positivo no satisfecho

El artefacto `exp_602_heldout_predictive_test/result.md` informa de un corte determinista por folio: 1.797 líneas de entrenamiento / 60 folios y 528 líneas reservadas / 21 folios. Ningún folio se reparte entre ambos conjuntos.

Para el objetivo primario literal `daiin`:
- Probabilidad inicial estimada solo en entrenamiento: 0,03450.
- Log-loss del modelo global en el conjunto reservado: 0,19917.
- Log-loss del baseline de inventario de tokens por línea: 0,11786.
- Ganancia definida como baseline menos modelo: −0,08131; IC bootstrap por folio del 95 %: [−0,11174; −0,05641].
- El Brier score también favorece al baseline.
- Los controles declarados `dain` y `saiin` muestran la misma dirección.

Interpretación: **la regla predeclarada para demostrar mejora predictiva no se cumplió**. Esto no demuestra que no haya regularidades posicionales; indica que este modelo simple no supera ese baseline exigente. No se debe reescribir la regla después de ver el conjunto reservado ni presentarlo como desciframiento.

### 2. Sensibilidad del procesamiento y cobertura

La auditoría de ligaduras y cobertura detectó que el lector legado de EXP-590 solo admite IDs de línea del tipo `f1r.1`, mientras que el lector amplio incluye identificadores como `f67r1.5` y `fRos.23`. Por eso los 4.188 registros/líneas de la línea base heredada y los 5.385 registros de cobertura amplia no deben compararse como si describieran el mismo universo.

La auditoría de las vistas entre llaves cambió el recuento exacto de `daiin` de 853 a 852 en la vista expandida de ZL3b, sin cambiar el número de líneas que comienzan por esa forma (161). Es una sensibilidad descriptiva; no valida una interpretación lingüística.

Fuentes:
- `research/ivtff_ligature_view_sensitivity_inventory_2026-10-22.md`
- `research/ivtff_brace_span_inventory_2026-10-22.md`
- `research/ivtff_tokenization_policy_2026-10-20.md`

## Siguiente prueba propuesta — diseño previo, aún no ejecutado

No asignar todavía un nuevo número EXP: primero reconciliar el registro histórico y las dos carpetas que comparten EXP-602. Después, registrar el protocolo antes de mirar resultados.

1. **Congelar la población y el parser.** Definir explícitamente la gramática IVTFF de identificadores de folio/línea, filtros de tags y anotaciones, política para spans entre llaves y tratamiento de líneas vacías. Guardar hashes de fuentes y una prueba de cobertura con recuentos esperados.
2. **Mantener el corte por folio congelado.** No usar el conjunto reservado para escoger rasgos, vocabulario, hiperparámetros ni umbrales. ZL3a y ZL3b son transcripciones relacionadas del mismo manuscrito, no réplicas independientes.
3. **Comparar modelos con información disponible en inferencia.** Evaluar un predictor contextual entrenado exclusivamente en folios de entrenamiento (por ejemplo, contexto de tokens previos y posición de línea) contra un baseline también entrenado solo con entrenamiento. No usar el inventario real de tokens de la línea de prueba como si estuviera disponible antes de predecir; conservar el baseline condicional antiguo solo como control diagnóstico separado.
4. **Predeclarar una métrica primaria y una regla de éxito.** Usar diferencia de log-loss por línea y un intervalo de incertidumbre agrupado por folio. Declarar éxito solo si la mejora frente al baseline entrenable es positiva y el intervalo del 95 % queda completamente por encima de cero. Informar Brier score y controles como secundarios.
5. **Añadir controles negativos.** Repetir el protocolo con palabras de frecuencia comparable elegidas antes de evaluar, y comprobar estabilidad entre Currier A/B sin tratar transcripciones alternativas como muestras independientes.
6. **Publicar el resultado aunque sea negativo.** Si no supera el criterio, conservar el resultado como evidencia contra ese modelo concreto y no reciclar el mismo conjunto reservado para seguir ajustándolo.

## Puertas de control antes de continuar

- [ ] Resolver la colisión de nombres EXP-602 sin renombrar ni borrar artefactos a ciegas.
- [ ] Verificar que el código de la prueba predictiva usa la misma población IVTFF que declara el protocolo.
- [ ] Separar claramente un modelo que predice de un test estadístico de asociación posicional.
- [ ] Ejecutar el protocolo predeclarado y comprobar la ejecución y los artefactos en CI.
- [ ] No usar expresiones como “descifrado”, “traducción” o “significado demostrado” sin evidencia semántica independiente.

## Conclusión

El avance real hasta ahora es metodológico: se detectaron diferencias de cobertura y una prueba predictiva que no superó el criterio preestablecido. El siguiente avance científico solo existirá si una hipótesis nueva produce predicciones fuera de muestra que superen un baseline justo y reproducible. Hasta entonces, el resultado debe describirse como **no demostrado**.
