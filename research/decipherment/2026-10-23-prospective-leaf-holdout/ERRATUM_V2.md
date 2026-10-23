# Errata y manifiesto prospectivo v2: paneles de desplegables

Fecha: 23-10-2026. Estado: **PROPOSED** hasta que la CI del commit exacto concluya correctamente.

## Defecto real identificado

El lector del manifiesto v1 utilizaba `^<f(\\d+)[rv](?:[.,][^>]*)?>`, que reconoce `<f69r.1>` pero no `<f67r1.1>` ni `<f68r2.1>`. Los sufijos numéricos tras r/v representan paneles de desplegables; son parte del mismo folio físico. En las transcripciones ZL3b e IT2a, un recuento de cabeceras sobre los bytes del repositorio da **92 hojas detectadas por v1 y 102 por la expresión corregida**. Las diez omitidas por v1 son **67, 68, 70, 72, 85, 86, 89, 90, 95 y 102** en ambas ediciones. Este es un error de cobertura, no una señal lingüística.

## Reparación sin reescribir historia

- Se conservan sin editar `scripts/prepare_prospective_leaf_holdout.py`, el manifiesto v1 y su run CI histórico.
- Se añade `scripts/prepare_prospective_leaf_holdout_v2.py` con lector de paneles y manifiesto `manifest-v2.json`, marcado como sustituto del v1 **para reglas futuras**.
- Se conserva exactamente la sal v1 `VOYNICH-FUTURE-RULES-2026-10-23-v1` y la función de asignación. Las 92 hojas antiguas mantienen el grupo que ya tenían; solo se asignan las diez hojas anteriormente omitidas. No se reabre ni se mueve ninguna hoja del conjunto de prueba previo.
- La nueva población esperada es **102 hojas**: entrenamiento 68, desarrollo 16, prueba 18 (añadidas 6, 2 y 2 respectivamente).
- La CI comprueba ambos manifiestos por reproducción byte a byte y conserva el v2 como artefacto adicional. Las pruebas sintéticas verifican identificadores de panel, disjunción, cobertura y no reasignación de las hojas antiguas.

## Riesgos y límites

Esta corrección no crea un test históricamente ciego: se conocen las hojas y existen análisis previos. El grupo de prueba debe permanecer excluido de cualquier ajuste posterior de reglas. La asignación por hash no estratifica por sección, idioma Currier o escriba; informar desequilibrios antes de inferencias científicas. Las dos ediciones no son muestras independientes. El parser de cabeceras no es un parser IVTFF completo. No se asigna significado ni se declara traducción.

## Reproducción prevista

```sh
python -m unittest discover -s tests -p 'test_prospective_leaf_holdout_v2.py' -v
python scripts/prepare_prospective_leaf_holdout_v2.py --out prospective-leaf-holdout-v2.json
cmp research/decipherment/2026-10-23-prospective-leaf-holdout/manifest-v2.json prospective-leaf-holdout-v2.json
```

## Autoauditoría de alcance

- **Conocimiento del objetivo:** ninguna regla ni parámetro se ajusta a una métrica del Voynich. La sal se mantiene para preservar la asignación anterior.
- **Destrucción de características:** no se altera una sola línea del corpus ni la tokenización; solo se corrige la cobertura de cabeceras. La selección de hojas comunes sigue siendo una restricción.
- **Extrapolación:** el resultado es un recuento de cobertura, no una prueba de hipótesis lingüística.
- **Resultado negativo / controles:** el defecto v1 queda documentado, no borrado; se prueba el caso que fallaba y que el lector v1 no lo reconocía.
- **Control comparativo:** se esperaba que v1 omitiese los paneles y que v2 añadiese exactamente diez hojas. Recuento observado por inspección de cabeceras: 92 frente a 102 en ambas fuentes; la CI debe confirmar la reproducción del manifiesto exacto.

No se actualizan `state/committed_claims.md`, hallazgos ni resultados históricos. No se asigna EXP nuevo.
