# Cierre propuesto: etiquetas angulares IVTFF desconocidas en predictor de límites

**Fecha:** 2026-10-29. **Estado inicial:** FIX PROPOSED / CI PENDING. Sin EXP nuevo.
**Base:** PR #138, SHA `e1a54054a342be48647a073d32250dc4491edbdc`. La rama master inspeccionada antes de actuar estaba en `1bce529f2dd4f572f05489443c7a4579e9c0894f`. PR abiertas: #5, #7, #13, #66, #82, #138.

## Defecto, contrato y falsación

El lector sustituía **cualquier** etiqueta cerrada `<...>` por un espacio. Esto convertía `ab<foo>cd` en dos palabras aparentemente ciertas, aunque IVTFF 2.0.2 §§6.7–6.9 solo atribuye separación a las interrupciones de dibujo `<->` y `<~>`. Los comentarios libres `<!...>`, marcadores de párrafo y metadatos válidos se gestionan antes por reglas propias.

**Corrección:** convertir a espacios únicamente `<->` y `<~>`; cualquier etiqueta angular no reconocida que sobreviva se pone en cuarentena **para la fila entera** mediante el guardia de markup existente. No se le inventa una lectura ni un espacio. Las etiquetas válidas mantienen su semántica anterior.

**Criterio previo:** cinco regresiones pasan en Python 3.12 normal y optimizado; la CI completa en el SHA exacto pasa; se confirma que la reparación no cambia los corpus ni `results.json`. No se fusiona en master: la rama de destino es la PR #138 en borrador.

## Corpus y alcance

Fuentes congeladas de solo lectura: ZL3b SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc` e IT2a `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`. Censo de filas P aceptadas: 4.130 y 4.118 respectivamente. Una inspección preliminar de contenido recuperado por GitHub, anterior a CI, no encontró etiquetas angulares cerradas desconocidas en esos registros. Esto es **expectativa, no ejecución de la regresión Python ni certificación de conformidad IVTFF**. La prueba comprueba ambos SHA-256 antes del censo.

Script de regresión: `tests/test_line_boundary_unknown_inline_tags.py`; script corregido: `research/analysis/2026-10-28-line-boundary-reproduction/line_boundary_replication.py`. Comandos fijados:
`python -m unittest discover -s tests -p 'test_line_boundary_unknown_inline_tags.py' -v`
`python -O -m unittest discover -s tests -p 'test_line_boundary_unknown_inline_tags.py' -v`
Semilla: no aplica (determinista). No hay entrenamiento, puntuación, permutaciones ni acceso a resultados de hojas reservadas.

## Autoauditoría (cinco controles)

1. **Target-awareness:** regla derivada del formato, no de AUC ni de vocablos objetivo; sin calibración a Voynich.
2. **Destrucción de la característica:** la cuarentena descarta una fila completa si contiene markup no admitido; puede excluir adyacencias verdaderas. No es un test del idioma, sino un guardia contra candidatos ficticios.
3. **Extrapolación:** solo cubre etiquetas angulares cerradas y guardias previos de marcas sin cerrar. No certifica conformidad IVTFF global.
4. **Negativos:** si los corpus no contienen esos tags, el impacto real es nulo en el universo examinado; no demuestra ausencia en otros corpus o vistas.
5. **Controles:** se espera que `<->` y `<~>` sigan creando espacios y que `<!...>` y `<@H=2>` sean de anchura cero; las regresiones verifican esos comportamientos frente a las etiquetas desconocidas.

**Límites:** no se reejecuta el predictor ni se validan sus AUC/AP; los resultados históricos permanecen `INVALID_FOR_CLAIM` para el lector corregido. No se modifican corpus, semillas, particiones ni resultados congelados. EXP-170, adjudicación IVTFF completa y conciliación de artefactos siguen bloqueados.

**Pendiente:** completar CI, registrar run/SHA y revisar si hay trabajo concurrente antes de integrar en la rama de investigación. No declarar éxito antes de ello.

Referencia normativa: René Zandbergen, *IVTFF* 2.0.2 (2025-07-08), §§6.7–6.9, https://voynich.nu/software/ivtt/IVTFF_format.pdf.
