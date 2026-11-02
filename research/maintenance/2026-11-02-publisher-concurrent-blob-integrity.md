# Publicador — rechazo de artefactos concurrentes corruptos

**Fecha:** 2026-11-02. **Clase:** reparación operativa acotada, sin EXP nuevo. **Base:** `a591feae9a3b7e953a4c42084f4f6018dced6f96`. **Estado científico:** no cambia; sin traducción.

## Defecto verificable

`scripts/check_publisher_source_drift.py` permite ignorar, durante el rebase del publicador, una adición en `master` si su nombre coincide con uno de los ocho outputs programados y el modo Git es `100644`. Antes de esta reparación, **no examinaba los bytes** del blob. Un archivo vacío, JSON truncado, JSON con claves duplicadas o `NaN` podía pasar como una adición inocua. El permiso de rebase no certifica su contenido, pero debe fallar ante corrupción básica en lugar de eximirla.

## Criterio de regresión

Una adición concurrente con nombre permitido y modo `100644` debe **bloquear** la exención si está vacía, es texto blanco, no es UTF-8, tiene JSON inválido/ambiguo/no finito o una raíz JSON que no es objeto. Un JSON objeto válido y un informe Markdown no vacío deben conservar la exención. Una modificación de archivos ya existentes, de scripts, de corpus o de resultados históricos continúa bloqueada.

## Reparación

- Se leen los bytes del **blob del commit candidato** mediante `git cat-file blob <object-id>`, no los del árbol de trabajo susceptible de carreras.
- JSON: UTF-8, objeto raíz, claves únicas incluso anidadas, sin `NaN`/`Infinity`. Markdown: UTF-8 y contenido no blanco. No se interpretan métricas, procedencia ni esquemas científicos.
- La comprobación existente de modo `100644` sigue precediendo a la lectura.
- Ocho nuevas pruebas sintéticas, seis rechazos de JSON, uno de Markdown y un control positivo Markdown; se mantienen los controles anteriores de Git, ancestros, symlinks, edición y contenido válido.

## Reproducción

```sh
python -m unittest discover -s tests -p 'test_publisher_source_drift.py' -v
python -O -m unittest discover -s tests -p 'test_publisher_source_drift.py' -v
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

Las pruebas operan sobre repositorios Git temporales. No ejecutan cifradores, no alteran corpus ni resultados congelados, no cambian seeds/holdouts y no realizan nuevas inferencias estadísticas. Conservar el SHA de la PR y de la CI al verificar; no inferir éxito de esta nota.

## Límites

Es una barrera de integridad **sintáctica** para outputs añadidos por otro publicador; no verifica esquema específico de EXP-590/593/622/623, hashes de inputs, corrección estadística ni validez científica. No prueba que hubiera un output corrupto en master ni repara la procedencia histórica de EXP-170. La adjudicación IVTFF integral, las contradicciones comprometidas y la conciliación de artefactos continúan pendientes.
