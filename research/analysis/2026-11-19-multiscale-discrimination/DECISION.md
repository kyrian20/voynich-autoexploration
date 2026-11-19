# Decisión de investigación: contraste multiescala con controles de verdad conocida
Fecha: 2026-11-19. Estado: **DISEÑO EXPLORATORIO, NO EXPERIMENTO EJECUTADO**. No se asigna identificador EXP nuevo.

## Problema que resuelve
EXP-623 observa predictibilidad de orden, mientras el contraste residual del 22–23 de octubre no sostiene una ventaja adicional de identidad/BPE frente a bordes, longitud o carácter final. No son resultados contradictorios: miden objetivos y controles diferentes. La señal de orden puede residir en plantillas subléxicas y posición de línea. No se infiere idioma, cifrado ni ausencia de significado.

## Hipótesis competidoras
H1: proceso de copia/modificación local sin texto plano; H2: generador de plantillas y estados dependientes de posición/folio; H3: cifrado reversible de un texto lingüístico, incluyendo alternativas multiclave o verbose; H4: código de clases/nomenclátor con dependencias de contexto; H5: escritura lingüística con segmentación EVA no equivalente a palabras.
No se atribuyen probabilidades previas ni se considera exhaustiva la lista.

## Prueba discriminante propuesta
Antes de tocar los folios de evaluación, implementar los cinco mecanismos en corpus de verdad conocida y comprobar si el procedimiento recupera la clase generadora; para H3/H4 exigir además recuperación de texto plano en controles cifrados. Un clasificador que solo iguale estadísticas superficiales no pasa esa puerta.

Congelar un manifiesto con hashes de corpus, transcripción, política de códigos opacos, segmentación, folios físicos y grupos Currier; declarar explícitamente toda exposición previa del equipo a los folios. Si no existe reserva no contaminada defendible, la evaluación será **exploratoria**, no confirmatoria. Las transcripciones ZL3b e IT2a son dos lecturas del mismo objeto, no réplicas independientes.

Cada mecanismo genera una muestra de longitud comparable y predicciones fuera de muestra de:
1. distribución de glifos condicionada por posición intratoken y extremos;
2. ganancia de orden local **residual** después de controlar primer/último glifo y longitud;
3. semejanza entre tokens próximos, con nulos dentro de línea y dentro de párrafo por separado;
4. probabilidad de límite de línea con separación por folio físico;
5. deriva entre folios y Currier A/B, evitando confundir secciones con bloques numéricos.

Calcular métricas con un único lector auditado y reportar vectores completos, incertidumbre por folio y complejidad de modelo (número de parámetros y coste de descripción). No elegir un ganador mediante una suma arbitraria de puntuaciones. Priorizar falsaciones claras: un mecanismo que no puede reproducir una restricción robusta queda limitado; si todos pasan, resultado no discriminante.

## Puertas de integridad
- Parser IVTFF independiente y tratamiento de códigos high-ASCII: pendientes; ninguna prueba sensible a ellos puede promoverse a conclusión firme.
- Controles de movilidad: informar cuántas posiciones pueden cambiar realmente; no interpretar nulos casi inmóviles.
- Calibración: fijar hiperparámetros en entrenamiento/desarrollo, sin consultar test.
- Auditoría: ejecutar skills/audit_experiment.md sobre resultados antes de alterar findings.md o committed_claims.md.
- No revivir pares semánticos rechazados (incluido daiin→dam) sin evidencia externa independiente.
- No reabrir máscaras del piloto visual bloqueado sin revisores/anotadores.

## Criterio de gran avance
Un avance de descifrado exige reglas reversibles consistentes, recuperación de contenido en controles de verdad conocida y predicciones nuevas acertadas sobre material Voynich reservado, más anclaje externo y revisión independiente. Un avance estructural consiste en excluir al menos una **implementación específica** bajo una prueba con potencia y controles adecuados. Ninguna de esas condiciones se ha demostrado en este documento.

## Próxima acción concreta
Auditar el lector IVTFF independiente y producir un manifiesto de folios, transcripciones y hashes; después construir el primer par H1/H3 sobre controles de verdad conocida, sin mirar Voynich-test. Documentar fallos y costes. La literatura reciente Zhang–Sheng (arXiv:2610.34499) y ProjectZero1 (16-11-2026) orienta el diseño, pero sus resultados no son reproducciones propias.

## Procedencia
Se basa en README.md, SOUL.md, research/OPERATIONAL_STATUS.md, research/DECIPHERMENT_AND_RECOGNITION_STRATEGY_2026-10-25.md y research/analysis/2026-10-23-subword-increment/REPORT.md consultados en master el 19-11-2026. Es una decisión metodológica nueva, no una afirmación de haber ejecutado nuevas mediciones.
