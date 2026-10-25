# Integración verificable del paquete visual — 25-10-2026

## Problema y cambio

La PR #48 conserva preparación visual y cobertura de etiquetas fuera de master. Su CI previa pasó sobre 13a9bd7aa353c9ae7ae250132e2bbe6764a344df, pero la CI canónica no ejecutaba sus tres archivos de pruebas ni regeneraba los paquetes nuevos. Se integra sin conflictos con la cabeza fa9235d6cbb079cd6318ceab743c7bb2264e5050 de PR #57, preservando corpus, manifiestos, colas bloqueadas y resultados históricos.

Se añade a Voynich Check un paso que ejecuta los tests visuales, de geometría del coordinador y de cobertura, regenera coverage.json y las dos colas gzip y coteja sus bytes y SHA256.json con lo archivado. El SVG sigue siendo una previsualización exclusiva del coordinador, con la imagen original recuperable; no se entrega como material ciego.

## Verificación local

Python 3.12.14: 290 tests, sin fallos, una omisión por el archivo crudo ausente de la batería histórica. Auditor de operaciones: éxito; identidad de 14 corpus: cero errores, cuarentena conservada. Regeneración del diagnóstico, ambas colas gzip y manifiesto SHA256: igualdad exacta mediante cmp. El cotejo de páginas de PR #57 forma parte del árbol integrado. La CI de esta nueva cabeza debe verificarse por separado antes de fusionar.

1.172 tareas para 2.196 registros; cero listas y cero anotaciones. Estas cifras reproducen el paquete previo, no constituyen un nuevo resultado científico. Los 1.024 localizadores comunes no acreditan alineamiento de objetos. El diagnóstico previo de ausencia de Lp en desarrollo/test no se resuelve cambiando la partición.

## Alcance y pendientes

No se han vuelto a descargar o inspeccionar imágenes, aprobado máscaras, solicitado anotaciones, llamado a Gemini, entrenado modelos ni evaluado texto reservado. No se modifica ningún ledger científico ni committed_claims. La omisión local no equivale a reproducción de la batería histórica; su reconstrucción se verifica en la CI remota conforme al workflow.

Después de la integración: revisión de regiones/máscaras con exposición documentada, correspondencia etiqueta/objeto y anotadores independientes. No convertir preparación operativa en evidencia semántica.
