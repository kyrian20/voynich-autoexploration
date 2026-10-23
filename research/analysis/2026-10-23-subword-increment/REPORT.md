# ¿Añade información la última subunidad frente a su último carácter?

23-10-2026. Estado: **REPRODUCED, exploratorio**, comprobación local completa de snapshot. Python 3.12.14, biblioteca estándar. Protocolo fijado antes de ejecutar este contraste; partición de evaluación reutilizada. Sin ID EXP nuevo.

## Resultado

El contexto BPE no muestra incremento respaldado frente a su último carácter en las cuatro vistas Voynich. Los incrementos puntuales son negativos y todos sus intervalos incluyen cero. En los dos textos naturales, el incremento es positivo con intervalos por encima de cero. Este contraste mide el instrumento y esta representación; no demuestra ausencia de lenguaje, equivalencia de modelos o un mecanismo de generación sin significado.

| Fuente | Pares | Ganancia BPE frente a base | Ganancia carácter frente a base | Incremento BPE, bits/par | Intervalo pareado exploratorio 95 % |
|---|---:|---:|---:|---:|---|
| ZL3b_split | 4190 | 0,194366 | 0,213189 | −0,018823 | [−0,035184; 0,006802] |
| ZL3b_join | 3724 | 0,146944 | 0,157261 | −0,010317 | [−0,028785; 0,013695] |
| IT2a_split | 4111 | 0,163205 | 0,180335 | −0,017131 | [−0,040239; 0,014536] |
| IT2a_join | 4111 | 0,163205 | 0,180335 | −0,017131 | [−0,040239; 0,014536] |
| César latino | 2547 | 0,093549 | 0,045598 | 0,047951 | [0,031250; 0,063330] |
| Dante italiano | 5161 | 0,234285 | 0,172100 | 0,062185 | [0,045287; 0,079878] |

Ambos modelos predicen exactamente la misma primera subunidad BPE siguiente sobre los mismos pares interiores, con base y representación aprendidas solo de entrenamiento. Solo cambia el contexto: última unidad completa o su último carácter. Los pesos se calibran separadamente en desarrollo con la misma rejilla. Las cifras BPE reproducen las del bloque anterior. El contexto de carácter recupera la señal predictiva sin necesitar el contexto multicaracter BPE en las vistas Voynich ensayadas; esto no significa que explique toda dependencia posible entre palabras. El objetivo sigue siendo una subunidad BPE y se conserva información multicaracter en él.

## Control estricto y su soporte

Se barajan palabras interiores de entrenamiento dentro de cada línea y clase (primer carácter, último carácter, longitud). Se conservan caracteres extremos y longitudes en cada posición, inventario de cada línea y sus dos palabras extremas. Son 16 entrenamientos con representación/base congeladas y recalibración sobre desarrollo real. No es una prueba confirmatoria ni una distribución de p-valores.

| Fuente | Posiciones interiores entrenamiento | Posiciones con alternativa léxica | Ganancia BPE de los 16 controles, bits/par |
|---|---:|---:|---|
| ZL3b_split | 15837 | 983 | [0,190180; 0,194003] |
| ZL3b_join | 14415 | 942 | [0,143906; 0,147485] |
| IT2a_split/join | 15538 | 989 | [0,160921; 0,163626] |
| César | 9203 | 54 | [0,092381; 0,094665] |
| Dante | 15141 | 94 | [0,232619; 0,233723] |

Solo 6,21–6,53 % de posiciones Voynich y 0,59–0,62 % naturales admiten cambiar de palabra bajo estas restricciones. Son oportunidades, no cambios efectivos ni pares independientes; results.json guarda cambios efectivos por semilla. La semejanza entre controles y orden real es esperable con tan poco soporte. Algunos controles superan ligeramente al real en ZL3b_join, IT2a y César. Se investigó su alcance: la diferencia máxima es aproximadamente 0,00112 bits/par y las restricciones dejan casi intacto el entrenamiento. Por ello no se usa esa comparación para interpretar el manuscrito ni refutar dependencia; no se afirma cálculo de potencia. El contraste principal sigue siendo la comparación pareada de modelos, no el rango de barajados.

## Reproducción y alcance

```
python tests/test_subword_increment.py
python scripts/analyze_subword_increment.py --check
```

Positivo sintético con último carácter constante: incremento 0,7776075787 bits/par. Negativo independiente balanceado: 0. Las puertas se ejecutan antes de cargar corpus reales. Se verifican identidad de objetivos, marcador desconocido, preservación de inventario/extremos/clases, determinismo y soporte de alternativas distintas. Se conservan resultados completos por grupo, calibración, controles, semillas y hashes de dependencias.

Los intervalos remuestrean grupos físicos heredados (folios para Voynich; grupos de 25 líneas en textos naturales), con aprendizaje y pesos fijos: no incorporan incertidumbre de entrenamiento ni decisiones previas. IT2a split/join son idénticas y las transcripciones proceden del mismo manuscrito. Dos textos naturales no representan todas las lenguas ni cifrados. Las limitaciones de IVTFF y del lector heredado permanecen. No se prueban otras segmentaciones ni se hace búsqueda de pesos sobre test.

## Autoauditoría — skills/audit_experiment.md

**Conciencia del objetivo:** el contraste responde a la limitación publicada del bloque anterior, con conocimiento de su señal; es exploratorio y reutiliza evaluación. No se ajustan fusiones, fórmulas o umbrales a las cifras nuevas. Se publican las seis vistas completas.

**Implementación:** el contexto de carácter elimina deliberadamente el detalle adicional que se contrasta, preservando exactamente el objetivo; BPE sigue siendo grafía EVA, no morfología certificada. La selección interior y las unidades pueden perder otras dependencias; no sería una prueba justa de ausencia de lenguaje y no se usa como tal.

**Extrapolación:** la conclusión se limita a 64 fusiones, una partición, una rejilla y estos corpus. El mejor rendimiento puntual del modelo simple no establece que toda dependencia se reduzca a caracteres. No hay discriminación de teorías ni recuperación semántica.

**Alcance negativo:** no se respalda incremento BPE en estas vistas; no se rechaza la clase de modelos multicaracter ni se demuestra equivalencia. Ninguna cifra histórica o afirmación pública C001–C008 se reanaliza o sustituye.

**Controles:** se espera incremento >0,5 en el positivo y absoluto <1e-10 en el negativo; se obtienen 0,7776075787 y 0. Se espera que el control estricto pueda atenuar dependencia adicional solo donde tenga movilidad; el soporte publicado muestra que mueve muy poco. Se investigaron los pequeños excesos sobre el real antes de interpretar y se descarta usar este control como evidencia discriminante. No se usan factores contra cero ni se atribuye significación al rango de 16 controles.

Autoauditoría completada antes de actualizar el registro cronológico. Se preservan committed_claims.md, findings.md y failed_approaches.md. La siguiente prueba útil requiere un control con movilidad suficiente y evaluación nueva; repetir más permutaciones de este control no resuelve su escaso soporte.
