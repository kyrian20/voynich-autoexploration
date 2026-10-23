# Incremento sobre contexto de un carácter — 23-10-2026

Estado inicial: PROPOSED. Diseño exploratorio fijado antes de esta ejecución; el test heredado ya se usó y no constituye confirmación independiente.

Pregunta: ¿la última unidad BPE aporta predicción adicional sobre su último carácter, para exactamente el mismo objetivo (primera unidad BPE siguiente), pares y partición del bloque subword-boundary? No comparar pérdidas con objetivos diferentes.

Se conserva BPE de 64 fusiones aprendido solo de entrenamiento, base, fórmula centrada, GRID y partición del bloque anterior. Calibrar por separado en desarrollo el contexto BPE y su último carácter. Publicar diferencia pareada de pérdidas (carácter menos BPE), intervalo por remuestreo de grupos, 2.000 réplicas semilla 2026102303 y cobertura. Un intervalo que incluye cero no respalda incremento bajo esta configuración; tampoco prueba equivalencia o ausencia de lenguaje. Se procesarán las seis vistas sin elegir por resultado; IT2a split/join no son réplicas independientes.

Control adicional: 16 permutaciones de palabras interiores de cada línea de entrenamiento dentro de clases (primer carácter, último carácter, longitud), semillas 2026102340+i. Conserva inventario, extremos, longitudes y caracteres inicial/final en cada posición, por tanto todos los pares de caracteres entre posiciones. Recalibrar y evaluar cada predictor BPE en desarrollo/test originales, con representación y base congeladas. Publicar soporte de posiciones que permiten cambiar de palabra y cambios efectivos por semilla. Si el control tiene poco soporte, su semejanza al real no se interpretará como refutación. No se convierten rangos en p-valores ni razones de ganancias próximas a cero.

Puertas de implementación antes de corpus reales: controles sintéticos del predictor previo; proyección preserva exactamente todos los objetivos; positivo con contexto de varios caracteres pero último carácter constante debe dar incremento >0,5 bits/par; negativo balanceado incremento absoluto <1e-10. Verificar preservación de clases, inventario y extremos. Cualquier fallo detiene el análisis real y se conserva.

Procedencia: base de código de8cee5a445abf4d8eb4dac452e6983db0063786. Consultados estado, registro, limitaciones y búsqueda local BPE/subword; KB externa no disponible. No se afirma novedad mundial, semántica ni discriminación de teorías. No modificar conclusiones históricas ni committed_claims; sin nuevo ID EXP.
