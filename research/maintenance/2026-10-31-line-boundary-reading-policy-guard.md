# Cierre acotado de política de lectura IVTFF — 31-10-2026

**Ámbito:** réplica en borrador PR #138; base de partida `492c15224710f45487943262d9645818ad5e4392`, rama `codex/line-boundary-leaf-replication-20261028`. No es un nuevo EXP ni una reproducción del predictor. La rama `master` observada al iniciar estaba en `2579f1233444dbe8c2e81cb30f0464af4bb60e51`. El resultado histórico `research/analysis/2026-10-28-line-boundary-reproduction/results.json` permanece `INVALID_FOR_CLAIM`.

## Defecto y falsación

`tokens(body, policy=...)` seleccionaba `drop_uncertain_word` mediante una comparación exacta y trataba **cualquier otro valor** como lectura primaria. Así, `tokens("ab[cd:ef]gh", "drop_uncertain_words")` devolvía `["abcdgh"]` en lugar de rechazar el nombre erróneo. Una ejecución mal configurada podía publicar una sensibilidad etiquetada como exclusión de incertidumbre sin haber aplicado esa exclusión. `parse()` tampoco validaba el nombre antes de leer filas, y con fuentes sin filas P la configuración incorrecta podía pasar desapercibida.

La corrección exige exclusivamente `primary` o `drop_uncertain_word` tanto en `tokens()` como en `parse()`; cualquier otro valor lanza `ValueError("unsupported reading policy: ...")` antes de procesar el contenido. No se modifica el algoritmo de las dos políticas válidas.

## Contrato de regresión y alcance

`tests/test_line_boundary_uncertainty_contract.py` añade pruebas que exigen rechazo de cuatro valores inválidos con y sin barreras, más rechazo inmediato al analizar una fuente que solo contiene metadatos. Las regresiones existentes de lectura primaria, exclusión de corchetes y barreras siguen siendo los controles positivos. Los dos modos de ejecución que exige la CI son:

```sh
python -m unittest discover -s tests -p 'test_line_boundary_uncertainty_contract.py' -v
python -O -m unittest discover -s tests -p 'test_line_boundary_uncertainty_contract.py' -v
```

**Fuentes originales protegidas y no modificadas:** ZL3b `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`; IT2a `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5` (SHA-256 declarados por el lector y comprobados por sus pruebas existentes). Este cambio no consulta hojas reservadas ni ejecuta el clasificador; no altera corpus, parámetros científicos, semillas, resultados históricos, particiones ni `state/committed_claims.md`. La prueba sintética no es evidencia de corrupción histórica: solo demuestra un modo de fallo potencial.

**CI remota:** pendiente de comprobar para el commit exacto de esta rama. No declarar cierre o reproducción antes de consultar el run y sus pasos.

## Autoauditoría según `skills/audit_experiment.md`

- **Target-awareness:** se revisa una opción del lector conocida, sin elegir tokens o umbrales por su relación con Voynich.
- **Feature-destroying:** la reparación rechaza una configuración inválida; no cambia rasgos ni unidades de análisis bajo políticas válidas.
- **Extrapolación:** solo se demuestra la protección frente a errores de nombre en este lector, no la conformidad IVTFF completa.
- **Alcance negativo:** no hay nuevo contraste estadístico ni inferencia sobre mecanismos de producción.
- **Controles:** ambas políticas válidas conservan las expectativas preexistentes; los valores inválidos deben producir error explícito incluso con un archivo sin registros P.

**Siguiente paso científico:** mantener `results.json` como `INVALID_FOR_CLAIM` y resolver adjudicaciones IVTFF antes de una reconstrucción completa y auditada del predictor. La limpieza general del proyecto sigue incompleta.
