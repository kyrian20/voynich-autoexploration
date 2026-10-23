# Partición prospectiva por hoja física — protocolo fijado

Fecha: 23-10-2026. **Estado: PROPOSED** hasta ejecución remota verificada y archivo del manifiesto. Sin EXP nuevo.

## Bloqueo metodológico que se aborda
Los informes recientes de lectura candidata y predicción han reutilizado material observado durante la exploración. No se dispone de una validación semántica independiente de una clave de descifrado. Esta partición bloquea una asignación estable para **reglas propuestas después de su publicación**. No convierte los folios en una muestra históricamente ciega ni borra su exposición anterior.

## Regla fijada antes de mirar resultados
- Unidad: **hoja física** numerada, no cara recto/verso, token ni línea. Ambas caras quedan en el mismo grupo.
- Universo: intersección de hojas con cabeceras identificables en ZL3b e IT2a; se publican las diferencias de cobertura.
- Asignación: SHA-256 de la cadena UTF-8 `VOYNICH-FUTURE-RULES-2026-10-23-v1:<número de hoja>`; convertir los primeros 8 bytes a entero big-endian, módulo 10000. Menor que 7000: entrenamiento; de 7000 a 8499: desarrollo; resto: prueba.
- Los porcentajes son umbrales, no cuotas exactas. El manifiesto registra números reales, SHA-256 de cada corpus, identificadores de hoja y exclusiones.
- Se detiene si hay menos de 50 hojas compartidas o menos de cinco en algún grupo; no se reajusta la sal para obtener un resultado favorable.
- El algoritmo no lee cuerpos de texto ni usa etiquetas de lengua, imágenes, valores esperados o frecuencias.

## Uso para una regla candidata futura
1. Antes de consultar el grupo de prueba, publicar clave, algoritmo de lectura, idioma candidato, reglas de normalización, unidades de evaluación, baseline y umbrales de aceptación, con commit SHA.
2. Ajustar exclusivamente con entrenamiento; elegir hiperparámetros solo en desarrollo.
3. Evaluar una única vez en prueba; archivar todas las predicciones y fallos sin correcciones retrospectivas. Una modificación de regla requiere una nueva evaluación prospectiva, no reutilizar la misma prueba como si fuera virgen.
4. Rechazar cualquier afirmación semántica sin evidencia independiente del texto Voynich (por ejemplo, una clave externa o controles de idioma verificables). Una partición predictiva por sí sola **no demuestra traducción**.
5. No interpretar ZL3b/IT2a como muestras independientes. Una misma hoja está en el mismo grupo en ambas.

## Reproducción propuesta
```sh
python -m unittest discover -s tests -p 'test_prospective_leaf_holdout.py' -v
python scripts/prepare_prospective_leaf_holdout.py --out prospective-leaf-holdout.json
```

La CI conserva el JSON como artefacto por 90 días. La ejecución solo valida la **partición técnica**, no un experimento lingüístico ni un descifrado.

## Autoauditoría de diseño (skills/audit_experiment.md)
- **Target-awareness:** semilla y umbrales fijados sin consultar métricas Voynich. Universo basado en cobertura de cabeceras; no se ajusta por efectos de lenguaje.
- **Feature destruction:** no altera corpus ni baraja secuencias; particionar por hoja puede reducir potencia y desbalancear secciones. Reportar esa limitación antes de probar reglas.
- **Extrapolación:** ninguna hipótesis lingüística se contrasta aquí; no se declara ausencia o presencia de significado.
- **Controles:** pruebas sintéticas de invariancia al orden, agrupación recto/verso, intersección, hashes, rechazo de corpus insuficientes y exclusividad de particiones.
- **Riesgo de fuga:** la investigación anterior ya vio estos folios. La única garantía es evitar **nueva** contaminación accidental si se respeta el protocolo; revisión humana de reglas sigue siendo necesaria.

No se modifican `state/committed_claims.md`, resultados negativos, transcripciones ni informes históricos.
