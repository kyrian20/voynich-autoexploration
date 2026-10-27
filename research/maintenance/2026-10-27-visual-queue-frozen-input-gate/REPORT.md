# Entrada congelada de la cola visual — 27-10-2026

**Tipo:** reparación operativa, sin EXP nuevo ni inferencia semántica. **Estado inicial:** propuesta; CI y comparación archivada pendientes de verificación. Base `master`: `76ccea96856ec33dc36f346b7ca2d9e03e15c4e8`, push CI [40453993558](https://github.com/kyrian20/voynich-autoexploration/actions/runs/40453993558) `success` antes de este cambio.

## Defecto, alcance y control negativo

El CLI `scripts/prepare_visual_annotation_queue.py` aceptaba directamente `json.loads(gzip.decompress(...))` del inventario visual y exportaba `annotator-queue.json.gz` y `coordinator-map.json.gz` sin comprobar el reparto congelado de hojas ni que cada fila correspondiera a una línea real de las transcripciones originales. Una copia manipulada podía intercambiar hojas de entrenamiento y prueba o alterar/omitir una etiqueta, conservando identificadores y hashes *declarados*, y producir paquetes sin error. No se ha demostrado corrupción en los archivos archivados. Es distinto del consumidor de cobertura reparado en PR #94 y del piloto de PR #93.

Se reutiliza `load_verified_coverage_inputs`, ya existente, que comprueba la sal y asignación histórica de los 102 folios, las claves JSON únicas del manifiesto, los hashes de fuentes, la vinculación de cada fila a los bytes originales y la completitud del censo L/R. El guard se ejecuta **antes** de crear los paquetes. `build` sigue siendo un helper para fixtures: invocarlo directamente no verifica fuentes. No se modifica la selección ni se autoriza ninguna imagen/anotación.

## Regresiones deterministas

Cinco pruebas nuevas en `tests/test_visual_annotation_queue.py`:
1. Archivo intacto: comparar **bytes gzip exactos** de los dos paquetes contra los originales congelados.
2. Rechazar intercambio `train/test` de tamaño constante.
3. Rechazar miembros JSON duplicados en el manifiesto.
4. Rechazar una línea de origen falsificada en el inventario.
5. Rechazar la omisión de una fila seleccionada L/R.

Las mutaciones existen solo en memoria. No se utilizan semillas aleatorias. El workflow `.github/workflows/voynich-check.yml` ya ejecuta este módulo de pruebas, el CLI y las comparaciones byte a byte. No se crea un workflow adicional ni se disparan ejecuciones redundantes.

## Entradas y conservación

- `data/transcriptions/eva_zl3b.txt`, SHA-256 de registro `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- `data/transcriptions/eva_it2a.txt`, SHA-256 de registro `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.
- `research/decipherment/2026-10-23-prospective-leaf-holdout/manifest-v2.json`.
- `research/decipherment/2026-10-25-label-inventory/inventory.json.gz`.
- Salidas archivadas: `research/decipherment/2026-10-25-visual-annotation/annotator-queue.json.gz` (SHA-256 `e7cc96675c1a7ebe9cfc5e9e88ab848ea20c065e63565ec08d4bf23fa6c4b7c5`), `coordinator-map.json.gz` (`ed5861f938d39a07bbc12faeaa46307b4d7963149cd6599e38cc36b725518f02`).
- Hashes anteriores tomados de informes/manifiestos archivados; **no** recalculados en un checkout local en esta sesión.
- Los corpus, inventario, manifiesto, paquetes históricos, resultados negativos, registro de EXP y `state/committed_claims.md` quedan intactos.

## Comprobaciones de aceptación

```sh
python -m unittest discover -s tests -p 'test_visual_annotation_queue.py' -v
python scripts/prepare_visual_annotation_queue.py --out-dir /tmp/voynich-visual-queue
cmp research/decipherment/2026-10-25-visual-annotation/annotator-queue.json.gz /tmp/voynich-visual-queue/annotator-queue.json.gz
cmp research/decipherment/2026-10-25-visual-annotation/coordinator-map.json.gz /tmp/voynich-visual-queue/coordinator-map.json.gz
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

CI y hashes reales de la ejecución deben documentarse tras finalizar; no se infiere éxito de la mera publicación de esta propuesta.

## Autoauditoría, límites y siguiente paso

No se han usado etiquetas EVA como resultados ni se ha seleccionado regla semántica: es un guard de procedencia, no un experimento de descifrado. El control negativo son las mutaciones que deben fallar; el positivo es el replay byte a byte. No hay calibración a un resultado deseado ni transformación destructiva de texto. No certifica conformidad IVTFF total, alineación etiqueta-imagen, independencia histórica de folios reservados ni significado de ninguna palabra.

Revisar la CI de la PR, sus logs y la comparación de los dos paquetes; comprobar que `master` no ha avanzado antes de fusionar. Después verificar CI de `master` y continuar con adjudicación IVTFF/procedencia histórica. No declarar limpieza global.
