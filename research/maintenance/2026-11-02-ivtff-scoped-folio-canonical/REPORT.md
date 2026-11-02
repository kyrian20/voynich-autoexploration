# Guardia de identidad canónica para folios en proyecciones IVTFF acotadas

**Fecha:** 2026-11-02. **Base de trabajo:** `master` `b95cdb8ea90c7625fc2f72f70f8242293b9d959b`. **Clase:** reparación de integridad de metadatos sintéticos; no experimento nuevo, sin traducción.

## Defecto, antecedente y criterio de falsación

La PR #44 incorporó `tokens_scoped_rows` para impedir que las continuaciones `/` crucen el ámbito (fuente, folio). La PR #77 rechazó etiquetas compuestas y caracteres invisibles, pero dejó `FOLIO_LABEL_RE` con `[0-9]+`. En consecuencia, `f01r` y `f1r` podían ser **dos ámbitos distintos para la misma página física**, y `f0r` también era aceptado como etiqueta válida. Los auditores de páginas ya comparan alias físicos (#211/#223); esta API auxiliar aún no aplicaba la misma precaución.

**Criterio fijado antes de CI:** `tokens_scoped_rows` debe rechazar `f0r`, `f00r`, `f01r`, `f001r`, `f086v6` y `f00086v6` como etiquetas de ámbito no canónicas, incluso cuando se intercalan con etiquetas válidas. Debe conservar `f1r`, `f86v6`, `fRos`, las uniones legítimas `a/` + `/b` en el mismo ámbito y el rechazo previo de ámbitos intercalados. No debe tocar los bytes de ninguna transcripción.

## Cambio implementado

- `scripts/ivtff_rows.py`: restringe **solo la API de proyección acotada** a números de folio positivos sin ceros iniciales (`[1-9][0-9]*`). La validación general de IVTFF sigue pudiendo leer identificadores crudos y compararlos por identidad física; no se reescriben las fuentes.
- `tests/test_ivtff_lossless.py`: doce casos adversariales de etiquetas no canónicas (seis etiquetas en dos contextos) y un control positivo de continuación y paneles.
- No se cambian `scripts/ivtff_lossless.py`, corpus originales, manifiestos de holdout, semillas, resultados históricos, resultados negativos, registros EXP ni `state/committed_claims.md`.

**Pruebas exigidas (no se presuponen aprobadas):**

```sh
python tests/test_ivtff_lossless.py
python scripts/check_corpus_integrity.py
python scripts/audit_repository_operations.py
```

La CI canónica `.github/workflows/voynich-check.yml` incluye el primer comando. Verificar la ejecución del head exacto de la PR y, si se integra, la ejecución posterior de `master` antes de declarar el cierre. No hay semilla aleatoria ni resultado numérico de descifrado en esta reparación; el criterio es determinista.

## Limitaciones y próximos pasos

Los IDs de fuente y folio siguen siendo **aportados por el llamador**; esta comprobación no autentica que el registro pertenezca a ese folio ni impide errores en los consumidores que no usen `tokens_scoped_rows`. Los ejemplos adversariales son sintéticos; no se afirma que haya alias en los corpus congelados. La conformidad IVTFF completa, la conciliación de artefactos y la reproducción exacta de EXP-170 permanecen bloqueadas o pendientes. PR #7/#138 requieren adjudicación científica separada. No iniciar ciclos científicos con contradicciones pendientes.

**Próximo paso:** comprobar CI y artefactos del head, confirmar que `master` no ha cambiado y fusionar únicamente si las pruebas son satisfactorias. Fecha de evaluación general: 22-11-2026, sin promesa de descifrado.
