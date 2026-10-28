# EXP-616 — rechazo de tasas booleanas en el auditor histórico (28-10-2026)

**Tipo:** reparación acotada del validador introducido por PR #132; no es un experimento de descifrado ni una reproducción de EXP-616. **Estado:** pendiente de CI e integración hasta comprobar los resultados actuales.

## Defecto concreto

En `scripts/audit_exp616_legacy_schema.py`, `check_summary` utilizaba `isinstance(valor, (int, float))` para los campos `ch_rate`, `sh_rate` y `difference_sh_minus_ch`. En Python, `bool` hereda de `int`, por lo que un `true` o `false` de JSON pasaba la comprobación de tipo. El caso sintético `ch_rate=true, sh_rate=1.0, difference_sh_minus_ch=0.0` pasaba también la igualdad aritmética: `1.0 - True == 0.0`. Así, el validador no rechazaba un esquema incorrecto.

La reparación exige tipo exacto `int` o `float` para esas tasas y conserva las comprobaciones de finitud, rango y diferencia. No cambia el tratamiento de recuentos enteros, ni los datos históricos. La regresión prueba `true`, `false` en los tres campos y un control válido con tasas numéricas.

## Procedencia y límites

Base de trabajo: commit de `master` `b0b920210f6c929f6c065826abd4217384e7e174` (PR #132). El auditor sigue exigiendo Git blob SHA-1 del archivo histórico EXP-616 `03b8316b10abd511d7bd55546ef7ac051ed97254` y los SHA-256 congelados ZL3b `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc` e IT2a `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`. La verificación de procedencia se ejecuta por el auditor existente, no por el fixture aislado.

No se han editado transcripciones, `results.json` archivado, parámetros, semillas, hojas reservadas ni afirmaciones comprometidas. El EXP-616 histórico sigue **no reproducido** porque no se dispone de su script original en la carpeta; el parche no valida tasas desde IVTFF.

## Pruebas requeridas

```sh
python -m unittest discover -s tests -p 'test_exp616_legacy_schema.py' -v
python -O -m unittest discover -s tests -p 'test_exp616_legacy_schema.py' -v
python scripts/audit_exp616_legacy_schema.py --out exp616-schema-correction.json
```

El workflow `.github/workflows/voynich-check.yml` ya ejecuta esas pruebas y conserva un artefacto derivado, por lo que no se añade otra ejecución redundante. Comprobar CI del commit de esta rama y el artefacto antes de cerrar.

## Autoauditoría

**Target-awareness:** ninguna tasa se calibra al objetivo Voynich; solo se valida un tipo JSON. **Destrucción de rasgos:** no se modifica tokenización ni datos. **Extrapolación:** la conclusión es exclusivamente que se rechazan booleanos en campos de tasa. **Negativos:** los resultados negativos históricos se conservan. **Control:** se espera aceptar tasas numéricas coherentes y rechazar booleanos; las regresiones lo comprobarán. No hay prueba semántica ni traducción.

**Siguiente paso:** verificar CI y contenido del artefacto; después continuar adjudicando discrepancias de procedencia de los experimentos predictivos sin reutilizar hojas de evaluación para elegir reglas. Evaluación general 22-11-2026.
