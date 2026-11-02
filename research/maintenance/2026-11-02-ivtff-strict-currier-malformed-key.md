# Guardía IVTFF: claves Currier malformadas en el auditor estricto

**Fecha:** 2026-11-02. **Base:** `master` `b00fedfa43f902438b7a5bbfbd00065a0db469fe`. **Tipo:** reparación de integridad operativa, sin nuevo EXP. **Estado:** propuesta; cerrar únicamente después de comprobar CI del head y de `master` tras integración.

## Defecto y alcance

`scripts/audit_ivtff_metadata_strict.py` usaba `re.findall(r'\\$L\\b', metadata)` para detectar asignaciones Currier. El límite de palabra `\\b` impide reconocer claves dañadas con un carácter de palabra después de L: `$Lfoo`, `$L1=A`, `$L_foo`. Si no había otra asignación, el auditor devolvía `None` y la página se trataba como no clasificada; si existía una asignación válida, podía ignorar el campo malformado adicional. Esto es distinto de la corrección en los lectores Zhang–Sheng de PR #241: el auditor estricto seguía usando su propio detector.

**Prueba previa a la reparación:** con Python, el patrón antiguo devuelve `[]` para esos tres ejemplos y detecta `$L=A`. Es un defecto demostrable en datos sintéticos; no se ha demostrado que aparezca en los corpus congelados.

## Reparación falsable

- En `scripts/audit_ivtff_metadata_strict.py`, detectar todo prefijo `$L`, sin `\\b`. La validación preexistente exige exactamente un valor completo A o B y rechaza múltiples marcadores, incluidos los nombres dañados.
- En `tests/test_ivtff_metadata_strict.py`, seis cabeceras adversariales deben producir `ValueError`; un caso positivo conserva la asignación con espacios y campos `$Q`/`$I` adicionales.
- En `.github/workflows/voynich-check.yml`, ejecutar también el módulo de regresiones con `python -O`.

Comandos de aceptación:
```sh
python tests/test_ivtff_metadata_strict.py
python -O tests/test_ivtff_metadata_strict.py
python scripts/audit_ivtff_metadata_strict.py
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

## Preservación, riesgos y decisiones

Se conservan los bytes de todas las transcripciones, scripts históricos, resultados congelados, semillas, particiones y manifiestos de folios reservados. No se cambia `state/committed_claims.md` ni se ejecutan simulaciones. La reparación solo afecta al **rechazo de metadatos inválidos** por el auditor aditivo, no recalcula la clasificación Currier histórica ni demuestra conformidad IVTFF integral. El patrón estricto rechaza incluso prefijos `$L` en metadatos descriptivos: la política es deliberadamente conservadora y debe reconsiderarse si aparece un ejemplo válido conforme a la especificación.

**Criterio de cierre:** CI de la PR verde para el head exacto, pruebas adversariales visibles, inspección de `master` antes de fusionar, y CI posterior de `master` observada. Si alguna falla, dejar la PR abierta y registrar el fallo, sin declarar éxito.

**Pendientes ajenos a esta incidencia:** EXP-170 `BLOCKED` para reproducción histórica exacta (falta vínculo probatorio con entradas externas), conciliación IVTFF completa, conciliación global de artefactos, revisión científica de PR #7/#138. No hay evidencia semántica ni traducción validada. Evaluación global: 2026-11-22, sin promesa de desciframiento.
