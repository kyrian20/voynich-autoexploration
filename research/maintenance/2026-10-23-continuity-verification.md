# Verificación local de continuidad — 23-10-2026

Base comprobada: `15d3b6b0b9c134656599007dcb2e5c0cb1068517`, rama master. Este recibo documenta una reproducción local; no añade un experimento, una prueba confirmatoria ni una traducción.

## Ejecución efectuada

| Comando | Resultado |
|---|---|
| python tests/test_exp173_currier_crosswalk.py | 6 pruebas, OK |
| python scripts/audit_exp173_currier_crosswalk.py --check research/maintenance/2026-10-23-exp173-currier-crosswalk/results.json | Snapshot completo coincidente |
| python tests/test_exp173_line_null.py | 4 pruebas, OK |
| python scripts/audit_exp173_line_null.py --check research/maintenance/2026-10-23-exp173-line-null/results.json | Snapshot completo coincidente |
| python tests/test_exp173_reader_bridge.py | 8 pruebas, OK |
| python scripts/audit_exp173_reader_bridge.py --check research/maintenance/2026-10-23-exp173-reader-bridge | Ambos snapshots completos coincidentes |
| python tests/test_exp173_paragraph_strata.py | 5 pruebas, OK |
| python scripts/audit_exp173_paragraph_strata.py --check research/maintenance/2026-10-23-paragraph-strata/results.json | Snapshot completo coincidente |

Total: 23 pruebas y cuatro comandos de reproducción, todos con retorno cero. El árbol de trabajo permaneció limpio después de ejecutarlos. Se reutilizan las salidas y hashes existentes, sin duplicar corpus ni regenerar resultados históricos para publicarlos como nuevos.

La consulta de ejecuciones de GitHub Actions para este SHA devolvió una lista vacía. No se atribuye CI satisfactoria a este commit; tampoco se interpreta la ausencia de ejecuciones como fallo. Este recibo requiere su propia comprobación si se publica en otro commit.

## Qué queda respaldado

Los cálculos descriptivos del cruce Currier, esperanza por línea, puente de lectores y estratos por marcador son reproducibles en esta copia del repositorio. La igualdad con snapshots prueba reproducibilidad computacional; no independencia del método ni corrección científica global. Las fixtures aportan cobertura finita, no conformidad completa IVTFF.

En particular, el exceso -am/final permanece en P0 sin marcador explícito, dentro del alcance publicado. Ausencia de marcador no equivale a interior de párrafo. No se asigna una función gramatical o significado a -am.

## Siguiente decisión científica pendiente

El informe de estratos pide pasar a contexto léxico y posición preservando estructura de línea/folio. Antes de implementarlo, cotejar los antecedentes, especialmente EXP-607 y el bloque residual V2, para no repetir un contraste genérico de bigramas.

Una prueba útil deberá separar identidad léxica de sus bordes, longitud y posición; fijar población, unidades y controles antes de ejecutar; y mostrar que el control conserva las variables que pretende conservar. Las variantes de transcripción del mismo manuscrito no cuentan como muestras independientes. Este párrafo es una condición de diseño, no un protocolo registrado ni un resultado ejecutado.

No se alteran committed_claims.md, findings.md ni failed_approaches.md. No se asignan IDs EXP nuevos.
