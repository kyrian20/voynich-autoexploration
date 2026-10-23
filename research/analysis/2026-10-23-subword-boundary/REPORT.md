# Predicción entre palabras con subunidades — 23-10-2026

**Estado: REPRODUCED, exploratorio.** Puerta de sensibilidad natural superada antes de procesar Voynich. No hay traducción ni discriminación de teorías.

## Resultado

Una representación de subunidades aprendida exclusivamente de entrenamiento recupera ganancia predictiva entre palabras interiores en los dos textos naturales y en las cuatro vistas Voynich examinadas. En cada fuente, el predictor entrenado sobre el orden real supera las 16 versiones entrenadas con interiores de línea barajados. Es dependencia predictiva bajo este modelo y estas particiones; no equivale a contenido semántico, sintaxis identificada o desciframiento.

| Fuente | Pares evaluados | Contextos vistos | Peso | Ganancia frente a marginal, bits/par | Intervalo exploratorio 95 % | Rango de 16 controles |
|---|---:|---:|---:|---:|---|---|
| Latin_Caesar_218 | 2547 | 2540 | 0.5 | 0.093549 | [0.070865; 0.116290] | [0.003083; 0.007017] |
| Italian_Dante_1012 | 5161 | 5161 | 0.5 | 0.234285 | [0.213007; 0.255220] | [0.010441; 0.021244] |
| ZL3b_split | 4190 | 4190 | 0.5 | 0.194366 | [0.157437; 0.215508] | [0.031511; 0.057431] |
| ZL3b_join | 3724 | 3724 | 0.5 | 0.146944 | [0.121481; 0.167946] | [0.023896; 0.036082] |
| IT2a_split | 4111 | 4109 | 0.5 | 0.163205 | [0.133229; 0.181770] | [0.022183; 0.041692] |
| IT2a_join | 4111 | 4109 | 0.5 | 0.163205 | [0.133229; 0.181770] | [0.022183; 0.041692] |

Ambos textos naturales superan la puerta fijada: >0,005 bits/par, ganancia superior a todos sus controles y límite inferior del intervalo >0. Las salidas naturales se completaron antes de las vistas Voynich; el código bloquea esas vistas si falla cualquiera de los dos textos. Las dos vistas IT2a son idénticas y no constituyen réplicas. Las cuatro vistas Voynich corresponden al mismo manuscrito.

La cobertura de contextos es casi completa frente al escaso soporte del predictor exacto anterior. **Las pérdidas de ambos modelos no se comparan directamente:** predicen objetivos distintos y usan poblaciones distintas. Este bloque no demuestra una mejora cuantitativa respecto a aquel modelo. Los únicos pares con una unidad límite desconocida son uno en César; en el resto son cero. La cobertura de contextos no establece potencia ni significado.

## Qué se midió

BPE ejecuta hasta 64 fusiones deterministas dentro de palabras, usando solo frecuencias de entrenamiento. El modelo predice la primera subunidad de la palabra siguiente a partir de la última subunidad de la actual. No cruza líneas y excluye ambos tokens extremos: una línea de cuatro palabras aporta un par. La marginal, vocabulario y representación permanecen iguales en los 16 controles; solo se baraja el interior de cada línea de entrenamiento y se recalibra el peso en desarrollo. Se conservan folios físicos en la partición heredada; los controles naturales usan sus grupos de 25 líneas heredados.

La dependencia observada puede incluir asociaciones locales de grafías, repeticiones, clases de palabras, temas o plantillas. No se ha condicionado por todas las características de los bordes, longitudes, posición exacta, sección o escriba. No se ha separado cuánto aporta la coincidencia de caracteres simples y cuánto las fusiones; ese contraste no estaba fijado y no se añade retrospectivamente como resultado favorable.

Los controles retienen el inventario y los extremos de cada línea; no destruyen necesariamente toda estructura temática ni de composición. Se esperaba que recuperasen menos dependencia local que el entrenamiento real, no ganancia exactamente cero. Se observa esa atenuación en las seis vistas. El entrenamiento barajado puede seguir aprovechando composición de línea y calibración sobre desarrollo real. No se convierten las 16 comparaciones en p-valores. Los intervalos remuestrean grupos con modelo y peso fijados; no incluyen incertidumbre de entrenamiento o decisiones previas.

