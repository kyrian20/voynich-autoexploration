# Correspondencia de páginas y hojas físicas — 25-10-2026

Auditoría operativa reproducida localmente sobre base `10e0670d8c263553c7cf3d74bfcbb386045f0669`, Python 3.12.14. Sin EXP nuevo, hipótesis semántica ni cambios de corpus o manifiestos.

## Pregunta y comprobación

¿Coinciden los identificadores admitidos por el auditor estructural IVTFF con las hojas reconocidas por la auditoría independiente de cobertura del manifiesto v2? El criterio de aceptación es igualdad exacta de conjuntos de hojas por edición y de asignaciones de todas las páginas compartidas, tras verificar hashes, estructura de los registros y cobertura del manifiesto. No se tokeniza ni puntúa texto reservado.

## Resultado

`results.json` conserva hashes y correspondencia completa por edición. Hay **225 páginas compartidas**, con asignación idéntica. ZL3b contiene además `f116v` y `fRos`; IT2a no contiene páginas exclusivas bajo estos lectores. Las hojas numéricas reconocidas por ambos auditores coinciden en cada edición. Los paneles recto/verso de una hoja comparten partición. `fRos` queda explícitamente sin hoja numérica y excluido; `f116v` no se fuerza dentro de la intersección elegible.

Esto confirma correspondencia de identificadores bajo estos lectores y fuentes exactas. No demuestra correspondencia visual, integridad de la encuadernación, conformidad IVTFF completa ni desciframiento. Las dos transcripciones pertenecen al mismo manuscrito y el holdout no es históricamente ciego.

## Reproducción y pruebas

```sh
python -m unittest discover -s tests -p test_holdout_page_crosswalk.py -v
python scripts/audit_holdout_page_crosswalk.py --out /tmp/page-crosswalk.json
cmp research/maintenance/2026-10-25-holdout-page-crosswalk/results.json /tmp/page-crosswalk.json
```

Cuatro controles sintéticos: paneles y exclusión de Ros; discrepancia con cabecera activa; panel que acepta el patrón amplio pero rechaza el estructural; sustitución de fuente tras congelar hash. Los cuatro pasan localmente. La suite completa y auditorías generales se documentan en la PR; la CI de la base no valida estos cambios.

## Revisión de alcance

Sin calibración con métricas Voynich, transformaciones léxicas ni comparación estadística. Los controles deben aceptar paneles válidos y rechazar las tres corrupciones; comportamiento observado conforme a lo esperado. No se extrapola a lectores históricos ajenos a los dos auditores cotejados ni a autenticación de imágenes. Ningún ledger científico ni afirmación comprometida se modifica.

Siguiente acción: usar esta correspondencia verificada en consumidores futuros y contrastar las anotaciones visuales de entrenamiento antes de ensayar una regla semántica. No calibrar reglas con las hojas de prueba.
