# Corrección del recorte f65r — candidato v2
25-10-2026. Preparación ejecutada; annotation_ready=false.

## Cambio concreto
El candidato previo fue rechazado por recortar dibujo a izquierda. Se conserva su plan e informe.
La v2 usa [0,0,2793,3707], es decir el lienzo completo de la fuente, sin recortar sus bordes.
Conserva máscaras de rótulo [370,2510,430,105] y foliación [2160,70,300,180].
Añade máscara [0,0,75,3707] para la franja de página vecina, identificada mediante inspección de un mosaico del borde a escala original.
[Plan ejecutado](f65r-region-plan-v2.json), [recibo](f65r-mask-v2-receipt.json).

## Ejecución y comprobaciones
Exportador de PR #59 fijado a 73e9729b5ecd2649a3239b83a5c031f3dcf91a54, Python 3.12.14 y Pillow 12.3.0.
Se inspeccionaron mosaicos de la fuente en el borde izquierdo, parte superior y rótulo, y el resultado completo con detalle original.
Comparación independiente por matrices sobre todos los píxeles:
- Dimensiones iguales a la fuente: 2793×3707.
- Todos los píxeles fuera de las máscaras iguales a la fuente decodificada.
- Todos los píxeles dentro de máscaras negros; 377.175 píxeles.
- Metadatos Pillow vacíos.
SHA256 del PNG: 335139284593decf903a82ff67daeb027530e03df4e16709c414d00b1719a6e2.
No se reconstruye contenido perdido en la propia fotografía, ni se atribuye completitud botánica al lienzo.

## Revisión visual y límites
El corte rectangular anterior desaparece. La franja añadida tapa la escritura visible de la página vecina en la vista inspeccionada.
La cercanía de dibujo al pliegue y de la máscara inferior a una punta/rasgo fino exige revisión independiente; no se certifica ausencia de pérdida anatómica.
Las figuras circulares del dibujo superior se conservan: no se ocultan por parecer caracteres. Tampoco se certifica por esta decisión que ninguna marca superior sea escritura.
No hay reconocimiento OCR que pruebe ausencia total de texto; no se ha sometido a un anotador ciego.
Por tanto: CANDIDATE_NOT_INDEPENDENTLY_REVIEWED. Ninguna tarea se marca READY; no se entrega como paquete de anotación.

## Reproducción
Usar el exportador de la cabeza fijada de PR #59 con --plan apuntando a f65r-region-plan-v2.json, --folio f65r y la fuente cuyo SHA256 es dc7a0c45454665f33287804ec56f8eaa952a691540fc6fd434e79d75c7ce597f.
El output debe ser un fichero nuevo. Los originales y la propuesta rechazada se conservan.
No se ha fusionado PR #59, ejecutado suite global ni verificado CI nueva. Las cuatro pruebas del exportador aprobadas en la continuación anterior se complementan con la comparación real de píxeles v2; no equivalen a revisión del dibujo.

## Autoauditoría
La modificación responde al defecto visual conocido, por tanto es reparación informada, no contraste independiente.
No se alteran píxeles fuera de máscaras; la posible destrucción de rasgos dentro de ellas sigue abierta y se declara junto al resultado.
No se extrapola a otras páginas ni se infiere taxón, significado, potencia o éxito de traducción.
Se esperaba igualdad exacta fuera de máscaras y negro dentro: ambos controles se cumplen.
Siguiente requisito: revisar este candidato contra la fuente por una persona distinta, antes de preparar anotación. Este asistente expuesto no puede aportar esa independencia.
