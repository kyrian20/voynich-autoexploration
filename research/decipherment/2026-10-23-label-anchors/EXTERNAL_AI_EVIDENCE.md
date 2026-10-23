# Incorporación crítica de investigación externa asistida por IA — 2026-10-23

**Estado:** revisión documental externa, NO reproducción independiente. No constituye desciframiento. No crea EXP nuevo.

## Fuente y condiciones de reutilización

- Simone Systems Research / Jon, repositorio público: https://github.com/thisisntjon/voynich (instantánea declarada 2026-10-19).
- Atlas público: https://simoneresearch.com/research/voynich/atlas/
- Documentación de datos: https://simoneresearch.com/research/voynich/atlas/data/
- El repositorio declara MIT para código y CC BY 4.0 para texto/resultados; atribuir al reutilizar y comprobar licencias de las transcripciones subyacentes.
- Fuente de esta ficha: documentación pública, **sin ejecutar scripts externos ni auditar los 619 archivos de resultados**.

## Hallazgos que justifican pruebas propias (NO adoptar como hechos confirmados)

1. **F-01/F-04:** las líneas son unidades estructurales y la longitud de palabras muestra ritmo intralínea; el propio equipo informa que verso métrico ordinario también puede mostrarlo. Nuestro contraste deberá incluir controles de verso y prosa, además de modelos nulos que preserven líneas.
2. **F-20:** el registro de hallazgos describe coincidencias visuales entre ilustraciones farmacéuticas y páginas herbales, pero ausencia de vínculo textual detectado en sus etiquetas. En la prueba `s128-p72` (18 parejas publicadas, comprobadas visualmente por los autores), informan `NO_LINK`, p=0,72, potencia estimada 0,958 y control positivo Egerton 200/200; no son resultados reproducidos por nosotros. En `db-s114`, 239 loci y 27 tipos repetidos, la concordancia por categoría fue 20/31, comparable al nulo (p=0,63); tras una corrección de filas fantasma: 6/15, p=0,745, con independencia de 14/15 parejas restantes sin verificar. **Advertencia para PR #13:** no repetir el mismo contraste imagen farmacéutica↔página herbal ni el mismo control de etiquetas repetidas sin aportar una hipótesis y datos nuevos. Consultar fuentes exactas y folios antes de cualquier prueba.
3. **F-33:** no encontraron vínculo fuerte entre vocabulario de núcleos y dibujos de plantas; reportan asociación de marcos de afijos con imágenes, con apoyo limitado. No convertir asociación en traducción ni aceptar una segmentación prefijo/núcleo/sufijo como verdad.
4. **F-28:** no observaron orden antidotario, alfabético o zodiacal bajo las pruebas realizadas. No generalizar a todos los posibles sistemas de ordenación.
5. **F-06/F-15:** reportan estructura predictiva en núcleos y dependencia entre afijos y núcleos; sus segmentaciones son vulnerables a la suposición X-01, cuyo control sintético falló. Toda comparación deberá repetir con segmentaciones alternativas y controles sintéticos.

## Límites de confianza

- El equipo declara 51 hallazgos: 17 triangulados, 14 corroborados, 15 de una sola línea y 5 controvertidos, **según su propia rúbrica**.
- La validación denominada «independiente» se realizó con otros agentes del mismo equipo, no con revisión científica externa.
- ZL3b, RF1b e IT2a proceden del mismo manuscrito; no son tres replicaciones independientes.
- Los autores informan de 79/238 líneas de evidencia post-hoc o sin verificación, 18 scripts con líneas modificadas tras fijarse y falta de corrección global por múltiples pruebas. Sus grados y pesos de hipótesis no son probabilidades.
- Nada de ello permite identificar el idioma o traducir una sola palabra.

## Decisión de integración y siguiente experimento

**INTEGRAR COMO ANTECEDENTE / NO IMPORTAR CONCLUSIONES.** Priorizar revisión detallada de F-20 (fuentes, folios, controles, resultados negativos), y después decidir si la PR #13 aporta una prueba realmente nueva. Si las mismas etiquetas y criterios ya se probaron sin éxito, no repetir; formular un contraste distinto, prerregistrado y con referencias visuales independientes. Antes de cualquier afirmación semántica: reproducir EXP-580, auditar tokenización, controles positivos sintéticos, partición por hoja física y corrección por multiplicidad.

## Otras fuentes de IA

- https://github.com/GSimonin90/voynich-system-decipherment — el propio autor aclara que sus interpretaciones semánticas son exploratorias, no confirmadas. **No importar propuestas de traducción** sin controles independientes.
- Cualquier blog o repositorio que afirme «desciframiento» se evaluará con los mismos criterios de falsación y predicción fuera de muestra.

## Registro de procedencia

Fecha de consulta: 2026-10-23. Lectura de las páginas públicas README, START-HERE y Atlas. La ficha no representa revisión completa del código fuente, reproducción ni validación de los 51 hallazgos.

## Verificación de integración — 2026-10-23

- Referencia externa primaria para F-20: https://github.com/thisisntjon/voynich/blob/main/FINDINGS.md#f-20 (registro de evidencias, no validación nuestra). F-20 cita `record/results_s53.txt`, `record/results_s53_p4a1_p4e1_anchors_and_errors.txt`, `record/lab/codex_lab/experiments/results_s114_repeated_label_object_consistency.txt` y `record/results_s128_20261019T090659.txt`. La documentación externa advierte que algunas líneas están marcadas POST-HOC o sin verificación y no se computan en su calificación.
- Compatibilidad interna: esta ficha es bibliografía crítica y se vincula conceptualmente a `PROTOCOL.md`, etapa 0 y controles adversariales. No reemplaza ni modifica `experiments/exp_580_label_corpus_grammar/`, `state/committed_claims.md`, los manifiestos de holdout o los resultados históricos.
- Puerta de decisión: no iniciar búsqueda semántica confirmatoria hasta (a) reproducir EXP-580, (b) auditar el detalle de F-20, (c) documentar una predicción nueva distinta de sus controles negativos, y (d) fijar referentes visuales sin consultar EVA.
- Alcance de la comprobación: presencia de archivos y referencias en la rama y contraste documental con FINDINGS.md público; no se ha descargado ni ejecutado el código externo. El resultado de GitHub Actions se verifica por separado; no inferir CI verde de la mera existencia del workflow.
