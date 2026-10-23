# Batería común lenguaje, cifrado y generación — informe en español

**Estado: NEGATIVE**, referido a la capacidad discriminante de la batería primaria. Ejecución completa; no VALIDATED como conclusión sobre origen del manuscrito. Identidad inequívoca: `experiments/common_battery_2026_10_22`, BC-2026-10-22.

## Resultado e interpretación

El perfil primario acepta 16/16 permutaciones de tokens Voynich. Las cuatro métricas no bastan para discriminar el orden del texto bajo estas condiciones. Naibbe latino entra en las tolerancias en 16/16 semillas; italiano e inglés en 15/16. Esto muestra cercanía descriptiva condicionada a unidades y tolerancias, no evidencia de que el manuscrito sea un cifrado Naibbe. La copia propia no alcanza cercanía conjunta; no se descartan Timm/Schinner ni generadores fuera de estas dos implementaciones.

La unidad primaria H2 mide caracteres dentro de palabra: una permutación de palabras la conserva exactamente, al igual que la longitud media. Dos de cuatro componentes son invariantes al control adversarial. La coincidencia de iniciales agrega clases y puede ocultar dependencias particulares. Por eso el control pasa la batería aun cuando colapsa am/y: es un límite de sensibilidad conocido por el resultado; no se cambia la primaria para obtener discriminación.

## Ejecución y trazabilidad

Protocolo escrito y comprometido en `57bf6be`, implementación previa en `cb25ade`; precisión de líneas `2fff97d`. Run-01 falló por ISO-8859-1 declarado en César; run-02 por presupuesto fuente superior al disponible. Ambos conservan selección y error. Correcciones técnicas/budget fuente en `8de8ae5` y `92bb830`, antes de generar simulaciones. No hubo métricas científicas descartadas en esos fallos. Las revisiones del protocolo son visibles en commits y los originales históricos permanecen intactos.

Comando ejecutado: `python experiments/common_battery_2026_10_22/script.py --out experiments/common_battery_2026_10_22/data/run-03`. Python 3.12.14, pandas 2.2.3. Parámetros, 16 semillas, límites, métrica, tolerancias y puertas están en PROTOCOL.md; hashes previos en freeze.json e implementation-freeze.json. SHA256.json fija todas las salidas y resultados.json fija código/protocolo y el contenido descomprimido del archivo de tokens.

201 evaluaciones, 21 brazos. Hay 3.999 tokens train y 2488 test en el esqueleto principal. El test solo contiene 5 hojas físicas: f39, f80, f81, f82, f85. El hash de partición usa el entero SHA-256 completo; otros análisis del proyecto usaron prefijos, por lo que no se presume identidad entre splits. La primera selección por orden y presupuesto limita representatividad por sección. No hay fuga entre lados/paneles de una hoja; los textos y criterios generales estaban previamente expuestos. No es confirmación sobre datos intactos.

La sensibilidad de líneas originales usa bloques fuente de al menos 8.000 tokens por partición; Naibbe produce más tokens por cambio de unidad. Su D es descriptiva y no una comparación de tamaño igualado. El inglés conserva front matter dentro del marcador START: control de identidad del archivo original, no reproducción literal del lector ni de la segmentación histórica.

## Tabla principal

