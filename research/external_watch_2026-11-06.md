# Actualización de evidencia externa — Voynich — 2026-11-06

## Fuente nueva consultada

Xin Zhang y Victor S. Sheng, *Can Statistics Tell Whether an Undeciphered Text Is Language? Calibrated Tests on the Voynich Manuscript*, arXiv:2610.34499v2, revisado el 2026-11-04: https://arxiv.org/abs/2610.34499

Es un preprint, no una traducción ni un resultado validado por nuestro proyecto. La versión v2 mantiene el análisis de recurrencia de pares de palabras entre líneas y añade una discusión más detallada de pruebas de descifrado calibradas con controles. Los autores informan 0,071 para ZL3b y 0,053 para IT2a, frente a 0,139–0,411 en sus 28 pasajes de control natural. Informan además que varias familias de cifrado no superan sus pruebas calibradas; un nomenclátor de dos claves sigue sin excluirse bajo algunos parámetros extremos y en árabe o hebreo. Son resultados de los autores, no reproducidos aquí.

## Discrepancia metodológica concreta con nuestra auditoría

Nuestra auditoría parcial del 2026-11-01, `research/maintenance/2026-11-01-zs-wordpair-audit/REPORT.md`, operacionalizó la exclusión de casi-copias como distancia Levenshtein de hasta un glifo, contando sustitución, inserción o borrado. En la versión v2, sección 5.1, la regla descrita es excluir pares que se vuelven iguales al quitar un glifo de cada forma. Esa regla no es equivalente: la versión de nuestra auditoría puede excluir pares de longitudes distintas por una sola inserción o borrado, mientras que la descripción v2 exige que ambas formas puedan reducirse al mismo tipo quitando un glifo de cada una.

Por esta diferencia, las cifras de nuestra auditoría del 1 de noviembre **no son una reproducción fiel de la métrica v2**. Se conservan como resultado de una operacionalización exploratoria concreta; no se sobrescriben. La discrepancia de valores no demuestra un error del artículo ni una propiedad del manuscrito.

## Próximo paso acotado

Cuando se reanude este subanálisis, recalcular la métrica con la regla literal de v2 sobre las mismas entradas congeladas, hashes, páginas comunes, selección de tipos, semillas y particiones ya registradas. Comparar ambas reglas en paralelo y conservar el resultado antiguo. Antes de interpretar cualquier cifra, revisar también el código cuando los autores lo publiquen: el apéndice v2 agradece a Igor E. Golub una réplica independiente y una corrección de la descripción inicial de la exclusión de casi-copias; el código y las reglas de decisión se anuncian para la versión publicada. No asignar EXP nuevo ni tratar el recálculo como prueba de idioma o significado.

## Alcance

Esta revisión identifica un desajuste entre una regla publicada y la regla de nuestra auditoría. No ejecuta de nuevo el análisis, no reproduce los controles multilingües ni cambia el estado de ninguna hipótesis semántica. La separación por bloques de diez páginas de la auditoría anterior también compartía cuatro hojas físicas; por tanto, sus mitades no deben describirse como validación por hoja independiente.
