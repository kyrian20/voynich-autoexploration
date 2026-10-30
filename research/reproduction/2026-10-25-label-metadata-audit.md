# Recurso reproducible: qué cuenta una selección IVTFF L/R
25-10-2026. **REPRODUCED**, alcance exclusivo de metadatos. No traducción, hipótesis lingüística ni certificación completa del inventario.

## Afirmación delimitada
En las versiones exactas ZL3b e IT2a archivadas en este repositorio, seleccionar cabeceras cuyo tipo comienza por L o R no equivale a seleccionar nombres de objetos: mezcla subtipos editoriales ligados a ilustraciones con escritura marginal, piezas sin cercanía clara a dibujo y texto radial.
La parte conceptual ya está descrita en IVTFF y por Zandbergen. La aportación de este paquete es instrumental: comando autónomo, hashes, conteos por subtipo y ausencias de cobertura. No se reclama descubrimiento de esa distinción ni prioridad científica.

## Reconstrucción desde fuentes
Se recuperaron ambos archivos del commit 83e002736cd77979dbe2fb4ea1158c139daeceef a un directorio nuevo.
SHA256:
- ZL3b: bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc.
- IT2a: 7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5.

El [script autónomo](../../scripts/audit_label_metadata_standalone.py) lee cabeceras literales, sin importar módulos del lector del proyecto, tokenizar cuerpos o cargar el inventario.
[Resultado íntegro](2026-10-25-label-metadata-audit.json).

| Edición | Registros L/R | Subtipos editoriales asociados a ilustración | L0/Lx/Ri/Ro |
|---|---:|---:|---:|
| ZL3b | 1171 | 729 | 442 |
| IT2a | 1025 | 724 | 301 |

Unión: 1172 IDs. En los IDs compartidos no se observaron discrepancias de subtipo. Los IDs ausentes por edición están enumerados en el JSON.
«Asociados a ilustración» significa únicamente pertenencia a La/Lc/Lf/Ln/Lp/Ls/Lt/Lz según la codificación, no objeto validado, categoría independiente ni identidad semántica.
Tampoco L0/Lx/R demuestra ausencia de referente o significado.

## Verificaciones ejecutadas
Python 3.12.14, biblioteca estándar. Los controles integrados comprueban que comentarios no cuentan, que distintos marcadores de cabecera se conservan, que cambiar el cuerpo no modifica la selección y que repetir un ID dentro de una edición provoca error.
Como contraste posterior, cada tripleta ID/subtipo/número-de-línea coincide exactamente con el inventario archivado: 1171 ZL3b y 1025 IT2a.
Esto es independencia de implementación limitada a extracción de metadatos, no revisión independiente de persona ni certificación de IVTFF. No se ejecutó el corpus completo por un nuevo parser general ni suite global.

## Reproducción
Desde la raíz de un checkout que incluya este paquete:
```sh
python scripts/audit_label_metadata_standalone.py \
  --source data/transcriptions/eva_zl3b.txt \
  --source data/transcriptions/eva_it2a.txt \
  --out /tmp/label-metadata-audit.json
cmp research/reproduction/2026-10-25-label-metadata-audit.json /tmp/label-metadata-audit.json
```
Comparar primero los hashes publicados. No interpretar coincidencia de salida como validación de significado.
El script no descarga ni redistribuye imágenes y no altera corpus.

## Antecedentes y evaluación de novedad
1. R. Zandbergen, IVTFF document issue 2.0.2, tabla 9: https://www.voynich.nu/software/ivtt/IVTFF_format.pdf . Define los subtipos y el alcance radial.
2. R. Zandbergen, Some special properties of labels in the Voynich MS, introducción: https://www.voynich.nu/extra/labels.html . Ya advierte que hay palabras/caracteres sin dibujo cercano y que no debe presuponerse que una etiqueta sea un nombre.
3. Se localizaron trabajos y recursos públicos de clasificación visual; no se reprodujeron ni se revisaron íntegramente en esta sesión. No son evidencia de novedad del presente recurso.

Conclusión de novedad: **no se ha establecido un descubrimiento científico original**. La distinción central es conocida. Este paquete es un recurso de trazabilidad y control de selección, potencialmente útil si otros reutilizan sus verificaciones. Su utilidad externa y originalidad instrumental aún deben ser evaluadas por terceros.

## Crédito y estado de difusión
Transcripciones: Zandbergen–Landini e IT/Takahashi, conforme a la documentación de datos del repositorio. Definiciones de formato y antecedente conceptual atribuidos a Zandbergen.
Juan ha impulsado el objetivo y las decisiones de rigor y continuidad documentadas en la conversación. El código y la redacción de esta entrega se generaron con asistencia de IA. No se atribuye a Juan una revisión paleográfica o autoría de material ajeno.
No se ha definido lista formal de autores académicos, asignado afiliación, obtenido DOI, enviado a revista ni contactado especialistas.
El repositorio público conserva procedencia y versiones; no acredita aceptación científica.

## Autoauditoría
- Conciencia del objetivo: la pregunta se elige a raíz de una limitación conocida; no se presenta como confirmación preinscrita ni búsqueda ciega.
- Implementación: no modifica ni tokeniza texto. Solo permite inferencias sobre cabeceras reconocidas; no es prueba justa de una teoría de lenguaje.
- Extrapolación: estas dos fuentes y esta selección. No objetos, muestras independientes, cifras universales o ausencia de significado.
- Negativos: falta de novedad demostrada no invalida la utilidad técnica; tampoco autoriza inflar la aportación.
- Controles: se esperaba invariancia al cambiar cuerpo y rechazo de duplicados; se observaron ambos. Se esperaba coincidencia con inventario y se obtuvo a nivel de ID/subtipo/línea.
Próxima decisión: conservar como recurso técnico. No redactar un artículo de «desciframiento» a partir de estos recuentos; elegir una pregunta lingüística discriminante solo tras comprobar controles y antecedentes.
