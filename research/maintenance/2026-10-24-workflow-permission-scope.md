# Auditoría acotada de permisos de GitHub Actions — 24-10-2026

**Estado:** propuesta técnica; CI remota pendiente. **Base:** `f2673fec153d518a1877a19cc1610ae375406bce`.

## Defecto reproducible por inspección

El auditor `scripts/audit_repository_operations.py` comprobaba que `contents` fuera `read` o `write` y rechazaba `contents: write` en jobs lectores, pero **no examinaba otros permisos de escritura**. Un workflow lector con `contents: read` y `actions: write`, o un job lector con `pull-requests: write`, superaba ese control. El único publicador también podía añadir `issues: write` sin aviso. Es una brecha del contrato de mínimos privilegios, **no evidencia de abuso ni de modificación de corpus**.

## Corrección

El auditor exige exactamente `contents: read` a nivel de workflow lector y exactamente `contents: write` al único publicador. Los overrides de job solo pueden establecer `contents: read`, o `contents: write` dentro del publicador; cualquier otro alcance, valor o forma se rechaza. El auditor continúa rechazando force-pushes y múltiples publicadores.

Se amplía `tests/test_repository_operations.py` con tres mutaciones negativas que antes pasaban inadvertidas: `actions: write` en lector, `pull-requests: write` en job lector e `issues: write` en publicador. Se mantienen los controles anteriores. La CI canónica ejecuta este archivo y el auditor completo.

## Verificación y límites

Comprobación por revisión del código anterior: los tres casos omitidos cumplían las condiciones previas del auditor; el nuevo control compara el mapa de permisos completo. **La ejecución automatizada y la CI de este commit deben verificarse antes de considerar cerrada la incidencia.** No se ha ejecutado ningún experimento científico, ninguna llamada a Gemini ni modificación de transcripciones, corpus, manifiestos, estados científicos o resultados históricos. No se asigna EXP. Los checks de Actions prueban este contrato de permisos, no la ausencia de todos los defectos operativos ni una traducción.

Siguiente paso: comprobar `Voynich Check` en el SHA de la PR, revisar los permisos reales de todos los workflows y decidir la integración sin sobrescribir trabajo concurrente.
