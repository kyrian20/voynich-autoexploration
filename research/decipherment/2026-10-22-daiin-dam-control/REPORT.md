# daiin dam: primer control local con denominadores

**Estado: análisis exploratorio ejecutado; no traducción ni confirmación independiente.**

Se continúa el inventario previo de ocho lugares, sin repetirlo como un experimento nuevo. Se conserva la unidad de registro P0; no se atraviesan límites de línea.

| Fuente / coma | Pares elegibles | daiin con sucesor | daiin→dam | Esperanza nula exacta | Media de 9.999 controles | Cola exploratoria +1 | Holm (4 vistas) |
|---|---:|---:|---:|---:|---:|---:|---:|
| ZL3b / split | 30091 | 667 | 8 | 2.0910 | 2.0903 | 0.0006 | 0.0018 |
| ZL3b / join | 27700 | 628 | 8 | 2.1453 | 2.1598 | 0.0002 | 0.0008 |
| IT2a / split | 29571 | 683 | 8 | 2.6269 | 2.6091 | 0.0019 | 0.0038 |
| IT2a / join | 29571 | 683 | 8 | 2.6269 | 2.6091 | 0.0019 | 0.0038 |

El número observado supera al esperado bajo permutación de tokens dentro de cada registro en las cuatro vistas. La frecuencia y longitud de cada registro permanecen fijas. El control distingue el orden de palabras de su mero multiconjunto dentro de esas líneas; no distingue gramática, grafotáctica, maquetación o copia. Las dos transcripciones y las dos políticas son vistas dependientes del mismo manuscrito.

**Selección retrospectiva:** la pareja ya se conocía y fue escogida tras inspeccionar candidatos. Holm solo cubre estas cuatro vistas; no corrige todas las decisiones históricas. Por ello las colas no son valores confirmatorios y no se promueve ninguna interpretación semántica.

## Autoauditoría

**Conciencia del objetivo:** ocho parejas conocidas; diseño exploratorio declarado antes de ejecutar. Semilla 2026102201 y 9.999 permutaciones, sin ajuste posterior.

**Destrucción de características:** el control destruye intencionadamente el orden local y conserva composición, folio, locus y longitud. No prueba hipótesis que dependan de conservar el orden. Solo se admiten conclusiones sobre este nulo.

**Extrapolación:** resultados limitados a P0, alternativas primarias, dos políticas y dos transcripciones. No se generalizan a todos los cifrados o lenguas.

**Alcance negativo:** no se rechaza una clase de sistemas de escritura ni se asignan significados. Resultado de control positivo para asociación local, no para semántica.

**Comportamiento del control:** se espera una media igual a la suma por registro de n(daiin)×n(dam)/longitud, porque cada par ordenado de posiciones distintas es equiprobable. Las esperanzas y medias observadas se muestran en la tabla; sus cocientes permanecen entre 1/1,5 y 1,5. No se observa la anomalía del control que activaría el bloqueo de interpretación.

## Reproducción y siguiente paso

`python tests/test_daiin_dam_control.py` y `python scripts/audit_daiin_dam_control.py`. Tres pruebas pasan, incluida enumeración exhaustiva de permutaciones de pequeños multiconjuntos que verifica la esperanza analítica. JSON completo con IDs, hashes, denominadores e histograma nulo en results.json.

Antes de inferir función, comparar con parejas rivales emparejadas por frecuencia y contexto, documentar el universo explorado y separar una evaluación prospectiva. No llamar nuevos a folios cuyos contextos ya se examinaron. El protocolo anterior de traducción sigue pendiente; este control no lo completa.
