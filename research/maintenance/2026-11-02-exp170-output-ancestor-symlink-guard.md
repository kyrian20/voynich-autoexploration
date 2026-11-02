# EXP-170 — rechazo de redirección del directorio de salida (02-11-2026)

**Tipo:** corrección acotada de aislamiento y trazabilidad; **sin EXP nuevo** ni simulación Naibbe. **Reproducción histórica exacta: BLOCKED.** Base revisada: `master` `08954d77b8cd6289da27222eb1a5af752396d125`.

## Incidencia reproducible

`preflight()` de `scripts/run_exp170_isolated_reconstruction.py` comprobaba que la ruta resuelta del resultado estuviera fuera del checkout y rechazaba un enlace simbólico en el componente final, pero **no** rechazaba un enlace en un directorio padre de la salida. Una ruta `redirected-output-parent/new-run` con padre simbólico a otro directorio externo y componente final inexistente superaba la validación. La reserva atómica impedía sobrescribir una carpeta ya existente, pero los logs y el recibo podían terminar en una ruta redirigida sin que la política de procedencia la detectara.

**Criterio falsable:** una salida nueva cuyo padre sea symlink, aun resolviendo fuera del repositorio, debe rechazarse antes de crear carpeta, escribir recibo o lanzar el proceso. La salida regular con padres no simbólicos debe seguir aceptándose. La prueba sintética usa únicamente directorios temporales; no ejecuta el cifrador.

## Corrección y regresión

- `scripts/run_exp170_isolated_reconstruction.py`: comprobar `has_symlink_component(out_dir)` tras la protección de salida dentro del checkout y antes de reservar la salida. Rechazar la ruta completa, no solo el componente final.
- `tests/test_exp170_isolated_reconstruction.py`: caso adversarial con directorio padre enlazado y dos modos (`execute=False` y `execute=True`); verifica ausencia de subprocess, carpeta y alteraciones del archivo original. Las pruebas existentes conservan el caso positivo de salida regular y el rechazo de destino existente.

## Evidencia y alcance de aceptación

Comandos de CI requeridos: `python -m unittest discover -s tests -p 'test_exp170_isolated_reconstruction.py' -v`, la misma prueba con `python -O`, auditoría del archivo EXP-170, suite general, auditorías operativas y de corpus. **La existencia de este informe no implica que hayan pasado**: comprobar la CI de la PR y la CI posterior de `master` antes de cerrar.

No cambian `experiments/exp_170_naibbe_simulation/script.py`, `result.md`, los 400 vectores archivados, la transcripción ZL3b, los hashes congelados, el esquema, semillas ni las particiones prospectivas. La reparación es de rutas de salida, **no** demuestra identidad de las entradas de abril de 2026 ni rehabilita C001. Quedan pendientes recibos históricos Naibbe/italiano, adjudicación IVTFF y conciliación global de artefactos.

**Limitación residual:** el candado es una comprobación previa; no pretende eliminar carreras de sustitución de directorios por otro proceso entre comprobación y creación. Una garantía resistente a ese adversario exigiría primitivas de directorio con descriptores y `openat`/equivalentes. No se presenta como limpieza global ni como evidencia de traducción.
