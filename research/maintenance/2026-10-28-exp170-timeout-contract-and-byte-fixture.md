# EXP-170 — timeout API y fixture binario real (28-10-2026)

**Tipo:** reparación operativa y de prueba de regresión, sin EXP nuevo. **Base comprobada:** `master` `cff80de8c84810446ea8c6e585aa411ed1148376`, con [CI push 40642940713](https://github.com/kyrian20/voynich-autoexploration/actions/runs/40642940713) `completed/success`. **Estado científico:** EXP-170 sigue **BLOCKED** para reproducción histórica exacta.

## Defectos identificados y criterios antes de probar

1. `run_reconstruction(..., timeout=...)` validaba el timeout positivo únicamente en la CLI, no en su API Python pública. Valores cero, negativos, booleanos o no enteros podían llegar a `subprocess.run`, provocar fallos después de reservar el directorio de salida y dejar recibos que no representaban un timeout válido. **Criterio:** rechazar esos cinco tipos de valores antes de preflight, reserva y lanzamiento, sin tocar el JSON histórico.
2. La prueba `test_failed_run_quarantines_exact_partial_output` de la [PR #119](https://github.com/kyrian20/voynich-autoexploration/pull/119) decía inyectar un byte UTF-8 inválido `ff`, pero su literal `b'...\\xff'` contenía los cuatro bytes ASCII `5c 78 66 66` (barra inversa y texto `xff`). Comprobaba copia exacta de bytes, pero **no** cubría la condición adversarial anunciada. **Criterio:** construir `bytes([0xff])`, comprobar que falla su decodificación UTF-8 y verificar que el resultado fallido se conserva byte a byte en cuarentena.

## Cambio acotado

- `scripts/run_exp170_isolated_reconstruction.py`: comprobación de timeout entero positivo (excluidos booleanos) antes de cualquier preflight o ejecución, sin cambiar la simulación histórica.
- `tests/test_exp170_isolated_reconstruction.py`: cinco casos adversariales de timeout con mocks que prohíben preflight/subproceso y aseguran que no aparece salida; se sustituye el falso `\\xff` por un byte `ff` real con aserción de `UnicodeDecodeError`.

No se modifica el script histórico, sus 400 vectores, los corpus, semillas, particiones reservadas, hashes congelados ni `state/committed_claims.md`. No se ejecuta Naibbe.

## Evidencia y límites

**Pendiente en el momento de abrir la PR:** CI de la rama y CI push posterior a la eventual fusión. No declarar cierre sin verificar ambas. El defecto de timeout es de la interfaz de reconstrucción moderna; la fixture incorrecta era una laguna en la cobertura, **no** evidencia de que los resultados históricos estuvieran corruptos. Otras regresiones ya prueban bytes inválidos en stdout/stderr, pero no en el archivo de resultados fallidos.

**Siguiente paso científico:** recuperar y acreditar las entradas y dependencias históricas exactas de EXP-170; conciliar artefactos e IVTFF antes de iniciar pruebas científicas bloqueadas. Sin traducción ni nueva inferencia lingüística.