| Brazo | n | Cercanía conjunta | D mediana | Ganancia caracteres bits/transición | am LL mediana | y LF mediana |
|---|---:|---:|---:|---:|---:|---:|
| VMS_IT2a_split | 1 | 1 | 0.0047 | 1.7808 | 6.9169 | 3.0497 |
| VMS_ZL3b | 1 | 1 | 0.0000 | 1.8118 | 7.0127 | 2.8946 |
| VMS_ZL3b_join | 1 | 1 | 0.0336 | 1.8035 | 6.5618 | 3.0137 |
| VMS_permutado | 16 | 16 | 0.0546 | 1.8118 | 0.9147 | 1.2736 |
| generador_caracter | 16 | 0 | 9.8642 | 0.4407 | 0.7329 | 0.7992 |
| generador_iid | 16 | 0 | 24.4128 | -0.0244 | 0.0000 | 0.9037 |
| generador_preserva | 16 | 0 | 5.2203 | 1.5715 | 0.9896 | 1.0129 |
| lenguaje_ingles_historico | 1 | 0 | 7.4941 | 0.8497 | 1.1155 | 2.6679 |
| lenguaje_italiano | 1 | 0 | 8.8856 | 0.7940 | 0.0000 | NA (sin soporte) |
| lenguaje_latin | 1 | 0 | 10.5128 | 0.7291 | 0.9147 | NA (sin soporte) |
| lenguaje_original_ingles_historico | 1 | 0 | 8.6437 | 0.8938 | 1.0020 | 0.7250 |
| lenguaje_original_italiano | 1 | 0 | 9.4471 | 0.7989 | 0.0000 | NA (sin soporte) |
| lenguaje_original_latin | 1 | 0 | 10.8842 | 0.7201 | 0.9128 | NA (sin soporte) |
| naibbe_ingles_historico | 16 | 15 | 0.3411 | 1.7134 | 1.0372 | 0.8918 |
| naibbe_italiano | 16 | 15 | 0.4038 | 1.7225 | 0.7785 | 1.0868 |
| naibbe_latin | 16 | 16 | 0.3755 | 1.7187 | 0.8669 | 0.9860 |
| naibbe_original_ingles_historico | 16 | 16 | 0.3436 | 1.7368 | 0.7130 | 1.4982 |
| naibbe_original_italiano | 16 | 16 | 0.3788 | 1.7207 | 1.1218 | 0.7455 |
| naibbe_original_latin | 16 | 16 | 0.3457 | 1.7243 | 0.8178 | 0.9204 |
| permutado_IT2a_split | 16 | 16 | 0.0716 | 1.7808 | 0.9022 | 1.0166 |
| permutado_ZL3b_join | 16 | 16 | 0.0762 | 1.8035 | 0.9985 | 1.0849 |

Todos los valores individuales y percentiles P2,5–P97,5 están en resultados.json. Los percentiles entre semillas describen variación de simulación, no incertidumbre de todos los mecanismos. Los bootstrap usan 400 remuestreos por hoja física, semilla 17099. Para am LL: [3.8242677824267783, 9.335689045936395]; para y LF: [2.157187536198309, 3.8626685049019605]. Cinco hojas producen intervalos inestables: no se usan como confirmación de C005/C006 ni para corregir las cifras históricas.

## Resolución de las limitaciones EXP-170

| Limitación | Resolución para este estudio | Límite histórico conservado |
|---|---|---|
| Archivo llamado Vulgata es inglés | César #218 latín, Dante #1012 italiano, y brazo inglés explícito; selección y hashes de vistas | Los brazos Lat-A/B históricos son INVALID_FOR_CLAIM sobre latín; no se reescriben |
| Identidad italiana externa no recuperada | Se usa Dante local de identidad documentada, declarado distinto del ejemplo histórico | No se finge identidad del texto italiano externo |
| Dependencia Naibbe ausente | Código y CSV exactos del commit 719f2f4c, licencia y cita preservados | No consta versión histórica exacta; comparación nueva |
| Currier por edy/número de folio | Lector existente por $L=B, P0 y hoja física; selección cruda archivada | No se migran ni sustituyen baselines históricos |
| Parser/tokenización | Proyección lossless y sensibilidad coma join e IT2a | No se afirma resolver toda la norma IVTFF ni todos los desacuerdos antiguos |
| Simulaciones sin secuencias | tokens.jsonl.gz: cada brazo/semilla/train/test, hashes y métricas reconstruibles | Los tokens de las 400 ejecuciones antiguas siguen irrecuperables desde sus resúmenes |

Fuentes: César https://www.gutenberg.org/ebooks/218 (cabecera latina y cuerpo latino cotejados en revisión existente), Dante https://www.gutenberg.org/ebooks/1012 (italiano, poesía); inglés https://www.gutenberg.org/ebooks/8300 (Douay-Rheims). Los originales conservan avisos Gutenberg; no se redistribuyen copias del corpus fuente completo. Las vistas analíticas normalizadas quedan archivadas. Naibbe: Greshko, Michael A. (2025), The Naibbe cipher, Cryptologia, https://doi.org/10.1080/01611194.2025.2566408. Licencia completa en vendor/LICENSE y aviso en código. No se atribuye la variante de copia propia al código oficial Timm/Schinner.

## Alertas C001 y soporte

La regla previa dispara tres alertas en mecanismos sin posición. Se cumplen los umbrales literales, de modo que la afirmación pública requiere adjudicación humana; no se edita committed_claims.md ni se continúa un ciclo de búsqueda. Son salidas nuevas, no reanálisis incompatible de EXP-170/171/176. Un máximo en 16 semillas, con soporte escaso y sin inferencia múltiple, no prueba reproducción estable de gramática.

| Brazo | Semilla | am LL | ocurrencias am | ocurrencias am finales |
|---|---:|---:|---:|---:|
| generador_caracter | 17003 | 3.049020 | 18 | 6 |
| generador_iid | 17003 | 4.573529 | 2 | 1 |
| generador_iid | 17012 | 4.573529 | 2 | 1 |

