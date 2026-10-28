# GH-602-HELDOUT-PREDICTION y EXP-603 — auditoría de fuga por hoja física (28-10-2026)

**Tipo:** reparación de atribución histórica, sin EXP nuevo ni nuevo contraste de hipótesis. **Decisión de alcance:** INVALID_FOR_CLAIM para la afirmación de generalización a hojas físicas completamente reservadas; se preservan las puntuaciones originales, incluido el resultado negativo de GH-602. **Estado:** rama propuesta; el cierre exige CI, artefacto e integración comprobados.

## Defecto concreto

Ambos scripts históricos asignan entrenamiento y evaluación usando los ocho primeros dígitos hexadecimales de SHA-256 de `voynich-exp602:` más el identificador de **cara o panel** (`f34r`, `f34v`, `f86v3`), módulo cinco. Ninguno agrupa las caras de una hoja numerada antes de dividir. EXP-603 reutiliza exactamente la regla de GH-602. El otro EXP-602 del repositorio es una auditoría de parser y queda fuera de esta corrección.

El lector retrospectivo conserva intencionadamente la selección Latin-1, las cabeceras `$L`, P0 y la limpieza regex de los originales. No reinterpreta IVTFF ni cambia el corpus. La unidad física se obtiene del número inicial del identificador de página; `f86v3` y `f86v4` pertenecen a la hoja 86.

## Reconstrucción de metadatos con corpus congelado

| Estudio | Líneas train/test | Páginas train/test | Hojas físicas train/test | Hojas test presentes en train | Hojas test físicamente nuevas |
|---|---:|---:|---:|---:|---:|
| GH-602-HELDOUT-PREDICTION (B) | 1797/528 | 60/21 | 37/18 | **15/18** | 3 |
| EXP-603 (A+B) | 2928/919 | 148/47 | 87/39 | **32/39** | 7 |

Identidades compartidas GH-602: 34, 39, 43, 50, 55, 66, 81, 84, 86, 94, 95, 105, 111, 113, 114. Hojas test no vistas: 46, 103, 116.

Identidades compartidas EXP-603: 5, 9, 11, 17, 18, 21, 27, 28, 30, 32, 34, 37, 39, 42, 43, 44, 49, 50, 55, 66, 81, 84, 86, 94, 95, 99, 100, 102, 105, 111, 113, 114. Hojas test no vistas: 3, 4, 29, 46, 58, 103, 116.

Las cuentas se obtuvieron por una reconstrucción independiente de los metadatos con el texto de GitHub y se congelan como invariantes para el auditor Python. La prueba definitiva de elegibilidad en CI debe concordar con los 1797/528 y 2928/919 loci de los JSON históricos.

## Identidades de fuente SHA-256

- ZL3b: `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- GH-602 script: `5e708a943c8340626ef30b0acf507987e843a27f6217f3f967ebde15d6d53232`.
- GH-602 results: `1bbba43b704e679289a4a820c887810d86ee2e648d79107b53cd64845f9e9085`.
- EXP-603 script: `7577395f6655254f26772fdc84c116f543a7fbcf3cfdf86561b8d7bc8ff36b01`.
- EXP-603 results: `b099507e104cab0483cdf646d91ba9bb785ed6217df8d086428bf94bace50c4f`.

La auditoría exige todos los hashes antes de analizar los datos, rechaza enlaces simbólicos y detecta tanto cambios de recuento como sustituciones de identidades de hojas con el mismo número. Los JSON de prueba se crean exclusivamente en modo `x` (no sobrescribir).

## Reproducción y criterios de cierre

```bash
python -m unittest discover -s tests -p 'test_exp602_exp603_physical_leaf_holdout.py' -v
python -O -m unittest discover -s tests -p 'test_exp602_exp603_physical_leaf_holdout.py' -v
python scripts/audit_exp602_exp603_physical_leaf_holdout.py --out exp602-exp603-physical-leaf.json
```

La CI debe ejecutar las regresiones normales y optimizadas, contrastar ambas salidas con los resultados históricos y publicar un artefacto JSON verificable. Una CI verde no reproduce las pérdidas ni las simulaciones originales; no se debe declarar REPRODUCED para ambos experimentos.

## Autoauditoría de alcance

**Target-awareness:** selección retrospectiva del defecto de partición; no se eligió ningún parámetro de modelo ni regla lingüística mirando los resultados test. **Feature destruction:** no se alteran textos ni secuencias; se reconstruyen exclusivamente metadatos históricos. **Extrapolación:** solo se retira la afirmación de evaluación independiente por hoja física; el rendimiento histórico no se reestima. **Resultado negativo:** GH-602 ya no satisfacía su criterio positivo y sigue siendo negativo bajo su evaluación original; no se transforma en éxito. **Control:** la prueba sintética `f34r`/ `f34v` debe quedar dividida y compartir hoja 34; `f46r`/`f46v` deben permanecer juntas en test sin aparecer en train. Esta expectativa se comprueba por la regresión, no por puntuaciones del manuscrito.

## Bloqueos y siguiente acción

No se han recuperado ni reejecutado los bootstraps históricos; el sesgo de la fuga no se puede cuantificar a partir de la auditoría. El parser IVTFF sigue sujeto a adjudicación, EXP-170 carece de entradas originales exactas y las PR científicas pendientes requieren revisión humana. El siguiente paso, tras verificar CI y fusionar, es revisar otro experimento predictivo no auditado o preparar un protocolo prospectivo por hoja física, sin utilizar los folios reservados para seleccionar reglas. Ninguna observación permite asignar significados ni afirmar descifrado. Evaluación general: 22-11-2026.
