# Incidencia acotada: etiquetas IVTFF inline convertidas en espacios ficticios

**Fecha:** 2026-10-29. **Estado al abrir la PR:** corrección propuesta, CI y cierre pendientes. **Sin EXP nuevo.**

## Preflight y procedencia

- Base exacta: PR #138, `e878f69f2cfa74c77d732748ed7e4e49d4c08409`, no master. Master observado en `9134d8c872f35602912512b33d27b8e9cc8bff67`.
- Se comprobaron PR abiertas #5, #7, #13, #66, #82, #138, PR #2/#8/#10 integradas, y correcciones previas #143–#153 para evitar repetirlas.
- Norma: IVTFF 2.0.2, §6.7 (solo punto, coma, <->, <~> son espacios) y §6.8 (<@X=y> es etiqueta de metadatos de alcance por línea/página). Fuente: https://www.voynich.nu/software/ivtt/IVTFF_format.pdf
- Registro consultado: `research/EXPERIMENT_REGISTER.md`, `research/RESEARCH_INTEGRITY_STANDARD.md`, `research/ivtff_tokenization_policy_2026-10-20.md` y erratas de la réplica. No se asigna un identificador EXP.

## Defecto falsable y reparación

El lector de `research/analysis/2026-10-28-line-boundary-reproduction/line_boundary_replication.py` convertía **todas** las anotaciones angulares que no fueran comentarios libres o marcadores de párrafo en espacios. Eso incluía `<@L=A>`, que no es un espacio de palabra según IVTFF. Contrafactual sintético: `ab<@L=A>cd` pasaba a `["ab", "cd"]` y podía crear un candidato negativo ficticio; la política corregida devuelve `["abcd"]`. Si hay un punto, coma o interrupción de dibujo real, la separación permanece.

**Regla de aceptación:** eliminar a anchura cero únicamente etiquetas bien formadas `<@[A-Z]=[^<>]>`, antes de procesar interrupciones de dibujo y otras anotaciones; preservar el tratamiento previo de comentarios libres, incertidumbre, párrafos y separadores. No asumir que una etiqueta malformada es válida.

## Evidencia y alcance

- Código: `research/analysis/2026-10-28-line-boundary-reproduction/line_boundary_replication.py`.
- Pruebas: `tests/test_line_boundary_inline_text_tags.py`, cinco casos: etiquetas dentro/al principio de palabras; cuatro separadores reales; marcadores de párrafo; conteo de candidatos sintéticos; auditoría de alcance de transcripciones congeladas.
- CI: `.github/workflows/voynich-check.yml`, Python 3.12 normal y `-O`.
- Comandos: `python -m unittest discover -s tests -p 'test_line_boundary_inline_text_tags.py' -v` y `python -O -m unittest discover -s tests -p 'test_line_boundary_inline_text_tags.py' -v`.
- Entradas solo de lectura, SHA-256 exigidos antes de contar: ZL3b `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`; IT2a `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.
- El test imprime por política y fuente el número de registros con etiquetas, los P admitidos y las listas de tokens que cambiarían frente al comportamiento previo. **No anticipar esos conteos antes de leer el log real.**
- Semilla: no aplica; comparación determinista, sin muestreo. Dependencias: biblioteca estándar de Python y módulos versionados del repositorio.
- El `results.json` histórico (blob Git `32756b8ec8430309079b82c288e2dd76807aead4`) permanece congelado. No se repite el predictor, no se consumen hojas reservadas, no se cambia ningún manifiesto, y no se reabren afirmaciones científicas.

## Autoauditoría de alcance

1. **Objetivo/calibración:** la regla procede de la especificación IVTFF, no de una búsqueda de mejora de AUC.
2. **Señal conservada:** los cuatro separadores explícitos siguen separando; solo desaparece el espacio inventado por una etiqueta de metadatos.
3. **Alcance:** la prueba demuestra el defecto sintético y audita su frecuencia en filas P congeladas; no certifica un parser IVTFF completo ni mide el impacto en AUC.
4. **Negativos:** si no hay etiquetas que cambien listas de tokens en las fuentes, publicar el cero; no presentarlo como mejora estadística.
5. **Controles:** marcador de párrafo, dibujo, comentario libre, ambas políticas de incertidumbre, corpus autenticados y ejecución con `-O`.

**Puerta de cierre:** CI verde en el commit exacto de la PR, lectura de logs de las cinco pruebas y sus conteos, comprobación de concurrencia antes de fusionar exclusivamente en la rama de #138, y CI posterior. Si no se cumplen, dejar la PR abierta y explicar el bloqueo. Persisten la adjudicación IVTFF integral, EXP-170 y conciliación de artefactos. No existe traducción validada.
