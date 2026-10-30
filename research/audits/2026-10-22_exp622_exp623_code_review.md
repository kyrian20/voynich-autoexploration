# Revisión estática de EXP-622 y EXP-623 — 22-10-2026

**Alcance:** revisión de código de `scripts/exp622_ch_sh_specificity.py` y `scripts/exp623_it2a_ch_sh_specificity.py` en master. No se han ejecutado los scripts ni verificado sus datos de salida en esta revisión.

## Hechos verificados en código
- Ambos usan coincidencias `ch|sh`, seleccionan posiciones con caracteres a ambos lados y estratifican por folio, longitud y posición.
- Calculan el contraste `[(sh-ch) siguiente] - [(sh-ch) anterior]` promediado sin ponderar entre estratos.
- Ejecutan 10.000 permutaciones con semillas fijas y p bilateral `(exceed+1)/(B+1)`.
- Ambos definen `VOWELS=set("aeiouy")`.

## Riesgos prioritarios
1. **Validez de constructo:** `aeiouy` son caracteres latinos de la transcripción EVA; llamarlos «vocales» no demuestra que representen vocales fonéticas del manuscrito. Renombrar a «caracteres EVA de clase aeiouy» en documentación y resultados; no derivar conclusiones fonológicas.
2. **Conformidad IVTFF:** la extracción con regex `[A-Za-z]+` y supresión de anotaciones puede alterar límites de tokens, incluir contenido editorial o fragmentar tokens. Crear fixtures con casos anotados y comparar con parser IVTFF validado antes de confiar en tamaños de muestra.
3. **Unidad de dependencia:** múltiples apariciones pueden compartir token, línea, folio y plantillas léxicas. La permutación dentro de estratos no garantiza intercambio de etiquetas bajo hipótesis nula realista; evaluar controles por folio y análisis de sensibilidad con remuestreo por folio.
4. **Selección y multiplicidad:** pruebas exploratorias motivadas por hallazgos previos. No interpretar p nominal como confirmación independiente.
5. **Replicación:** IT2a y ZL3b son transcripciones alternativas del mismo manuscrito, no corpus independientes.

## Pruebas exigidas antes de afirmar un hallazgo
- Fixture de parser: encabezados, etiquetas de línea, ediciones, incertidumbres, separadores y tokens inválidos; rechazo o recuento explícito de casos ambiguos.
- Comparar recuentos por folio entre transcripciones y reportar folios compartidos, exclusiones y cobertura.
- Análisis de sensibilidad por folio, por longitud y posición, además de permutación original.
- Controles negativos con clases de caracteres predefinidas y pruebas de múltiples contrastes.
- Tabla de diferencias entre resultados antiguos y revisados; jamás sobrescribir silenciosamente resultados históricos.

## Interpretación provisional
EXP-622/623 son pruebas de regularidad ortográfica en EVA. Por sí solos no identifican lengua, sonido, semántica ni descifrado. La revisión es estática y no implica que los resultados numéricos sean correctos o incorrectos.

## Acción siguiente
Desarrollar tests de conformidad de parser y análisis de sensibilidad en PR separado; ejecutarlos en CI y adjuntar hashes, logs y diferencias antes de fusionar cambios a experimentos.