Dos alertas IID contienen solo dos am y uno cae en última posición: 1/272 dividido por 2/2488 = 4,573529. La razón grande resulta de un denominador de dos, no de concentración repetida demostrada. La copia con sustitución tiene 18 am, 6 finales: razón 3,049020. Es el motivo de registrar incertidumbre y soporte antes de atribuir gramática. Se conserva cada salida adversa.

## Autoauditoría obligatoria (skills/audit_experiment.md)

1. **Target-awareness:** Naibbe usa tablas publicadas que imitan el Voynich; copia usa top200, alfabeto y longitudes de train VMS; IID también. Cercanía es condicional a esa calibración. No se ajustan parámetros con el test; las tolerancias fijadas son operativas, no validación independiente del constructor. Una versión con vocabulario ajeno podría comportarse distinto.

2. **Destrucción de rasgos:** recolocar por esqueleto elimina límites lingüísticos originales; se publican brazos de líneas originales. Sustituir caracteres puede destruir onsets; se ensaya también preservación de prefijo. La condición preservadora conserva el prefijo jerárquico de EXP-170, no una gramática completa. La primaria es injusta como prueba universal de lenguaje o de mecanismos porque cambia unidades, ignora orden interpalabra en dos componentes y evalúa pocas hojas. No se generaliza su fallo.

3. **Extrapolación:** cp=0,85, mp=0,25, ventana50, 16 semillas, un Naibbe fijado, dos variantes propias; no rejilla completa. No se concluye imposibilidad, descifrado, causalidad lingüística ni equivalencia de familias. La diferencia latín/italiano también confunde autor, género y orden de textos.

4. **Alcance negativo:** NEGATIVE significa que esta primaria no discrimina el control adversarial y que estas variantes de copia no alcanzaron tolerancias; no valida ninguna teoría sobre el manuscrito. La sensibilidad de coma/IT2a no es réplica independiente. am/y son diagnósticos secundarios, no una primaria nueva elegida después.

5. **Controles, expectativas y observación:** se esperaba ganancia >=0,05 en lenguas conocidas por dependencia de caracteres; se observó latín 0.7291 e italiano 0.7940. Se esperaba ganancia IID <=0,1; observada -0.0244. Se esperaba coincidencia de iniciales permutada ≈1 por destrucción del orden; observada 0.9932. Se esperaba am/y permutados ≈1 con soporte suficiente; medianas 0.9147 y 1.2736. Las desviaciones individuales >1,5 y los controles que exceden VMS se investigan como razones de bajo soporte/concentración: alertas IID y copia arriba; y en inglés natural se debe a iniciales léxicas y corte arbitrario, no a equivalencia de EVA y ortografía inglesa. H2 IID mayor que VMS es esperado al destruir dependencia; no es evidencia de estructura superior. La invariancia de H2/longitud a permutación explica el control primario cercano. No interpretar diferencias mecanísticas más allá de esta descripción.

## Trabajo previo, verificación y pendientes

No se duplica PR #2 https://github.com/kyrian20/voynich-autoexploration/pull/2: su auditoría archivada es antecedente, no dependencia de código. Registro inequívoco y estudios existentes consultados; KB externa y Biblioteca completa no disponibles, por lo que el cotejo no se declara exhaustivo. Sin EXP numérico nuevo.

Pruebas: siete contratos automáticos, incluidas reconstrucción de todas las métricas test/train a partir de tokens y hashes, control sintético con pérdida conocida, vocabulario desconocido, partición física, denominadores ausentes, determinismo y preservación de prefijo; comprobaciones operativas e integridad de los 14 corpus. Reejecución completa y comparación de bytes se registran en VERIFICACION.md. CI remoto se informará según estado real; pasar CI solo respalda esos contratos.

Pendientes: adjudicar públicamente C001 y su soporte histórico; definir otra primaria sensible al orden y validarla primero en controles, con protocolo nuevo; ampliar folios/secciones y sensibilidad de transcripción para todos los mecanismos; localizar versión/ejemplo exactos de EXP-170 si se requiere reproducción histórica. No modificar esta batería tras ver resultados para promover una conclusión.

Se publican las 32 banderas de controles con desviación >1,5 (o <1/1,5) en diagnosticos_controles.json, con numerador, soporte y expectativa bajo colocación aleatoria. No se descartan selectivamente. La normalización ASCII separa letras como æ que no se descomponen por NFD; es una pérdida de representación documentada y no una normalización filológica completa.
