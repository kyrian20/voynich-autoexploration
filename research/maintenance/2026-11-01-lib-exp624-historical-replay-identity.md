# LIB-EXP-624 — integridad exacta del recibo de partición histórica

**Fecha:** 2026-11-01. **Base:** `master` `69e077351eddd54845fd5e262ae0aeedae582054`. **Tipo:** reparación de auditoría, no nuevo EXP ni prueba de descifrado. **Estado científico:** `INVALID_FOR_CLAIM_PHYSICAL_LEAF_HOLDOUT_ONLY` para los resultados históricos; puntuaciones confirmatorias `BLOCKED`.

## Defecto falsable y criterio de cierre

`scripts/audit_library_exp624_leaf_leakage.py::check` comparaba únicamente los **recuentos** de hojas físicas compartidas y de páginas de prueba contaminadas, además de los totales de elegibilidad. Por inspección del código anterior, un resultado en memoria con un identificador de hoja sustituido por `999`, con un ID de página contaminada inventado o con la semilla modificada mantenía los mismos recuentos y no activaba la barrera. No se ha encontrado evidencia de que los archivos congelados contengan tales sustituciones.

**Criterio:** rechazar recibos alterados aunque conserven los 28 recuentos de solapamiento; aceptar el replay de ambas fuentes originales con las semillas históricas; no modificar los originales ni reejecutar el modelo de la Biblioteca.

## Reparación y pruebas

`check` mantiene las series esperadas independientes (no sustituye su comprobación) y compara el objeto completo por edición contra un **nuevo replay determinista desde los bytes congelados y verificados por SHA-256**. Así protege las semillas, el orden y contenido de los IDs de páginas, las hojas y los campos de recuento. No es una segunda implementación independiente del algoritmo: un error compartido por `analyze` y el replay aún podría pasar; los recuentos históricos esperados limitan parte de ese riesgo.

`tests/test_library_exp624_leaf_leakage.py` incorpora dos regresiones adversariales: hoja física inventada con el mismo número de intersecciones, y cambio de semilla o de página contaminada manteniendo los tamaños. Los tests anteriores siguen verificando el corpus real y el rechazo de recuentos erróneos.

Comandos de verificación (Python 3.12):

```sh
python -m unittest discover -s tests -p 'test_library_exp624_leaf_leakage.py' -v
python -O -m unittest discover -s tests -p 'test_library_exp624_leaf_leakage.py' -v
python scripts/audit_library_exp624_leaf_leakage.py --check --out library-exp624-leaf-leakage.json
python scripts/check_corpus_integrity.py
python scripts/audit_repository_operations.py
```

La CI canónica ejecuta estos controles y archiva `library-exp624-leaf-leakage.json` con `sha256sum`. Su éxito, los artefactos y el SHA exacto de integración deben verificarse después de la PR.

## Fuentes, parámetros, negativos y límites

- ZL3b: `data/transcriptions/eva_zl3b.txt`, SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- IT2a: `data/transcriptions/eva_it2a.txt`, SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.
- Biblioteca, script: `1f00846ab8e91cefd07bc2dcd26ad12cf8a7c4bc7b2478d480afec391a13f3a9`; resultados: `d6e1b7490e563c96367ff10ab56feb5487d6b2775a885494f249c89f87bd4bab`; informe: `7de18cce59ea21598af7958a7ded3e05b03e305e8a6cc84c0740917b807447c4`.
- Reproducción de **asignación únicamente**: LCG 32 bits, Fisher–Yates, corte por páginas 70/30; ocho semillas `624010 + i*7919` por edición, seis semillas `625010 + i*7919` por estrato A/B de ZL3b. No se ajusta modelo, no se calcula rendimiento y no se genera aleatoriedad nueva.
- El control adversarial es **sintético y negativo**: debe rechazarse. El replay de los corpus originales es el control positivo.
- El lector histórico es permisivo y no equivale a una adjudicación IVTFF; el replay no es una reproducción histórica de las puntuaciones, y las particiones originales siguen contaminadas por hoja física. Las ediciones son testimonios relacionados, no muestras independientes.
- No se alteran corpus, scripts o resultados históricos, semillas, particiones prospectivas, hashes, `state/committed_claims.md` ni resultados negativos. No se asigna significado ni traducción.

**Siguiente prioridad tras CI y eventual integración:** recuperar recibos independientes que acrediten las entradas históricas de EXP-170 y terminar la adjudicación IVTFF. Evaluación general: 2026-11-22, sin promesa de descifrado.
