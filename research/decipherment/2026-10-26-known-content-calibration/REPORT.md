# Recuperación exacta en un ejercicio de cifrado conocido

26-10-2026, Madrid. Estado **REPRODUCED**, exclusivamente para esta calibración artificial y sus resultados deterministas. No se evaluó el manuscrito ni se propone una lectura. Sin EXP nuevo ni pretensión de originalidad criptográfica.

## Resultado y decisión

La búsqueda de 312 claves, elegida solo con desarrollo, recuperó las claves generadoras y el 100 % de los tokens reservados en César y Dante para los dos cifrados fijados. La baja ganancia del predictor residual no impidió la recuperación del texto bajo una familia e idioma conocidos. Este ejercicio muestra un límite del instrumento; no establece que Voynich use este código ni que su contenido sea recuperable con él.

| Texto | Tokens reservados | Rotación fija: clave/token exacto | Periódico: clave/token exacto |
|---|---:|---|---|
| César latino | 4115 | periodo 1, offset 13 / 100 % | periodo 7, offset 11 / 100 % |
| Dante italiano | 7925 | periodo 1, offset 13 / 100 % | periodo 7, offset 11 / 100 % |

El baseline que deja el ciphertext sin decodificar acierta 0 % de tokens latinos y 0.5804 % de italianos en ambos cifrados. Todos los caracteres ajenos a ASCII a-z se dejan intactos; no todos los tokens italianos contienen letras cifrables. No se infiere contenido por cercanía estadística: la exactitud se comprueba contra el claro conocido después de fijar la clave.

## Qué sucede con el predictor usado antes

| Texto | Ganancia EL-W claro | Rotación fija | Rotación periódica | UNK claro → periódico |
|---|---:|---:|---:|---:|
| César | 0.028801 | 0.028801 | 0.002053 | 21.56 % → 43.54 % |
| Dante | 0.009633 | 0.009633 | 0.001990 | 15.43 % → 30.83 % |

Bits por transición; vocabulario completo aprendido en entrenamiento. La biyección fija conserva exactamente la ganancia dentro de 1e-10. El cifrado periódico cambia identidades y bordes y fragmenta la reutilización del vocabulario: UNK aproximadamente se duplica. La disminución no se atribuye exclusivamente a una causa, pero este cambio de cobertura explica por qué no es una comparación equivalente de la identidad original. Un descifrador con fase correcta vuelve al texto original exactamente. No se ha ajustado este código para imitar ninguna métrica EVA ni se ha comparado aquí numéricamente con Voynich.

## Control adversarial: inversión no equivale a validación semántica

Al barajar palabras dentro de cada línea antes de cifrar, el mismo selector recupera la clave y el 100 % de las palabras del mensaje barajado en ambos textos. La pérdida de unigramas del claro correcto y barajado es exactamente igual: César 3.9936013466788105 y Dante 4.015938692309724 bits por carácter ASCII. Es una invariancia del criterio al orden de palabras, no una sorpresa lingüística ni un p-valor.

Por tanto, este ejercicio supera la puerta de inversión/recuperación de un código artificial, pero **el criterio de unigramas no es válido para certificar orden lingüístico o significado**. Las palabras barajadas conservan contenido léxico e interior de palabra; no son un control de ausencia absoluta de semántica. No se usarán frecuencias favorables, una clave seleccionada o la etiqueta REPRODUCED como evidencia suficiente de una lectura del manuscrito.

## Método, trazabilidad y comprobaciones

PROTOCOLO fijado antes de ejecutar; fuentes analíticas y agrupaciones V2 conservadas. Frecuencias del claro solo en train, búsqueda de claves solo con ciphertext dev, clave congelada antes de puntuar test. No se pasa al selector la clave verdadera ni el claro dev/test. El investigador conoce la construcción; no hubo cegamiento o revisión independiente. Se reinicia el índice de token en cada línea y se conoce la familia y el idioma: condiciones mucho más fáciles que las de Voynich.

