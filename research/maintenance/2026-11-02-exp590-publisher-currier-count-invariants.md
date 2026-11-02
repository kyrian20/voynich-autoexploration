# EXP-590: coherencia de recuentos en la exención de publicación concurrente

**Fecha:** 2026-11-02. **Base revisada:** `afed7f57adc64fa84da88f4efea2c753b5a252ed` (master después de PR #252).
**Clase:** corrección operativa de integridad; **sin EXP nuevo**, sin hipótesis científica ni traducción.

## Defecto identificable y alcance

La puerta introducida en PR #252 validaba que los recuentos EXP-590 fueran enteros no negativos, pero aceptaba un artefacto nuevo en `research/experiments/*-exp590-corrected-L-metadata.json` aun cuando el número de apariciones de `daiin` excediera los tokens, el número de líneas iniciales excediera las líneas, faltara una clase Currier o los subtotales A/B/unknown no coincidieran con el agregado. Esto podía eximir un resultado internamente contradictorio de la comprobación de deriva de fuentes al rebasar una publicación programada. No hay evidencia de que se haya publicado un resultado así.

**Criterio falsable:** un archivo nuevo con cualquiera de esas inconsistencias debe provocar `RuntimeError` en `assert_no_source_drift`; los cuatro JSON publicados, que actúan como controles positivos de esquema, deben seguir aceptándose. La validación lee el blob del commit candidato y no modifica ningún archivo histórico.

## Corrección y regresiones

- `scripts/check_publisher_source_drift.py`: exige recuentos agregados posibles, presencia de A/B/unknown, enteros no negativos en sus cuatro campos, límites por subgrupo y suma exacta de los cuatro campos de la partición a sus respectivos agregados.
- `tests/test_publisher_source_drift.py`: seis casos sintéticos adversariales (apariciones > tokens; iniciales > líneas; clase ausente; iniciales de subgrupo > líneas; suma de apariciones incorrecta; booleano en recuento de subgrupo). El control positivo existente lee los cuatro resultados versionados.

**Fuente positiva EXP-590:** `research/experiments/2026-11-02-exp590-corrected-L-metadata.json` (Git blob `b542a123e3a7a146b93564a7078a5dfefef992a7`; transcripción ZL3b declarada SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`). En el JSON congelado: 853 apariciones = 502+314+37; 161 iniciales = 60+91+10; 134 finales = 104+27+3; 5376 líneas = 1815+2806+755. No se recalcularon estos datos a partir de la transcripción.

## Reproducción y verificación

Comandos previstos en la CI canónica (`.github/workflows/voynich-check.yml`):

```sh
python -m unittest discover -s tests -p 'test_publisher_source_drift.py' -v
python -O -m unittest discover -s tests -p 'test_publisher_source_drift.py' -v
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

El resultado de CI, la URL de la ejecución, el SHA de integración y los artefactos deben comprobarse en GitHub Actions antes de declarar la reparación cerrada. No se considera una ejecución local verificada mientras no se haya realizado.

## Conservación y límites

No se modifica la fuente ZL3b, los cuatro JSON de control, los 400 vectores históricos EXP-170, sus semillas, los manifiestos de folios reservados ni `state/committed_claims.md`. Los casos sintéticos no son datos del manuscrito y no requieren semillas aleatorias. La puerta sigue siendo un control **mínimo**: no reproduce el experimento ni verifica los p-valores, el tokenizador, la procedencia histórica de EXP-170 o la conformidad IVTFF integral. No se ejecuta ningún ciclo científico mientras existan contradicciones pendientes.

**Siguiente acción:** comprobar la CI del commit de esta rama y del eventual commit de integración; continuar con procedencia de EXP-170 y conciliación IVTFF/artefactos sin sustituir entradas históricas.
