# IVTFF — cabeceras de folio físico repetidas (26-10-2026)

**Tipo:** reparación de auditoría estructural; **sin EXP nuevo ni inferencia lingüística**.
**Base exacta de la rama:** `master` `99b1cb6fba6ba3dda5658e7aa6368304c6965191`.
**Estado:** propuesta de corrección; verificar CI en la PR y, si se fusiona, en el nuevo SHA de `master`. No declarar éxito antes de ello.

## Defecto y riesgo

`scripts/audit_ivtff_page_locus_ids.py` ya contaba `page_header_count` y `distinct_page_headers`, pero `structural_errors()` no consideraba una segunda cabecera del **mismo folio físico** un error. Si los registros de la segunda aparición usan números de locus diferentes, no se produce ni error de locus duplicado ni discrepancia de página activa. Una transcripción corrupta podría dividir el mismo folio en bloques separados sin alarma, debilitando las garantías de segmentación por folio y las auditorías de procedencia. Esto **no demuestra fuga efectiva** en un experimento concreto.

Fixture adversarial sintético:

```text
<f1r> <! $L=A>
<f1r.1,@P0> daiin
<f2r> <! $L=B>
<f2r.1,@P0> chedy
<f1r> <! $L=A>
<f1r.2,@P0> or
```

El comportamiento anterior admitía esta estructura sin `structural_errors`, porque los tres registros eran distintos y coincidían con la cabecera activa. El nuevo comportamiento cuenta una cabecera duplicada y devuelve `duplicate_page_header_count=1`, con líneas primera/repetida (1/5). Otro fixture comprueba `fRos`; el fixture válido existente permanece limpio.

## Cambios acotados

- `scripts/audit_ivtff_page_locus_ids.py`: inventario de cabeceras repetidas, primera línea y repetición, con contador y fallo estructural; se conservan los datos crudos y el límite de 50 ejemplos de diagnóstico.
- `tests/test_ivtff_page_locus_ids.py`: regresiones deterministas para bloques no contiguos de `f1r` y duplicado `fRos`, sin duplicación de identificadores de locus.
- No se alteran corpus, lectores históricos, snapshots, resultados negativos, folios reservados ni `state/committed_claims.md`.

## Comprobación de alcance sobre las fuentes actuales

Inspección de las tres transcripciones en `master` con el patrón de cabeceras físicas aceptadas por el auditor; **recuento de inspección, no CI ni reproducción de experimentos**:

| Archivo | Git blob SHA | Cabeceras | Distintas | Repetidas |
|---|---|---:|---:|---:|
| `data/transcriptions/eva_zl3b.txt` | `2a4533ab9bdfa85db9bad602d590978953055df1` | 227 | 227 | 0 |
| `data/transcriptions/zl3a.txt` | `fe09c6a2f7fbc9649eecbe0c97147e00a3a86934` | 227 | 227 | 0 |
| `data/transcriptions/eva_it2a.txt` | `4d6d3f2537b1f507a257529b49c94af7d6e03446` | 225 | 225 | 0 |

Estas identidades son **Git blob SHA-1**, no SHA-256 de contenido. Para afirmar conservación de los SHA-256 archivados, ejecutar `scripts/check_corpus_integrity.py` en CI y comprobar sus logs.

## Verificación requerida

```sh
python tests/test_ivtff_page_locus_ids.py
python -m unittest discover -s tests -v
python scripts/audit_ivtff_page_locus_ids.py
python scripts/check_corpus_integrity.py
python scripts/audit_repository_operations.py
```

Los comandos y sus resultados deben confirmarse en una ejecución de Actions del SHA exacto. Los ejemplos sintéticos no requieren semillas; no se hacen permutaciones ni se consulta el conjunto reservado. No se afirma conformidad integral con IVTFF ni validación semántica.

## Limitaciones y siguiente paso

La regla es una **invariante de integridad para estos ficheros de una transcripción por folio**, no una prueba de que toda repetición de cabecera esté prohibida por cualquier variante de IVTFF. La identidad del folio y la política de lectura siguen requiriendo adjudicación independiente. Después de CI, continuar con diferencias entre lectores y auditoría de experimentos históricos que dependan de su tokenización.