Cinco pruebas de implementación aprobadas: biyección de alfabeto/Unicode, reinicio de línea/periodo, selección sin recibir verdad, invariancia adversarial y rechazo de claves fuera de familia. Se verifican además reversibilidad de todos los registros, disjunción de grupos, invariancia monoalfabética y puertas de recuperación durante cada ejecución. Dos ejecuciones completas con destinos distintos deben coincidir byte a byte; VERIFICATION.json conserva sus hashes. No se ha vuelto a ejecutar la suite global del repositorio ni se certifican todos sus experimentos.

Reproducción desde la raíz del repositorio, Python 3.12:

```sh
python -m unittest discover -s research/decipherment/2026-10-26-known-content-calibration -p 'test_run.py' -v
python research/decipherment/2026-10-26-known-content-calibration/run.py --model-dir research/analysis/2026-10-22-residual-order --output /tmp/known-content-results.json
```

El destino debe ser inexistente. No se distribuyen aquí los textos íntegros: results.json incluye hashes de ciphertext, claro y recuperado; la entrada exacta y ambos módulos V2 ya están archivados. run-01.log/run-02.log conservan las puertas observadas. El código produce estado REPRODUCED cuando pasan las puertas; para el paquete archivado este estado se respalda además en la comparación externa de las dos ejecuciones, no solo en esa etiqueta del script.

Antecedentes cotejados: batería común BC-2026-10-22, EXP-177, V2 residual, soporte efectivo y sensibilidad de cantidades iguales. La KB externa histórica no existe en este entorno; no se afirma búsqueda bibliográfica exhaustiva ni novedad. La crítica de la respuesta Gemini v2 se conserva como antecedente metodológico, sin nueva llamada API ni revisión de este paquete por Gemini.

## Autoauditoría — skills/audit_experiment.md

**Conciencia del objetivo:** cifrados y claves se escogieron para una prueba artificial acotada, sin calibrarlos a estadísticas Voynich. La pregunta surge después de los resultados residuales y no es confirmatoria. Conocer familia, idioma, reinicios y claro train concede información fuerte; la recuperación es condicional a ella.

**Destrucción de características:** el periódico fragmenta identidades de tokens y altera bordes, suprimiendo reutilización para el predictor de identidad no consciente de la fase. Por ello sería injusto usar su baja ganancia para excluir contenido recuperable. La variante mono conserva estas igualdades y sirve de control. Decodificar con la fase recuperada preserva el texto exacto; no se supone que esa fase exista en Voynich.

**Extrapolación:** solo dos textos, dos claves, periodos 1..12 y 26 offsets, letras ASCII y partición heredada. No es estimación de tasa general de éxito, modelo de cifrado medieval, recuperación con idioma desconocido ni algoritmo general de desciframiento. No se optimizaron variantes después de ver la evaluación.

**Alcance negativo:** el selector de unigramas no discrimina orden de palabras porque agrega sus caracteres; la prueba adversarial lo verifica. El predictor residual pierde señal bajo este código periódico particular. Ninguno de estos límites demuestra ausencia de lengua en un corpus ni imposibilidad de otro método.

**Comportamiento de controles:** se esperaba 100 % de recuperación en positivos; observado 100 % en cuatro brazos. Se esperaba invariancia de ganancia monoalfabética dentro de 1e-10; observada igualdad numérica. Se esperaba igualdad de pérdida de claros ordenado/barajado; observada igualdad exacta. El adversarial también alcanza 100 % de recuperación, explicado por la misma reversibilidad y conservación de frecuencias: esto bloquea interpretar el criterio de claves como validador semántico. No se compara un control superior a Voynich ni se calcula significación.

## Siguiente decisión acotada

Conservar este paquete como control de integración y cerrar esta familia didáctica; no ampliar periodos o claves para acumular éxitos. Antes de una lectura candidata del manuscrito, exigir una prueba de reglas y contenido adicional que rechace alternativas adversariales, con alfabeto/idioma/segmentación no conocidos por adelantado y exposición de datos declarada. Ese diseño aún no está implementado; no se promete recuperación del manuscrito por superar esta calibración.
