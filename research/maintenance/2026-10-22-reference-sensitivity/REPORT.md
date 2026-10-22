# Sensibilidad de la referencia de EXP259 — 22-10-2026

Estado: **REPRODUCED**, únicamente las dos tablas de referencia histórica y el diagnóstico de sensibilidad. No equivale a validación lingüística del experimento completo. Fuente: `96609813191caff5478ced3f5f7d4a90ed701fe7`.

## Resultado

Las 12 filas de entropía marginal y las 11 filas de entropía condicional del control histórico coinciden a la precisión publicada. El archivo usado contiene 112.081 tokens y mezcla latín e inglés. No se encontró un error aritmético en esas dos tablas: el problema es su interpretación como muestra monolingüe latina.

Además, el alfabeto observado del archivo histórico contiene **26 letras ASCII**, frente a las 23 afirmadas por el informe original. Por tanto, su máximo teórico para ese inventario observado es log2(26) = 4,70044 bits, no log2(23) = 4,52356. Normalizar por un alfabeto nominal exige justificarlo; no se ha corregido silenciosamente el informe original.

Se conserva la tokenización ASCII y el cálculo de EXP259. Dos implementaciones, una mediante H(X,Y)−H(X) y otra calculando directamente H(Y|X), coinciden con tolerancia de 1e-12 bits en las tres vistas. La variante del cuerpo latino de César se usa como sensibilidad; no como sustitución definitiva del control de Cicero.

| Posición desde 0 | Bilingüe histórico | César archivo completo | César cuerpo | N cuerpo |
|---:|---:|---:|---:|---:|
| 0 | 4.236011 | 4.179004 | 4.090588 | 20516 |
| 1 | 3.814643 | 3.741057 | 3.654310 | 20301 |
| 2 | 4.119244 | 4.148587 | 4.107849 | 17640 |
| 3 | 3.994312 | 3.831915 | 3.725879 | 15685 |
| 4 | 3.967320 | 3.812277 | 3.780389 | 13582 |
| 5 | 3.929846 | 3.753503 | 3.685503 | 11130 |
| 6 | 3.859639 | 3.647148 | 3.618376 | 8603 |
| 7 | 3.882529 | 3.679360 | 3.611012 | 6077 |
| 8 | 3.810313 | 3.688038 | 3.544251 | 4185 |
| 9 | 3.814947 | 3.551557 | 3.436586 | 2670 |
| 10 | 3.791114 | 3.396014 | 3.320968 | 1512 |
| 11 | 3.625109 | 3.360180 | 3.258934 | 760 |

Entropías en bits. Los conteos completos, entropías condicionales, alfabetos observados, hashes y diferencias están en [results.json](results.json).

## Interpretación y límites

César contiene 23.626 tokens al leer el archivo entero y 20.516 bajo el recorte del cuerpo declarado. El contraste entre esas vistas mide el efecto de excluir material editorial en ese archivo. La entrada bilingüe y César difieren también en autor, obra, longitud y composición: sus diferencias no estiman aisladamente la contaminación inglesa. No se controla aquí el sesgo de tamaño de los estimadores de entropía.

El límite de palabras ASCII fragmenta ciertos caracteres ajenos a ese inventario; por eso este recuento no debe confundirse con la tokenización Unicode del bloque de orden residual. Cada diagnóstico mantiene su política explícita. A posiciones tardías solo llegan palabras largas: no son posiciones alineadas con la terminación de cada palabra.

No se ha vuelto a ejecutar el parser del manuscrito ni validado sus rangos Currier simplificados, su selección de etiquetas o su alfabeto EVA. Las tablas del manuscrito y las conclusiones comparativas continúan pendientes. Una estructura de caracteres no demuestra traducción ni discrimina por sí sola entre lenguaje y producción artificial estructurada.

## Reproducción y controles

```sh
python tests/test_reference_entropy_sensitivity.py
python scripts/audit_reference_entropy_sensitivity.py --check research/maintenance/2026-10-22-reference-sensitivity/results.json
```

Cuatro pruebas: transición determinista de cero bits, transición independiente de un bit, supervivientes por longitud y coincidencia con las funciones históricas aisladas. No se importa ni ejecuta el cuerpo del experimento. Los hashes congelados de entrada se comprueban antes del cálculo; el modo `--check` exige igualdad del JSON completo.

## Autoauditoría

- Conocimiento del objetivo: no se ajustan parámetros a una métrica del Voynich; se fija el protocolo antes de ejecutar.
- Destrucción de rasgos: se conserva la política ASCII histórica para aislar la sensibilidad; su posible fragmentación se declara.
- Extrapolación: no se estima el efecto causal del inglés ni se validan otras tablas del experimento.
- Resultado negativo: ninguna inferencia sobre ausencia de lenguaje o imposibilidad de descifrado.
- Controles: se reproducen ambas tablas archivadas y coinciden las dos formulaciones matemáticas; los ejemplos de resultado conocido pasan.

## Siguiente comprobación

Adjudicar un control monolingüe de Cicero con offsets de origen y revisar las mediciones del manuscrito mediante el lector canónico. Solo entonces podrá evaluarse una comparación corregida con menor confusión por cambio de obra. No se asigna un nuevo EXP ni se modifica ningún compromiso histórico.
