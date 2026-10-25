# Puerta de revisión Gemini: campos anidados no vacíos (25-10-2026)

**Tipo:** reparación de validación de propuestas externas; sin EXP nuevo, sin acceso a corpus y sin resultados de desciframiento.

## Defecto comprobable

En `scripts/validate_gemini_review.py` de `master` `28e29aafbcb75a6cbaccd31081681dbbff617c8a`, los campos de `proposed_design` y `pre_registration` se aceptaban si eran cadenas o listas no vacías. Esto permitía que una propuesta con `negative_controls: [null]`, `decision_rule: [false]` o `stopping_rule: "  "` pasase la validación estructural. El informe se habría marcado `SCHEMA_VALID_ONLY` sin advertir estos campos inutilizables. No implica que se hubiera ejecutado una revisión Gemini concreta con esas respuestas.

## Reparación y controles

Se exige ahora una cadena con texto no blanco o una lista no vacía compuesta íntegramente por cadenas con texto no blanco en los doce campos anidados. Se mantiene el formato de listas válido para controles y condiciones múltiples. Las pruebas nuevas incluyen nueve entradas defectuosas y una lista válida, sin red ni credenciales.

Comando de regresión: `python -m unittest discover -s tests -p 'test_gemini_review.py' -v`. La CI canónica ejecuta este contrato y `test_gemini_review_request.py`. La rama se debe verificar por CI y comparar contra `master` antes de fusionar.

## Procedencia, alcance y límites

Base Git: `28e29aafbcb75a6cbaccd31081681dbbff617c8a`. Se modifican exclusivamente el validador y su prueba; los corpus, EXP, informes científicos, hashes originales, semillas y resultados negativos permanecen intactos. Las regresiones son deterministas y no utilizan semilla.

Esta puerta verifica **solo tipos y contenido no vacío**: no verifica veracidad científica, diversidad real de hipótesis, procedencia bibliográfica, umbrales preregistrados ni disponibilidad de modelos o créditos de API. El workflow `gemini-methodological-review.yml` sigue siendo manual y opt-in; no debe presentarse como revisión de Gemini realizada hasta disponer de una ejecución real y su recibo.
