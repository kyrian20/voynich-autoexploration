# Orden residual e identidad de corpus — bloque privado, 22-10-2026

PROPOSED antes de ejecutar métricas predictivas. Fuente fijada: b566b6fa461f3a4e6fd8bb3a1aaa6e71f035f190. Sin EXP nuevo ni publicación GitHub.

## Puerta de corpus
Auditar cabeceras reales de los diez TXT de referencia; contrastar título/idioma esperado y localizar referencias estáticas a los seis archivos problemáticos (dos traducciones inglesas en latin/, un texto inglés en arabic/, un libro inglés con título incorrecto, Cicerón bilingüe y el fichero vacío). No se declara automáticamente inválido todo experimento que los mencione: distinguir carga, filtros y estimando. Conservar originales y resultados históricos. Usar en este bloque solo César latino #218 y Dante italiano #1012; no usar Cicerón como latín sin adjudicar su filtro.

## Pregunta nueva
¿La identidad completa del token anterior mejora la predicción de la identidad siguiente tras controlar primer/último carácter y longitud? Cuatro modelos normalizados jerárquicos, parámetros fijados sin usar test:
U: unigramas de destinos de transición con alpha=0,1.
E: distribución condicionada a primer/último carácter del token anterior, prior U.
EL: añade longitud del token anterior, prior E.
W: identidad completa del token anterior, prior EL.
Cada capa: (conteo local + tau*prior)/(total local + tau), tau=20.

El vocabulario se aprende SOLO en train: dos perfiles, completo y 2.000 tipos de mayor frecuencia más UNK. Los contextos de borde/longitud se calculan sobre el token crudo; W utiliza identidad mapeada a UNK si no se conoce en train. Nunca se interpretan UNK como caracteres EVA. Salidas de probabilidad sobre exactamente V+1 eventos.

Voynich: ZL3b/IT2a × split/join, P0, alternativas primarias/ligaduras expandidas, todos los tipos de página aceptados por el lector. Intersección de IDs con ≥2 tokens entre cuatro vistas. Partición 80/20 aproximada por SHA-256 del folio FÍSICO: f89r1, f89v2 y demás caras/subdivisiones se agrupan como f89; resto módulo 5=0 es evaluación. Folios ya explorados, no confirmación nueva.

Controles: César #218 desde el título latino del libro I hasta el colofón Gutenberg; Dante desde Nel mezzo hasta el marcador final. Tokenizar letras latinas Unicode y apóstrofo como separador. Crear líneas con la plantilla de longitudes ZL3b/split; descartar fragmento final incompleto, nunca repetir un texto corto. Agrupar 25 líneas consecutivas por bloque de comparación; reservar bloques por el mismo hash. No son folios materiales ni igual género; no comparar pérdidas absolutas entre lenguas.

Publicar pérdidas pareadas por grupo, ganancia EL−W y bootstrap de grupos (2.000 réplicas, semilla 2026102203). Control negativo: 16 barajados independientes dentro de cada línea SOLO de train (semillas derivadas de SHA-256); test permanece real. Volver a aprender vocabulario/modelos por control. Informar todos los controles, nunca usar su rango como IC ni p confirmatorio. No tunear tau ni vocabulario tras ver resultados.

Expectativa: si la identidad importa más allá de los bordes/longitud, W podría mejorar EL; los controles naturales calibran sensibilidad, no traducen nada. Una pérdida o ganancia pequeña bajo este modelo no excluye sintaxis, cifrado ni lengua. Prueba injusta para una estructura de memoria larga o unidades distintas de estos tokens: el modelo solo usa un token previo. Clasificarlo como exploratorio y no inferir significado.

## Integridad
Guardar hashes de corpus, scripts, entrada preparada, protocolos, resultados, versiones y logs. Pruebas de normalización, UNK, separación por folio físico y mantenimiento de inventario en barajados. No tocar afirmaciones comprometidas; abrir incidencias privadas sobre controles históricos con identidad dudosa. No marcar el proyecto global como limpio.
