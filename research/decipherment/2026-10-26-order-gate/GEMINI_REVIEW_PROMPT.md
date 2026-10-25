# Solicitud preparada; NO EJECUTADA

Revisar críticamente este resultado acotado, sin atribuirse acceso a corpus, ejecución de código o validación independiente. No proponer una traducción Voynich. No confundir disponibilidad de API con calidad de revisión.

Dos textos naturales de identidad conocida, César/Dante; train/dev/test por bloques disjuntos existentes. Familia artificial: rotar todas las letras ASCII de cada token por offset+posición_mod_periodo, reiniciada por línea. Se buscan dos idiomas y312 claves por idioma, solo en dev. Gate de orden entrenado en claro train, mezcla calibrada en dev y umbral max(.01,máximo de16barajados dev); cobertura>=.5 y margen de clave>1e-6. No se presenta idioma/familia/alfabeto general desconocidos.

Resultados: positivos100% exactos;32/32barajados rechazados; empate uniforme NO_IDENTIFICABLE. Pero verdadero periodo13 fuera de la búsqueda1..12 produce clave12/offset11 admitida en ambos:19/4115 y79/7925 palabras incorrectas. Son exactamente las posiciones>=12, únicas donde las reglas divergen en estos textos. Dos mensajes de un generador empírico de pares train son admitidos con S superior al original. Filtro no admitido como validador de contenido, sin tocar umbrales después del fallo.

V1 detectó un sesgo de suavizado en sintético independiente antes de corpus; V2 corrige mediante multiplicador centrado y normalización. Siete pruebas V2 pasan; dos ejecuciones byte idénticas y todos los624 candidatos en39desafíos conservados. La reproducción no certifica significado. Bootstrap pareado por grupos solo describe contraste de orden, no recuperación de clave/semántica.

Auditar: (1) si las afirmaciones quedan dentro del diseño; (2) si la prueba de no identificabilidad para periodos>=máximo de tokens por línea es correcta y dónde deja de aplicar; (3) qué usos limitados del filtro siguen siendo legítimos; (4) qué evidencia independiente sería necesaria antes de una lectura Voynich y cuáles recursos actuales NO la proporcionan. No pedir más semillas o ajustar el mismo filtro a estos fallos. No atribuir originalidad externa ni exclusión de clases de teorías.

Devolver críticas concretas con supuestos y alcance; señalar cualquier dato faltante. Una respuesta fluida no cuenta como nueva evidencia. Esta solicitud se conserva para una ejecución posterior identificada, sin modificar prompts históricos ni afirmar que ya fue enviada.
