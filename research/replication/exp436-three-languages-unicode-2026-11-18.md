# EXP-436 — comparación Unicode de tres corpus (2026-11-18)

## Ejecución independiente
Se recuperó el contenido íntegro de tres archivos de GitHub mediante `fetch_file` y se calculó en JavaScript sobre el cuerpo entre marcadores Gutenberg START/END. Tokenización: secuencias de letras Unicode `/\\p{L}+/gu`, minúsculas, longitud mínima de 2 caracteres, clases por frecuencia de token: hapax=1, intermedio=2–4, frecuente>=5. Medias ponderadas por tokens. **Este cálculo no es una ejecución del workflow Python.**

| Control | Blob Git | Tokens | Tipos | Hapax tokens | Hapax media | Intermedios tokens | Intermedios media | Frecuentes tokens | Frecuentes media | Ratio |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Latín César | `5c97ce10bcc81960dccd440b7a6fefd97b3d4626` | 20325 | 5674 | 3455 | 8.6772793054 | 3832 | 7.8131524008 | 13038 | 4.8485964105 | 1.7896476775 |
| Italiano Dante | `97bcdbe34b864bbb2ef4dc31abc39a6005a162c9` | 89812 | 12870 | 7360 | 7.3599184783 | 8816 | 6.4429446461 | 73636 | 3.8258053126 | 1.9237566674 |
| Alemán Goethe | `8dd368bf62509bb8b49cb6c03e0a0116682617f2` | 30683 | 6213 | 3909 | 8.0365822461 | 3749 | 6.4515870899 | 23025 | 3.9986102063 | 2.0098438786 |

El código Python de `research/replication/replicate_exp436.py` se actualizó para incorporar Goethe y un tokenizador Unicode, con prueba adicional de letras alemanas e italianas. **Su ejecución y CI siguen pendientes de verificación**.

## Interpretación
Los tres controles exhiben gradiente hapax/frecuente >1. La relación alemana es mayor en esta muestra, pero los corpus no están emparejados por época, género ni tamaño. Los valores VMS A/B históricos siguen sin reproducción independiente. No es prueba de universalidad, parentesco lingüístico, idioma alemán ni traducción.

## Próximos experimentos de mayor valor
1. Verificar salida CI del runner Python y comparar con estas cifras JavaScript.
2. Medir estabilidad mediante remuestreo de bloques textuales de igual longitud y controles de mezcla.
3. Reproducir Voynich A/B a partir de transcripción EVA fijada y etiquetado Currier auditable.
4. Contrastar modelos nulos de longitud/frecuencia y obtener intervalos de confianza antes de proponer mecanismos.
