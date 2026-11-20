# Nota exploratoria — contraste Currier A/B en la familia daiin (20-11-2026)

**Estado:** análisis secundario aritmético sobre los recuentos publicados en EXP-593 (commit `21a69194ee279aa6c9b7f9afce20ac7caf6ab51d`). **No se ha vuelto a parsear el corpus, no es experimento independiente, y no es evidencia de desciframiento.** No se asigna ID EXP.

## Pregunta

¿La frecuencia de aparición en posición inicial, condicionada a ocurrencia exacta de cada forma, difiere descriptivamente entre las clases Currier A y B?

## Datos, idéntica cobertura EXP-593

| Forma | A inicial/total | A % | B inicial/total | B % | OR A/B | Fisher bilateral no ajustado |
|---|---:|---:|---:|---:|---:|---:|
| daiin | 50/440 | 11,36 % | 80/278 | 28,78 % | 0,3173 | 8,37e-9 |
| dain | 11/92 | 11,96 % | 34/106 | 32,08 % | 0,2876 | 0,00109 |
| daiiin | 0/11 | 0 % | 2/8 | 25 % | 0 | 0,164 |

Los 8+ casos «unknown» de otros recuentos no se asignan a A/B. Se evita mezclar la población ampliada de EXP-590 (5.376 líneas) con la restringida de EXP-593 (4.188 líneas).

Los cálculos Fisher utilizan tablas `[[inicial_A, total_A-inicial_A], [inicial_B, total_B-inicial_B]]`. Para daiin el intervalo de confianza OR Wald aproximado del método Table2x2 es [0,2143, 0,4699]; para dain [0,1358, 0,6090]. Estos intervalos tampoco corrigen agrupación.

## Interpretación correcta

Las dos formas frecuentes tienen diferencias descriptivas de tamaño notable en el mismo sentido: son relativamente más iniciales en B que en A. **Los valores p de Fisher NO son inferencia válida por folio:** las ocurrencias comparten líneas/folios, pueden estar correlacionadas y la selección de formas fue retrospectiva; no deben promoverse a hallazgos confirmatorios. `daiiin` tiene n=19 y no permite interpretación sólida. La prueba permutacional max-T de EXP-593 responde a otra cuestión (posición frente a barajado intralínea), no valida automáticamente la diferencia A/B.

## Próxima prueba falsable requerida

1. Verificar las etiquetas Currier en cabeceras IVTFF y congelar parser, hash, política de high-ASCII y universo de folios en un manifiesto.
2. Calcular por **folio físico**, separando secciones ilustrativas para evitar confusión A/B-sección; incluir número de folios y distribución de observaciones por folio.
3. Estimar la diferencia B-A con bootstrap por folio y un nulo restringido que preserve composición de línea, longitud, posición y sección; registrar movilidad del nulo.
4. Probar las formas y métricas preespecificadas frente a controles de verdad conocida (textos y generadores); reservar datos nuevos no vistos para la evaluación cuando exista una partición no contaminada.
5. Auditar conforme a `skills/audit_experiment.md` antes de escribir en `findings.md`; no inferir significado ni clase generativa por esta sola diferencia.

## Reproducibilidad del cálculo secundario

```python
from scipy.stats import fisher_exact
for token, a, na, b, nb in [
    ("daiin", 50, 440, 80, 278),
    ("dain", 11, 92, 34, 106),
    ("daiiin", 0, 11, 2, 8),
]:
    odds, p = fisher_exact([[a, na-a], [b, nb-b]], alternative="two-sided")
    print(token, a/na, b/nb, odds, p)
```

**Procedencia:** `research/experiments/2026-11-19-exp593-*.json` en el commit señalado. Esta nota no modifica afirmaciones comprometidas.
