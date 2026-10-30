# Adjudicación de alcance de loci — piloto v2
25-10-2026. Revisión documental y conteo ejecutado; no experimento semántico.

## Fuente normativa
R. Zandbergen, IVTFF, document issue 2.0.2, 08/07/2025, tabla 9 (página impresa 22):
https://www.voynich.nu/software/ivtt/IVTFF_format.pdf
El tipo L incluye piezas cortas y caracteres, no exclusivamente nombres de objetos. L0 no establece cercanía clara a un elemento dibujado; Lx corresponde a escritura ajena/adicional, por ejemplo marginal. R corresponde a escritura radial. Estos códigos describen disposición y clasificación editorial, no valores semánticos.

## Casos revisados
f17r.13 figura solo en ZL3b, tipo Lx, cuerpo oteeeon.oiil. La vista completa muestra escritura adicional en el margen superior, pero no se ha alineado paleográficamente esa secuencia con píxeles precisos. Decisión: no admisible ahora como par nombre-de-planta/imagen; conservar como escritura marginal pendiente de alineación.
Los 26 localizadores de f49v son L0 en ambas ediciones, varios de un carácter y otros con códigos extendidos. La imagen contiene una ilustración vegetal y marcas marginales. No existe aquí evidencia de 26 rótulos de objetos distintos. Decisión: bloquear su uso como pares objeto/rótulo, sin borrar registros ni afirmar ausencia de significado.

## Conteo por subtipo en las 12 hojas
| Subtipo | Localizadores distintos |
|---|---:|
| Lp | 3 |
| L0 | 99 |
| Lx | 1 |
| Ro | 47 |
| Ri | 44 |
| Ls | 12 |
| La | 6 |
| Lz | 30 |
| Ln | 25 |
| Lt | 21 |

Total: 288 localizadores, 571 registros de edición. No se encontraron discrepancias de subtipo entre ediciones para IDs compartidos de esta selección.
191 localizadores (L0/Lx/Ro/Ri) carecen de vínculo explícito a objeto en el subtipo; 97 llevan subtipo editorial referido a elemento ilustrado. Ninguno queda aprobado para evaluación por ese dato. El subtipo no demuestra identidad ni independencia del objeto.

## Decisión de análisis
No entrenar la categoría objetivo tomada de Lp/Ls/La/Lz/Ln/Lt: eso reproduciría la codificación del transcriptor y podría aprender secciones, no una anotación visual independiente.
Mantener las 12 hojas y los 288 localizadores como selección congelada. Añadir elegibilidad por relación real con objeto solo después de adjudicación documentada; no reemplazar exclusiones por otras hojas.
Los 97 son candidatos de revisión, no tamaño muestral efectivo. Las relaciones de objeto compartido y los recortes siguen sin resolver.

## Reproducción del conteo
Sobre inventory.json.gz y pilot-selection-v2.json archivados: reunir folios seleccionados; agrupar records por id; reunir los valores locus de cada grupo y contar conjuntos de subtipos. Se ejecutó localmente con Python y se verificó que todos los conjuntos son de un subtipo. No se usó texto EVA para seleccionar hojas o filtrar el conteo.
Insumos: inventario SHA256 cc4f79d106e21d9e690a6f1e38436761f5770808713c3fef3aaa51ad0f680ce4; selección publicada en 1c39d3a046e35395ced953d6538a5ce50944a3e5.

## Autoauditoría y límites
La clasificación se basa en metadatos y su especificación primaria, con conocimiento del problema encontrado. No es una prueba ciega ni una preinscripción original.
No se destruye o modifica corpus; se restringe una afirmación de elegibilidad. L0/R no se declaran textos sin referente.
No se extrapola a todo el manuscrito ni se estima potencia. Conteos no equivalen a muestras independientes.
Control contable: suma de grupos esperada 288, obtenida 288; sin grupos de subtipos discordantes. No se ejecutó suite global ni CI.
Próxima acción: adjudicar objetos y regiones de los candidatos con subtipo ilustrado, conservando todos los bloqueos y exclusiones.
