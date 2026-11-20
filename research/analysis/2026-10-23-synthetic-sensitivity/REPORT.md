# Sensibilidad con dependencias conocidas — 23 octubre 2026

Estado: REPRODUCED. 48 brazos y 48 controles de entrenamiento barajado, dos ejecuciones con JSON exactamente idéntico. Es una validación técnica limitada del diagnóstico; no valida ninguna teoría del Voynich.

## Resultado

Se detectan los 12 controles de dependencia fuerte con bordes constantes, y los 12 de dependencia moderada. Ninguno de los 12 brazos independientes tiene intervalo positivo. Con exactamente la misma secuencia y una codificación biyectiva que revela la identidad en el borde, ninguno de los 12 brazos fuertes presenta intervalo residual positivo. La dependencia se recupera en E frente a U. Esto demuestra un punto de identificación: residual pequeño puede coexistir con dependencia fuerte conocida. No permite afirmar que ese sea el mecanismo del manuscrito.

| Vocabulario | Probabilidad de copia | Identidad visible en borde | Ganancia W−EL, rango bits | Intervalos residuales positivos | Ganancia E−U, rango bits |
|---|---:|---|---:|---:|---:|
| 32 | 0 | No | -0.000579 a 0.000000 | 0/6 | 0.000008 a 0.000010 |
| 32 | 0.25 | No | 0.463582 a 0.524329 | 6/6 | 0.000008 a 0.000010 |
| 32 | 0.75 | No | 2.925668 a 3.006593 | 6/6 | 0.000007 a 0.000009 |
| 32 | 0.75 | Sí | 0.000000 a 0.000000 | 0/6 | 2.925677 a 3.006599 |
| 256 | 0 | No | 0.000000 a 0.000040 | 0/6 | 0.000000 a 0.000000 |
| 256 | 0.25 | No | 0.828876 a 0.930968 | 6/6 | 0.000000 a 0.000000 |
| 256 | 0.75 | No | 4.896831 a 5.028523 | 6/6 | 0.000000 a 0.000000 |
| 256 | 0.75 | Sí | -0.001095 a 0.001474 | 0/6 | 4.896831 a 5.028523 |

## Desviación de la expectativa y explicación comprobada

La expectativa de W−EL exactamente cero con bordes identificadores no se cumple en todos los brazos V=256: rango −0,001095 a +0,001474. No se cambia el protocolo retrospectivamente. verify.py comprueba para las 256 identidades de un brazo que E, EL y W tienen exactamente los mismos conteos suficientes y particionan igual los contextos. Sin embargo, cada nivel vuelve a mezclar esos conteos con su padre: pesos [1, 0.1, 0.1] producen probabilidades diferentes. Es una diferencia de regularización jerárquica, no información nueva del contexto. El indicador W−EL no debe describirse como información condicional pura.

El control barajado conserva correlación de inventario por línea en procesos de copia, y puede retener capacidad predictiva; no se esperaba un cero exacto ni se usa como nulo inferencial. Resultados y pesos de cada control están publicados. La comparación contra Voynich permanece fuera del alcance de este ensayo.

## Autoauditoría

1. Conciencia del objetivo: se usa el tamaño y agrupación Voynich, conocidos antes; las dependencias son impuestas y calibradas para controles técnicos positivos. El éxito es condicional a este generador; no ajusta valores observados del manuscrito.
2. Destrucción de rasgos: la codificación expuesta preserva exactamente índices, orden y dependencia; redistribuye dónde se hace visible la identidad. El barajado destruye orden y conserva inventario. No es un modelo de lengua.
3. Extrapolación: V=32/256, d=2/3, p=0/.25/.75, tres semillas. No mide potencia poblacional ni sensibilidad para vocabularios o dependencias arbitrarios.
4. Alcance negativo: residual cero no excluye dependencia; no se concluye nada sobre contenido semántico.
5. Controles: se esperaba detección de dependencia fuerte y ausencia de intervalos positivos en IID. Observado: 12/12 fuertes constantes positivos; 0/12 IID positivos. Expuestos: E recupera señal y W residual no tiene intervalo positivo. La desviación del cero exacto se investigó mediante conteos y probabilidades; se revisó la interpretación, sin alterar protocolo ni resultados.

## Reproducción y alcance operativo

`python research/analysis/2026-10-23-synthetic-sensitivity/replay.py` ejecuta todos los brazos en temporal y compara cada campo científico, hash y semilla; solo admite cambio de cadena de intérprete. `verify.py` verifica 100 construcciones de parejas y el caso de contextos redundantes. Generación verifica biyectividad, inversión, plantilla de longitud/grupo y aislamiento por folio; probabilidades normalizadas y vocabulario idéntico bajo barajado. No se han cambiado corpus ni resultados anteriores.

La PR anterior pasó Voynich Check: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39903394851 (commit 12766dc0db3a9c96826b2dfba812b9bd264f4ac1). Ese run no ejecutaba este nuevo diagnóstico; su CI se comprobará aparte.

## Próxima decisión

Separar ganancia por regularización de ganancia por contexto, con controles de particiones idénticas, antes de atribuir señal residual a identidad léxica. Mantener los resultados anteriores como métricas predictivas exploratorias, sin reinterpretarlos como información condicional ni traducción.
