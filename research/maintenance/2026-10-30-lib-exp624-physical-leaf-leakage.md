# LIB-EXP-624: particiones por cara no equivalen a hojas físicas reservadas

**Fecha:** 2026-10-30. **Estado:** defecto de diseño de evaluación identificado; métricas originales conservadas, sin repetición del modelo. **Tipo:** auditoría de integridad de un piloto histórico de Biblioteca; sin asignar nuevo EXP.

## Fuente y pregunta

El informe histórico `Informe_Voynich_exp624_Control_posicional_2026-10-20.md` presenta un modelo de regularidad posicional con un 70/30 de «folios reservados». El script de Biblioteca `exp624_positional_holdout.py` selecciona *page IDs* de IVTFF (`f1r`, `f1v`, `f68r1`, etc.), no hojas físicas. Una hoja puede aportar varias caras/paneles. Pregunta falsable: **¿alguna hoja física numerada tiene texto en entrenamiento y prueba en los splits archivados?** Nulo de auditoría: intersección vacía en cada partición.

Evidencia original congelada en Biblioteca `/Investigación Voynich/` (SHA-256 de bytes materializados, no Git blobs):

- Script: `1f00846ab8e91cefd07bc2dcd26ad12cf8a7c4bc7b2478d480afec391a13f3a9` (9.109 bytes).
- JSON de resultados: `d6e1b7490e563c96367ff10ab56feb5487d6b2775a885494f249c89f87bd4bab` (8.141 bytes).
- Informe: `7de18cce59ea21598af7958a7ded3e05b03e305e8a6cc84c0740917b807447c4` (7.912 bytes).
- ZL3b `data/transcriptions/eva_zl3b.txt`: SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`; Git blob `2a4533ab9bdfa85db9bad602d590978953055df1`.
- IT2a `data/transcriptions/eva_it2a.txt`: SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`; Git blob `4d6d3f2537b1f507a257529b49c94af7d6e03446`.

## Método (sin mirar resultados predictivos)

`scripts/audit_library_exp624_leaf_leakage.py` reproduce **únicamente** la selección de páginas y los splits deterministas del script de Biblioteca, sin importar ni ejecutar su clasificador: regex original para loci `P0/Pt`, selección de primera alternativa, exclusión de llaves, extracción `[a-z]+`, existencia de tokens de longitud 2–12, LCG 32-bit, Fisher–Yates y partición 70/30 con semillas `624010 + i*7919` (8 splits). Para Currier A/B en ZL3b usa `$L` y semillas `625010 + i*7919` (6 splits por estrato). Una hoja física se identifica por el número inicial `fNNr/v`, ignorando la cara y el panel. Se enumeran los números compartidos entre train/test y las páginas de test cuya hoja también está en train.

Se recuperan **203 IDs elegibles en cada transcripción**; ZL3b contiene 114 A, 81 B y 8 sin etiqueta, exactamente como el JSON histórico. No se reestima entropía cruzada, pérdida nula, significación ni diferencias de puntuación. Las semillas de los controles de barajado intrapalabra no intervienen en esta auditoría de partición.

## Resultado de la auditoría de asignación

| Partición | Hojas físicas compartidas por split | Páginas de prueba con hoja presente en entrenamiento |
|---|---|---|
| ZL3b total (8) | 37, 46, 38, 39, 40, 43, 36, 39 | 40, 49, 41, 43, 44, 47, 36, 39 (de 61 por split) |
| IT2a total (8) | 37, 46, 38, 39, 40, 43, 36, 39 | 40, 49, 41, 43, 44, 47, 36, 39 (de 61) |
| ZL3b A (6) | 23, 25, 27, 24, 22, 20 | 23, 25, 27, 25, 23, 21 (de 35) |
| ZL3b B (6) | 23, 15, 18, 14, 16, 19 | 23, 15, 18, 18, 17, 20 (de 25) |

**Todos los 28 splits (8+8+6+6) presentan contaminación de hoja física.** En el primer split total, 37 hojas se reparten entre train/test y 40 de las 61 páginas de test comparten número de hoja con entrenamiento. Es un defecto de la afirmación de independencia *por hoja física*, no una demostración de fuga literal de tokens ni una medida de inflación de la métrica.

**Decisión de alcance:** los valores históricos de ganancia ~0,95–0,97 bits/unidad y las comparaciones A/B **no deben citarse como validación sobre hojas físicas no vistas** (`INVALID_FOR_CLAIM_PHYSICAL_LEAF_HOLDOUT_ONLY`). Permanecen como resultados exploratorios de partición por *page ID* con el nulo indicado, sin demostrar traducción ni especificidad lingüística. La falta de corpus de control, las transcripciones no independientes y la política IVTFF incompleta siguen siendo limitaciones separadas. No se afirma que los valores numéricos históricos sean erróneos ni se cambia el JSON original.

## Verificación, conservación y límites

Comando desde la raíz (Python 3.12):

```sh
python -m unittest discover -s tests -p 'test_library_exp624_leaf_leakage.py' -v
python -O -m unittest discover -s tests -p 'test_library_exp624_leaf_leakage.py' -v
python scripts/audit_library_exp624_leaf_leakage.py --check --out library-exp624-leaf-leakage.json
```

La CI `Voynich Check` ejecuta estas regresiones y archiva el JSON de evidencias durante 90 días; la ruta de salida se crea exclusivamente para evitar sobrescribir artefactos. La salida contiene por semilla los IDs de hojas compartidas y de páginas afectadas. Los recuentos se fijan por regresión; la comprobación de corpus SHA-256 falla antes de analizar bytes alterados. Semillas, filtros y política quedan en el script y en este informe. **La evidencia de CI y el commit exacto deben verificarse después de publicar; el presente informe no equivale a una CI ejecutada.**

No se han modificado las fuentes, scripts ni resultados de Biblioteca, corpus de GitHub, resultados científicos congelados, particiones prospectivas ni `state/committed_claims.md`. La reconstrucción de asignación sigue siendo una implementación independiente de la lógica del script histórico; no es una reproducción de su piloto JavaScript ni de sus puntuaciones. Un futuro estudio confirmatorio debe agrupar recto, verso y paneles por hoja física, congelar la partición antes de evaluar y usar controles naturales/cifrados sin consultar los folios reservados.
