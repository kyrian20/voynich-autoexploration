# Protocolo EXP-612 — Dependencia entre bordes de token y control por folio

Fecha: 2026-10-19  
Estado: **protocolo propuesto; no ejecutado**  
Repositorio: `kyrian20/voynich-autoexploration`

## Motivación

El EXP-611 encontró una diferencia descriptiva entre la tasa de vocal siguiente a `ch` y `sh` que persiste al emparejar por longitud exacta, posición del dígrafo y folio. Ese control todavía no separa identidad de plantilla léxica, sección y mano. En paralelo, el preprint de Rozanova y Temerev (arXiv:2608.17096, 17-08-2026) cuestiona que los espacios marcados equivalgan siempre a límites de palabra y propone estudiar unidades recurrentes en los bordes de los tokens. Es una hipótesis publicada, no un resultado que debamos dar por validado.

## Pregunta

¿La asociación entre los símbolos inmediatamente anteriores y posteriores a los espacios de la transcripción excede lo esperable bajo permutaciones que preservan la estructura local del manuscrito?

## Hipótesis registradas

- H1: los pares de símbolos en bordes de token tienen dependencia mayor que la obtenida al permutar tokens dentro de la misma línea.
- H2: el efecto, si existe, se mantiene al analizar por separado ZL3b e IT2a.
- H3: el efecto se reduce al excluir espacios de transcripción incierta, pero no desaparece por completo.

## Datos y unidad

Usar las transcripciones ya versionadas de Zandbergen–Landini ZL3b y la transcripción IT2a presentes en el repositorio. Registrar la ruta exacta, SHA-256, reglas de normalización y número de líneas/tokens antes de calcular resultados. No mezclar cabeceras, notas editoriales ni marcas de folio con el texto.

## Diseño preregistrado

1. Calcular la información mutua observada entre el último grafema del token izquierdo y el primero del token derecho, reportando también frecuencias conjuntas y entropías marginales.
2. Comparar con una distribución nula obtenida permutando el orden de tokens **dentro de cada línea**, sin mover tokens entre folios ni alterar la composición de las líneas.
3. Ejecutar un control adicional permutando líneas dentro del mismo folio, conservando las líneas como bloques.
4. Repetir en ZL3b e IT2a, con espacios dudosos incluidos y excluidos cuando la transcripción permita identificarlos de forma inequívoca.
5. Reportar tamaño del efecto, intervalo por bootstrap de folios, distribución nula, valor p empírico con corrección +1, número de permutaciones y semilla fija.
6. Aplicar corrección de Holm si se prueban múltiples definiciones de borde o subconjuntos. Marcar cualquier análisis añadido después de ver los resultados como exploratorio.

## Criterios de falsación e interpretación

- H1 no recibe apoyo si el valor observado no supera el percentil 95 de la distribución nula preregistrada o si el intervalo del efecto incluye cero.
- La falta de replicación entre transcripciones debilita H2.
- Los resultados solo describirán regularidades de la transcripción; no demostrarán que los espacios sean límites lingüísticos, que los tokens sean palabras, ni que exista un desciframiento.
- No cambiar el protocolo tras inspeccionar los resultados sin documentar una nueva versión.

## Referencia externa

Rozanova, Liudmila; Temerev, Alexander. *A Glyph Is Not a Letter, a Token Is Not a Word, a Space Is Not a Space: What the Units of Voynichese Are Not*. arXiv:2608.17096 (17 de agosto de 2026): https://arxiv.org/abs/2608.17096

## Relación con EXP-611

Este protocolo es una línea distinta y complementaria. No reemplaza ni repite EXP-611. No se han calculado estadísticas ni se afirma ningún resultado para EXP-612 todavía.
