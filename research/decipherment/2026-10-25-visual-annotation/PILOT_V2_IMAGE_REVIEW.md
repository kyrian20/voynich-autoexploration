# Comprobación material de imágenes del piloto v2
25-10-2026. Preparación de datos, sin anotación independiente ni resultado semántico.

## Fuente y verificaciones ejecutadas
Se descargó el manifiesto primario https://collections.library.yale.edu/manifests/2002046 : 213 canvases, SHA256 317d58fd9ea90392a83d9858a91eada3d0b41416a3c835857dc0154bd123a309.
Proveedor indicado: Yale University Library. No se encontró campo rights en este manifiesto; eso no establece licencia de redistribución.
Se buscaron coincidencias exactas de etiqueta para las 18 caras/paneles seleccionados.
Se descargaron f17r, f49v y f57v, se verificó decodificación JPEG y dimensiones declaradas frente a decodificadas y se registraron hashes: [recibo](pilot-v2-fresh-images.json).
Se inspeccionaron visualmente las tres páginas completas en la vista proporcionada al asistente; no examen paleográfico a escala original ni anotación ciega. No se publican derivados ni fuentes binarias en Git.

## Hallazgos operativos
- f17r: imagen de una estructura vegetal con escritura intercalada entre las partes superiores; relación exacta de f17r.13 con objeto/región sin adjudicar. No se asigna especie.
- f49v: una ilustración vegetal extensa junto a varios bloques de escritura. Los 26 localizadores del inventario no acreditan 26 objetos independientes. No convertirlos en 26 ejemplos con una etiqueta de página sin resolver relación rótulo/objeto. Eso inflaría muestra y facilitaría aprender sección/página.
- f57v: composición circular con escritura en anillos y figuras interiores. Una máscara rectangular global destruiría gran parte del contexto; requiere segmentación local y revisión. No se asignan referentes a partir de parecidos.
Las observaciones son del coordinador expuesto; no entran como categorías independientes en el estudio.

## Dos imágenes conjuntas que cruzan particiones
El manifiesto ofrece «69v and 70r» en canvas 1006199 y «71v and 72r» en canvas 1006203.
Las hojas 69 y 71 pertenecen a train; 70 y 72 a test según manifiesto v2.
No se descargaron ni inspeccionaron esos dos JPEG en esta continuación; solo se leyó su etiqueta en el manifiesto.
Las imágenes completas no son aptas para un paquete exclusivo de entrenamiento. Mantener f69v y f71v bloqueadas. Una eventual separación exige coordenadas verificadas y ausencia de contenido de test; si no se puede garantizar, excluir esos registros sin reemplazarlos.
Compartir captura no demuestra compartir objeto: no se fusionan automáticamente hojas por objeto. Se registra riesgo de exposición de la captura.

## Paneles sin correspondencia directa
f67r1, f67r2, f67v1 y f67v2 no tienen coincidencia exacta; Yale ofrece 67r y 67v.
No adivinar distribución de paneles ni copiar la misma imagen como cuatro objetos independientes. Exigir crosswalk con regiones verificadas antes de recortar.
Las 12 hojas seleccionadas se mantienen; los casos difíciles no se sustituyen.

## Decisión
Tres imágenes nuevas recuperadas y comprobadas, ninguna máscara aprobada. Continúan cero anotaciones independientes producidas por esta sesión. Se puede preparar adjudicación de regiones en las páginas disponibles; no hay autorización metodológica para entrenar todavía.
Prioridad material siguiente: revisar raw_line/locus contra imagen para distinguir rótulos, bloques y marcas marginales, empezando por f17r y f49v; conservar los casos no resolubles como exclusiones.

## Autoauditoría
Selección de tres fuentes en orden de disponibilidad exacta, sin buscar un nombre o efecto favorable; se inspecciona material train previamente seleccionado.
No se altera texto ni imagen. La inspección reducida limita geometría: no se certifican coordenadas o máscaras.
No se extrapola a los 288 localizadores ni se concluye nada sobre significado.
No hay contraste estadístico ni resultado negativo. Control de dimensiones: se esperaba igualdad con manifiesto y se obtuvo en las tres descargas; decodificación JPEG aprobada. No suite global ni CI certificada.
