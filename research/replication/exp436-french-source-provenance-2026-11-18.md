# EXP-436: cuarto control francés — incorporación (2026-11-18)

**Fuente seleccionada:** Voltaire, *Candide, ou l'optimisme*, Project Gutenberg ebook #4650, `https://www.gutenberg.org/ebooks/4650`, catalogado explícitamente como **Language: French**. No confundir con Gutenberg #19942, una edición **inglesa**. Publicación original: 1759 (muy posterior a la datación habitual del Voynich).

**Código implementado:**
- `research/replication/fetch_french_candide.py`: descarga #4650 en UTF-8 desde dos rutas oficiales alternativas; exige cabecera `Language: French`, delimitadores START/END y tamaño plausible; registra bytes y SHA-256; falla si no verifica.
- `research/replication/replicate_exp436.py`: incluye `french` junto a `latin`, `italian`, `german`, con el mismo tokenizador Unicode y clases por frecuencia.
- `.github/workflows/exp436-replication.yml`: descarga el corpus francés validado antes de generar el JSON de los cuatro controles.

**Estado de resultados:** El archivo francés todavía no se ha descargado ni procesado satisfactoriamente en esta sesión; no hay cifra francesa verificada. No afirmar que CI pasó hasta inspeccionar su ejecución y el artefacto. El runner falla explícitamente si la fuente no existe o no supera controles, en vez de inventar datos.

**Limitaciones:** Edición de siglo XVIII, no comparable históricamente sin controles; las ediciones de Gutenberg pueden contener prólogos, notas y paratextos entre marcadores, y las elisiones francesas (l', d') se separan por tokenización. Futuro: comparar corpus de francés medieval/medio, segmentación con y sin clíticos, y remuestreo de tamaños igualados.

**Siguiente acción:** inspeccionar ejecución de GitHub Actions, recuperar JSON y SHA-256, registrar recuentos franceses y comparar incertidumbre.