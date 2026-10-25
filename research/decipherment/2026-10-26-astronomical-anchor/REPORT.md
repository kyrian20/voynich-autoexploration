# Ancla astronómica f68r3: forma documentada, significado sin establecer

26-10-2026, Madrid. Estado **BLOCKED** para utilizar este candidato como texto plano conocido o ejecutar una validación semántica. El inventario léxico limitado se reprodujo byte a byte. No se ajustó una clave ni se afirmó una traducción.

## Qué se comprobó

Se recuperó e inspeccionó la imagen original completa Yale1006196, canvas68r,7993×3828, y una región IIIF de coordenadas5050,1050,800,550. La ubicación del texto a la derecha del pequeño grupo de estrellas es compatible con el locus f68r3.11,@Ls de los archivos consultados. Hay otro texto junto a la línea curva: no se transfiere la propuesta entre ambos. Los tres paneles comparten imagen y hoja física; no son tres muestras independientes.

Las dos transcripciones actuales coinciden en la secuencia literal doaro en ese locus: ZL3b línea3179 e IT2a línea1994. El registro histórico Stolfi1998 muestra doary en f68r3.X.1. Esta diferencia se conserva como diferencia entre versiones/lecturas; el acuerdo de dos ediciones no es adjudicación paleográfica independiente ni prueba de cuál signo es correcto. La inspección asistida de la imagen tampoco sustituye esa adjudicación.

| Forma exacta | ZL3b split/join | IT2a split/join | Uso permitido |
|---|---:|---:|---|
| doaro | 1/1 | 1/1 | Única ocurrencia en f68r3.11 bajo estas vistas |
| doary | 0/0 | 0/0 | Forma histórica, no localizada aquí con esa grafía exacta |
| dary | 23/23 | 24/24 | Forma distinta; sus repeticiones no validan doaro/doary |

Se examinaron5385 registros numéricos ZL3b y5215 IT2a, con lexer canónico, alternativas primarias, ligaduras expandidas y dos políticas de coma. No apareció ningún renglón no analizado que contuviera literalmente estas cadenas. No es una enumeración de todas las combinaciones editoriales ni garantía completa de IVTFF. Las dos transcripciones describen el mismo manuscrito.

## Contraste con la propuesta publicada

Bax2014 pp19–21 propone una interpretación relacionada con Taurus y una lectura aproximada terminada en n, presentada como especulativa en esa discusión. Su tabla de p56 asigna valores diferentes a EVAo e EVAy. Se consultó la extracción de pp19–21 y se inspeccionaron las representaciones de p20 y p56. Por tanto, no se puede trasladar sin revisión una conclusión que depende de finaly/n a un archivo que termina en o. No se infiere aquí otra pronunciación ni se refuta la propuesta completa.

La descripción de Zandbergen del grupo registra como identificación tentativa las Pléyades y como alternativa los siete planetas; también distingue el rótulo del grupo y el de la conexión con la luna. Esta fuente orienta rivales, no establece una palabra conocida. Nuestra imagen permite examinar la disposición gráfica, pero no fija por sí sola el nombre Tauro, el idioma o una forma histórica.

Un comparador nombrado citado por Bax, accession19.68.1 del Met, no se recuperó con identificación oficial resuelta en esta continuación: la URL histórica falló y una consulta API no aportó el registro. Una página consultada por un identificador de colección distinto correspondía a un chal y se descartó. No se incorpora como comparación astronómica ni se presume que una fuente externa confirme el rótulo Voynich.

## Puerta de admisión

| Requisito | Evidencia actual | Estado |
|---|---|---|
| Localización del locus | Fuente cruda e imagen compatibles | Documentado, con alcance de inspección asistida |
| Transcripción independiente | Ediciones doaro frente a forma histórica doary | Pendiente |
| Referente/nombre sin usar la clave | Varias interpretaciones del grupo | No establecido |
| Idioma y forma histórica del nombre | No identificados de forma independiente | Pendiente |
| Regla completa congelada | No aportada para este test | Pendiente |
| Predicción fuera del origen | doaro no se repite; no hay otro nombre independiente establecido | No disponible |

