# Cuatro lectores históricos: verificar scripts congelados antes de ejecutar AST — 28-10-2026

**Alcance:** reparación operativa de procedencia; no es un nuevo EXP, no reejecuta simulaciones y no constituye reproducción histórica completa. **Base de rama:** `master` `d8f232f1e4c710f529df189ba83dea8752308bed`, CI push `40677514001` completada con éxito. **Estado al redactar:** propuesta pendiente de código, pruebas, CI y eventual integración.

## Defecto comprobable

`scripts/audit_remaining_reference_loaders.py::compute()` verifica las identidades de los corpus mediante manifiesto/overlay, pero **no verifica la identidad de los cuatro scripts históricos antes de extraer y ejecutar sus nodos AST**. Sus SHA-256 se calculan en `replay()` para el recibo y se comparan con `results.json` solo después de ejecutar las funciones extraídas mediante `--check`. Si un script cambia, la comprobación tardía no impide que el AST alterado se ejecute. Esto es una vulnerabilidad de orden de validación, **no evidencia de que los scripts congelados estén alterados**.

## Criterio de reparación fijado antes de la ejecución

1. Incluir cuatro SHA-256 independientes del JSON sometido a `--check`, copiados del snapshot histórico de `research/maintenance/2026-10-22-remaining-readers/results.json`. Validar bytes, ausencia de symlinks y existencia de cada script **antes** de cualquier `replay()` o extracción AST en el comando `compute()`.
2. Rechazar explícitamente un byte alterado en cualquiera de los cuatro scripts, una ruta ausente y un symlink aunque apunte a bytes idénticos. Demostrar con mocks que una alteración no alcanza la lectura de metadatos ni `replay()`.
3. En el árbol auténtico, los cuatro hashes deben coincidir con las referencias históricas; la CI debe ejecutar las pruebas y el `--check` existente con **igualdad completa** de `results.json` (sin regenerar ni sobrescribir el original). Probar también con Python `-O`.
4. Exigir ejecución `pull_request` satisfactoria del SHA final y `push` posterior en `master` antes de declarar cierre. No cambiar los corpus, los scripts históricos, los resultados, los hashes archivados, las semillas ni las particiones reservadas.

### Hashes de script previamente registrados

| Consumidor | SHA-256 archivado |
|---|---|
| `exp_267_word_length_position` | `f4197d8c18802d9d54def8d13f5ab83967d94c82f78427e77b67d92720ba4f44` |
| `exp_288_stolfi_onset_decomp` | `913ae5a8c5abd34f4bd7966aa36950e1b4d96835d5ad06f7f5aad628e27c8b32` |
| `exp_001_word_initial_entropy` | `91cb9febee7752d56fe91eeaa43155590b405b46cdd18330acb9271fd7816f59` |
| `exp_170_naibbe_simulation` | `8fe0f7d153211b320b34ca8543dac1ba029e629c4413c203fb2df0031063721c` |

## Delimitación y autoauditoría

La protección afecta al punto de entrada `compute()`/CLI. La función auxiliar `replay()` sigue aceptando fixtures sintéticos de prueba, por diseño; no se presenta como ejecutor aislado seguro de código arbitrario. La ejecución AST histórica puede contener riesgos propios: el guard de hash verifica identidad, no seguridad ni autenticidad de los scripts originales. No acredita que los archivos actuales fueran los usados en cada ejecución histórica.

No se modifica selección de tokens, métrica, tokenización, control, familia de cifrado ni umbral. **Target-awareness:** ninguna. **Destrucción de rasgos:** ninguna en el algoritmo; se añade solo una condición previa. **Extrapolación:** cuatro scripts y el comando de auditoría, no el repositorio completo. **Resultado negativo:** rechazar alteraciones sintéticas no implica detectar corrupción real. **Control:** el árbol real debe pasar y las mutaciones/symlinks deben fallar antes de `replay`. No se asignan significados al manuscrito.

EXP-170 permanece **BLOCKED** para reconstrucción histórica exacta; la Vulgata archivada sigue siendo una traducción inglesa y el Cicero archivado sigue siendo bilingüe, no baselines latinos monolingües. La adjudicación IVTFF y la conciliación de artefactos de GitHub/Biblioteca siguen pendientes. No ejecutar ciclos científicos nuevos mientras subsistan contradicciones bloqueantes.

## Comandos previstos

```bash
python tests/test_remaining_reference_loaders.py
python -O tests/test_remaining_reference_loaders.py
python scripts/audit_remaining_reference_loaders.py --check research/maintenance/2026-10-22-remaining-readers/results.json
python -O scripts/audit_remaining_reference_loaders.py --check research/maintenance/2026-10-22-remaining-readers/results.json
```

**No declarar éxito antes de observar resultados y hashes/artefactos de CI.** Conservar fallos, en su caso, y enlazarlos desde la PR.
