# Soporte del control de contexto anterior al cierre — 23-10-2026

Estado: **REPRODUCED**, limitado al diagnóstico y snapshot. No se ejecuta una prueba de asociación ni se estima potencia estadística. Base científica: bloque de estratos del 23-10-2026; integración anterior `34b9beb89e397e5dd38efc56720e2aa1ab0b5ba0`.

## Resultado principal

El control que conserva inventario, extremos de línea, bordes y longitud de cada posición interior permite cambiar el predecesor en solo **16 de 325 cierres -am de ZL3b** bajo la vista por defecto (4,92%). Las otras 309 líneas tienen el mismo predecesor en todas las permutaciones admitidas. El número esperado de predecesores diferentes en una realización es exactamente **8**. Esto diagnostica soporte restringido; no prueba independencia léxica ni ausencia de significado.

Se utilizan los mismos IDs B/P0 sin marcador explícito, las tres ediciones y las ocho políticas del bloque de estratos. Los cuatro controles fijan primera/última palabra, longitud de línea e inventario completo; difieren en las clases dentro de las que se permuta el interior. La palabra final nunca cambia, por lo que el diagnóstico no contrasta el exceso -am/final ya observado.

## Vista por defecto: split/primary/expand

Cada celda muestra líneas con predecesor variable / total y, entre paréntesis, el número esperado de predecesores distintos del observado en una permutación.

| Restricción adicional del interior | ZL3b: cierre -am | ZL3b: otros cierres | IT2a: cierre -am | IT2a: otros cierres |
|---|---:|---:|---:|---:|
| Ninguna | 325/325 (283,37829) | 1.555/1.558 (1.332,49920) | 324/324 (282,03646) | 1.541/1.543 (1.317,62961) |
| Longitud | 224/325 (135,72381) | 1.012/1.558 (605,17857) | 226/324 (139,35000) | 1.029/1.543 (616,67857) |
| Primer y último carácter | 90/325 (47,46667) | 428/1.558 (231,13333) | 87/324 (46,96667) | 433/1.543 (232,76667) |
| Bordes y longitud | 16/325 (8) | 117/1.558 (59,08333) | 15/324 (7,83333) | 121/1.543 (60,16667) |

ZL3a coincide con ZL3b en las cuatro cifras de cierres -am. En otros cierres difiere en longitud: 1.011 líneas variables y esperanza 604,67857. La salida conserva todas las demás cifras; las coincidencias entre ediciones relacionadas no cuentan como evidencia independiente.

En las ocho políticas ZL, el control de bordes y longitud permite variar **15–16** predecesores de cierres -am; la esperanza varía entre **7,33333 y 8**. IT2a conserva 15 y 7,83333 en las ocho vistas. En otros cierres, el rango ZL es 116–119 líneas variables; IT2a conserva 121. No son intervalos de confianza.

## Método, reproducción y controles

Para una línea con tres o más tokens se toma la penúltima posición. Sus candidatos son todos los tokens interiores de la misma clase, incluyéndola a ella y manteniendo repeticiones. Si k es el número de candidatos y c los iguales al observado, P(cambio)=1-c/k. Se suman fracciones exactas. Las líneas de una o dos palabras no tienen predecesor interior intercambiable y aportan cero.

El snapshot conserva hashes de fuentes, IDs seleccionados, código, protocolo y dependencias, las 96 combinaciones fuente/política/control y los IDs/candidatos variables del control más restrictivo. Antes de calcular se exige reconstrucción exacta de las métricas del paquete de estratos para cada vista. No se mezcla información entre líneas, caras o folios.

Cinco pruebas pasaron. Se enumeran todas las secuencias interiores de longitud 1–4 sobre {aba,aca,aa,bb}, y todas sus permutaciones admisibles con multiplicidad bajo los cuatro controles: las probabilidades enumeradas coinciden exactamente con la fórmula. Se comprueba conservación de inventario y extremos; las permutaciones se admiten solo si conservan la clase de cada posición. También se cubren candidatos repetidos, líneas cortas, partición -am/otros, entradas inválidas y ausencia de mutación.

```
python tests/test_predecessor_opportunities.py
python scripts/audit_predecessor_opportunities.py --check research/maintenance/2026-10-23-predecessor-opportunities/results.json.gz
```

## Decisión y límites

No se inicia una prueba confirmatoria de identidad del predecesor sobre el conjunto completo usando este control como si las 325 líneas pudieran aportar variación. Cualquier contraste futuro deberá declarar las 15–16 líneas variables, su agrupación por folio y su selección retrospectiva, o definir otra población/pregunta antes de ejecutarse. El número de líneas variables por sí solo no establece suficiencia ni insuficiencia estadística para un efecto dado.

Este control condiciona bordes y longitud de transcripción: podría conservar precisamente parte de una estructura lingüística real. Una falta de diferencia no descartaría lenguaje, gramática o cifrado. Las longitudes no son longitudes fonológicas y los bordes no son glifos adjudicados. No se prueba aquí dependencia del predecesor, ni se comparan mecanismos de generación.

Antecedentes: el control daiin→dam mostraba 1–2 registros variables; este diagnóstico examina el predecesor de todos los cierres de línea del universo reciente, sin volver a contrastar aquella pareja. EXP-607 y V2 de orden residual predicen tokens y no sustituyen este cálculo de soporte. El cotejo de antecedentes se limita al repositorio.

## Autoauditoría — skills/audit_experiment.md

**Target-awareness:** -am, el universo y los bordes se conocen de trabajos previos; el diagnóstico es condicional a esa selección retrospectiva. Los cuatro controles se fijaron antes de ejecutar y se publican completos.

**Implementación:** ninguna palabra se elimina o reemplaza. Las permutaciones conservan los invariantes declarados. El control más restrictivo suprime oportunidades de cambiar identidad, que es precisamente la limitación medida. Por ello no se interpreta como prueba justa contra cualquier mecanismo lingüístico.

**Extrapolación:** los resultados describen este predecesor, estas líneas y estas vistas. No se generalizan a dependencias largas, otras unidades ni todos los contextos posibles.

**Alcance negativo:** no hay resultado negativo de una hipótesis semántica o lingüística; hay un diagnóstico de soporte restringido. No se convierte un predecesor forzado en evidencia de independencia.

**Controles:** se espera que la frecuencia de cambio bajo enumeración exhaustiva sea exactamente 1-c/k, porque cada candidato ocupa la posición con la misma probabilidad. Se observa igualdad racional en todos los fixtures enumerados. La caída de 325 a 16 líneas variables se explica por el refinamiento de las clases: las otras 309 no contienen una identidad alternativa admisible para esa posición. Se muestran por separado longitud y bordes para hacer visible la restricción; no se atribuye a una propiedad semántica.

No se cambian committed_claims.md, findings.md o failed_approaches.md, ni se añade un ID EXP. Las órdenes se añaden a CI; su éxito remoto requiere verificación separada.
