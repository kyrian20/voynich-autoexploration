# IVTFF: dígitos Unicode en códigos high-ASCII — 2026-10-26

**Tipo:** reparación de validación de entradas; sin EXP nuevo ni resultado lingüístico.
**Base revisada:** `master` `955c82f97c9872254c614b5c7ac93a21d0658340`.
**Estado de verificación remota:** pendiente de comprobar en la PR (no declarar éxito antes de inspeccionar CI).

## Defecto reproducible

El lexer histórico `scripts/ivtff_lossless.py` utiliza `re.match(r'@(\d{3});', ...)`. En Python, `\\d` reconoce cifras decimales Unicode. Por ejemplo, el patrón acepta tanto `@140;` como `@١٤٠;` (arábigo) y `@１２８;` (ancho completo), y `int()` convierte estas últimas en 140 y 128. Son sustituciones de caracteres que no respetan la grafía decimal ASCII del código high-ASCII IVTFF.

**Reproducción mínima (comprobada localmente con Python 3.13.5; CI usa Python 3.12):**

```sh
python - <<'PY'
import re
for s in ('@140;', '@١٤٠;', '@１２８;'):
    m = re.match(r'@(\d{3});', s)
    print(repr(s), bool(m), int(m[1]) if m else None)
PY
```

Salida observada de la comprobación mínima: `True 140`, `True 140`, `True 128`.

## Reparación acotada

Se deja **sin cambios** el lexer histórico y sus experimentos archivados. El adaptador de proyección derivada `scripts/ivtff_rows.py` vuelve a analizar cada fila (como ya hacía) y ahora rechaza los spans `high_ascii` cuyos dígitos no sean ASCII. La comprobación visita ligaduras y **todas** las alternativas, incluso las no elegidas para una vista; no confunde el texto libre de comentarios `<!...>` con códigos de transliteración.

La regresión de `tests/test_ivtff_lossless.py` cubre códigos árabes, de ancho completo, mezcla de cifras, ligadura, alternativa, ambas APIs del adaptador, control ASCII válido y comentario inocuo.

## Comprobaciones y alcance

```sh
python tests/test_ivtff_lossless.py
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

La ejecución completa y los artefactos deben comprobarse en la CI del SHA exacto de la PR y, si se integra, en la CI posterior de `master`. Los datos de prueba son **cadenas sintéticas deterministas**: no hay semilla aleatoria, corpus externo nuevo ni evaluación de folios reservados. Los hashes y logs de CI son evidencia de ejecución, no validación científica.

**Límite importante:** el API histórico `ivtff_lossless.tokens([lex(...)])` continúa aceptando estos lookalikes si se invoca directamente; esta reparación protege **solo** las proyecciones por `tokens_rows` / `tokens_scoped_rows`. La conformidad integral IVTFF y la adjudicación de resultados históricos siguen pendientes. No se reescriben corpus, snapshots ni resultados negativos. No se obtiene traducción ni significado independiente.
