# Reconciliación completa de población del predictor de límites de línea

**Fecha:** 2026-11-05  
**Clase:** auditoría determinista del lector, sus unidades y los candidatos derivados; no es un EXP y no ajusta ni evalúa el predictor.  
**Estado:** la diferencia predeterminada de 5.412 unidades queda explicada por cambios concretos del lector. La vista alternativa de comas separadas + ligaduras ASCII expandidas aún difiere del lector inicial en 538 unidades; esa cifra es específica de esa sensibilidad, no un residuo del lector predeterminado.

## Preguntas y fuente

Concilié tanto las unidades como los candidatos generados por cada versión del lector a lo largo de los cambios de la PR #138. En cada snapshot usé el mismo ZL3b y el mismo lector de filas físicas.

- Corpus: `data/transcriptions/eva_zl3b.txt`, 411.671 bytes, SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`; Git blob `2a4533ab9bdfa85db9bad602d590978953055df1` en todos los snapshots.
- Lector de filas físicas: Git blob `eb50eee4b7ca3e44fb2e9f265337e6cbefbe0678` en todos los snapshots.
- Lector inicial: `76717eff613c3235526a3e9097a581149fca5e1b`.
- Lector actual analizado: `60d0bdb64931f1659c5f662a31d7471dbef5058f`, lector SHA-256 `97e5cbc0f63cf3ca52fc555334e595d6f24d94a425e549c0c125d00f5d016059`.

Cada snapshot conservó 4.130 filas P y 207 páginas. El corte cada quinta página se recalculó con el mismo orden de páginas y el embargo por texto duplicado; no encontró duplicados en estos snapshots.

## Atribución secuencial de la diferencia predeterminada

| Cambio del lector | Unidades | Candidatos totales | Positivos |
|---|---:|---:|---:|
| Barreras para interrogaciones/grafemas desconocidos | −131 | −226 | −31 |
| Cuarentena de unidades con llaves/ligaduras | −555 | −908 | −83 |
| Barreras para códigos de grafema high-ASCII | −79 | −136 | −29 |
| Barreras para símbolos internos no admitidos | −44 | −64 | −9 |
| Cuarentena de comas inciertas IVTFF | −4.603 | −6.405 | −669 |
| **Cambio total: inicial → predeterminado actual** | **−5.412** | **−8.287** | **−1.369** |

La suma de cambios explica exactamente 35.318 → 29.906 unidades, 35.111 → 26.824 candidatos y 3.923 → 2.554 positivos. La diferencia predeterminada ya no tiene unidades sin atribuir.

Dos correcciones alteraron candidatos aunque no el total de tokens: excluir pares que cruzaban loci no-P retiró 71 positivos; respetar marcadores de párrafo retiró 477 positivos. Cambios en comentarios de anchura cero, continuaciones con barra, numeración de loci y etiquetas IVTFF no alteraron estos recuentos en los snapshots revisados, aunque las barreras de loci y párrafos sí afectan qué pares pueden formarse.

## Población por hitos

| Hito del lector | Tokens | Candidatos / positivos | Corte cada quinta página: candidatos / positivos |
|---|---:|---:|---:|
| Inicial, 28-10 | 35.318 | 35.111 / 3.923 | 6.229 / 719 |
| Barrera de interrogaciones | 35.187 | 34.885 / 3.892 | 6.210 / 714 |
| Cuarentena de ligaduras | 34.632 | 33.977 / 3.809 | 6.049 / 701 |
| Barrera high-ASCII | 34.553 | 33.841 / 3.780 | 6.017 / 696 |
| Loci no-P interpuestos | 34.553 | 33.770 / 3.709 | 6.004 / 683 |
| Marcadores de párrafo | 34.553 | 33.293 / 3.232 | 5.913 / 592 |
| Símbolos internos no admitidos | 34.509 | 33.229 / 3.223 | 5.905 / 592 |
| Coma incierta en cuarentena | 29.906 | 26.824 / 2.554 | 4.792 / 468 |

## Regresión transitoria detectada

El commit `9acca718` introdujo una expresión regular de llaves defectuosa: su snapshot baja a 27.510 unidades y 24.744 candidatos. El commit `e94994a` corrige la expresión y devuelve el recuento a 29.906 y 26.824. Excluí ese snapshot intermedio de la atribución estable; no describe un cambio del corpus ni del resultado vigente.

## Sensibilidades actuales

La matriz actual confirma los recuentos en los cuatro escenarios:

| Política de coma | Política de ligaduras | Tokens | Candidatos / positivos | Corte cada quinta página |
|---|---|---:|---:|---:|
| Cuarentena | Cuarentena (predeterminada) | 29.906 | 26.824 / 2.554 | 4.792 / 468 |
| Cuarentena | Expandir ligaduras ASCII | 30.158 | 27.294 / 2.596 | 4.876 / 474 |
| Separar (sensibilidad histórica) | Cuarentena | 34.509 | 33.229 / 3.223 | 5.905 / 592 |
| Separar | Expandir ligaduras ASCII | 34.780 | 33.755 / 3.270 | 6.001 / 600 |

El valor **538** es la diferencia entre el lector inicial y la última fila de esta matriz. Esa fila combina dos alternativas respecto del valor predeterminado actual; no queda como discrepancia abierta del análisis principal. La expansión ASCII es una sensibilidad, no una decisión de que todas esas unidades sean palabras.

## Reproducción y alcance

El script `audit_line_boundary_population.py` fija los hashes del corpus y del lector actual; reproduce el parser inicial y las cuatro vistas actuales; y verifica la suma de la atribución y los recuentos de candidatos. La tabla histórica registra el lector, el commit y el Git blob exactos de cada snapshot. Para revisión directa, los snapshots de código se encuentran en el historial de Git en las rutas de commits indicadas en `results.json`.

La auditoría no reentrenó el modelo, no recalculó AUC ni ganancias logarítmicas y no cambió corpus, EXP o resultados históricos. El siguiente paso es adjudicar qué exclusiones conservadoras cambian el conjunto de candidatos plausibles, revisar las hojas afectadas y después evaluar el modelo solo sobre la población acordada. Ninguna de estas cifras aporta una traducción.

La primera auditoría de población quedó en el commit `cfb64127d518231ee3208940fb9c2adb79b1127e`; su CI terminó correctamente en run [42120777639](https://github.com/kyrian20/voynich-autoexploration/actions/runs/42120777639). Este seguimiento añade la atribución por snapshots y el censo de candidatos; se comprobará con una nueva CI.

