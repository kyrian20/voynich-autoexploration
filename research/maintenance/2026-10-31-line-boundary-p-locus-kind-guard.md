# Control de tipo explícito y ordinal en loci P — 31-10-2026

**Alcance:** reparación técnica de la rama borrador de la PR #138, no un nuevo EXP ni una reproducción científica. La base exacta al abrir esta rama era `c2984ef72bbdeae2781ae15fb25638e1b24f8698`; `master` observado: `2579f1233444dbe8c2e81cb30f0464af4bb60e51`. Las PR #2, #8 y #10 constaban fusionadas; #7, #138 y otras PR seguían abiertas. Se conserva `results.json` original **INVALID_FOR_CLAIM** para el lector/clasificador corregidos.

## Incidencia, falsación y reparación

En `line_boundary_replication.parse()`, el sufijo de tipo `P0` o `+P0` se utilizaba para admitir filas P sin comprobar el identificador de locus anterior a la coma. Por ejemplo, `<f1r.L.2,P0> gamma.delta` se trataba como cuerpo P aunque el identificador declara explícitamente tipo L. Una ruta con componente extra, `<f1r.P.extra.2,P0>`, también se admitía con ordinal final 2. Esto puede crear positivos P→P artificiales y negativos intralínea de registros que no son P. El estándar IVTFF 2.0.2, §6.4 (tabla 9), distingue tipos de locus P/L/C/R.

**Criterio previo a las pruebas:** solo admitir como filas P los identificadores `f1r.2` o `f1r.P.2` (con página válida y ordinal ASCII), acompañados de un sufijo P válido. Un identificador con tipo explícito distinto de P, componentes extra u ordinal no numérico no aporta tokens al modelo; si aparece después de una P del mismo folio, deja una barrera física `INVALID_P_LOCUS_KIND` que impide una frontera falsa entre P anteriores y posteriores. No inventar una corrección del identificador. Los casos válidos mantienen su positivo y negativos.

**Pruebas añadidas a `tests/test_line_boundary_interposed_loci.py`:** cinco variantes sintéticas inválidas, dos formas válidas, ambas políticas `primary` y `drop_uncertain_word`, y un censo de la clase afectada sobre los dos originales. Para cada variante inválida se esperan dos negativos interiores de las P válidas y cero positivos cruzando el locus rechazado. Las formas válidas deben mantener la secuencia [0, 1, 0]. La comprobación del corpus exige autenticación SHA-256 antes del censo; no usa puntuaciones ni folios de evaluación.

## Datos, reproducibilidad y aceptación

- `data/transcriptions/eva_zl3b.txt`: SHA-256 esperado `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- `data/transcriptions/eva_it2a.txt`: SHA-256 esperado `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.
- Código: `research/analysis/2026-10-28-line-boundary-reproduction/line_boundary_replication.py`.
- Pruebas: `tests/test_line_boundary_interposed_loci.py`. Python 3.12; sin dependencias nuevas, semillas, aleatoriedad ni entrenamiento.
- Comandos requeridos (desde la raíz): `python -m unittest discover -s tests -p 'test_line_boundary_interposed_loci.py' -v` y `python -O -m unittest discover -s tests -p 'test_line_boundary_interposed_loci.py' -v`. La CI de `Voynich Check` ejecuta ambos, junto a las comprobaciones de integridad generales.
- Verificar run/commit exactos, logs y artefactos antes de afirmar éxito. La ejecución de CI no reproduce `results.json`.

## Autoauditoría y límites

1. No se ha elegido la regla a partir de AUC, AP, ganancia o palabras Voynich; se deriva de la distinción documental de tipos de locus.
2. La exclusión conservadora de un registro malformado podría disminuir cobertura; por eso se conservan los originales y se exige un censo autenticado del alcance, no una sustitución silenciosa.
3. Un censo de cero registros afectados no demuestra conformidad IVTFF global ni rehabilita los resultados del predictor.
4. No se cambia `state/committed_claims.md`, corpus, manifiestos, resultados históricos, parámetros, semillas ni hashes. No se crea un EXP ni se ejecuta un ciclo científico prohibido.
5. No es traducción ni evidencia semántica. Persisten las discrepancias de tokenización, la procedencia histórica de EXP-170 y la conciliación de artefactos.

**Estado de verificación:** pendiente de CI del commit propuesto y de comprobación posterior en la rama borrador de #138. Esta nota no declara el defecto cerrado ni la limpieza global del repositorio.
