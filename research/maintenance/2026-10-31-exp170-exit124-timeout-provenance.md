# EXP-170: distinguir salida 124 del hijo de timeout real

**Fecha:** 2026-10-31. **Tipo:** corrección de integridad de registros, sin experimento lingüístico ni nuevo EXP. **Base de trabajo:** `master` `7cd303b46e96d9c6d7948594ca23c519ee1fee55`. **Estado científico:** EXP-170 histórico **BLOCKED**; sus 400 simulaciones no se han reproducido.

## Defecto y falsación

El runner aislado de reconstrucción moderna añadía `TIMEOUT` al log de stderr siempre que `returncode == 124`. Sin embargo, `subprocess.run` también puede devolver 124 si el hijo termina por sí mismo con ese código, sin que el proceso padre haya agotado su límite. Así, dos causas distintas producían una atribución de timeout falsa. Este defecto se desprende de la condición del código anterior; no hay evidencia de que afectara a las ejecuciones históricas.

**Control adversarial:** un hijo sintético devuelve `returncode=124`, `stderr=b"child exit"` y no lanza excepción: el recibo debe indicar `timed_out=false` y stderr no debe contener `TIMEOUT`. **Control positivo:** una excepción `subprocess.TimeoutExpired` debe registrar `timed_out=true`, código 124, conservar bytes originales y añadir el marcador de timeout en la vista textual. Ambos casos deben conservar un estado `FAILED` y no publicar un JSON de simulación válido.

## Cambio propuesto

En `scripts/run_exp170_isolated_reconstruction.py`, el marcador de timeout pasa a depender exclusivamente de la excepción `TimeoutExpired`. El recibo de ejecución incorpora el booleano `timed_out`, que permite distinguir ambas causas aunque compartan código 124. Se añaden regresiones en `tests/test_exp170_isolated_reconstruction.py`. No se ejecuta Naibbe: los controles usan dobles sintéticos.

## Puerta de cierre y evidencia pendiente

Verificar `python -m unittest discover -s tests -p 'test_exp170_isolated_reconstruction.py' -v` y `python -O -m unittest discover -s tests -p 'test_exp170_isolated_reconstruction.py' -v`, junto con la CI canónica, en el SHA exacto de la rama. Inspeccionar logs y comprobar ausencia de conflictos concurrentes antes de integrar; después verificar CI del nuevo `master`. Este documento no declara CI verde ni integración antes de comprobarlas.

No se modifican transcripciones, fuentes históricas, `experiments/exp_170_naibbe_simulation/script.py`, vectores originales, semillas, parámetros, hashes, folios reservados ni `state/committed_claims.md`. El runner conserva sus logs binarios y resultados fallidos. No se recuperaron los insumos externos originales; una ejecución moderna no equivaldría a reproducción histórica. No hay significado asignado ni traducción validada. Evaluación general prevista para 2026-11-22 sin prometer descifrado.
