# Control exploratorio de duplicación y contaminación entre particiones

Estado inicial: PROPOSED. Sin EXP nuevo. Fuente: HEAD 2da0b63617a3d6dc29b47b99a731a8c9692e9aaa.

Antes de ejecutar: inventariar SHA-256 de todos los archivos versionados y agrupar igualdad exacta por bytes (no equivalencia científica). No borrar ni fusionar nada. Separar archivos vacíos.

Para EXP-607, conservar corpus, lectores, intersección de registros elegibles, partición por folio y parámetros existentes. Evaluar mixed y P0, con los perfiles native_607 y candidate_conservative_ascii. Identificar secuencias de tokens completas del test presentes en train; eliminar únicamente esas filas del test y volver a puntuar modelo y control con el train intacto. Publicar IDs excluidos, hashes, denominadores y todos los resultados. No cambiar reglas después de verlos.

Resultado esperado: si la ventaja depende de líneas completas compartidas, caerá tras excluirlas; si conserva signo positivo, esa dependencia concreta no explica por sí sola la ventaja observada. No define significación ni valida semántica. No constituye confirmación nueva: los folios ya fueron explorados.

Prueba injusta si la eliminación se interpreta como limpieza de errores: una línea repetida puede ser real, especialmente un rótulo corto. Se trata de sensibilidad a una exclusión exigente, no de demostrar corrupción. Las coincidencias parciales y el ajuste previo del modelo no quedan descartados. Las dos transcripciones no son réplicas independientes.
