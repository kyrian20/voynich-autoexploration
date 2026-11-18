# EXP-436 — comprobación directa de rutas e identidad (2026-11-18)

## Archivos inspeccionados en master
| Ruta | Blob SHA GitHub | Cabecera observada | Estado |
|---|---|---|---|
| `data/reference_corpora/latin/caesar_de_bello_gallico_latin.txt` | `5c97ce10bcc81960dccd440b7a6fefd97b3d4626` | Project Gutenberg #218; «Cæsar's Commentaries, Books I-IV»; Language: Latin | Existe; identidad declarada latina; falta auditar cuerpo, recorte y bytes completos |
| `data/reference_corpora/latin/caesar_gallic_wars.txt` | `56d5a3ddbce30c20541ed9f2d1356d85c33004fc` | Project Gutenberg #10657; «De Bello Gallico and Other Commentaries»; Language: English; Translator: W. A. McDevitte | Existe; traducción inglesa |
| `data/reference_corpora/italian/dante_divine_comedy_italian.txt` | — | GitHub contents: 404 | No existe en master |
| `data/reference_corpora/italian/dante_divina_commedia.txt` | `97bcdbe34b864bbb2ef4dc31abc39a6005a162c9` | Project Gutenberg #1012; «La Divina Commedia di Dante»; Language: Italian | Existe; identidad declarada italiana; falta auditar cuerpo y recorte |

La cabecera de un archivo no acredita por sí sola que todo el cuerpo sea monolingüe. Los SHA aquí son hashes de blob Git, NO SHA-256 de contenido; no confundirlos.

## Código y resultado histórico
- `experiments/exp_436_latin_hapax_length/script.py` en master usa `caesar_de_bello_gallico_latin.txt` y busca la ruta italiana inexistente, protegida por `os.path.exists`.
- `experiments/exp_436_latin_hapax_length/result.md` afirma 23.274 tokens latinos y 92.754 italianos; relaciones hapax/frecuente de 1,79× y 1,92× respectivamente. No se han reproducido.
- La errata `CORRECTION.md` atribuye el control latino a `caesar_gallic_wars.txt`, distinta de la ruta del script actual. La identidad exacta de los datos que produjeron los números históricos sigue SIN RESOLVER.
- No inferir que el archivo italiano inexistente jamás existió en otra revisión; solo está ausente de master en esta comprobación.

## Decisión
Q022 continúa ABIERTA. No editar `result.md`, no rehabilitar sus conclusiones, no asignar idioma al Voynich y no generar nuevas estadísticas sin reproducir primero el recorte y la procedencia de los archivos.

## Próxima comprobación
1. Inspeccionar historial Git de `script.py`, `result.md`, `CORRECTION.md` y los cuatro corpus.
2. Auditar cuerpo completo, SHA-256, limpieza de encabezados y recuentos de tokens de los archivos latino e italiano presentes.
3. Ejecutar reproducción en checkout fijado, registrando stdout, versión de Python y hashes.
4. Comparar contra los 23.274 y 92.754 tokens históricos; cualquier divergencia debe conservarse, no ajustarse retrospectivamente.

Esta es una auditoría documental; no constituye experimento estadístico ni traducción.
