# Estudio único de categorías visuales — decisión de continuidad

Fecha: 25-10-2026. **Estado: BLOCKED.** Reorientación autorizada por el usuario.
Este documento actualiza el esquema existente; no crea EXP ni comunica resultados semánticos.

## Pregunta y alcance
¿Las características de los rótulos EVA predicen categorías de ilustraciones anotadas independientemente, en hojas reservadas, mejor que sección, longitud y posición?
La hipótesis nula es que EVA no añade capacidad predictiva a esos metadatos.
Un eventual resultado positivo sería asociación predictiva, no traducción ni identificación de plantas.

## Decisión de trabajo
Concentrar el siguiente esfuerzo científico en esta única pregunta. No abrir nuevas tandas de estadísticas descriptivas, búsquedas fonéticas ni repeticiones de daiin→dam sin datos o pregunta nuevos. Conservar originales, negativos y correcciones. Mantenimiento mínimo: solo el que desbloquee esta prueba o preserve integridad.
Esta decisión documental no desactiva workflows ni garantiza cambiar otras sesiones remotas.

## Viabilidad comprobada documentalmente
Fuentes: [guía visual](../decipherment/2026-10-25-visual-annotation/GUIDE.md) y [verificación](../decipherment/2026-10-25-visual-annotation/VERIFICATION.md).
El paquete documenta 1.172 tareas, cero tareas listas y cero anotaciones; tres imágenes fuente inspeccionadas por un asistente expuesto a hipótesis previas.
No son 1.172 objetos independientes demostrados. La cola y los tests de software no sustituyen identificación de regiones, máscaras aprobadas ni anotación.
PR #59 exporta candidatos PNG; sigue siendo preparación. No acredita revisión independiente.
Conclusión de esta revisión documental: NO-GO para entrenar o evaluar ahora. No se ha vuelto a ejecutar la cola ni inspeccionado nuevamente las imágenes.

## Única preparación admisible: piloto de viabilidad
Usar el inventario existente, sin seleccionar por palabra EVA ni nombre de planta esperado.
Antes de anotación, congelar selección determinista de un piloto de hasta 12 hojas físicas de entrenamiento del manifiesto v2; ordenar por identificador de hoja, sin examinar resultados. No consumir desarrollo ni prueba.
Antes de extraer recortes, adjudicar relación rótulo/objeto y grupos de ilustración compartida. Si no se puede resolver, conservar exclusión motivada.
Preparar imágenes aplanadas y revisadas que oculten texto y metadatos sin destruir rasgos necesarios.
Dos anotadores distintos trabajan por separado conforme a GUIDE.md y declaran exposición previa. Este asistente expuesto no cuenta como anotador ciego. No se han identificado participantes disponibles ni se ha contactado con nadie.

El piloto mide solo viabilidad: cobertura, exclusiones, tiempo de preparación, acuerdo y diversidad de categorías dentro de sección. No entrena el predictor ni prueba una clave.
Se admite una sola revisión de la guía tras el piloto, archivando las respuestas originales. Si requiere sucesivas redefiniciones, pausar esta vía.

## Puertas obligatorias antes del estudio
1. Regiones, correspondencias de edición y lector auditados para la selección efectiva; hashes y exclusiones conservados.
2. Imágenes aptas y dos anotaciones independientes reales; incertidumbre y desacuerdos archivados.
3. Variación de categorías dentro de secciones y soporte de permutación suficientes: si las categorías solo distinguen secciones, la pregunta no es identificable.
4. Agrupar caras por hoja y objetos compartidos por componente; si cruzan particiones, excluir el componente completo según regla fijada antes de resultados. Reutilizar manifiesto v2; no cambiar la sal para mejorar cobertura. Reconocer exposición histórica del holdout.
5. Antes de evaluar, congelar categorías finales, métrica primaria, modelos, rejilla, semilla, tratamiento de desconocidos, baselines, control positivo, nulo intercambiable y umbral de efecto útil.
6. Justificar tamaño muestral y potencia mediante simulación agrupada con datos de entrenamiento/piloto. No fijar un número mágico de etiquetas como garantía de potencia.

Mientras falte una puerta: BLOCKED y no consultar resultados de prueba. No fabricar anotaciones, acuerdos ni potencia.

