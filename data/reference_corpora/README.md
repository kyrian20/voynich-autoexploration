# Corpus de comparación — identidad revisada el 22-10-2026

Los nombres heredados de varios archivos no describen su contenido real. Se conservan los bytes y las rutas para no romper procedencia ni ocultar resultados históricos. El manifiesto de hashes verifica integridad; no certifica idioma ni representatividad.

| Archivo | Identidad observada | Uso y estado |
|---|---|---|
| `latin/caesar_de_bello_gallico_latin.txt` | César, *De Bello Gallico* I–IV, latín, Gutenberg #218 | Control latino del bloque de orden residual, con selección de cuerpo explícita |
| `italian/dante_divina_commedia.txt` | Dante, *Divina Commedia*, italiano, #1012 | Control italiano del mismo bloque; poesía, no prosa |
| `latin/virgil_aeneid_latin.txt` | *The Aeneid*, cabecera Language: Latin | Identidad según cabecera; no se declara aquí su adjudicación completa |
| `german/goethe_faust.txt` | *Faust*, cabecera Language: German | Misma limitación de adjudicación |
| `latin/vulgate.txt` | Biblia Douay-Rheims, **inglés**, #8300 | No usar como latín |
| `latin/caesar_gallic_wars.txt` | César en traducción **inglesa**, #10657 | No usar como latín |
| `latin/cicero_de_officiis_latin.txt` | Cicerón, **latín e inglés alternados**, #47001 | Requiere revisar el extractor antes de tratar su salida como monolingüe |
| `arabic/quran_arabic.txt` | Whitman, *Drum-Taps*, **inglés**, #8801 | No es Corán ni control árabe |
| `english/kjv_bible.txt` | *Book of Mormon*, inglés, #17 | No describir como KJV; pertinencia del género pendiente |
| `latin/cicero_caesar_latin.txt` | Vacío | `BLOCKED_EMPTY_DO_NOT_USE` |

Revisión canónica de identidad: [CORPUS_IDENTITY_REVIEW.json](../../research/CORPUS_IDENTITY_REVIEW.json). Evidencia y alcance: [incidencias](../../research/analysis/2026-10-22-residual-order/CORPUS_INCIDENTS.md) y [fuentes primarias](../../research/analysis/2026-10-22-residual-order/SOURCES.md).

El inventario localiza 103 scripts con referencias literales a Cicerón o al archivo llamado Vulgata. Esto no demuestra 103 ejecuciones ni 103 resultados inválidos. Algunos extractores de Cicerón aplican filtros de inglés que requieren revisión específica. Los resultados históricos no se recalculan ni se invalidan masivamente por este inventario.

## Reproducción integrada

El bloque de [orden residual](../../research/analysis/2026-10-22-residual-order/README.md) verifica hashes, rechaza el uso de corpus con incidencias no adjudicadas en sus nuevas comparaciones, regenera las entradas desde `data/` y reproduce modelos y controles. No añade copias crudas de estos textos.

No hay todavía un control árabe o hebreo aprobado por esta revisión. La exclusión de un archivo mal identificado no equivale a excluir una lengua como posible explicación del manuscrito.
