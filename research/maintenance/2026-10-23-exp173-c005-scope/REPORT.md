# EXP-173 / C005 — alcance de la clasificación y del valor p (23-10-2026)

**Estado:** auditoría metodológica documental; no se crea EXP ni se reproduce el cálculo del manuscrito. Base inspeccionada: `ae090544b22ab1cb2f751b784515005c30f99815`. El bloque de cuatro lectores ya estaba integrado; no se repite. Originales y compromiso C005 intactos.

## Tres observaciones verificables

1. EXP-173 asigna Currier A/B por **folio** según la frecuencia de `edy` o `eedy` y umbral `0.05`. No usa el metadato IVTFF `$L`. Por ello la cifra histórica **6,811×** no debe atribuirse sin reservas a Currier B definido documentalmente. No se ha cuantificado aquí la diferencia respecto a `$L`.
2. La prueba F3 calcula la tasa base `am_base_b` con las mismas palabras del grupo B y aplica `binom_p(am_ll_b, n_ll_b, am_base_b)` a líneas como ensayos independientes. El `p = 6,27 × 10^-161` histórico corresponde a **ese modelo**; no es una inferencia robusta a correlación intrafolio, estimación del nulo en la misma muestra ni reclasificación por metadatos. No se recalcula ni se retracta aquí el enriquecimiento.
3. `state/committed_claims.md` incorpora la cifra en C005 y ya registra una delimitación por EXP-208 (finales de línea dentro del párrafo frente a final de párrafo). No se modifica ese registro reservado al responsable humano. La revisión no constituye contradicción numérica demostrada.

La fuente primaria para el significado de `$L` es la [especificación IVTFF 2.0 de René Zandbergen](https://www.voynich.nu/software/ivtt/IVTFF_format.pdf), que define `$L=A/B` como lengua Currier de la página o sección. Una clasificación basada en `edy` no es equivalente por definición.

## Control adversarial exacto, únicamente sintético

Supónganse 20 folios artificiales con 10 líneas cada uno, de los cuales dos tienen todas sus líneas positivas y los otros 18 ninguna. Con probabilidad nula fija `p0=0,05`, el modelo ingenuo de 200 líneas independientes produce `P[Bin(200,0.05)≥20] = 0,002664579550`. El modelo de 20 folios independientes, con correlación perfecta dentro de cada folio, produce `P[Bin(20,0.05)≥2] = 0,264160475056`. Ambas probabilidades son exactas bajo sus respectivos supuestos y **no son p-valores del Voynich**. El ejemplo demuestra sensibilidad a la unidad de independencia, no error numérico en EXP-173.

## Trazabilidad, pruebas y límites

- Fuentes archivadas: `experiments/exp_173_multiple_testing/script.py` (Git blob SHA-1 `3fb1eeb92c301d3caf841499571f5e1a8b590bcc`), `result.md` (`6c192f887af65e1153435fab1561c52fedb0f608`) y `state/committed_claims.md` (`02cb4c1780aadf4c3d94fd907621ec1416b49bed`). Son hashes Git de archivos, no SHA-256 del corpus.
- Auditor de solo lectura: `scripts/audit_exp173_c005_scope.py`; pruebas: `tests/test_exp173_c005_scope.py`; parámetros, resultados y decisiones: `results.json`. Python estándar, sin semilla ni aleatoriedad. Comprueba hashes, AST, expresiones del método y snapshot; no ejecuta EXP-173.
- Comandos desde checkout completo: `python tests/test_exp173_c005_scope.py` y `python scripts/audit_exp173_c005_scope.py --check research/maintenance/2026-10-23-exp173-c005-scope/results.json`.
- **Comprobado localmente:** cinco pruebas puras y cálculo exacto del control sintético. **No comprobado localmente:** auditor integral sobre checkout completo, nuevo p del manuscrito, sensibilidad por folio ni clasificación `$L`. La CI del nuevo commit debe verificarse separadamente; no certifica una reproducción científica.

## Próximo contraste falsable (no ejecutado)

Congelar la transcripción ZL3b y su SHA-256; usar el lector IVTFF canónico con `$L` y folios identificados. Reproducir F3 bajo la clasificación original y bajo `$L` sin cambiar simultáneamente la tokenización. Informar cruce de folios, `n`, `k`, tasa base y enriquecimiento. Después definir y auditar un nulo de permutación dentro de folio que conserve longitud de líneas y cantidad de `-am` por folio; estimar incertidumbre por bootstrap de folios. Si cambian de manera relevante la magnitud o la inferencia, someter C005 a adjudicación humana. Consultar el registro antes de crear EXP.

## Autoauditoría según `skills/audit_experiment.md`

**Target-awareness:** el ejemplo no ajusta parámetros a los valores del Voynich. **Feature-destroying:** la correlación intrafolio perfecta es deliberada y no simula el manuscrito. **Extrapolación:** solo se audita el método EXP-173 y un ejemplo sintético, no se demuestra un fallo de la magnitud F3. **Alcance negativo:** ninguna hipótesis de lengua/cifrado queda descartada. **Controles:** bajo el modelo de líneas se espera y observa 0,00266458; bajo el modelo de folios se espera y observa 0,26416048. La diferencia es consecuencia de supuestos distintos y no una señal del manuscrito.
