# Reconciliación de población del predictor de límites de línea

**Fecha:** 2026-11-05  
**Clase:** auditoría determinista de población y sensibilidad del lector; no es un EXP ni una reejecución del predictor.  
**Estado:** la diferencia histórica queda parcialmente descompuesta; 538 unidades netas siguen sin atribución por regla IVTFF.

## Pregunta

¿Qué parte de la diferencia entre las 35.318 unidades del lector inicial y las 29.906 unidades del lector corregido se debe a las políticas de coma incierta y ligaduras ASCII, y qué parte permanece pendiente?

## Fuentes fijadas

- ZL3b: `data/transcriptions/eva_zl3b.txt`, 411.671 bytes, SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- Lector inicial: commit `76717eff613c3235526a3e9097a581149fca5e1b`; el script de auditoría reproduce su selección de registros P y su tokenizador histórico.
- Lector corregido: commit `60d0bdb64931f1659c5f662a31d7471dbef5058f`, script SHA-256 `97e5cbc0f63cf3ca52fc555334e595d6f24d94a425e549c0c125d00f5d016059`.
- El script del lector corregido en ese commit coincide byte por byte con el del commit `3c243692a7a98ccef40ca80c5004075bd87bdebb`, citado para la reejecución de la PR #138.

## Recuento reproducido

Las cuatro vistas conservan 4.130 filas P y 207 páginas; cambian las unidades reconocidas dentro de las filas.

| Separadores inciertos | Llaves/ligaduras | Unidades |
|---|---|---:|
| Cuarentena (política actual) | Cuarentena (política actual) | 29.906 |
| Separar coma (sensibilidad histórica) | Cuarentena | 34.509 |
| Cuarentena | Expandir solo ligaduras ASCII | 30.158 |
| Separar coma | Expandir solo ligaduras ASCII | 34.780 |
| Lector inicial | Política histórica | 35.318 |

## Descomposición

La diferencia total es 5.412 unidades. Bajo esta matriz de sensibilidad:

- **4.603** corresponden al efecto de separar comas inciertas, manteniendo las ligaduras en cuarentena.
- La expansión de ligaduras ASCII añade **252** unidades con la coma en cuarentena.
- La interacción entre ambas decisiones es de **19** unidades (la expansión añade 271 con coma separada, frente a 252 con coma en cuarentena).
- Tras ambas sensibilidades, quedan **538 unidades netas** entre el lector inicial y la vista de coma separada con ligaduras ASCII expandidas.

La identidad aritmética es 5.412 = 4.603 + 252 + 19 + 538. Los 538 no se atribuyen aquí a categorías concretas: pueden incluir reglas de corchetes, símbolos no EVA, anotaciones y diferencias de lectura que todavía deben separarse por fila. La expansión de ligaduras es solo una sensibilidad y no rehabilita esas unidades como palabras válidas.

## Reproducción y alcance

Ejecutar desde la raíz del repositorio:

```sh
python research/maintenance/2026-11-05-line-boundary-population-reconciliation/audit_line_boundary_population.py
```

La salida estructurada está en `results.json`. El script comprueba hashes, fija ambos lectores, exige los recuentos de filas/páginas y verifica la identidad de la descomposición. Se ejecutó con éxito sobre los bytes exactos de ZL3b.

Esto es un diagnóstico de conteos, no una validación del modelo ni una comparación de rendimiento. No ajusta ni evalúa predicciones, no crea un EXP, no modifica transcripciones ni sustituye resultados congelados. No aporta idioma, significado ni traducción. La siguiente tarea concreta es atribuir las 538 unidades residuales mediante una tabla por fila y reglas mutuamente excluyentes, conservando también los casos con más de una anotación.

## Estado de integración

Preparado para la rama de la PR #138. La CI del HEAD anterior terminó correctamente en run 41274533462; esa ejecución no cubre estos archivos nuevos. Se comprobará una ejecución posterior antes de considerar este cambio verificado en GitHub.
