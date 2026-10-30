# Auditoría acotada — cambios concurrentes en evidencia histórica del publicador

Fecha: 2026-10-30. Tipo: reparación de integridad, **sin EXP nuevo**. Estado: **corrección propuesta; pendiente de CI de la PR y revisión antes de integrar**.

## Fuente, contexto y alcance

- Base fijada: `master` `e080229c3dc324b9b2e4d8e97dc132d8bd414880`. El último commit de publicación añade cuatro archivos a `research/experiments/`; no tiene una CI de `push` acreditada para ese SHA. La CI verde del commit previo `f2b11989...` no lo sustituye.
- Revisadas PR abiertas #5, #7, #13, #66, #82, #138; #138 sigue siendo borrador científico con métricas históricas `INVALID_FOR_CLAIM`. PR #2 y #8 fusionadas en master; #10 fusionada en la rama de investigación y no equivale a fusión directa en master.
- Consultados README, SOUL, CLAUDE, AGENTS, norma de integridad, registro EXP, registro de iteraciones y cierre de PR #161. No se modifica ninguna transcripción, script EXP, resultado histórico, semilla ni partición de folios.
- Evidencia de defecto: `scripts/check_publisher_source_drift.py` en la PR #161 excluía **todo** `research/experiments/**` del `git diff`. En esa carpeta existen erratas y JSON históricos, no solamente salidas generadas. Una modificación concurrente de una errata o de un resultado archivado pasaba inadvertida durante el rebase de resultados, aunque podía alterar la interpretación de los archivos publicados.

## Criterio de reparación predefinido

La barrera debe rechazar **cualquier modificación o borrado** de archivos preexistentes y **cualquier archivo nuevo no perteneciente a las cuatro familias de salida** que generan los scripts programados. Solo puede permitir una **adición** (`A`) con nombre completo correspondiente a los generadores EXP-590, EXP-593, EXP-622 o EXP-623. No debe depender de los caracteres especiales de los nombres de archivo.

Se reemplaza el `git diff --name-only` con exclusión de directorio por `git diff --name-status -z --no-renames` sobre todo el árbol. Se examina el estado Git y una lista cerrada de nombres de salida. Los movimientos se descomponen en borrado + adición; los borrados nunca se eximen. Los cambios de `README`, corpus, scripts y evidencia histórica siguen siendo bloqueantes.

## Verificación y reproducibilidad

Comandos exactos de regresión:

```sh
python -m unittest discover -s tests -p 'test_publisher_source_drift.py' -v
python -O -m unittest discover -s tests -p 'test_publisher_source_drift.py' -v
```

En un entorno local aislado con repositorios Git temporales y una plantilla mínima del workflow, el código y las 14 pruebas del parche dieron **14/14 + 14/14**, sin semilla aleatoria. Este resultado local **no sustituye** la CI del repositorio completo. Las regresiones cubren adición de resultado permitido, edición de errata, edición de JSON histórico, modificación/borrado de resultado anterior, adición no reconocida, nombre con sufijo espurio, cambio de script/corpus, carrera mixta, refs inválidos y orden de operaciones.

La CI real de la PR debe confirmar el comportamiento sobre el checkout del repositorio y las pruebas de integridad habituales. Cualquier fallo se conserva y se repara sin cambiar los originales.

## Limitaciones y autocrítica

- Esta es una **reparación del contrato de procedencia**, no una reproducción científica ni una traducción.
- Un nuevo archivo con nombre permitido puede contener bytes incorrectos; el guard no comprueba contenido, licencias, firmas ni validez estadística. Las salidas nuevas siguen necesitando auditoría y hashes.
- Las modificaciones concurrentes de resultados existentes se rechazan de forma conservadora, incluso si las produjo legítimamente otro publicador; se preservan los artefactos Actions para reintento desde fuentes nuevas.
- No se han usado folios reservados ni asignado ID EXP. Las contradicciones científicas de IVTFF, EXP-170 y conciliación de Biblioteca permanecen sin resolver.
- No se afirma limpieza global ni `VALIDATED` de los resultados históricos.

## Siguiente paso

Comprobar CI de PR y SHA de master inmediatamente antes de integrar; si el merge es seguro, comprobar CI del commit de integración y la ausencia de alteración de corpus/resultados congelados. Después retomar una discrepancia IVTFF de impacto medible, sin reciclar métricas `INVALID_FOR_CLAIM`.
