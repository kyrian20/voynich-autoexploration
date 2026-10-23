# Estado de publicación

El experimento completo se ejecutó y se reejecutó localmente. El commit local 87701fd conserva todos los tokens, selecciones, vistas y logs; paquete completo en work/entrega/bc-2026-10-22-completo.tar.gz del entorno de trabajo. El informe se refiere a ese paquete íntegro.

La revisión automática rechazó la publicación de seleccion.json como divulgación de corpus crudo sin autorización específica, incluso después de comprobar que las transcripciones fuente ya eran públicas en este repositorio. Se ha solicitado autorización explícita para seleccion.json (también run-01/02), vistas_referencia.json y tokens.jsonl.gz. Hasta recibirla, esta PR publica código, hashes, métricas e informe, y omite esos datos crudos; no intenta eludir el bloqueo.

La prueba de reconstrucción de métricas a partir de tokens se ejecutó localmente con éxito. En la PR, si falta tokens.jsonl.gz, se declara SKIPPED con motivo explícito; una CI verde no significa que haya reconstruido el archivo ausente. Los otros seis contratos sí se ejecutan. Para reconstruir los tokens desde las fuentes públicas y el código fijado puede ejecutarse el comando de README en un directorio nuevo. No confundir una regeneración técnica con validación científica.

Los hashes SHA256.json conservan los compromisos del paquete completo; la falta de archivos en esta PR está declarada y no se reescriben esos hashes. Protocolo y código se fijaron en commits locales antes de simular; su historial completo se conserva en work/entrega/historial-prerregistro.txt. La publicación remota del snapshot ocurre después del análisis, circunstancia que no se presenta como prerregistro público anterior.

## Entrega tras omitir la autorización

La autorización dio error y se pulsó Omitir. Esto no autoriza la divulgación de los archivos bloqueados. No se han repetido experimentos ni regenerado tokens.

En el entorno de continuación no se han localizado el commit local 87701fd, work/entrega/bc-2026-10-22-completo.tar.gz ni historial-prerregistro.txt. Su conservación fue declarada por la entrega anterior, pero aquí no se ha podido verificar ni recuperar. Los archivos bloqueados siguen ausentes de esta PR: data/run-01/seleccion.json, data/run-02/seleccion.json, data/run-03/seleccion.json, data/run-03/vistas_referencia.json y data/run-03/tokens.jsonl.gz. Los hashes originales se conservan sin cambios; no sustituyen los archivos.

La entrega recuperable reúne código, protocolos, resultados, informes, corpus fuente y hashes, con instrucciones para una reproducción futura voluntaria. Es parcial: no contiene los tokens archivados ni permite verificar ahora su replay. Completar la entrega requiere recuperar el paquete original del entorno anterior y resolver el control de publicación por su vía autorizada. No se fusiona la PR ni se activa fusión automática.


## Reconstrucción verificada posterior — 22-10-2026

Se regeneró run-03 desde el commit e2d082e333bed5a0f0444d13160af088f5c92518 con Python 3.12.14 y pandas 2.2.3, sin cambiar parámetros, semillas ni criterios. Los cuatro archivos resultados.json, seleccion.json, vistas_referencia.json y tokens.jsonl.gz coinciden exactamente con los SHA-256 publicados previamente. RECONSTRUCCION.json conserva las comparaciones. Es reconstrucción determinista, no recuperación del sistema de archivos ni un experimento nuevo.

Con los tres archivos ausentes reconstruidos en el árbol local, las 53 pruebas de tests pasan sin omisiones, incluida la reconstrucción de métricas desde los tokens. La copia verificable se entrega al usuario por separado; los datos crudos no se suben a esta PR; en ese commit la CI pública todavía omitía su replay. La autorización pública específica sigue sin resolverse. La reparación de integración de la PR #4, ya fusionada en master, se incorpora sin cambiar los resultados científicos.

Las selecciones de run-01 y run-02 no están recuperadas: no hay hashes originales individuales disponibles para acreditar una reconstrucción exacta. Los errores originales permanecen conservados. Este avance resuelve la ausencia de los datos de la ejecución final, pero no completa los dos intentos históricos ni convierte esta publicación en una entrega pública íntegra.

## Verificación automática sin publicación de corpus

El workflow prepara Python 3.12.14 y pandas 2.2.3, reconstruye run-03 en una carpeta temporal del runner y compara los cuatro hashes históricos con scripts/verify_common_battery_reconstruction.py. BC_REPLAY_DIR dirige el test de métricas a esa carpeta; si se solicita explícitamente y falta el archivo de tokens, la prueba falla en lugar de omitirse. Los datos temporales no se incluyen en los artefactos publicados, commits ni logs. Solo se muestran conteos y hashes.

Verificación local del mecanismo: cuatro hashes idénticos, 54 pruebas de tests sin omisiones, cinco contratos de integración y auditoría operativa correctos. Se conserva la comprobación de corrupción y ausencia de archivos. El resultado de CI remoto se consulta por commit; esta modificación no lo presupone aprobado. No se cambian el script científico congelado, las semillas, las tolerancias ni los resultados históricos.
