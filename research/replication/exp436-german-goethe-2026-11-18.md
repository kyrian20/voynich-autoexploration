# EXP-436 — control alemán Goethe, cálculo independiente (2026-11-18)

Archivo: `data/reference_corpora/german/goethe_faust.txt`, blob Git `8dd368bf62509bb8b49cb6c03e0a0116682617f2`. Cabecera: Project Gutenberg #2229, `Faust: Der Tragödie erster Teil`, idioma German.

Método idéntico al cálculo independiente de latín e italiano de 2026-11-18: contenido entre START y END de Gutenberg, tokens `[a-zA-Z]+` de longitud >=2, minúsculas, frecuencia por tipo, medias ponderadas por ocurrencias.

| Métrica | Alemán Goethe |
|---|---:|
| Tokens | 31495 |
| Tipos | 5854 |
| Hapax tokens | 3539 |
| Hapax longitud media | 7.7293020627 |
| Intermedios (f=2–4) tokens | 3652 |
| Intermedios longitud media | 6.0837897043 |
| Frecuentes (f>=5) tokens | 24304 |
| Frecuentes longitud media | 3.8592001317 |
| Relación hapax/frecuente | **2.0028248857** |

Comparación externa con el mismo procedimiento: César latín 1.7896476775; Dante italiano 1.9055567708. Las relaciones históricas VMS A 1.42 y B 1.33 no están reproducidas aquí.

**Advertencia metodológica crítica:** el tokenizador ASCII divide palabras alemanas con ä, ö, ü, ß y otros caracteres no ASCII; la magnitud 2.003 es provisional y no debe atribuirse al alemán general. Además, Goethe es teatro poético, César prosa histórica y Dante poesía, con corpus de distinta longitud y época. Se requiere tokenización Unicode, extracción depurada y controles de género y tamaño antes de inferir diferencias lingüísticas.

Cálculo efectuado en herramienta JavaScript a partir del archivo completo leído por conexión GitHub; NO ejecutado en GitHub Actions. No hay traducción ni inferencia sobre lengua de Voynich.
