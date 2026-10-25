# Revisión de continuidad y protocolos de etiquetas — 25-10-2026

Estado: revisión documental y comprobaciones operativas acotadas; sin nuevo EXP ni resultado semántico.

## Fuentes fijadas
- Checkout comprobado: 412fd7cc2f830f1e9f4a298154d163af95cbc79a.
- PR #13 abierta, cabeza 31d7fc9bd5166a7727c36bd731e95b410f978a3a; se inspeccionaron su protocolo y listado de ocho archivos cambiados. No se ejecutó su código ni se fusionó.
- Propuesta en master: research/protocols/semantic-anchor-study.md.
- Decisión de segmentación: research/decipherment/2026-10-24-label-segmentation-decision-matrix.md.

## Comparación y decisión
| Dimensión | Propuesta en master | PR #13 |
| --- | --- | --- |
| Objetivo | Predecir categorías visuales independientes | Recuperar referentes/nombres históricos concretos |
| Evidencia mínima | Anotación ciega, inventario y fiabilidad pendientes | Referentes externos con fuentes; puertas de cinco hojas de prueba y veinte etiquetas por sección |
| Salida | Ganancia predictiva sobre sección/longitud/posición | Top-1/top-k y ganancia sobre baselines, incluidos parecidos ortográficos |
| Estado | Propuesta incompleta | PROPOSED; reproducción del lector histórico no sustituye auditoría independiente |

Comparten trazabilidad, separación por hoja, controles negativos y prohibición de inferir categorías desde EVA. Sus objetivos no son intercambiables: predecir una categoría no valida el nombre de una planta ni una traducción. Los umbrales de PR #13 no acreditan potencia por sí solos.

Decisión de esta revisión: no fusionar automáticamente PR #13 ni tratar sus documentos como metodología adoptada en master. El siguiente paso admisible es una especificación común de inventario por ocurrencia (fuente/hash, línea física, folio, locus, política de lectura, segmentación, categoría/referente externo, fuente visual, elegibilidad y motivo de exclusión), antes de entrenar o evaluar cualquiera de los dos objetivos. Congelar después un protocolo por objetivo, con métrica, baselines y regla de decisión propios. Preservar variantes ausentes y las dos segmentaciones de f65r; no escoger una para favorecer un nombre.

No se ha generado dicho inventario en esta revisión. Continúan pendientes anotación independiente, suficiencia de datos y auditoría de extracción de etiquetas. Cero anclas semánticas validadas.

## Verificación ejecutada
Entorno Python 3.12.14:
- python -m unittest discover -s tests -v: 246 tests; OK, skipped=1. El test de replay de batería requiere tokens.jsonl.gz no disponible; no se considera reproducido.
- python scripts/audit_repository_operations.py: exit 0; 35 workflows, un publicador, 624 rutas de experimento y siete grupos históricos de alias numéricos.
- python scripts/check_corpus_integrity.py: exit 0; 14 archivos, cero errores; cicero_caesar_latin.txt permanece en cuarentena. Comprueba identidad por bytes, no licencia ni conformidad IVTFF.

Estas comprobaciones corresponden al SHA anterior, no certifican este commit documental ni todo el historial. La CI #849 seguía en curso al iniciar la revisión: https://github.com/kyrian20/voynich-autoexploration/actions/runs/40175308038
No se ejecutó la CI completa local, los 624 experimentos ni las llamadas reales Gemini. No se modificaron corpus, committed_claims o hallazgos científicos.
