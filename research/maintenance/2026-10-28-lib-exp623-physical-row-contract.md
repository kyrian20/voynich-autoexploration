# LIB-ORDER-2026-10-19-A/B — contrato de líneas físicas en auditoría (28-10-2026)

**Tipo:** reparación de integridad del auditor de particiones; **no** es un EXP nuevo ni reproducción de puntuaciones históricas. **Estado:** propuesto en rama; pendiente CI y revisión de integración.

## Defecto y alcance

`scripts/audit_library_exp623_leaf_leakage.py` recorría tanto la elegibilidad del piloto A como la del piloto B mediante `str.splitlines()`. Python considera separadores de línea a ocho caracteres que no delimitan una fila física IVTFF: U+000B, U+000C, U+001C, U+001D, U+001E, U+0085, U+2028 y U+2029. Por ejemplo, un carácter de este conjunto dentro del cuerpo de un locus seguido de `<f2r>` podía promover una cabecera incrustada a una fila separada, alterando la reconstrucción de páginas elegibles y sus estratos.

Este defecto es demostrable con **datos sintéticos adversariales**, no se ha demostrado su presencia en los corpus originales. No cambia la conclusión de que los dos pilotos históricos de Biblioteca separaron por cara y no por hoja física.

## Reparación acotada

- Reutilizar `scripts/ivtff_physical_rows.py::checked_physical_lines` en **ambos** lectores de elegibilidad, conservando CR, LF y CRLF como delimitadores físicos válidos.
- Rechazar explícitamente los ocho separadores no físicos en vez de normalizarlos a filas nuevas.
- Añadir dos regresiones: ocho separadores adversariales frente a ambos lectores y tres estilos válidos de fin de línea.
- Mantener sin cambios el algoritmo de barajado, las semillas, la agrupación Currier `?`, las 60 particiones históricas y los controles de SHA-256 de su evidencia.

## Datos inmutables y criterio de cierre

- ZL3b: SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- IT2a: SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.
- Programas históricos de Biblioteca: hashes conservados en `research/maintenance/2026-10-28-lib-exp623-physical-leaf-leakage.md`; no se reescriben ni se incorporan a GitHub.
- La CI existente ejecuta los tests normales y con `python -O`, y `python scripts/audit_library_exp623_leaf_leakage.py --check --out library-exp623-leaf-leakage.json`. `--check` debe confirmar que siguen idénticos los 60 recuentos, hashes de filas, tamaños, semillas y listas de hojas compartidas, además de los ocho folios sin `$L`.
- Solo declarar la reparación integrada tras comprobar los logs de CI del SHA de la rama, la PR y el commit final. Conservar cualquier fallo intermedio.

## Interpretación y límites

**Resultado adversarial local aislado:** el lector físico compartido rechaza los ocho separadores y admite LF/CR/CRLF; esto no equivale a ejecutar la suite del repositorio. No se leen tokens de prueba para escoger una regla, no se entrena un predictor y no se infieren significados.

El estado de los pilotos sigue siendo **INVALID_FOR_CLAIM** para evaluación con hojas físicas completamente reservadas. La reparación protege la auditoría frente a filas falsas; no reproduce ni invalida por sí sola sus puntuaciones predictivas.

**Siguiente paso:** verificar CI y artefacto de esta rama; después revisar si los experimentos predictivos históricos que aún alegan holdout físico agrupan ambas caras, antes de seleccionar cualquier hipótesis con folios reservados. Evaluación general: 22-11-2026, sin prometer descifrado.
