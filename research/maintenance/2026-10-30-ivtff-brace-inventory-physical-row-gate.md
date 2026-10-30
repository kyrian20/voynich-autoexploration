# Inventario de ligaduras IVTFF: cierre de filas físicas falsas y etiquetas malformadas

**Fecha:** 2026-10-30. **Tipo:** reparación de software y regresiones de integridad; no es un EXP nuevo. **Estado inicial:** propuesta en rama, pendiente de CI del SHA final y revisión de integración. No rehabilita ningún resultado lingüístico.

## Defecto reproducible y riesgo

El inventario descriptivo `scripts/audit_ivtff_brace_spans.py` separaba filas con `str.splitlines(keepends=True)` sin comprobar los separadores físicos. Python considera U+2028, NEL, VT y otros caracteres como límites de línea; un texto `# comentario\u2028<f1r.2,@P0> {falso}` podía convertirse en un registro aparentemente válido y sumar una ligadura falsa. Además, el `RECORD_PREFIX_RE` aceptaba dígitos Unicode mediante `\\d` y una etiqueta pegada al texto sin separador (`<f1r.2,@P0>junk`), sin puerta de estructura previa en `main`.

La prueba adversarial es **sintética**. No hay evidencia de esos defectos en los tres corpus congelados; no se presenta como cambio de sus conteos. El inventario era descriptivo, no un validador completo de IVTFF.

## Corrección acotada

- `scripts/audit_ivtff_brace_spans.py`: verifica filas con `checked_physical_lines` antes de utilizar `splitlines(keepends=True)`, conservando offsets de caracteres; exige `structural_errors(audit_text(...)) == []` antes de publicar recuentos; limita los dígitos de los loci a ASCII y exige separador tras `>`. El inventario histórico de todos los spans fuera de comentarios se conserva, no se reescribe.
- `tests/test_ivtff_brace_spans.py`: regresiones para los ocho separadores falsos, etiqueta pegada, dígitos Unicode y control de las tres fuentes congeladas; se ejecutan en Python normal y optimizado.
- `.github/workflows/voynich-check.yml`: conserva JSON de inventario, SHA-256 y registros en artefacto de CI (90 días).

## Línea base real, comprobada antes del cambio

GitHub Actions `master` `591a2a7f4f65ebef4e9911dbef44493a922b6b10`, [run #41070017868](https://github.com/kyrian20/voynich-autoexploration/actions/runs/41070017868), `success` el 2026-10-30. Se inspeccionó el log del job `124111332271` para el inventario v3:

| Fuente | SHA-256 congelado | Ligaduras en cuerpos de loci |
|---|---|---:|
| ZL3b | `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc` | 446 |
| ZL3a | `56419297682d338ff1a0a17f5ae251e3ee3e2c5bf05a62db04c5385ef30b36a2` | 444 |
| IT2a | `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5` | 0 |

**Criterio de aceptación predefinido:** todas las regresiones pasan con Python normal y `-O`; las tres fuentes originales mantienen los hashes y los recuentos anteriores; el auditor estructural acepta las fuentes reales; la CI de la PR se ejecuta en el head exacto, y se verifica el JSON y su SHA-256 del artefacto. Si se integra, comprobar por separado CI `push` del nuevo `master`.

## Reproducción

```sh
python -m unittest discover -s tests -p 'test_ivtff_brace_spans.py' -v
python -O -m unittest discover -s tests -p 'test_ivtff_brace_spans.py' -v
python scripts/audit_ivtff_brace_spans.py > ivtff-brace-inventory.json
sha256sum ivtff-brace-inventory.json > ivtff-brace-inventory.sha256
```

No hay aleatoriedad ni semilla. Los scripts históricos, resultados negativos, transcripciones, folios prospectivos y `state/committed_claims.md` no se alteran.

## Límites y autoauditoría

Esta reparación impide falsos recuentos ante entradas estructuralmente defectuosas, pero **no** demuestra una diferencia en los corpus actuales ni certifica conformidad IVTFF 2.0.2 completa. No se modifica el criterio de lectura de ligaduras, ni se ejecuta un predictor, ni se asignan significados. La prueba adversarial se eligió para falsar la integridad del lector, no para maximizar una señal Voynich. La señal real permanece descriptiva. Quedan pendientes la adjudicación de alternativas/ligaduras IVTFF, EXP-170 exacto y conciliación de artefactos. La prioridad posterior es una discrepancia de datos/procedencia con impacto real, no nuevas variantes del mismo guardia sin evidencia.
