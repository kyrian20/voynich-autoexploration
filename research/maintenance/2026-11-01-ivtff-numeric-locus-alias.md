# IVTFF — alias decimal de un mismo locus físico (reparación acotada)

**Fecha:** 2026-11-01. **Base revisada:** `master` `c9487758519abc0abe39271d807719edc3096a57`. **Clase:** integridad estructural del lector; **no** experimento científico. **Estado científico:** sin cambio; reproducción exacta de EXP-170 **BLOCKED**.

## Defecto concreto y criterio falsable

Los lectores `scripts/audit_ivtff_page_locus_ids.py` y `scripts/audit_holdout_locus_coverage.py` guardaban los identificadores completos como cadenas para detectar duplicados. El patrón admitía de 1 a 3 dígitos en el número de línea. Así, `<f1r.1,@P0>` y `<f1r.01,@P0>` eran dos cadenas distintas aunque señalan la **misma línea física numérica** del mismo folio, código de locus y transcriptor. Los contadores de registros podían aceptar ambas observaciones sin advertencia. La coincidencia del SHA de una fuente sintética y su manifiesto no elimina esa ambigüedad.

**Criterio de aceptación predefinido:** ambos auditores deben rechazar la pareja numéricamente equivalente con el mismo folio/código/transcriptor, incluidos paneles y `fRos`, pero deben conservar como diferentes los identificadores con otro código de locus o transcriptor. La salida estructural del corpus original no debe cambiar si no contiene tales alias. No se prohíbe globalmente la escritura `.01` cuando aparece sola: se evita contarla dos veces junto a `.1`.

## Cambio

- El auditor IVTFF estricto compara la clave `(page, int(num), code, transcriber)` para detectar duplicados. Mantiene el campo de informe `duplicate_record_tag_count` y el identificador textual original para diagnóstico.
- El auditor independiente del holdout compara `(page, int(line), locator+transcriber)` antes de certificar la cobertura; no decodifica tokens.
- Regresiones sintéticas en `tests/test_ivtff_page_locus_ids.py` y `tests/test_holdout_locus_coverage.py`: `f1r`, `f86v4`, `fRos`; control negativo con otro locator; y modificación sintética de fuente con SHA de manifiesto actualizado.

## Ejecución y verificación requerida

Desde la raíz, Python 3.12:

```sh
python tests/test_ivtff_page_locus_ids.py
python -m unittest discover -s tests -p 'test_holdout_locus_coverage.py' -v
python -O -m unittest discover -s tests -p 'test_holdout_locus_coverage.py' -v
python scripts/audit_ivtff_page_locus_ids.py
python scripts/audit_holdout_locus_coverage.py --out /tmp/voynich-ivtff-alias-coverage-UNIQUE.json
```

Comprobar el estado y los logs de la CI de la PR, y de `master` **después** de una posible integración, en los SHA exactos. No interpretar este informe como una ejecución remota por sí solo.

## Límites y conservación

El defecto se deduce del código anterior y se comprueba con datos **sintéticos**; no hay evidencia aquí de duplicados de este tipo en las transcripciones originales. La auditoría sigue siendo estructural, **no** conformidad IVTFF completa ni adjudicación de los desacuerdos de tokenización. Los corpus originales y sus hashes congelados, manifiestos, particiones por hoja, semillas, scripts históricos, salidas negativas, `state/committed_claims.md` y EXP-170 no se modifican. No se han asignado significados a glifos ni ejecutado ciclos científicos bloqueados.

**Siguiente prioridad:** recuperar recibos y bytes de entrada de EXP-170 para vincular la ejecución histórica con una revisión concreta de Naibbe; sin esa prueba permanece `BLOCKED`. La evaluación global está prevista para el 22-11-2026, sin promesa de descifrado.
