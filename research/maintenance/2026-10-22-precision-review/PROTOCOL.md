# Revisión de precisión del bloque 48a76dd

Antes de ejecutar: sustituir la aproximación Monte Carlo por distribución combinatoria exacta del MISMO nulo de daiin→dam, sin modificar corpus, selección P0, lectores ni familia de cuatro vistas. Conservar resultados históricos. Agrupar tokens como A=daiin, B=dam, O=resto; todas las secuencias de categorías con sus multiplicidades son equiprobables bajo permutación uniforme. Contar secuencias por número de adyacencias A→B con programación dinámica y convolucionar registros mediante fracciones racionales. Verificar normalización, esperanza analítica y casos pequeños por enumeración exhaustiva independiente. Reproducir las ocho localizaciones conocidas.

No existe nueva hipótesis semántica ni muestra independiente. La exactitud de la cola no corrige la elección retrospectiva de la pareja. Si los resultados difieren de Monte Carlo, documentar la diferencia sin seleccionar el más favorable.

Revisar también el manifiesto: IDs repetidos, campos inválidos y claves JSON duplicadas deben provocar rechazo. No modificar los 14 corpus ni el manifiesto para hacer pasar pruebas.
