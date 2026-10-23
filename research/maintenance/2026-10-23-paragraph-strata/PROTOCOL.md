# Estratos de marcadores de párrafo — protocolo descriptivo

Base: 29b86941250e75be46eb62ac9d6efb5032563da0. Escrito el 23-10-2026 antes de ejecutar. Análisis retrospectivo sin nuevo EXP, valores p ni elección de una vista favorable.

Usar el puente ya fijado: tres transcripciones, $L=B, todos los locus P, lector histórico y ocho vistas candidatas. Reconstruir la misma población común no vacía y exigir coincidencia de su hash de IDs y las métricas agregadas con el snapshot anterior.

Separar P0 y otros locus P; dentro de cada grupo distinguir presencia de un span superior `paragraph_end` (<$>) de su ausencia. **Ausencia de marcador no equivale automáticamente a línea interior de párrafo.** No ensamblar párrafos ni inferir fines al cambiar de página. Publicar también el inventario por locus exacto y lista de IDs de cada estrato. Rechazar marcadores de párrafo anidados hasta adjudicarlos.

Para -am/final calcular en cada lector y estrato O, E=sum(k_i/n_i) y O/E, con sus propios inventarios. Publicar adicionalmente O/n_líneas y la tasa de tokens -am. Conservar las líneas unitarias e informar su número; tienen extremo fijo. Comprobar que los cuatro estratos suman todos los registros comunes y sus observados/esperanzas. Evaluar exhaustivamente las ocho vistas. No comparar cocientes con denominadores distintos como si fueran el mismo estimando.

Para P0 sin marcador final, en ZL3b, retirar por turno cada folio numérico que contribuya líneas, conservando las caras/paneles del mismo número juntas. Informar rango de O/E en cada vista; no llamarlo intervalo de confianza.

Control sintético: `y.xam<$>` debe pertenecer a P0/con marcador, con O histórico=0 y O candidato=1. `y.xam` debe pertenecer a P0/sin marcador, con O=1 en ambos. `y.xam` bajo Pb se mantiene separado. La suma de los estratos debe recuperar los totales de esta fixture. EXP-208 y C005 se inspeccionan como antecedentes, no se reproducen ni modifican: sus parsers y reconstrucción de párrafos son diferentes. Aplicar los cinco controles de auditoría antes del informe.
