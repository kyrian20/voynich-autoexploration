# Auditoría de la revisión externa Gemini 001 — ch/sh

Fecha: 2026-10-24. Estado: **REVIEWED PROPOSAL / NO VALIDATED EXPERIMENT**.

## Procedencia
- GitHub Actions: https://github.com/kyrian20/voynich-autoexploration/actions/runs/40133431957
- Artefacto: `gemini-method-review-40133431957-1` (ID 12575314834).
- Modelo informado por receipt: `gemini-3.8-flash`; `api_attempts=1`; `schema_error_count=0`; `manuscript_corpus_sent=false`.
- SHA-256 respuesta: `19c94186fd621e527178144cc62a4f10eb10f944df1caf2ad8950ed5e9480316`.
- SHA-256 prompt: `c718a5e246b2b95b2cae315fc2c7f0ca1742c605c2c896a1b8a5f1656111c9ea`.
- Los artefactos GitHub tienen caducidad: 2026-11-23. Guardar copia duradera antes de esa fecha, sin interpretar la respuesta como evidencia del manuscrito.

## Qué propone el revisor (no son resultados)
1. H0 plantillas de tokens: condicionar por longitud y posición podría anular diferencias `ch/sh`.
2. H1 asimetría de adyacencia: contraste `Delta = (p_post_ch-p_post_sh)-(p_pre_ch-p_pre_sh)`.
3. H2 artefacto de transcripción/segmentación: comprobar estabilidad entre lecturas y acuerdo estricto.
4. Folios separados exploración/holdout, parser IVTFF independiente, controles de permutación y reporte de sensibilidad.

## Auditoría crítica independiente
- **Sin decisión preinscrita:** `decision_rule="needs_data"`. No se puede ejecutar prueba confirmatoria hasta fijar definición de vocal EVA, soporte mínimo, tamaño efectivo, potencia y umbral de decisión usando solo calibración.
- **Permutación condicionada no necesariamente intercambiable:** permutar etiquetas `ch/sh` dentro de longitud/posición/sección puede romper restricciones de tipo de palabra, folio y dependencias entre tokens. Verificar intercambiabilidad y elegir nulo generativo apropiado; estratificar por folio o modelar dependencia.
- **Bordes:** `t-1` y `t+1` ausentes al principio/final del token no deben tratarse como consonantes ni omitirse asimétricamente. Predefinir población con ambos vecinos presentes para Delta primario, y análisis separado de bordes.
- **Definición EVA:** la palabra «vocal» es una etiqueta operacional, no afirmación fonética. Congelar conjunto explícito de glifos antes del holdout.
- **Folio como conglomerado:** estimar incertidumbre a nivel folio, no asumir ocurrencias independientes. Reportar heterogeneidad por sección/Currier.
- **Transcripciones correlacionadas:** ZL3b e IT2a son lecturas del mismo manuscrito; no contarlas como replicaciones independientes ni corregir p-values como si fueran dos estudios.
- **Confianza vs ausencia de señal:** un IC que contiene cero no refuta efecto; evaluar precisión y equivalencia solo si existe margen justificado preinscrito.
- **Control t±2:** la existencia de t±2 selecciona palabras más largas; comparar en población compatible y no equiparar ese control a un placebo sin justificar.
- **Criterio 20% de folios:** el umbral de descarte propuesto carece de justificación; fijar mediante calibración y análisis de sensibilidad, sin usar holdout.
- **50/50 holdout:** es sugerencia, no diseño óptimo demostrado. Determinar partición y semilla antes de mirar resultados, y registrar hashes de entrada.

## Próximos pasos antes de cualquier EXP nuevo
1. Auditar parser IVTFF y conteos de borde contra ejemplos manuales independientes.
2. Registrar universo de folios y trazabilidad de filtros para ZL3b/IT2a; fijar definición operacional de «vocal».
3. Hacer diagnóstico de soporte y simulación de potencia **solo con calibración**, decidir estratos y estadístico.
4. Congelar preregistro, semillas y plan de análisis; ejecutar holdout una sola vez.
5. Guardar resultados positivos y negativos, código, hashes y controles. No alterar `state/committed_claims.md` ni asignar EXP prematuramente.

**Interpretación prohibida:** un Delta positivo no demuestra idioma natural, cifrado, fonología ni traducción.
