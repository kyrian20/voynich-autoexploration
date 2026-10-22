# Estado de publicación

El experimento completo se ejecutó y se reejecutó localmente. El commit local 87701fd conserva todos los tokens, selecciones, vistas y logs; paquete completo en work/entrega/bc-2026-10-22-completo.tar.gz del entorno de trabajo. El informe se refiere a ese paquete íntegro.

La revisión automática rechazó la publicación de seleccion.json como divulgación de corpus crudo sin autorización específica, incluso después de comprobar que las transcripciones fuente ya eran públicas en este repositorio. Se ha solicitado autorización explícita para seleccion.json (también run-01/02), vistas_referencia.json y tokens.jsonl.gz. Hasta recibirla, esta PR publica código, hashes, métricas e informe, y omite esos datos crudos; no intenta eludir el bloqueo.

La prueba de reconstrucción de métricas a partir de tokens se ejecutó localmente con éxito. En la PR, si falta tokens.jsonl.gz, se declara SKIPPED con motivo explícito; una CI verde no significa que haya reconstruido el archivo ausente. Los otros seis contratos sí se ejecutan. Para reconstruir los tokens desde las fuentes públicas y el código fijado puede ejecutarse el comando de README en un directorio nuevo. No confundir una regeneración técnica con validación científica.

Los hashes SHA256.json conservan los compromisos del paquete completo; la falta de archivos en esta PR está declarada y no se reescriben esos hashes. Protocolo y código se fijaron en commits locales antes de simular; su historial completo se conserva en work/entrega/historial-prerregistro.txt. La publicación remota del snapshot ocurre después del análisis, circunstancia que no se presenta como prerregistro público anterior.
