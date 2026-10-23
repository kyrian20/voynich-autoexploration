# Soporte efectivo de la corrección de identidad — 23-10-2026

Estado: **REPRODUCED**, diagnóstico descriptivo del predictor existente. No es una prueba de lengua, potencia estadística ni traducción.

## Resultado

La capa de identidad de dos predecesores solo dispone de distribuciones de entrenamiento distintas en el 7,29–8,27 % de las tripletas de evaluación Voynich. En César es 0,42 % y en Dante 2,95 %. En las demás tripletas, la corrección centrada es algebraicamente neutra con estas tablas, incluso si se fijara un peso positivo. La falta de ganancia anterior no permite descartar dependencias lingüísticas: este predictor tiene muy poco soporte efectivo para medirlas. Esto no demuestra que la escasez sea la única causa del resultado ni que otra representación vaya a funcionar.

| Fuente | N evaluación | H2 ausente | W2 ausente con H2 visto | Identidad única | Proporcional | Distribución distinta | Distinta con ≥5 ejemplos |
|---|---:|---:|---:|---:|---:|---:|---:|
| ZL3b_split | 4927 | 3300 | 657 | 582 | 4 | 384 (7.79 %) | 74 |
| ZL3b_join | 4457 | 3185 | 586 | 358 | 3 | 325 (7.29 %) | 54 |
| IT2a_split | 4848 | 3270 | 682 | 495 | 0 | 401 (8.27 %) | 81 |
| IT2a_join | 4848 | 3270 | 682 | 495 | 0 | 401 (8.27 %) | 81 |
| Latin_Caesar_218 | 3065 | 2524 | 65 | 463 | 0 | 13 (0.42 %) | 0 |
| Italian_Dante_1012 | 6075 | 3822 | 296 | 1778 | 0 | 179 (2.95 %) | 40 |

Ninguna tripleta Voynich ni César en la categoría distinta tiene 20 ejemplos W2 en entrenamiento; Dante tiene siete. No se interpreta 5 o 20 como umbral de potencia. Los recuentos de desarrollo también se publican en results.json; no se cambia selección de pesos. Las vistas IT2a coinciden y no son réplicas independientes.

## Por qué la corrección se anula

W2 compara la distribución de objetivos para una identidad concreta con la distribución agrupada H2, dentro de la misma firma de extremos/longitud y contexto del predecesor inmediato. Si H2 o W2 no se observaron, la implementación usa cociente uno. Si H2 contiene una sola identidad, ambas distribuciones son iguales. Si hay varias identidades pero la distribución de la identidad evaluada es proporcional a H2, también lo son. En los tres casos el multiplicador centrado es uno para todos los objetivos y su normalización es uno. La comparación se hace con productos de enteros; no depende de redondeos.

La quinta categoría indica únicamente que la distribución puede cambiar con peso positivo. No garantiza una mejora para el objetivo observado, ni predicción lingüística útil. Con el peso cero elegido previamente en las cuatro vistas Voynich, la corrección efectiva sigue siendo cero en todas las tripletas. No se cambia ese peso ni se reevalúa el test para escoger otro modelo.

## Verificación y continuidad

Se conservaron las entradas, vocabulario, partición por folios físicos y pesos del análisis anterior. Los N, contextos H2/W2 vistos y pesos coinciden exactamente con sus seis salidas archivadas. Los controles sintéticos positivo y negativo producen, respectivamente, 100 % de distribuciones distintas y 100 % proporcionales. Se comprueban además identidad única, H2 ausente y W2 ausente. No se cruzan líneas ni se usan objetivos de evaluación para construir tablas.

La ejecución push de la base e522c552676f3791e3c2ecff31113a3d584bcef1 fue comprobada en la colección completa de Actions: [39941371054](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39941371054), completed/success. Es evidencia de esa base; este cambio requiere su propia comprobación.

Reproducción: `python scripts/audit_two_token_identity_support.py --check`. Protocolo previo y hashes de entradas/código acompañan los resultados.

## Decisión de investigación

Cerrar esta variante de memoria exacta como instrumento no discriminante en estas condiciones. El siguiente diseño debe fijar una representación con mayor reutilización entre contextos, aprendida solo de entrenamiento, y acreditar sensibilidad en controles naturales antes de interpretar Voynich. No se fijan aquí segmentos, sonidos ni significados; elegirlos para mejorar el resultado evaluado invalidaría su uso confirmatorio.

## Autoauditoría — skills/audit_experiment.md

**Conciencia del objetivo:** el diagnóstico se eligió tras observar el escaso rendimiento del predictor. Las categorías se fijaron antes de contar fuentes reales; los umbrales 5/20 son descriptivos. No es confirmatorio.

**Implementación:** las firmas detalladas y UNK limitan la reutilización y pueden suprimir información. Se mide esa limitación sin sustituirla silenciosamente. La neutralidad es una propiedad de estas tablas y esta corrección, no del manuscrito.

**Extrapolación:** seis vistas ya seleccionadas, una partición y vocabulario 2000+UNK. Los porcentajes no representan todos los modelos, lenguas ni segmentaciones.

**Alcance negativo:** no se puede concluir ausencia de dependencia por falta de ganancia de este predictor. No se afirma que una alternativa vaya a recuperarla.

**Controles:** se esperaba 100 % distinto en el positivo y 100 % proporcional en el negativo balanceado, por construcción; se obtiene exactamente eso. También pasan los tres casos límite y la reconciliación con la salida anterior. No se calcula significación ni se compara una métrica Voynich con un nulo para decidir lengua. La KB externa no está disponible en esta copia; la búsqueda local detecta cobertura bruta previa, no esta descomposición.

No se modifican committed_claims.md, findings.md ni failed_approaches.md; no se asigna EXP nuevo.