## Evaluación prevista, aún no preregistro completo
Comparar baseline mayoritario y modelo de sección/longitud/posición con el mismo modelo ampliado con n-gramas EVA. Aprender representaciones solo en entrenamiento y ajustar solo en desarrollo.
Métrica propuesta: reducción de pérdida logarítmica con igual peso por hoja, frente al baseline más fuerte. Congelar su implementación antes de evaluación.
Control positivo sintético de verdad conocida y control negativo con intercambios admisibles, cuyo soporte se documente. Si no existe nulo defendible, no anunciar contraste confirmatorio.
Publicar incertidumbre agrupada, sensibilidad a transcripción, predicciones completas, errores y análisis de dependencia de una sola hoja. Ediciones alternativas no son réplicas independientes.
La evaluación de prueba se hace una vez. Este esquema permanece incompleto hasta satisfacer las puertas anteriores.

## Criterios de cierre
- Ahora: BLOCKED por falta de datos visuales independientes; pausar modelado.
- Piloto inviable o sin anotadores independientes disponibles: archivar viabilidad y pausar la vía; no sustituir anotación por intuición del asistente.
- Prueba válida sin mejora suficiente según umbral congelado: NEGATIVE para este método y estas categorías; no concluye ausencia de significado.
- Intervalo demasiado amplio, controles fallidos o soporte insuficiente: no concluyente/BLOCKED; no repetir con nuevas semillas o umbrales para buscar éxito.
- Apoyo: requiere superar baselines y controles, alcanzar el efecto útil fijado y no depender de una sola hoja. Justifica un estudio independiente posterior; no una traducción.

## Convivencia con propuestas y verificación
PR #13 estudia recuperación de referentes/nombres con correspondencias: no es este objetivo de categorías amplias. Permanece propuesta, sin fusionarla como un segundo estudio activo ni importar automáticamente sus umbrales. El diseño histórico se conserva en Git.
No se modifican committed_claims.md ni resultados históricos.
Comprobación de esta actualización: lectura cruzada de guía, verificación, partición, README, norma de integridad y PR #13. Cambio exclusivamente documental; sin tests, ejecución científica, nueva anotación ni certificación de CI.

## Resultado de viabilidad de la selección inicial — 25-10-2026
La [comprobación de cobertura ejecutada](../decipherment/2026-10-25-visual-annotation/PILOT_FEASIBILITY.md) seleccionó las primeras 12 hojas de entrenamiento en orden numérico, sin sustituciones. Solo dos contienen registros en el inventario archivado: tres registros/localizadores en total. La selección se pausa por cobertura insuficiente, además de seguir faltando máscaras revisadas y dos anotadores independientes. No es un resultado negativo sobre significado. Cualquier selección restringida primero a hojas con rótulos requiere una enmienda explícita y trazable; no se aplica retrospectivamente para presentar este piloto como viable.

## Enmienda prospectiva de selección v2 — 25-10-2026
Autorizada la continuación, se corrige el universo de muestreo antes de calcular la nueva selección: intersección de hojas train del manifiesto v2 con hojas que tengan al menos un registro en inventory.json.gz. Extraer hoja mediante coincidencia completa f(numero)[rv](panel opcional), ordenar numéricamente y tomar las primeras 12; si hay menos, conservar todas sin buscar fuera de train. No usar tokens EVA, categorías, nombres esperados ni disponibilidad de imagen para elegir. Conservar todos los localizadores de esas hojas, aunque solo consten en una edición; documentar cobertura sin declararla equivalencia visual. No reemplazar seleccionadas después de inspeccionar imágenes. Un folio no interpretable queda como exclusión. Esta es una enmienda informada por el fallo previo, no selección preinscrita desde el inicio ni muestra representativa de todo el manuscrito. El piloto inicial permanece archivado.

## Límite de elegibilidad por locus — 25-10-2026
El [cotejo de subtipos](../decipherment/2026-10-25-visual-annotation/PILOT_V2_LOCUS_ADJUDICATION.md) contabiliza 97 candidatos con subtipo referido a ilustración y 191 localizadores L0/Lx/Ro/Ri sin esa relación explícita. No entrenar con categoría derivada del subtipo IVTFF como sustituto de anotación visual independiente. f17r.13 y los 26 loci de f49v permanecen bloqueados para pares objeto/rótulo. La selección de 288 localizadores se conserva, sin reemplazar exclusiones. Ninguno se declara objeto independiente o listo por el código de locus.
