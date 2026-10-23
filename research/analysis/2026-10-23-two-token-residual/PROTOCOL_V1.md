# Identidad residual con dos predecesores

Diseño fijado antes de ejecutar este paquete, 23-10-2026. Extensión exploratoria de V2, sin EXP nuevo. Los folios y las hipótesis ya se han explorado; no se presenta una confirmación nueva.

Pregunta: ¿añadir la identidad del segundo token anterior mejora la predicción del token actual, más allá de la identidad del inmediatamente anterior y de bordes/longitud de ambos?

Se reutiliza inputs.json del bloque integrado de orden residual, sin cambiar corpus ni proyecciones. Se publican sus seis fuentes (cuatro vistas Voynich relacionadas y dos referencias). Vocabulario: 2.000 tipos de entrenamiento más UNK, tau=20, alpha=0,1; partición V2 por hash del grupo módulo 5: train=2/3/4, desarrollo=1, evaluación=0. No se dividen caras/paneles entre particiones.

W1 es el modelo V2 ya calibrado en desarrollo. Se añaden dos capas normalizadas: H2, que condiciona identidad/bordes/longitud del token inmediatamente anterior y bordes/longitud del segundo anterior; W2, que añade identidad del segundo anterior, manteniendo esas firmas. Cada capa interpola con el padre, con rejilla heredada [0; 0,01; 0,025; 0,05; 0,1; 0,25; 0,5; 1]. Se minimiza pérdida solo en desarrollo, empate por menor peso. Los nuevos conteos se entrenan solo con tripletas internas a una línea.

Evaluar W1/H2/W2 sobre las mismas tripletas de evaluación, omitiendo las primeras dos posiciones y sin cruzar líneas. Primaria descriptiva: pérdida H2 menos W2, bits/tripleta. Publicar también incrementos H2-W1 y W2-W1, pérdidas, pesos, cobertura de contexto, UNK y grupos. Repetir 16 controles de entrenamiento barajado por línea, semillas de V2, recalibrando todo en desarrollo. Bootstrap pareado de grupos, 2.000 muestras, semilla 2026102301, solo incertidumbre de evaluación con modelos fijados.

Antes de interpretar Voynich, verificar control sintético positivo: aba.mid.xx / aca.mid.yy con iguales bordes/longitud para aba/aca y grupos disjuntos. Debe recuperar >0,5 bits/tripleta de identidad adicional. Control negativo: ambas identidades con ambos destinos en proporciones iguales; ganancia absoluta <1e-10. Enumerar probabilidades sobre vocabulario+UNK para comprobar normalización en contextos vistos/no vistos y rechazo de fugas de grupos. Si falla un control, bloquear interpretación y conservar el fallo; no ajustar parámetros usando evaluación.

Los controles naturales comprueban el comportamiento de esta memoria de dos tokens en dos textos, no todas las lenguas. Si no recupera incremento en ellos, no atribuir ausencia de estructura a Voynich. Ningún resultado asigna fonemas, significados o una traducción. Esta extensión difiere de los trigramos descriptivos históricos y de la predicción de un único predecesor de EXP-607/V2; el cotejo de antecedentes se limita al repositorio.

