# Diagnóstico exploratorio de distancia 2/3

Estado inicial PROPOSED; definido antes de ejecutar. No EXP nuevo ni prueba confirmatoria. Complementa el predictor de un token del 22-10; EXP-175 estudió MI de clases y EXP-266 enriquecimientos seleccionados, no predicción léxica residual fuera de entrenamiento. KB externa local ausente; revisión de antecedentes limitada a repositorio.

Pregunta: ¿mejora la identidad del token situado dos o tres posiciones antes frente a sus bordes/longitud? No pregunta si añade información condicionada al token inmediatamente anterior; tampoco prueba dependencias largas arbitrarias.

Reutilizar inputs.json, seis fuentes, vocabulario 2000+UNK, partición hash por folio, GRID/TAU/ALPHA de V2. Para distancia d descomponer cada línea en cadenas de residuos tokens[r::d]. Cada transición representa exactamente (i,i+d), sin cruzar líneas ni duplicar parejas. No barajar cadenas: los controles barajan la línea original antes de descomponerla. Mantener 16 semillas originales; calibrar en desarrollo. Todas las fuentes y distancias se publican, incluidas vistas duplicadas IT2a. Pesos/intervalos exploratorios; ningún p confirmatorio ni selección del mejor brazo.

Criterio diagnóstico: ganancia W-EL positiva e intervalo de grupos por encima de cero, controles naturales sensibles a esta distancia. Si no hay sensibilidad en controles, no interpretar ausencia de efecto Voynich. Controles que superen Voynich requieren revisar calibración y soporte antes de inferir estructura. No asignar significado.

Prueba de construcción: comparar parejas obtenidas por cadenas con zip(tokens,tokens[d:]) para longitudes 0..19 y distancias 1..5. Bootstrap de 2000 grupos, semillas heredadas. Fijar commit base y SHA256 de entradas y scripts. Reproducción numérica con el comparador científico original.

Corrección previa a obtener resultados: conservar también cadenas de un solo token, que aportan vocabulario pero cero transiciones. Excluirlas hacía cambiar el vocabulario bajo barajado; la guardia heredada lo detectó y abortó. No se interpretó ninguna cifra de ese intento.
