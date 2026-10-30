# Cierre acotado de proyecciones IVTFF: caracteres Unicode fuera de comentarios

Fecha: 2026-10-26. Tipo: reparación de validación de entrada, **sin EXP nuevo**.
Base inspeccionada: `master` `45a87075ede033dac1a0d070b678e562042e1b21`.
Estado inicial: **pendiente de CI del SHA de la PR**; no interpretar este archivo como prueba de ejecución remota.

## Defecto y alcance

El lector congelado `scripts/ivtff_lossless.py` clasifica caracteres Unicode arbitrarios como `glyph`, espacios Unicode como `layout_whitespace` y ciertos valores Unicode en `text_tag` sin emitir diagnósticos. Por ello una proyección derivada podía aceptar `d\u0430iin` (a cirílica), `da\u200biin` (separador invisible) o `da\u00a0iin` (espacio no separable), creando tipos de palabra distintos o concatenaciones no deseadas. La comprobación anterior solo rechazaba dígitos Unicode en códigos `@NNN;`.

La reparación se limita a `scripts/ivtff_rows.py`: `tokens_rows` y `tokens_scoped_rows` rechazan caracteres no ASCII en spans que representan contenido de transliteración, incluidos los de ligaduras, alternativas no elegidas y etiquetas de texto. Los comentarios `<!...>` siguen permitiendo texto Unicode libre. Se preservan el lexer histórico, los corpus y todos los resultados anteriores.

## Regresiones sintéticas deterministas

En `tests/test_ivtff_lossless.py` se añaden seis entradas adversariales: homoglifo cirílico, separador invisible, NBSP, ligadura con glifo Unicode, alternativa no seleccionada y etiqueta de texto con valor Unicode. Ambas API de proyección deben rechazarlas. Como controles negativos se comprueba que `qo<!café>dy` y un comentario Unicode dentro de una alternativa se proyectan correctamente. Permanecen las pruebas previas de `@140;` ASCII válido y de dígitos Unicode prohibidos.

Comando de verificación: `python tests/test_ivtff_lossless.py`. Este comando ya está incluido como paso explícito en `.github/workflows/voynich-check.yml`; verificar su resultado para el SHA exacto de la PR y, si se integra, de `master`. Sin datos aleatorios: semilla no aplicable. Entradas: cadenas sintéticas declaradas en la prueba, sin corpus externos, sin acceso al holdout.

## Límites y decisión

Esto **no** establece conformidad integral IVTFF ni adjudica discrepancias históricas de tokenización. El API congelado `ivtff_lossless.tokens` sigue con su comportamiento original y los scripts que lo invoquen directamente requieren auditoría propia. No se afirma que haya caracteres Unicode de este tipo en las transcripciones archivadas. No se asigna significado, idioma ni traducción.

Evidencia a comprobar: código y regresiones en la PR; log y conclusión del paso «Probar capa léxica IVTFF sin pérdida» de Voynich Check. No se borran originales ni resultados negativos. La incidencia se considerará reparada **solo para las dos API derivadas** tras superar esas comprobaciones.
