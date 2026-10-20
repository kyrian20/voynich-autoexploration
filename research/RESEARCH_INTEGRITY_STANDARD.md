# Norma de integridad, reproducibilidad y archivo — Manuscrito Voynich

Versión: 1.0  
Fecha: 20-10-2026  
Estado: norma operativa adoptada; las auditorías no ejecutadas siguen pendientes.

## 1. Principio de publicación

Ningún resultado se considera validado por existir un JSON, un informe o una ejecución de Actions. Se valida únicamente cuando se puede reconstruir desde la fuente exacta, con un script revisado, parámetros explícitos, pruebas, controles y salida coincidente.

No se promete “cero errores” antes de ejecutar los controles. Se informa con precisión de lo comprobado, lo fallido y lo que aún no se ha podido verificar.

## 2. Estados obligatorios

Cada experimento debe llevar exactamente uno de estos estados:
- **PROPOSED**: protocolo escrito; no ejecutado.
- **RUNNING**: ejecución en curso; aún no interpretable.
- **REPRODUCED**: el script se ha vuelto a ejecutar y coincide con la salida archivada bajo la misma fuente y parámetros.
- **VALIDATED**: además de reproducido, supera controles de calidad, análisis de sensibilidad y el criterio de aceptación preregistrado.
- **NEGATIVE**: la prueba se ejecutó correctamente, pero el resultado no apoya la hipótesis.
- **BLOCKED**: un defecto de datos, parser, permisos o entorno impide una interpretación fiable.
- **SUPERSEDED**: reemplazado por una versión identificada, sin borrar el historial.
- **INVALID_FOR_CLAIM**: el artefacto existe, pero un error conocido impide utilizarlo para una afirmación concreta.

La validez siempre es específica: un resultado puede ser útil para conteos globales y no válido para el análisis por clase Currier.

## 3. ID y archivo

- No asignar EXP hasta buscar el ID en el registro, nombres, scripts, informes y resultados de GitHub y de la Biblioteca.
- Las fases, EXP, versiones de scripts, números de informe y ejecuciones de Actions son series diferentes.
- Si ya hay colisión, usar identificadores técnicos inequívocos como GH-EXP-623 y LIB-ORDER-2026-10-19-A/B en el inventario, conservando los nombres originales como alias históricos. No renombrar masivamente hasta mapear referencias.
- Nunca borrar el original defectuoso. Marcarlo INVALID_FOR_CLAIM, guardar el motivo y enlazar el artefacto corregido.
- No considerar una copia de la Biblioteca idéntica a GitHub sin hash de contenido y commit.

## 4. Paquete mínimo de experimento

Cada paquete debe contener:
1. ID único y estado.
2. Pregunta falsable, hipótesis nula y criterio de aceptación definido antes de ver el resultado.
3. Corpus, edición/transcripción, URL/licencia cuando proceda, SHA-256 y política de selección.
4. Script ejecutable y versión de Python/dependencias.
5. Semilla, parámetros y comando exacto.
6. Unidad de análisis y exclusiones explícitas.
7. Baseline sencillo y control adversarial apropiado.
8. Separación por folio para pruebas predictivas; ninguna división aleatoria de líneas que permita fuga entre entrenamiento y prueba.
9. Resultado bruto estructurado, informe interpretativo y logs.
10. Pruebas automatizadas, hash de los artefactos y commit de Git.
11. Limitaciones, análisis de sensibilidad y decisión final (apoya/no apoya/no concluyente).

No se debe usar un p-valor aislado como evidencia de desciframiento. Corregir comparaciones múltiples cuando haya exploración de varias palabras, modelos, métricas o variantes.

## 5. Corpus y formato IVTFF

- Tratar la transcripción original como inmutable.
- $L=A/B es la fuente de clase Currier; $Q es quire y $I es tipo de ilustración. No intercambiar estos campos.
- Preservar las líneas crudas, identificadores de locus, etiquetas y checksum antes de normalizar.
- La política para puntos, comas, corchetes, llaves, interrupciones de dibujo, etiquetas y continuación de línea debe quedar escrita y testeada.
- ZL3a, ZL3b e IT2a son transcripciones/ediciones alternativas del mismo manuscrito, no muestras independientes.
- Hasta resolver los 1.466/1.472 desacuerdos históricos, cualquier resultado sensible al tokenizador es BLOCKED o INVALID_FOR_CLAIM.

## 6. Controles de interpretación

- Separar análisis exploratorio de confirmatorio.
- Si se prueban múltiples variantes, corregir multiplicidad y publicar el conjunto completo de pruebas.
- Comparar con baseline mayoritario, baseline de metadatos y un control adversarial cuando sean pertinentes.
- Usar bootstrap/permutaciones al nivel que corresponda (normalmente folio, no token aislado) y explicar los supuestos.
- Reportar tamaños de efecto e intervalos de incertidumbre, además de p-valores.
- Los resultados negativos se archivan igual que los positivos.
- Las conclusiones de literatura externa son hipótesis hasta replicarlas en un protocolo propio; las transcripciones alternativas no cuentan como replicación independiente.

## 7. CI: lo que comprueba y lo que no

El workflow actual comprueba existencia/no vaciedad de dos transcripciones, sintaxis Python, pruebas de regresión de metadatos y el inventario de $L. Esto no garantiza corrección estadística, tokenización completa, ausencia de duplicados históricos, ni reproducibilidad de todos los experimentos.

Una ejecución se declara verde solo con una URL/ID de run verificado y sus logs. Un estado vacío de checks no equivale a CI verde.

## 8. Prioridades actuales

P0. Verificar ejecución real del workflow y corregir fallos de CI.  
P1. Resolver tokenización IVTFF con fixtures y comparación diferencial de ambos parsers.  
P2. Construir inventario automático de todos los artefactos EXP en GitHub y Biblioteca; resolver colisiones sin borrar nada.  
P3. Reproducir los análisis afectados por errores de metadatos o parser; mantener outputs antiguos como históricos.  
P4. Consolidar informes, registro maestro, índices y hashes.  
P5. Solo después, continuar investigación confirmatoria.

## 9. Regla de auditoría

Toda revisión debe terminar con:
- qué se inspeccionó;
- qué se cambió (rutas y commit);
- pruebas ejecutadas y resultado observable;
- defectos que quedan abiertos;
- siguiente acción concreta.

No afirmar que el proyecto entero está limpio hasta que el inventario global, los hashes, los conflictos de ID y la reproducción de los resultados críticos hayan sido auditados.
