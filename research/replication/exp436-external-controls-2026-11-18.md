# EXP-436 — reproducción independiente de controles externos (2026-11-18)

## Método ejecutado
Se descargó mediante la conexión GitHub el **contenido completo** de los archivos de la rama por defecto, se localizó el primer marcador Gutenberg START y el primer END, se conservó el texto entre ambos y se aplicó la expresión regular `[a-zA-Z]+`, pasando a minúsculas y descartando tokens de menos de 2 letras. Se contaron frecuencias por forma exacta; hapax=f1, media=f2–4, frecuente=f5+. Las medias de longitud están ponderadas por ocurrencia. El cálculo se realizó en JavaScript en el entorno de ejecución de herramientas, **no** con el workflow Python ni con CI.

## Resultados calculados
| Métrica | César (latín) | Dante (italiano) |
|---|---:|---:|
| Archivo | `data/reference_corpora/latin/caesar_de_bello_gallico_latin.txt` | `data/reference_corpora/italian/dante_divina_commedia.txt` |
| Blob SHA GitHub | `5c97ce10bcc81960dccd440b7a6fefd97b3d4626` | `97bcdbe34b864bbb2ef4dc31abc39a6005a162c9` |
| Caracteres archivo | 169680 | 601242 |
| Caracteres entre marcadores | 150031 | 581472 |
| Tokens | 20325 | 88249 |
| Tipos | 5674 | 12667 |
| Hapax tokens | 3455 | 7175 |
| Hapax longitud media | 8.6772793054 | 7.2812543554 |
| Intermedios tokens | 3832 | 8780 |
| Intermedios longitud media | 7.8121085595 | 6.3676537585 |
| Frecuentes tokens | 13038 | 72294 |
| Frecuentes longitud media | 4.8485964105 | 3.8210639887 |
| Relación hapax/frecuente | **1.7896476775** | **1.9055567708** |

## Contraste histórico
`experiments/exp_436_latin_hapax_length/result.md` publica 23.274 tokens para César, 92.754 para Dante, relaciones redondeadas 1,79 y 1,92. Los nuevos recuentos **no** coinciden: −2.949 y −4.505 tokens. La relación latina redondea igual (1,79), la italiana es 1,91 frente a 1,92 histórico. NO se considera réplica exacta del resultado antiguo.

## Limitaciones
1. La selección entre marcadores incluye títulos/editoriales internos, notas, posibles errores de codificación y contenido no literario; falta depuración de cuerpo y normalización de caracteres acentuados.
2. El tokenizador ASCII separa caracteres no ASCII, por lo que no es un tokenizador lingüístico óptimo.
3. No se calculó aquí SHA-256 de bytes ni se ejecutó el workflow de GitHub Actions. Las identidades de blob Git permiten fijar las revisiones.
4. Las cifras VMS A/B de 1,42 y 1,33 proceden de informes históricos, **no** de una reproducción contemporánea. No es válido concluir universalidad ni identificar lengua o cifrado a partir de dos controles.
5. No se han calculado incertidumbres, controles aleatorios ni replicación por documento/folio.

## Próximo bloque de investigación
- Ejecutar y verificar CI del nuevo runner Python y guardar su JSON.
- Explicar las diferencias de recuento con el histórico antes de rehabilitar afirmaciones.
- Reproducir VMS A/B sobre transcripción EVA versionada y documentar filtros.
- Añadir control de permutación que preserve frecuencias y longitudes y prueba por folios, evitando interpretar la relación de longitud como desciframiento.

Estado: **CÁLCULO REAL DE CONTROLES EXTERNOS, NO TRADUCCIÓN**.
