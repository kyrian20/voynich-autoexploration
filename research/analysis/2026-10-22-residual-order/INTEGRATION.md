# Integración pública y estado operativo — 22-10-2026

## Qué queda unido

El bloque de orden residual, creado inicialmente como paquete privado, queda incorporado al repositorio abierto `kyrian20/voynich-autoexploration`. Scripts, protocolos, entradas preparadas, resultados V1/V2, fuentes y auditoría de corpus forman una sola ruta versionada. El usuario autorizó su publicación expresamente.

El runner `run_integrated.py` conecta el bloque con los corpus y el lector del proyecto anterior; el workflow `Voynich Check` ejecuta esa reproducción junto con las comprobaciones existentes. No se crean workflows escritores ni se añaden secretos.

## Evidencia de migración

- Corpus originales reutilizados por ruta y SHA-256; cero copias crudas añadidas.
- `INTEGRATION_ORIGIN.json` conserva hashes de los artefactos originales del paquete privado.
- `MIGRATION_CHECK.json` contrasta todos los campos de los arrays científicos con los resultados originales. Los metadatos de preparación/entrada cambian al reutilizar los datos canónicos; no se modifica ninguna pérdida, semilla, peso ni intervalo.
- Regeneración completa de entradas y comparación estructural, además de 14 pruebas (10 previas y cuatro contratos de integración).
- El runner produce un recibo por ejecución, logs y resultados en una carpeta nueva externa al repositorio. Rechaza resultados diferentes; no regenera snapshots para hacer pasar la CI.

## Dos clases de corrección

La guardia anterior de hashes sigue protegiendo bytes. La nueva revisión `research/CORPUS_IDENTITY_REVIEW.json` añade identidad/uso: el bloque nuevo rechaza como entradas los seis archivos que requieren adjudicación. El README de los corpus se corrige sin renombrar ni sobrescribir los originales.

La búsqueda de referencias históricas se reproduce excluyendo el propio código de esta auditoría. No se cuentan sus declaraciones de nombres como nuevos experimentos afectados. Los 103 scripts localizados requieren determinar si cargaron el archivo, cómo lo filtraron y qué conclusión dependía de su idioma.

## Alcance científico

Integración operativa no equivale a validación científica total. V1 permanece conservado y no sirve para afirmar ausencia de lenguaje. V2 sigue siendo exploratorio y condicionado al modelo y a una calibración de desarrollo hecha después del fallo V1. La conformidad independiente de IVTFF y la revisión histórica de corpus siguen pendientes. No se presenta una traducción.

## Autoauditoría

Esta integración no selecciona una nueva hipótesis ni ajusta resultados para mejorar una métrica. Se comprueba igualdad de resultados antes de aceptar cambios de metadatos. Se preservan fuentes, intentos fallidos, limitaciones y numeración. Las pruebas de integración rechazan datos alterados, corpus con incidencias, revisiones de identidad ambiguas y cambios de resultados. Solo se permite variar la cadena de versión del intérprete.
