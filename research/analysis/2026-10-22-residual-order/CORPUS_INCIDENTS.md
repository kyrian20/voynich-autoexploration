# Incidencias de identidad de corpus — revisión pública integrada

Fecha: 22-10-2026. Fuente: b566b6fa461f3a4e6fd8bb3a1aaa6e71f035f190. Originales conservados sin modificación.

| Ruta bajo data/reference_corpora | Identidad observada | Decisión para nuevos análisis |
|---|---|---|
| latin/vulgate.txt | Biblia Douay-Rheims, inglés, Gutenberg #8300 | No usar como latín |
| latin/caesar_gallic_wars.txt | César en traducción inglesa, #10657 | No usar como latín |
| latin/cicero_de_officiis_latin.txt | Cicerón, latín e inglés alternados, #47001 | No usar como monolingüe sin auditar extracción |
| arabic/quran_arabic.txt | Drum-Taps, Walt Whitman, inglés, #8801 | No usar como árabe ni Corán |
| english/kjv_bible.txt | Book of Mormon, inglés, #17 | No llamar Biblia KJV; evaluar pertinencia del género |
| latin/cicero_caesar_latin.txt | Vacío | Bloqueado |

Las cabeceras de los ficheros, sus SHA-256 y las referencias estáticas están en reference_identity_audit.json. Se contrastaron con el catálogo original de Project Gutenberg: https://www.gutenberg.org/ebooks/8300 , /10657 , /47001 , /8801 y /17. No se utilizan sus resúmenes automáticos para adjudicar idioma: se comprueba la ficha bibliográfica y Language.

## Alcance histórico

Se detectan 103 archivos Python con referencias literales directas: 100 mencionan el Cicerón bilingüe y tres la supuesta Vulgata latina. No son necesariamente 103 experimentos ejecutados ni 103 resultados inválidos. La auditoría no resuelve dependencias transitivas, aliases o rutas construidas dinámicamente.

Siete de las cien referencias a Cicerón mencionan un filtro de stopwords inglesas. Por ejemplo, EXP-180 selecciona párrafos con una proporción de esas palabras inferior a 0,08. Ese filtro debe comprobarse sobre segmentos adjudicados; no se afirma que todo el texto bilingüe se utilizara sin limpiar. Tampoco se certifica su salida como latín puro. Otras referencias pueden ser opcionales o no ejecutadas.

El siguiente saneamiento histórico requiere para cada experimento: cargar su función exacta sin ejecutar simulaciones a ciegas, registrar segmentos elegidos, medir contaminación y luego evaluar qué afirmaciones dependían del idioma/obra. Ningún resultado numérico histórico se sustituye silenciosamente. Las afirmaciones que identifiquen una lengua basándose en estos nombres no se admiten para nuevos avances hasta esa revisión.

Esto es una incidencia de identidad/procedencia, distinta de integridad por hash: un archivo mal identificado puede conservar perfectamente sus bytes. La guardia anterior de hashes no certificaba idioma y su documentación ya limitaba ese alcance.

## Entradas aprobadas SOLO para este contraste

- latin/caesar_de_bello_gallico_latin.txt: catálogo #218, idioma Latin, texto desde el encabezamiento latino del libro I hasta antes del colofón. Se conserva el archivo íntegro con sus avisos; la vista analítica se prepara aparte.
- italian/dante_divina_commedia.txt: catálogo #1012, idioma Italian, desde Nel mezzo hasta antes del marcador final. Poesía italiana, sin presentarla como prosa ni como equivalente del manuscrito.

La aprobación aquí es para esta selección y estos usos. No declara completamente adjudicados todos los textos ni su representatividad de un idioma histórico.
