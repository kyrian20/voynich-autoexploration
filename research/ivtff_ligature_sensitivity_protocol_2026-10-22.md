# Protocolo de sensibilidad para ligaduras IVTFF

Fecha: 2026-10-22  
Estado: protocolo pre-registrado; **sin resultados nuevos calculados**  
Repositorio: `kyrian20/voynich-autoexploration`

## Pregunta

¿Cuánto cambian las estadísticas que dependen de la tokenización cuando se procesa una ligadura IVTFF `{…}` de maneras distintas? La especificación oficial IVTFF 2.0.2 §6.6 define el span como representación de una ligadura de caracteres Voynichese y exige que cierre en la misma línea: https://www.voynich.nu/software/ivtt/IVTFF_format.pdf.

## Reglas de seguridad

1. Conservar siempre el texto bruto exacto, los offsets y la etiqueta de ligadura. Ninguna vista derivada sustituye a la fuente.
2. No editar, borrar ni regenerar ningún EXP histórico.
3. No escoger la política que produzca el resultado estadístico más llamativo.
4. ZL3a y ZL3b son transcripciones alternativas del mismo manuscrito, no réplicas independientes. Informar sus resultados por separado.
5. Si la especificación no resuelve una decisión analítica, marcarla como decisión experimental y no como requisito normativo.

## Vistas que se compararán

- **V0 — histórica:** reproducir exactamente la conducta de los tokenizadores actuales que descartan el contenido entre llaves. Solo sirve como comparador de compatibilidad, no como verdad de referencia.
- **V1 — ligadura atómica:** conservar cada `{…}` como una unidad de tipo `ligature`, distinta de una palabra/token ordinario. Las estadísticas deben declarar cómo cuentan esa unidad.
- **V2 — expansión controlada:** conservar el span y producir además una vista derivada que expanda el contenido interno a caracteres de transliteración, sin perder la marca ni los offsets que señalan que esos caracteres procedían de una ligadura.

V1 y V2 son políticas analíticas alternativas. La norma confirma la ligadura; no afirma que una sola vista sea apropiada para toda pregunta lingüística.

## Plan de evaluación

1. Construir fixtures mínimos revisados a mano: ligadura al inicio/medio/final de una palabra, ligadura sola, múltiples ligaduras en una línea, códigos high-ASCII válidos dentro de llaves, y delimitadores abiertos/cerrados en líneas distintas.
2. Probar primero la estructura y trazabilidad: el texto bruto reconstruido debe coincidir byte por byte con la entrada; cada unidad derivada debe apuntar a un rango original; una ligadura nunca puede atravesar un salto de línea.
3. Comparar V0/V1/V2 sobre ZL3b y ZL3a por separado. Registrar hashes SHA-256 de cada fuente y de cada salida.
4. Cuantificar cambios en número de unidades, límites de palabra, tokens afectados, conteos de frecuencia y estadísticas posicionales. Identificar expresamente los experimentos existentes cuyas variables dependan de esas medidas; no asumir que todos los EXP se ven afectados.
5. Ejecutar pruebas de sensibilidad en un experimento nuevo con ID libre comprobado en el registro. No asignar un ID por conjetura ni reutilizar uno de los identificadores colisionados.
6. Revisar manualmente muestras de cada clase de diferencia antes de interpretar resultados.

## Criterios de aceptación

- Los fixtures pasan en CI.
- Ninguna salida pierde el texto bruto ni los offsets.
- V0 reproduce el comportamiento histórico documentado.
- V1/V2 tienen resultados y reglas separados, con parámetros declarados.
- El informe presenta magnitudes y limitaciones, sin tratar ZL3a/ZL3b como muestras independientes.
- Los resultados históricos permanecen intactos; cualquier corrección posterior se publica como nuevo experimento y referencia explícita al resultado anterior.

## Situación actual

- [x] Confirmada la semántica normativa de las llaves en IVTFF 2.0.2 §6.6.
- [x] Inventario mecánico: 446 spans en ZL3b, 444 en ZL3a y ninguno en IT2a (véase `research/ivtff_brace_span_inventory_2026-10-22.md`).
- [x] Auditoría reforzada para exigir cierre en la misma línea.
- [ ] Validar el fixture multilínea en CI tras corregir su escape.
- [ ] Implementar las vistas V1/V2 sin tocar los resultados históricos.
- [ ] Ejecutar y revisar la sensibilidad en un EXP nuevo.
