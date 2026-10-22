# Descomposición de daiin→dam bajo controles restringidos

PROPOSED antes de implementar/ejecutar. Sin nuevo EXP. Continuación exploratoria, fuentes/candidatos vistos; ningún folio se considera nuevo.

## Pregunta
¿La cola baja del control uniforme persiste al conservar posición o bordes EVA? Se compara exactamente la misma pareja en P0, ZL3b e IT2a, split/join, alternativas primarias y ligaduras expandidas. Sin atravesar registros, sin borrar signos opacos. Corpus fijados por el manifiesto y por hashes de los resultados anteriores.

## Controles fijados
Permutar tokens dentro de cada registro y SOLO entre posiciones de la misma categoría:
1. `fixed_endpoints`: primera y última posición fijas por separado; interior intercambiable.
2. `same_initial`: mismo primer carácter EVA (proxy textual, no certificación de glifo).
3. `same_edges`: mismo primer y último carácter EVA.
4. `same_edges_position`: igual que 3, separando primera/interior/última posición.

No se ajustan categorías después de ver resultados. Enumerar colocaciones de A=daiin y B=dam dentro de cada estrato; el resto es O. Las asignaciones de categorías equiprobables se cuentan con enteros y se convolucionan entre registros con fracciones racionales. Umbral de seguridad de 1.000.000 asignaciones por registro; si se supera, abortar y declarar bloqueo, no cambiar selección.

Mostrar esperanza, varianza, soporte y cola exacta por control. Holm sobre las 16 vistas nuevas; baseline uniforme histórico solo como referencia, sin presentarlo como hipótesis nueva. Registrar todos los IDs y contribuciones, en especial controles degenerados. Si la varianza es cero, el control NO puede discriminar y no constituye evidencia contra significado. No usar umbral p como prueba semántica; la selección retrospectiva queda sin corregir.

## Expectativas y criterio de decisión
Si la evidencia residual disminuye al fijar posición o bordes, la comparación uniforme era insuficiente para atribuirla a identidad de token. Si persiste bajo un control con variación, solo se conserva como candidata a dependencia adicional, sin traducir. Es una prueba injusta para una hipótesis que defina el signo/función precisamente por esos bordes: el control condiciona parte de la señal. No refutar gramática ni lengua por un resultado nulo/degenerado.

## Antecedentes y diferencia
Reddy/Knight 2011 §5 y Smith/Ponzi, preprint julio 2018 de artículo 2019, describen dependencia entre bordes. Rozanova/Temerev arXiv:2608.17096v1 compara escala de borde e identidad y declara código público. Montemurro/Zanette 2013 trata organización a larga escala: no equivale a adyacencia local. Nuestro control exacto por registro de esta pareja es una aplicación específica, no una réplica integral de esos artículos. El KB ~/voynich-kb no está disponible en este entorno; se consultan el registro y documentos versionados más fuentes primarias, sin afirmar búsqueda exhaustiva de literatura.