## Fallo sintético conservado y reparación

La versión V1 producía +0,0095765041 bits/par en el negativo independiente balanceado y +0,7966785112 en el positivo. Falló el criterio absoluto <1e-10 y se detuvo antes de cargar fuentes reales. Se conservan código completo, protocolo V1 y salida sintética. Ese intento es INVALID_FOR_CLAIM para atribuir su mejora a dependencia.

La reparación sustituyó la interpolación aditiva por el cociente centrado y normalizado ya conocido en el proyecto. Cuando la distribución condicional coincide con su marginal empírica, el multiplicador es exactamente uno. Se fijó la reparación antes de procesar fuentes reales, sin variar los umbrales. Positivo corregido: +0,7776075787 bits/par, frente a >0,5 exigido. Negativo corregido: 0, frente a absoluto <1e-10. La ganancia artificial anterior no se suma a los resultados reales.

## Reproducción

```
python tests/test_subword_boundary.py
python scripts/analyze_subword_boundary.py --check
```

Siete pruebas cubren positivo/negativo, negativo con tamaños condicionales diferentes, normalización en contextos vistos y no vistos para toda la rejilla, reconstrucción y congelación de segmentación ante letras nuevas, desempate determinista, límites de línea y preservación de inventarios/extremos en el control. La primera comprobación de snapshot detectó además tuplas de fusiones en memoria frente a listas JSON; se normalizó la salida a listas sin cambiar el aprendizaje ni las cifras. La reproducción compara estructura e enteros y floats finitos con tolerancia 1e-12; results.json conserva unidades, fusiones, pesos, desarrollo completo, pérdidas por grupo, controles y hashes de dependencias.

## Decisión

El instrumento cumple su puerta de sensibilidad en estos dos textos naturales. Su señal en Voynich merece un contraste posterior explícito con una representación de caracteres simples y controles que preserven bordes/longitudes. Ese contraste deberá fijarse antes de ejecutarse. Este resultado no autoriza elegir una segmentación fonética, asignar significado a las unidades ni excluir textos sin significado. No se reutilizará esta evaluación como confirmación independiente.

## Autoauditoría — skills/audit_experiment.md

**Conciencia del objetivo:** se eligió una representación compacta tras observar el problema de soporte de identidad exacta; el diseño es retrospectivo y exploratorio. Las 64 fusiones y puerta se fijaron antes de resultados reales y se publican todas las vistas. El predictor se calibra en desarrollo; la representación usa solo entrenamiento. No hay tabla fonética ni calibración para un valor Voynich concreto.

**Implementación:** BPE agrupa letras EVA, no glifos paleográficos certificados. Puede representar palabras completas y perder otras dependencias al tomar solo unidades de borde y pares interiores. Una falta de señal sería injusta como prueba de ausencia de lengua; aquí no se hace esa inferencia. La corrección centrada evita el sesgo sintético observado; no garantiza ausencia de todos los sesgos.

**Extrapolación:** una representación, una partición heredada y dos textos naturales. No se afirma generalidad entre lenguas, manuscritos, clases de cifrado ni tamaños de vocabulario. No se comparan numéricamente pérdidas de objetivos diferentes.

**Alcance negativo:** el intento V1 falló su control; se conserva sin interpretación de fuentes reales. La señal positiva corregida no refuta generación estructurada. No afecta por reanálisis a las cifras de las afirmaciones públicas C001–C008.

**Controles:** se esperaba >0,5 bits en el positivo y absoluto <1e-10 en el negativo; se obtiene 0,7776075787 y 0. Se esperaba atenuación bajo barajado de entrenamiento; los máximos observados se publican en tabla y son inferiores a la ganancia real en todas las vistas. La ganancia positiva de los controles no es una sorpresa incompatible con su diseño parcialmente conservador. No se interpreta una comparación de factores contra cero ni una significación confirmatoria.

Se consultaron estado, registro y búsquedas locales antes del protocolo; ~/voynich-kb no estaba disponible. No se afirma revisión bibliográfica exhaustiva ni novedad mundial. Autoauditoría completada antes de actualizar el registro cronológico. No se modifican committed_claims.md, findings.md ni failed_approaches.md; no se asigna EXP nuevo.
