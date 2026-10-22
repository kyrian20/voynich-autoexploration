# Orden residual — bloque público integrado

Este bloque se incorpora a la investigación abierta por petición del usuario. [Informe científico](REPORT.md) · [Integración y límites](INTEGRATION.md) · [Incidencias de corpus](CORPUS_INCIDENTS.md).

Requisitos: Python 3 y la biblioteca estándar. El lector canónico se importa desde el propio repositorio. La CI del proyecto ya instala PyYAML para sus auditorías anteriores; este bloque no añade dependencias externas ni usa red.

Desde cualquier directorio:

```bash
python /ruta/al/repositorio/research/analysis/2026-10-22-residual-order/run_integrated.py --out /ruta/temporal/nueva/fuera-del-repositorio
```

La carpeta de salida debe ser nueva y estar fuera del repositorio. El runner conserva logs, verifica los corpus contra `research/CORPUS_IDENTITY_REVIEW.json`, ejecuta 14 pruebas, regenera `inputs.json`, reproduce la auditoría de referencias históricas y contrasta ambos modelos con sus snapshots. Solo omite la cadena de versión de Python al comparar resultados; no omite conteos, semillas, pesos, hashes o pérdidas.

Las salidas nuevas quedan en esa carpeta temporal, no en los corpus originales ni en los snapshots de referencia. No existe modo de aceptar automáticamente un resultado diferente. La publicación conserva la arquitectura del proyecto: un publicador automático y workflows de comprobación/artefactos lectores.

`PROTOCOL.md` y `PROTOCOL_V2.md` se conservan literalmente y describen que el análisis se hizo inicialmente en privado. Su publicación posterior no los convierte en protocolos confirmatorios ni borra el fracaso de V1. V1 sigue siendo inadecuado para afirmar ausencia de lenguaje; V2 sigue siendo exploratorio.

La parte analítica usa entradas congeladas para reproducibilidad; el runner regenera esas entradas desde los mismos archivos canónicos y compara todos sus campos. Los archivos crudos ya están en `data/` y no se duplican aquí. La migración solo cambia metadatos de preparación/ruta: `MIGRATION_CHECK.json` verifica igualdad de todos los resultados científicos anteriores.
