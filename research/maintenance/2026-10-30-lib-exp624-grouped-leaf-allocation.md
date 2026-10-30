# LIB-EXP-624: corrección ejecutable de la unidad de partición (hoja física)

**Fecha:** 2026-10-30. **Estado de la intervención:** reparación de código propuesta; no rehabilita puntuaciones históricas. **Sin EXP nuevo.**

## Defecto reproducido y original conservado

La auditoría previa [LIB-EXP-624](2026-10-30-lib-exp624-physical-leaf-leakage.md) demostró que **28/28** particiones históricas por ID de página compartían hojas físicas entre entrenamiento y evaluación. Se conserva sin cambios el script de Biblioteca `exp624_positional_holdout.py` (SHA-256 `1f00846ab8e91cefd07bc2dcd26ad12cf8a7c4bc7b2478d480afec391a13f3a9`), sus resultados (SHA-256 `d6e1b7490e563c96367ff10ab56feb5487d6b2775a885494f249c89f87bd4bab`) y su informe (SHA-256 `7de18cce59ea21598af7958a7ded3e05b03e305e8a6cc84c0740917b807447c4`). No se presenta un script nuevo como reproducción histórica de esos bytes.

## Corrección delimitada

`scripts/prepare_library_exp624_leaf_grouped_splits.py` reutiliza únicamente la selección histórica de páginas elegibles y el generador LCG archivado en `scripts/audit_library_exp624_leaf_leakage.py`. Cambia deliberadamente **la unidad de asignación**: recto, verso y paneles de un mismo número de hoja se agrupan antes de barajar; la división 70/30 se realiza por **número de hojas**, no por número de páginas. La salida registra por semilla los IDs exactos de hojas y páginas de entrenamiento/prueba. Rechaza IDs no reconocidos, duplicados, corpus de hash incorrecto, deriva de páginas elegibles, grupos vacíos y asignaciones distintas entre ediciones.

Fuente ZL3b: SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`. IT2a: SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`. Semillas totales: `624010 + 7919*i`, `i=0..7` por edición. Semillas por Currier A/B (ZL3b): `625010 + 7919*i`, `i=0..5` por estrato. Política de selección y algoritmo completos en el script.

**Criterio de aceptación predefinido:** las 28 asignaciones nuevas deben cubrir todas las páginas elegibles sin repetirlas y tener intersección de hojas físicas train/test vacía; cada transcripción debe aportar 203 páginas elegibles (A=114, B=81, sin etiqueta=8). Los splits totales de ZL3b e IT2a deben ser idénticos. Ninguna métrica predictiva se calcula.

## Reproducción y evidencia

Desde la raíz con Python 3.12:

```sh
python -m unittest discover -s tests -p 'test_library_exp624_leaf_grouped_splits.py' -v
python -O -m unittest discover -s tests -p 'test_library_exp624_leaf_grouped_splits.py' -v
python scripts/prepare_library_exp624_leaf_grouped_splits.py --out library-exp624-grouped-allocation.json
sha256sum library-exp624-grouped-allocation.json > library-exp624-grouped-allocation.sha256
```

El workflow `.github/workflows/voynich-check.yml` conserva JSON, SHA-256 y logs en artefactos de CI durante 90 días. **La ejecución de CI, el commit exacto y la lectura del artefacto deben verificarse tras publicar; este texto no afirma que ya hayan pasado.**

## Interpretación y límites

Se repara el mecanismo de **asignación de grupos**, no la reproducción histórica del clasificador ni su fuga ya registrada. Las ganancias históricas ~0,95–0,97 bits/unidad continúan `INVALID_FOR_CLAIM_PHYSICAL_LEAF_HOLDOUT_ONLY`. Las nuevas particiones son una propuesta técnica sobre hojas ya examinadas, **no** una validación prospectiva ciega ni una prueba de descifrado. No se entrenó ni evaluó ningún modelo, ni se asignó significado a palabras.

La selección de páginas replica el tokenizador histórico permisivo, cuya conformidad IVTFF completa está pendiente. Dos ediciones del mismo manuscrito no son controles independientes. Las particiones A/B se calculan dentro de cada estrato; no se garantiza ausencia de una hoja compartida **entre estratos** si se entrenasen modelos cruzados. Para un futuro contraste confirmatorio se requieren adjudicación IVTFF, corpus de controles y particiones prospectivas previamente congeladas.

## Autoauditoría (cinco comprobaciones)

- **Ajuste al objetivo:** la agrupación se elige para reparar el defecto observado de fuga física, no para optimizar una puntuación Voynich. Los splits no son un test confirmatorio independiente.
- **Destrucción de la característica:** el cambio conserva juntos recto/verso/paneles; no transforma tokens ni calcula la señal posicional.
- **Extrapolación:** la propiedad demostrable se limita a ausencia de intersección física en los splits generados; no a validez científica general.
- **Resultado negativo:** la invalidez de la antigua afirmación física sigue restringida al piloto y las 28 semillas auditadas; no excluye otras arquitecturas ni particiones.
- **Control:** la condición nula para esta auditoría es **cero hojas compartidas** por construcción; se comprueba exactamente, no se utiliza como contraste de hipótesis lingüística.

**Pendientes:** confirmar CI y artefactos, adjudicar IVTFF, recuperar y ejecutar bajo controles el clasificador histórico exacto solo si se autoriza y cumple los requisitos, y conservar separadas las puntuaciones originales. No se toca `state/committed_claims.md`, ni los corpus, ni los resultados congelados, ni el manifiesto prospectivo.
