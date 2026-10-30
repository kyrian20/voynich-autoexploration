# EXP-590 — contacto directo de códigos high-ASCII con letras ASCII

**Fecha:** 2026-10-30. **Tipo:** auditoría descriptiva de una entrada real; sin EXP nuevo. **Estado:** propuesta en PR; la CI del commit final debe verificarse antes de integrar. No reproduce ni rehabilita el resultado histórico de EXP-590.

## Pregunta y criterio fijados antes del recuento

¿Cuántos códigos `@NNN;` de la lectura primaria, en los cuerpos IVTFF congelados, están inmediatamente junto a letras ASCII? El lector histórico descarta esos códigos y tokeniza secuencias `[a-z]+`. Un código situado **fuera de una ligadura** y entre dos letras puede convertir una unidad opaca en dos fragmentos ASCII. Si el código está **dentro de una ligadura `{...}`**, el lector histórico elimina el tramo completo, lo que es una operación diferente. No confundir ambas clases ni inferir cambios de puntuaciones sin reproducir el experimento.

La prueba es una **auditoría retrospectiva** de un mecanismo conocido, no un contraste confirmatorio de una hipótesis lingüística. Se seleccionó para resolver el impacto de los 168/160 códigos high-ASCII ya identificados en la PR #177. El criterio operativo exige inventario completo por edición, separación dentro/fuera de ligaduras, coincidencia de hashes y pruebas adversariales; no requiere un resultado positivo.

## Censo preliminar de las fuentes congeladas

Un segundo recorrido independiente de las filas de GitHub (separadores CR/LF, identificador de locus, exclusión de comentarios `<!...>` y alternativas entre corchetes) dio los siguientes valores. **Estos recuentos requieren cotejo con el JSON del auditor Python publicado por CI antes de considerarlos verificados de forma independiente.**

| Edición | Códigos | Filas con códigos | Fuera de ligadura | Fuera con letra adyacente | Fuera entre dos letras | Dentro de ligadura | Dentro entre dos letras | Filas con alguna adyacencia |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ZL3b | 168 | 122 | 110 | 72 | **19** | 58 | 41 | 102 |
| ZL3a | 160 | 117 | 103 | 66 | **19** | 57 | 41 | 98 |
| IT2a | 0 | 0 | 0 | 0 | **0** | 0 | 0 | 0 |

Las 19 posiciones por edición **no son 19 traducciones ni necesariamente 19 tokens distintos**. Son códigos fuera de ligaduras que tienen letras ASCII directamente a ambos lados. Los códigos dentro de ligaduras requieren una interpretación distinta. Las ediciones ZL3a/ZL3b son testigos relacionados del mismo manuscrito, no dos muestras independientes.

Identidad SHA-256 exigida por el script: ZL3b `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`; ZL3a `56419297682d338ff1a0a17f5ae251e3ee3e2c5bf05a62db04c5385ef30b36a2`; IT2a `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.

## Implementación y reproducción

El auditor nuevo `scripts/audit_exp590_high_ascii_adjacency.py` usa los offsets del lexer lossless, cuenta solo códigos de la lectura primaria y distingue ligaduras. Comprueba el SHA-256 de cada archivo y la estructura de página/locus. Emite para cada locus afectado número de línea, cuerpo exacto, SHA-256 del cuerpo, códigos y posiciones; la salida se crea con modo exclusivo y nunca sustituye un resultado existente. `tests/test_exp590_high_ascii_adjacency.py` incluye cuatro controles: contacto a ambos lados, alternativas/comentarios excluidos, dígitos Unicode y códigos inválidos, y el inventario real congelado.

Comandos (desde la raíz, Python 3.12):

```sh
python -m unittest discover -s tests -p 'test_exp590_high_ascii_adjacency.py' -v
python -O -m unittest discover -s tests -p 'test_exp590_high_ascii_adjacency.py' -v
python scripts/audit_exp590_high_ascii_adjacency.py --out /ruta/nueva/exp590-high-ascii-adjacency.json
sha256sum /ruta/nueva/exp590-high-ascii-adjacency.json
```

La CI archiva JSON y archivo SHA-256 durante 90 días. No hay aleatoriedad ni semilla. El primer intento de CI detectó un defecto de importación del **nuevo auditor ejecutado directamente como script** (los tests por importación pasaban); se reparó añadiendo la raíz al `sys.path`, sin tocar el lexer ni los resultados históricos. El fallo se conserva en la ejecución #41096135266; no se presenta como éxito.

## Alcance, auditoría y pendientes

- **Conciencia del objetivo:** no se eligen códigos por una métrica predictiva ni se ajusta el umbral a una señal; el criterio es adyacencia literal.
- **Preservación:** los originales, semillas, resultados negativos, folios reservados, corpus y `state/committed_claims.md` no se modifican.
- **Limitación:** la adyacencia literal no cuenta vecinos separados por etiquetas, puntuación ni llaves. Una ligadura completa se elimina bajo la política histórica; no se deben sumar sus códigos a los 19 posibles fragmentadores directos.
- **No inferencia:** no se ha recalculado `daiin`, la permutación de EXP-590, ni las métricas de ningún predictor. La adjudicación IVTFF completa y la reproducción histórica exacta de EXP-170 siguen bloqueadas.
- **Siguiente puerta:** contrastar recuentos y hashes del artefacto CI del commit final; si pasa, evaluar por locus cómo cambiarían los tokens con una política opaca explícita, **sin** reescribir el experimento histórico ni abrir un ciclo confirmatorio con folios reservados.

No hay traducción validada ni atribución de significado a `@NNN;`.
