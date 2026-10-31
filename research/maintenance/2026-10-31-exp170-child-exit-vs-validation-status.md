# EXP-170 — distinguir el código de salida del simulador del código del auditor

**Fecha:** 2026-10-31. **Clase:** reparación operativa de procedencia, sin experimento nuevo. **Base inspeccionada:** `master` `dbe54d83077ceb11097313c359f448c62cc05f7c`. **Estado científico:** reproducción histórica exacta **BLOCKED**.

## Defecto comprobado en código

En `scripts/run_exp170_isolated_reconstruction.py::run_reconstruction`, `subprocess.run` puede devolver `returncode=0` y generar un archivo inválido. En ese caso, la comprobación estructural posterior modifica `receipt["returncode"]` a **65**. Antes de esta corrección el recibo no conservaba el código de salida **0** del proceso hijo: un lector no podía reconstruir de ese campo si había fallado el simulador o la validación posterior. El `validation_error` daba una pista, pero no era un campo explícito y estable de salida del hijo. Se trata de una pérdida de procedencia demostrable por el flujo del programa; no hay evidencia de que afectara a las simulaciones históricas.

## Reparación falsable

Se añade `child_returncode` al recibo de ejecución sin cambiar el significado previo de `returncode`, que continúa siendo el estado **del runner**. El nuevo campo es el retorno real de `subprocess.run` cuando el hijo termina; es `null` cuando el lanzamiento falla o `TimeoutExpired` impide observar un retorno ordinario. `timed_out` continúa siendo el indicador independiente de timeout. La nueva clave se escribe en el mismo `receipt.json` que los hashes de logs y los metadatos de entorno.

La regresión distingue siete escenarios: éxito sintético (runner=0, hijo=0); hijo con fallo (3,3); hijo con retorno 0 pero JSON malformado (65,0); hijo con retorno 0 pero métrica requerida nula (65,0); error al lanzar (126,null); salida ordinaria 124 (124,124, `timed_out=false`); timeout (124,null, `timed_out=true`). Los tests usan dobles sintéticos; **no se ejecuta Naibbe** ni se reproducen los 400 vectores. Se comprueba también la persistencia del nuevo campo en el recibo del caso de éxito.

## Criterios de verificación y límites

Ejecutar en Python 3.12 y comprobar ambos modos:
```sh
python -m unittest discover -s tests -p 'test_exp170_isolated_reconstruction.py' -v
python -O -m unittest discover -s tests -p 'test_exp170_isolated_reconstruction.py' -v
python scripts/audit_exp170_archive.py --check research/maintenance/2026-10-22-exp170-audit/results.json
```
Verificar CI de la PR y CI posterior a una eventual integración en los SHA exactos. Este documento no anticipa el resultado de ninguna ejecución.

**Conservación:** no se alteran el script histórico, los corpus, los 400 vectores, semillas, parámetros, hashes congelados, folios reservados, informes negativos ni `state/committed_claims.md`. El arreglo es de **trazabilidad operativa**, no de desciframiento. EXP-170 continúa **BLOCKED** hasta acreditar los bytes y el commit originales de Naibbe, el input italiano histórico y los recibos individuales. El fichero etiquetado `latin` sigue siendo inglés; no se sustituye. Tampoco se han resuelto la adjudicación IVTFF, la conciliación general de artefactos ni las PR científicas abiertas. Evaluación global: **2026-11-22**, sin prometer traducción.
