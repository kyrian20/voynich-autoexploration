# Diagnóstico exploratorio de distancia 2/3 — 23 octubre 2026

Estado: REPRODUCED para la construcción y ejecución determinista; diagnóstico lingüístico no concluyente. Reproducción completa V1/V2 anterior realizada desde el commit c70a0ba5a97276edce09d7bfe7b8dc88514a2881. Véase receipt.json. No se declara CI verde.

12 brazos, 16 controles por brazo, vocabulario 2000+UNK y partición por folio heredada. IT2a split/join son duplicados analíticos, no replicaciones independientes.

| Fuente | Distancia | Ganancia W sobre EL (bits) | Intervalo exploratorio 95% | Media control | Parejas |
|---|---:|---:|---|---:|---:|
| ZL3b_split | 2 | -0.000933 | [-0.004018; 0.003051] | 0.000285 | 4927 |
| ZL3b_join | 2 | 0.000453 | [-0.001036; 0.002066] | 0.000297 | 4457 |
| IT2a_split | 2 | 0.000082 | [-0.001521; 0.001965] | 0.000305 | 4848 |
| IT2a_join | 2 | 0.000082 | [-0.001521; 0.001965] | 0.000305 | 4848 |
| Latin_Caesar_218 | 2 | 0.007777 | [0.003350; 0.012556] | 0.001090 | 3065 |
| Italian_Dante_1012 | 2 | 0.000476 | [-0.002804; 0.004186] | -0.000004 | 6075 |
| ZL3b_split | 3 | -0.000240 | [-0.001080; 0.000721] | -0.000241 | 4190 |
| ZL3b_join | 3 | -0.000191 | [-0.000932; 0.000793] | 0.000143 | 3724 |
| IT2a_split | 3 | -0.000186 | [-0.001041; 0.000822] | 0.000114 | 4111 |
| IT2a_join | 3 | -0.000186 | [-0.001041; 0.000822] | 0.000114 | 4111 |
| Latin_Caesar_218 | 3 | 0.000731 | [-0.000084; 0.001696] | -0.000058 | 2547 |
| Italian_Dante_1012 | 3 | -0.000877 | [-0.002085; 0.000427] | -0.000046 | 5161 |

## Interpretación y límites

Todos los intervalos Voynich incluyen cero. Solo César a distancia dos presenta intervalo positivo. Dante no ofrece sensibilidad suficiente en ninguna distancia; tampoco César a tres. Por ello no hay evidencia diagnóstica suficiente para excluir dependencias lingüísticas en Voynich. No comparar pérdidas absolutas entre obras. El predictor utiliza un token distante, sin condicionar el token inmediatamente anterior: no es una prueba de información incremental sobre un modelo de memoria corta. No hay recuperación semántica.

Los controles superan varios brazos Voynich. La revisión de soporte muestra 3724–4927 parejas Voynich frente a 2547–3065 César y 5161–6075 Dante; las ganancias reales negativas coinciden con calibración/desarrollo inciertos. Estos diagnósticos no explican causalmente la diferencia. Se mantiene bloqueada cualquier interpretación sustantiva de esas comparaciones, según la autoauditoría. No interpretar un resultado pequeño como ausencia de lenguaje.

## Autoauditoría

- Conciencia del objetivo: distancias propuestas después de V2 y antecedentes EXP-175/266. Exploratorio; sin parámetros elegidos con evaluación nueva. KB externa local ausente.
- Destrucción de rasgos: barajado destruye orden intencionadamente; conserva vocabulario por cadenas unitarias. Bordes y longitud pueden absorber información lingüística.
- Extrapolación: solo distancias 2/3, seis vistas y cap 2000. No evalúa todas las lenguas ni cifrados.
- Alcance negativo: sensibilidad insuficiente en controles; no concluyente.
- Controles: se esperaba ganancia positiva en textos conocidos; César d2=0,007777, Dante d2=0,000476 y d3=-0,000877, César d3=0,000731. La expectativa no se cumple de forma general; se bloquea inferencia negativa sobre Voynich.

## Verificación

Repetición completa: JSON idéntico en las dos ejecuciones. 12 brazos, 192 controles y aislamiento de las tres particiones comprobados. 100 comprobaciones de parejas por enumeración y guardia de vocabulario en 192 controles. Normalización de probabilidades comprobada para seis fuentes. El primer intento abortó por descartar cadenas unitarias; corregido antes de obtener cifras. Se conserva explicación en protocolo. Resultados completos, semillas, pesos, grupos y hashes en results.json.

Comando: `python research/analysis/2026-10-23-lag-screen/run.py`. Próximo paso: calibrar sensibilidad con procesos sintéticos de dependencia conocida antes de ampliar a más distancias. No asignar palabras españolas ni sonidos a EVA a partir de este resultado.
