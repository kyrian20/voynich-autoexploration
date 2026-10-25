# Calibración mínima de recuperación de contenido

26-10-2026, Madrid. Estado inicial PROPOSED. Calibración exploratoria de instrumentos; sin EXP numérico, sin análisis nuevo del manuscrito ni pretensión de novedad criptográfica.

## Pregunta y puertas fijadas antes de ejecutar

¿Un procedimiento acotado recupera la clave y el contenido reservado de dos cifrados artificiales conocidos, y cómo responde el predictor residual V2 a los mismos contenidos codificados?

Controles positivos: César latino #218 y Dante italiano #1012, vistas analíticas ya archivadas en research/analysis/2026-10-22-residual-order/inputs.json, SHA256 c069548868854c29d294efbc3da891a0f5cf7c62878786be78fa13ce5ba5225d. No regenerar extracción. Mantener agrupación hash V2: train>=2, dev=1, test=0; no cambiar límites de línea ni cantidades. Aprender frecuencias de caracteres de texto claro SOLO en train. Se proporciona la familia de cifrado y el idioma de referencia: ventajas que no tenemos para Voynich.

Cifrados propios: (a) rotación monoalfabética ASCII de 13, periodo 1; (b) rotación de todas las letras ASCII de cada token por (11 + índice_del_token mod 7) mod 26, reiniciada en cada línea. Las letras ajenas a a-z permanecen intactas, incluidos acentos. Son ejemplos didácticos, no reconstrucciones de sistemas históricos ni hipótesis sobre Voynich. Claves fijadas sin consultar métricas del manuscrito. El codificador preserva longitud de token, cantidad de tokens, límites de línea y grupos; debe ser exactamente reversible.

Recuperación: enumerar periodos 1..12 y offsets 0..25, 312 candidatos por brazo. Elegir solo en dev la menor pérdida de caracteres ASCII decodificados bajo unigramas entrenados en texto claro train, alpha=.5 sobre 26 letras. Desempate por periodo y offset. Publicar mejor clave, cinco primeras pérdidas, margen y exactitud test de tokens/caracteres frente al claro reservado, después de fijar la clave. Puerta positiva de este ejercicio: clave generadora exacta y 100% tokens test exactos en ambos textos y ambos cifrados; si falla cualquier brazo, conservar fallo y no reajustar reglas en esta versión.

Control de implementación: codificar/decodificar todos los caracteres y tokens, incluyendo Unicode; ausencia de fuga entre grupos; decoder recibe ciphertext dev y probabilidades train, no clave verdadera ni claro dev/test. La evaluación con claro test solo puntúa la clave ya elegida. La clave no es secreta para el investigador; no se presenta cegamiento independiente.

Control adversarial: barajar tokens dentro de cada línea de dev/test, semilla 2026102601, antes de cifrar con periodo7/offset11; usar el mismo decoder. Esperamos recuperación del mensaje barajado pero ninguna capacidad del criterio de unigramas de certificar su orden lingüístico: la pérdida del claro correcto y barajado debe ser idéntica (tolerancia 1e-12). Si el procedimiento también recupera el texto barajado, eso certifica inversión del código, no semántica. No llamar a este control ausencia de toda semántica; conserva palabras y estructura local interna.

Diagnóstico V2 secundario: seis ajustes (dos textos x claro/mono/periódico), vocabulario completo para evitar cambios de desempate top2000 al renombrar caracteres. Conservar tau=20, alpha=.1 y calibración V2 solo en dev. Publicar EL-W, UNK, pesos y tamaños. Esperamos invariancia entre claro/mono dentro de 1e-10 porque una biyección fija preserva igualdades de caracteres, longitudes y tokens. El periódico puede alterar la reutilización de contextos: no fijar umbral de caída ni escogerlo para parecerse a Voynich. No usar ganancia residual como puerta de recuperación ni como clasificador de origen.

## Antecedentes, archivos y alcance

Revisados: batería BC-2026-10-22 (primaria no discriminante frente a barajado), EXP-177 (calibración al objetivo y falta de prueba de inversión), V2 residual, soporte de dos predecesores y diagnóstico de cantidades iguales. Búsqueda interna de rutas cipher/calibration/recovery y backlog realizada. KB histórica ~/voynich-kb ausente; no se afirma revisión exhaustiva de literatura ni originalidad. La pregunta nueva aquí es recuperación exacta reservada y prueba adversarial del selector; no otro ajuste a rasgos EVA.

Gemini: se incorpora la cautela metodológica de su revisión v2 archivada, sin aceptar sus errores sobre $L, plantillas o intervalos. No hay nueva llamada API ni revisión independiente de este protocolo.

Guardar script, pruebas, log, resultados con hashes y autoauditoría skills/audit_experiment.md. Ejecutar dos veces el script con destinos distintos y exigir identidad byte a byte; la repetición verifica determinismo, no independencia. Las fuentes/avisos y licencias originales permanecen en el paquete residual; no redistribuir aquí textos íntegros ni ejemplos largos. Publicar solo hashes y métricas de las secuencias generadas.

No aplicar un descifrador a Voynich por aprobar este ejercicio. Un método general deberá afrontar alfabeto, familia, idioma y segmentación desconocidos, múltiples claves y controles adversariales más exigentes. El resultado de esta prueba no decide esas cuestiones.
