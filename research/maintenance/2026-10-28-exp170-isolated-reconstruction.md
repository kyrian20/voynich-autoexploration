# EXP-170 — ejecución reconstruida sin sobrescribir el archivo histórico (28-10-2026)

**Alcance:** reparación operativa acotada, no experimento nuevo ni reproducción de las 400 simulaciones históricas. **Estado de la reproducción histórica: BLOCKED.** No se asigna ID EXP. La dependencia Naibbe y el texto italiano públicos no están acreditados como los bytes de la ejecución original; véase [procedencia](../2026-10-27-exp170-naibbe-source-provenance/REPORT.md).

## Defecto y decisión

El código congelado `experiments/exp_170_naibbe_simulation/script.py` escribe incondicionalmente en `experiments/exp_170_naibbe_simulation/data/simulation_results.json` (bloque final de simulaciones). Ejecutarlo directamente desde el checkout puede sobrescribir los 400 vectores históricos. No se edita el script congelado porque su SHA-256 `8fe0f7d153211b320b34ca8543dac1ba029e629c4413c203fb2df0031063721c` es evidencia de procedencia.

## Reparación: ruta alternativa de reconstrucción

`scripts/run_exp170_isolated_reconstruction.py` requiere rutas explícitas a un árbol Naibbe que contenga `naibbe_v2.py` y `references/naibbe_tables.csv`, al input italiano y a los tres SHA-256 externos. Antes de cualquier escritura comprueba los cuatro hashes históricos congelados con el auditor existente, la identidad del archivo inglés históricamente etiquetado Latin, los hashes externos, que no haya symlinks en esos tres archivos y que la carpeta de salida no exista ni esté dentro del repositorio.

**Sin `--execute` solo ejecuta preflight; no lanza cifrado ni escribe archivos.** Con `--execute`, copia el script original y los cinco recursos necesarios a un directorio temporal y ejecuta allí el script sin tocar el checkout. No copia el JSON histórico al directorio temporal. Valida que la nueva salida tenga cuatro condiciones, 100 vectores por condición y las claves numéricas archivadas. Crea una **carpeta de salida nueva fuera del repositorio**, sin sobrescribir, con `receipt.json`, `stdout.log`, `stderr.log` y, únicamente si la ejecución fue completa y válida estructuralmente, `simulation_results.json`. Los errores de ejecución, incluidos fallo al lanzar el intérprete y timeout, y de validación conservan recibo y logs, pero no publican un JSON parcial como resultado. El recibo siempre declara `historical_reproduction: false` y la salida se etiqueta `MODERN_RECONSTRUCTION_UNVALIDATED`.

Ejemplo **no ejecutado**, que requiere sustituir rutas y SHA-256 por valores verificados:

```sh
python scripts/run_exp170_isolated_reconstruction.py \
  --naibbe-dir /ruta/a/naibbe-cipher \
  --italian-source /ruta/a/divina_commedia.txt \
  --naibbe-sha256 SHA256_DEL_CODIGO \
  --tables-sha256 SHA256_DE_TABLAS \
  --italian-sha256 SHA256_DEL_TEXTO \
  --out-dir /tmp/exp170-reconstruction-nueva
# Agregar --execute SOLO para una reconstrucción nueva expresamente autorizada.
```

La copia temporal es **aislamiento de rutas**, no sandbox de seguridad del sistema operativo: el Python externo sigue teniendo los permisos del usuario. El wrapper no puede impedir que alguien ejecute el script histórico **directamente**. Se prohíbe esa vía en la práctica operativa; un bloqueo completo requeriría cambiar el script histórico (rompiendo su identidad congelada) o controles externos de permisos. No hay prueba de que una ejecución nueva reproduzca las métricas originales, ni prueba de identidad de los bytes externos históricos. Las dependencias `pandas` y el entorno exacto del upstream deben fijarse antes de cualquier ejecución real.

## Regresiones y criterios

`tests/test_exp170_isolated_reconstruction.py` contiene diez pruebas sin cifrado real: preflight sin escritura, destino existente, hash erróneo y symlink, destino dentro del checkout, alteración de bytes durante el copiado posterior al preflight, copia a temporal y publicación nueva con subprocess simulado, fallo de subprocess con logs, JSON generado incompleto con recibo de error, error de lanzamiento de subproceso con recibo/logs y timeout con bytes no UTF-8 decodificados de forma segura. El test de éxito **copia un JSON histórico como fixture sintético en el temporal** para comprobar el mecanismo de publicación: no es reproducción científica. Se ejecutan tanto con Python normal como con `-O` en la CI canónica. El auditor histórico y sus 18 pruebas siguen separados.

**Aceptación requerida:** CI de la PR en su SHA exacto, revisión de logs y CI de `master` después de la fusión. Ninguna prueba de este bloque autoriza ejecución real de Naibbe. No se modifican corpus, simulaciones, parámetros, semillas, folios reservados ni `state/committed_claims.md`.

## Pendientes

- Recuperar recibos de los 400 vectores, commit exacto de Naibbe y bytes originales italianos; sin ello EXP-170 permanece BLOCKED para reproducción histórica.
- La ejecución directa del script original continúa siendo peligrosa. Usar exclusivamente la ruta alternativa y comprobar salida nueva fuera del checkout.
- IVTFF independiente, conciliación de artefactos y PR científicas en borrador continúan pendientes. No hay traducción validada.
