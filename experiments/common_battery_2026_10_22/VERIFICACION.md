# Verificación técnica

53 pruebas de unittest pasan (incluidas siete nuevas); siete pruebas de batería también ejecutadas directamente. Auditoría operativa pasa; 14 hashes de corpus verificados, archivo vacío en cuarentena sin usar. git diff --check sin errores.

Reejecución completa: `python experiments/common_battery_2026_10_22/script.py --out work/battery-replay`. Los cinco archivos deterministas de run-03 son idénticos byte por byte:

- `resultados.json`: `ef884f11fb01c28749936b2f3cb91d60837d639a513e7416aef3155f33ab133b`
- `seleccion.json`: `75fd47b8511235980004eb82913d963b008931f569a08dd33938ebe17cbd1d68`
- `tokens.jsonl.gz`: `d0e8d367785c943b65b91cb49eb0e07ebec5e10d0f765895d4a568ad7bd39716`
- `vistas_referencia.json`: `bfe3fac3ce127d4f37412bc5e1449e8ce9ccbfb441dc9e3188bfd2ec96b1acc2`

El log ejecucion.log se añadió después del replay y queda cubierto por Git, no por SHA256.json. Los originales EXP-170 y corpus conservan hashes de freeze.json.

Estas pruebas no validan origen lingüístico, intención histórica, significado ni una lectura del Voynich. CI remoto: pendiente al publicar la rama; no se afirma verde sin run verificado.

Intervalo de escritura observado run-03 (UTC, primera selección a último resultado; aproximación al tiempo de ejecución):
- seleccion.json: 2026-10-22T19:38:32.415805+00:00
- resultados.json: 2026-10-22T19:39:06.068892+00:00

Publicación: ver PUBLICACION.md. Las siete pruebas y el replay completo se verificaron localmente. En la PR parcial el replay se marca SKIPPED por archivo crudo no publicado; no se afirma su verificación en CI.


## Verificación posterior de reconstrucción

Los cuatro archivos deterministas se regeneraron desde e2d082e y coinciden con los SHA-256 anteriores, incluido el gzip de tokens. La suite original pasó sus 53 pruebas sin omisiones; con el contrato añadido de detección de archivo ausente/corrupto pasan 54 pruebas. Cinco contratos de integración y auditoría operativa también pasan. RECONSTRUCCION.json documenta ambas suites.

La CI actual reconstruye los datos en una carpeta temporal con Python 3.12.14/pandas 2.2.3, verifica los cuatro hashes y dirige el replay a esa carpeta. Ya no depende de que los datos crudos estén publicados en el árbol. No los incluye en artefactos ni commits. El éxito remoto se registra según el check del commit concreto; no se infiere del éxito local. Las selecciones de run-01/run-02 siguen sin recuperar y no se acreditan mediante hashes inventados.
