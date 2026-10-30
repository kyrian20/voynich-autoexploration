# Selección corregida del piloto — v2
25-10-2026. Preparación ejecutada, sin prueba semántica.
La enmienda se publicó antes del cálculo en a486ff4c9152214c1883377c6af31215f9560168.
El [selector](../../../scripts/select_visual_pilot_v2.py) usa exclusivamente metadatos del inventario y el manifiesto v2.
[Salida completa con hashes](pilot-selection-v2.json).

Resultado: 21 hojas train contienen registros; se seleccionan numéricamente las primeras 12:
2, 17, 41, 49, 57, 65, 67, 69, 71, 75, 77, 81.
571 registros de edición y 288 localizadores distintos. No equivalen a 288 objetos independientes.
Solo f2r, f41v y f65r tienen referencias visuales archivadas en este inventario. No se han recuperado nuevas imágenes ni comprobado disponibilidad actual.
La selección anterior permanece en PILOT_FEASIBILITY.md. No se ha usado desarrollo o prueba para elegir esta selección.

## Verificación local
Se ejecutó el selector con Python y se comprobó invariancia ante inversión del orden de registros, 12 hojas, pertenencia exclusiva a train y ausencia de aprobación de tareas.
No se ejecutó la suite global ni se certifica CI.
Comando desde la raíz del repositorio:
`python scripts/select_visual_pilot_v2.py --out /tmp/pilot-selection-v2.json`
El JSON conserva hashes de bytes de entrada, folios y localizadores; no contiene EVA ni categorías inferidas. Es material del coordinador, no paquete ciego para anotadores.

## Autoauditoría
- Conciencia del objetivo: cambio informado por escasez del piloto inicial; selección condicionada a presencia de registros. No muestra representativa ni preregistro original.
- Implementación: no altera texto ni imágenes. El orden numérico favorece hojas tempranas, por lo que limita representatividad; se acepta solo para viabilidad.
- Extrapolación: resultados limitados al inventario archivado; presencia no prueba identidad visual ni ausencia en el inventario implica ausencia en el original.
- Negativos: no hay contraste sobre significado ni estimación de potencia.
- Controles: se esperaba la misma selección al invertir el orden; se obtuvo igualdad exacta. Se esperaba cero hojas fuera de train y cero tareas aprobadas; se verificaron ambos.

## Próximo paso material y límite
Resolver fuentes visuales de los folios seleccionados y adjudicar regiones/objetos, sin reemplazar hojas tras inspección. Las particiones recto/verso/panel se conservan.
Continúan pendientes máscaras revisadas y dos anotadores independientes con exposición documentada. El asistente expuesto no cumple ese papel. No entrenar ni medir acuerdo sobre anotaciones inexistentes.
