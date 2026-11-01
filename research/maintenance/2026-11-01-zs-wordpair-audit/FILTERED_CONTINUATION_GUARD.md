# Reparación acotada: continuaciones IVTFF interrumpidas por filas excluidas

**Fecha:** 2026-11-01  
**Base inspeccionada:** `master` `bd6b21dbc608f7420c5a641bd69364e89919c456`  
**Tipo:** defecto de lector y regresión; **no** experimento nuevo ni descifrado.

## Defecto y reproducción adversarial

`read_pages(..., categories={"P"})` filtraba los registros por categoría **antes** de reconstruir las cadenas de continuación con `/`. Al guardar solo las filas P, dos fragmentos P físicamente no contiguos podían convertirse en vecinos artificiales si entre ellos había un registro excluido (por ejemplo, `@L0`), una línea vacía o un comentario físico.

Fixture sintético mínimo:

```text
<f1r> $L=A
<f1r.1,@P0> dai/
<f1r.2,@L0> ignored
<f1r.3,@P0> /in
```

La implementación anterior concatenaba `dai` e `in` como `daiin` pese a que la cadena está interrumpida físicamente. Esto es una **posibilidad de corrupción silenciosa del lector**, no una demostración de que ocurriera en los corpus congelados.

## Reparación

El lector principal conserva el ordinal de la fila física para cada registro seleccionado. Si una continuación `/` pendiente salta una o más filas físicas, se rechaza con `ValueError: Interrupted IVTFF continuation`. Las continuaciones contiguas válidas se mantienen y las filas independientes separadas por categorías excluidas siguen siendo independientes. No se modifica `read_pages_legacy`: es una proyección ASCII histórica con limitaciones propias, sin reconstrucción de continuaciones.

Se añaden regresiones sintéticas para interrupción por categoría, comentario y línea vacía, más controles positivos de continuación contigua y filas independientes.

## Verificación requerida y alcance

Desde la raíz, ejecutar:

```sh
python -m unittest discover -s tests -p 'test_zs_wordpair_source_lock.py' -v
python -O -m unittest discover -s tests -p 'test_zs_wordpair_source_lock.py' -v
python -m unittest discover -s tests -p 'test_zs_wordpair_archive_contract.py' -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

Comprobar además el resultado del workflow `.github/workflows/voynich-check.yml` en el commit exacto de la PR y, si se integra, en el commit posterior de `master`. El contrato de archivo reproduce **solo dos de las 54 filas**, no todo el histórico. Las dos transcripciones fijadas siguen identificadas por sus SHA-256 y SHA Git en `SOURCE_LOCK`. Las 54 filas de `results.json` quedan congeladas y no se reescriben.

**Limitaciones:** las regresiones adversariales usan texto sintético. Una CI verde no demuestra conformidad IVTFF completa, ni que este defecto afectara al material original. La métrica Zhang–Sheng continúa siendo una reimplementación parcial, y la separación histórica por páginas comparte cuatro hojas físicas entre mitades; no sirve como validación held-out independiente. EXP-170 y la conciliación general de artefactos permanecen fuera de este arreglo.

**Estado de cierre:** pendiente de CI y verificación de artefactos al abrir la PR; registrar posteriormente el run exacto. No se modifica ninguna afirmación semántica ni `state/committed_claims.md`.
