# Alcance de corrección y revisión — 23-10-2026

## Corregido en este ciclo

El predictor nuevo de dos predecesores falló un control sintético negativo: la segunda capa de suavizado podía mejorar la distribución marginal aunque no hubiera dependencia de identidad. Se detuvo antes de procesar los corpus reales. Se reemplazó esa atribución por una corrección de cociente centrado, conservando código y protocolo iniciales y el criterio negativo. Los dos controles sintéticos pasan y seis pruebas cubren el arreglo. Informe y comandos: [memoria de dos tokens](../analysis/2026-10-23-two-token-residual/REPORT.md).

El análisis reparado se ejecutó y reprodujo completo sobre las seis fuentes y los 16 controles por fuente. Los resultados negativos/no concluyentes se conservan; no se ajusta evaluación para fabricar un avance semántico.

## Comprobado

- Revisión de sintaxis/formato en esta copia: 659 archivos Python analizados con ast.parse y 150 JSON leídos, cero errores de formato.
- Auditoría de contratos operativos y reconciliación de IDs: retorno cero.
- Nueva suite: seis pruebas, retorno cero; normalización en contextos vistos/no vistos, sensibilidad conocida, negativos balanceados/proporcionales, separación de grupos y ausencia de tripletas entre líneas.
- Snapshot completo del predictor reparado: estructura/enteros exactos y floats finitos coincidentes dentro de 1e-12.
- La CI de la base 319085f091eeba47b088e99cdad85f2a7f3d2372 terminó en éxito: [39939182169](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39939182169). El nuevo commit requiere comprobar su propia ejecución.

## Pendientes que no se ocultan

No se declara ausencia de errores en todo el historial ni se confunde formato correcto con validez científica. Persisten la adjudicación completa IVTFF, referencias históricas a corpus mal identificados y equivalencia de todos los archivos históricos. La conformidad tiene cobertura finita.

EXP-170 conserva una dependencia Naibbe ausente. Se localizó un commit externo fijado en el registro de fuentes, pero todavía no se ha acreditado que sea la versión exacta usada por el experimento histórico. Además, su ruta latina apunta a un corpus cuya identidad histórica está en revisión. Copiar la versión externa o sustituir ese corpus sin adjudicación no resolvería la reproducción científica; cambiaría el experimento. No se ejecuta ni se presenta como reparado con entradas distintas. Véanse [revisión intensiva](../INTENSIVE_REVIEW_2026-10-22.md), [registro de fuentes](../external/2026-10-22-professional-sources/registry.json) y [identidad de corpus](../CORPUS_IDENTITY_REVIEW.json).

Los tokens archivados de algunos intentos de la batería común tienen una situación de publicación/recuperación separada. La reconstrucción temporal verificada en CI ya permite comprobar run-03 sin divulgar esos archivos; no completa las selecciones históricas de run-01/run-02. No se modifica su registro de publicación.

Estos pendientes no impiden ejecutar el nuevo predictor con sus fuentes fijadas. Sí impiden afirmar que todo el proyecto histórico está validado o que existe una traducción del manuscrito.
