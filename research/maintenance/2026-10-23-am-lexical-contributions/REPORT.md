# -am/final: descomposición por forma léxica — 23-10-2026

Estado: **REPRODUCED** para la descomposición y su snapshot. Sensibilidad descriptiva retrospectiva, sin traducción ni significación confirmatoria. Población heredada de la base local `15d3b6b0b9c134656599007dcb2e5c0cb1068517`.

## Resultado

El exceso agregado no depende de una sola forma proyectada. Al excluir del rasgo objetivo cualquiera de las formas terminadas en am, el cociente observado/esperado restante sigue por encima de uno en las ocho políticas de cada transcripción. Las líneas y todos sus tokens permanecen intactos: no se borran palabras ni se desplazan extremos.

| Fuente | Líneas B/P0 sin marcador explícito | Formas -am, vista por defecto | Finales -am | Esperanza por línea | Rango O/E restante: todas las formas y ocho políticas |
|---|---:|---:|---:|---:|---:|
| ZL3b | 1.883 | 146 | 325 | 38,48430 | 7,84850–8,57457 |
| ZL3a | 1.883 | 146 | 325 | 38,48430 | 7,84850–8,57457 |
| IT2a | 1.867 | 142 | 324 | 39,01975 | 8,23175–8,42119 |

Las ediciones representan el mismo manuscrito y están relacionadas; no se cuentan como tres replicaciones independientes. Los rangos son una sensibilidad exhaustiva finita, no intervalos de confianza.

En la vista split/primary/expand de ZL3b, la forma con más finales es am (35 de 325). Al dejar de contar am como objetivo quedan O=290 frente a E=34,38553: O/E=8,43378. Otras formas con muchos finales son otam (21), dam (20), qokam (19), okam (17) y ram (10). Se publica el inventario completo, incluidas formas sin apariciones finales. No se afirma que cada forma individual esté enriquecida.

## Método y controles

Para cada forma w, O_w es el número de líneas cuyo último token es w. E_w=sum_i count_i(w)/n_i, esperanza de situar w al final bajo intercambio uniforme dentro de cada línea. Se usan fracciones exactas. Las sumas por forma reconstruyen exactamente O y E del snapshot anterior para cada una de las 24 combinaciones fuente/política. El cálculo (O-O_w)/(E-E_w) cambia solo qué tokens cuentan como rasgo, conservando los denominadores de línea.

Cinco pruebas automatizadas pasaron. Una enumera exhaustivamente todas las líneas de longitud 1–5 sobre {a,xam,yam} y todas sus permutaciones, con multiplicidad: la media enumerada coincide exactamente con E para el sufijo completo, cada forma y su complemento. Otras cubren aditividad, conservación del texto, formas sin finales, ausencia de rasgo, denominador restante cero y rechazo de líneas vacías. No se usa Monte Carlo ni semilla.

El protocolo se escribió antes de ejecutar este paquete, después de conocer el patrón histórico. El script regenera resultados y compara el snapshot completo. Se añaden las dos órdenes de reproducción a Voynich Check; la CI del commit publicado debe verificarse separadamente.

```
python tests/test_am_lexical_contributions.py
python scripts/audit_am_lexical_contributions.py --check research/maintenance/2026-10-23-am-lexical-contributions/results.json.gz
```

## Antecedentes y límites

EXP-086 ya describía varias formas -am y EXP-136 trataba párrafos mediante otro lector. Este paquete no descubre por primera vez la diversidad ni reproduce esos experimentos: añade una descomposición racional exacta y exclusión exhaustiva de una forma en el universo reciente. El cotejo de antecedentes se limita al repositorio; no se consultó un KB externo disponible.

Una forma proyectada puede contener incertidumbre o códigos opacos según la política. No se adjudican palabras, glifos o morfemas. La ausencia de marcador no demuestra interior de párrafo. La selección de -am, B y P0 es retrospectiva. No se equiparan secciones, manos o longitudes de palabras, ni se prueba asociación residual con el token precedente. No se elimina un conjunto de varias formas a la vez. No se distinguen lengua, cifrado o generación artificial.

## Autoauditoría — skills/audit_experiment.md

**Target-awareness:** sufijo, población y ocho políticas se heredan de análisis conocidos. La conclusión es condicional a esa selección; no hay calibración nueva para maximizar el efecto ni validación independiente.

**Implementación:** excluir una forma del rasgo no elimina sus tokens del inventario. Conserva longitudes y posiciones y evita una exclusión que desplazaría artificialmente el final. Las políticas aún pueden cambiar proyecciones; se informa toda la rejilla.

**Extrapolación:** la conclusión se limita a las exclusiones de una forma, una a una, en estas líneas y vistas. No se afirma clase funcional cerrada ni causalidad.

**Alcance negativo:** no se rechaza una teoría de producción o una lectura semántica. La persistencia agregada tampoco confirma la función gramatical de -am.

**Controles:** se espera que la media de finales de todas las permutaciones de cada fixture sea exactamente E, porque cada posición es equiprobable. El control produce igualdad racional exacta en todos los casos enumerados, también por forma y complemento. Se espera que las sumas por forma reproduzcan O/E del paquete anterior; se observa coincidencia exacta en las 24 combinaciones. No se detectó discrepancia de control.

No se modifican committed_claims.md, findings.md ni failed_approaches.md; no se asigna EXP nuevo.

Siguiente cuestión distinta: cuánto aporta el contexto precedente una vez conservados posición, bordes y longitud. Este paquete no la ejecuta; antes de formular ese contraste hay que reconciliarlo con EXP-607 y V2 de orden residual.
