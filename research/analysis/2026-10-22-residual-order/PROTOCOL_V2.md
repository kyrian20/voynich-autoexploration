# Reparación exploratoria del predictor: calibración solo en desarrollo

Escrito después de observar V1: todas las capas empeoran también en César latino y Dante italiano. Ese fallo de sensibilidad bloquea interpretar V1 como ausencia de identidad léxica en Voynich. V1 y su protocolo/resultados se conservan íntegros.

Sin variar corpus, tokenización, tau=20, alpha=0,1 ni dos perfiles de vocabulario: partición por grupo SHA-256 módulo 5; evaluación=0, desarrollo=1, entrenamiento=2/3/4. El grupo es folio físico en Voynich y bloque de 25 líneas en referencias. Los grupos de evaluación ya fueron vistos en V1; esto NO los convierte en una confirmación nueva.

Cada capa E, EL y W se interpola con su padre. Pesos candidatos fijados: 0, 0,01, 0,025, 0,05, 0,1, 0,25, 0,5, 1. Se elige secuencialmente el peso de menor pérdida en desarrollo (empate: menor peso), sin consultar evaluación. El prior de cada capa usa su padre ya calibrado. El vocabulario y todos los conteos se aprenden solo en entrenamiento. Peso cero habilita descartar una capa que empeora el control. No se exige resultado favorable.

Mismos 16 barajados de train y 2.000 bootstrap por grupo de test; cada control pasa la misma calibración con desarrollo real y train barajado. Publicar pesos, todos los scores de desarrollo, pérdidas de evaluación y controles. No son p confirmatorios ni prueba semántica. Si los controles conocidos no muestran recuperación de estructura, declarar sensibilidad insuficiente; no cambiar otra vez el método para conseguir una conclusión.