La evidencia nueva **no convierte el candidato en ancla**. Tampoco demuestra que no pueda ser Tauro, que las Pléyades sean incorrectas o que ninguna otra ancla sea posible. Los candidatos f2r/f41v/f65r siguen con los límites documentados el22oct; esta revisión no los revalida ni los somete otra vez al mismo ajuste.

## Prueba concreta preparada y por qué no se ejecuta todavía

TRANSFER_TEST.md especifica hipótesis rivales, información que tendría que fijarse sin la clave, separación de datos, predicciones en posiciones donde las reglas difieran y abstención ante no identificabilidad. La transferencia de la misma palabra no es ejecutable: en estas vistas solo hay una doaro y ninguna doary. No se sustituye por una forma parecida para crear una segunda muestra.

Una prueba entre reglas de signos requiere al menos nombres adicionales identificados por una vía independiente y dos reglas completas que hagan predicciones distintas. Ninguna de esas entradas está establecida en este paquete. Inventar referentes, sonidos o un tamaño muestral «suficiente» convertiría el ejercicio en ajuste retrospectivo. No se presentará el diseño condicional como una prueba semántica ya ejecutada o preregistro estadístico completo.

## Trazabilidad y reproducción

image-source.json fija imagen, canvas, dimensiones y hashes; sources.json fija bibliografía, páginas y límites de acceso. No se redistribuyen las imágenes en GitHub: los originales se recuperan desde las URLs del proveedor. inventory.json conserva todas las coincidencias, cuerpos, posiciones y líneas, incluido el locus objetivo y sus cinco signos tal como están en cada archivo. VERIFICATION.json conserva hashes y comprobación de las dos ejecuciones idénticas.

Desde la raíz del repositorio con Python3.12:

```sh
ANCHOR_REPO_ROOT=. python -m unittest discover -s research/decipherment/2026-10-26-astronomical-anchor -p 'test_run.py' -v
python research/decipherment/2026-10-26-astronomical-anchor/run.py --repo-root . --output /tmp/astronomical-anchor-new.json
```

El destino debe ser inexistente. Cinco pruebas específicas pasan: coincidencia exacta/no substrings, alternativas y coma, exclusión no numérica visible, duplicados rechazados y preservación de posiciones de signos. No se volvió a ejecutar la suite global localmente. No hay prueba botánica/astronómica de experto, revisión independiente de la lectura, nueva respuesta Gemini ni evaluación semántica sobre material reservado.

## Autoauditoría — skills/audit_experiment.md

**Conciencia del objetivo:** se eligió una propuesta conocida y se observaron los dos registros antes de escribir el inventario. Es diagnóstico exploratorio; no una prueba ciega ni descubrimiento de una palabra. No se elige idioma o valor fonético por encaje.

**Destrucción de características:** las vistas usan alternativas primarias y pueden omitir otras lecturas; por ello los ceros son condicionales. No se borran signos ni se equiparan doaro/doary/dary. La hipótesis visual no se refuta por una ausencia léxica bajo estas proyecciones.

**Extrapolación:** una posible ancla astronómica y tres formas exactas en dos ediciones relacionadas. No se concluye que todos los nombres sean ilegibles, que las siete estrellas tengan necesariamente un referente particular o que una clave sea imposible.

**Alcance negativo:** BLOCKED significa falta de entradas independientes para usar esta propuesta como texto conocido. La ausencia de repetición limita una prueba concreta de transferencia, no todas las comprobaciones de signos o hipótesis de lengua.

**Controles:** se esperaba conservar las diferencias de formas y evitar substrings; cinco pruebas lo comprueban. El inventario encuentra una doaro por edición, cero doary y23/24dary, sin líneas no analizadas que contengan las cadenas. No existe distribución nula de significados ni valor esperado de frecuencia semántica; no se fabrica una significación. Los conteos no adjudican la imagen.

## Decisión

No usar «Taurus» como palabra conocida para aprender ni validar una clave. Conservar la discrepancia de transcripción y los rivales como requisitos explícitos de revisión. La siguiente acción de contenido requiere una transcripción y una identificación independientes, o un paralelo documental que aporte nombres sin usar la clave candidata. No se simulará ese papel con una nueva conjetura de IA ni se contactará a investigadores sin autorización para hacerlo.
