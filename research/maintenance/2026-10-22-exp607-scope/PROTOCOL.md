# EXP-607: diagnóstico de alcance y semillas — v1

Este protocolo se fija antes de ejecutar el diagnóstico por tipos de locus. Es seguimiento exploratorio de un modelo ya observado, no un nuevo test confirmatorio ni búsqueda de hiperparámetros.

## Pregunta
¿La ventaja del modelo frente a entrenamiento barajado se conserva al restringir tanto entrenamiento como evaluación a texto P0, excluyendo etiquetas y otros tipos de locus?

## Elementos fijos
- ZL3b e IT2a, versiones y hashes de las auditorías previas.
- Universo original de páginas básicas y misma intersección física de registros entre lector nativo y candidata conservadora ASCII.
- Mismos lectores, alpha=0,1, mezcla=0,5 y separación por hash de folio del EXP-607. No ampliar páginas ni reajustar con el test.
- Primero reproducir los resultados mixtos del snapshot del diagnóstico previo; abortar si no coinciden.

## Diagnósticos completos, sin selección posterior

Cruzar dos alcances de entrenamiento (mixto y P0 exclusivo) con seis evaluaciones: mixto, P0, no-P0, etiquetas L*, circular/radial C*/R* y otros párrafos P*. Informar todos, incluso valores desfavorables y alcances vacíos. Mantener train/test disjuntos por folio y registrar recuentos y hashes de IDs.

Para el diagnóstico primario P0→P0, usar 64 semillas de barajado de entrenamiento: la original 6072026 y 63 derivadas de SHA-256 de EXP607-scope-control-v1:0 ... :62. Se fijan todas antes de puntuar; no buscar semillas favorables. El control baraja cada locus conservando longitud, multiconjunto y folio; el test conserva su orden original. El primer control debe reproducir native.score(..., shuffled=True).

Informar la ganancia real frente a unigram, media/rango/cuantil 95 de las ganancias de controles, y número de controles que alcanzan o superan al real. No convertir este ranking en p-valor confirmatorio ni confundir el cuantil de controles con un intervalo de confianza.

Precisión de implementación fijada antes de puntuar: las semillas derivadas usan los primeros 16 dígitos hexadecimales del SHA-256 como entero sin signo. El cuantil usa interpolación lineal en el índice (n−1)q. La selección de loci se realiza antes de barajar, conservando el orden físico de origen dentro de cada folio.

## Límites

No comparar pérdidas absolutas entre lectores como el mismo estimador. Las evaluaciones por alcance tienen distintos eventos y tamaños; las pequeñas no permiten generalizaciones. Un resultado P0 favorable excluye las etiquetas de ese diagnóstico, pero no demuestra causalidad, naturalidad lingüística, semántica o desciframiento. Transcripciones del mismo manuscrito no son réplicas independientes.

Aplicar la autoauditoría de cinco controles del repositorio antes de actualizar estado; conservar resultados históricos y no asignar nuevo ID EXP.
