# Revisión del estado histórico — 23-10-2026

Base inspeccionada: `e4f4408eda6975ab10bc69694c3f546bf9f60305`, Python 3.12.14. Revisión operativa y documental; no es validación científica global ni experimento nuevo.

## Correcciones

- README: distinguir acuerdo v7 de parsers de conformidad IVTFF completa; distinguir IDs por ruta ya resueltos de referencias históricas todavía ambiguas. La redacción anterior mezclaba estos estados.
- README: identificar explícitamente working_position.md como archivo histórico. Sus etiquetas de teoría no deben reutilizarse como adjudicaciones actuales.
- working_position.md: advertencia adicional sobre etiquetas históricas y enlaces a revisiones actuales. Se conserva íntegro el contenido anterior, sin modificar committed_claims.md.
- CI: enlazar el procedimiento que distingue consultas filtradas de ejecuciones realmente ausentes. No se atribuye éxito remoto al nuevo commit antes de comprobarlo.

## Comprobaciones ejecutadas

| Comando o comprobación | Resultado | Límite |
|---|---|---|
| `python -m unittest discover -s tests -v` | 127 pruebas: 126 aprobadas, una omitida | La prueba de replay crudo de batería común no se ejecutó; no contar como aprobada |
| `python scripts/audit_repository_operations.py` | Retorno 0; 32 workflows, un publicador, 624 rutas únicas | No valida las conclusiones de 624 directorios |
| `python scripts/check_corpus_integrity.py` | Retorno 0; 14 archivos; un corpus vacío en cuarentena | Integridad de bytes, no certificación de lengua o procedencia |
| `python scripts/analyze_subword_increment.py --check` | Retorno 0; snapshot completo coincidente | Reproduce un análisis exploratorio, no demuestra significado |
| `ast.parse` sobre todos los Python y `json.loads` sobre todos los JSON | 665 Python y 157 JSON; cero errores | Solo sintaxis/formato; JSON no comprobado por esquemas universales |
| Destinos relativos de enlaces Markdown en README, CLAUDE, AGENTS, OPERATIONAL_STATUS, working_position y current_state | Sin destinos ausentes antes de esta edición | No comprueba anclas ni enlaces web |

Logs de suite y reproducción: [history-status-review-logs](2026-10-23-history-status-review-logs/).

## Pendientes y criterio de cierre

1. IVTFF: completar adjudicación documental de casos, códigos extendidos, ligaduras y alternativas; acuerdo entre lectores no basta para certificar corrección.
2. Corpus: revisar consecuencias de cada referencia histórica afectada por la identidad de corpus. Conservar bytes y resultados originales; no sustituir entradas y presentar el resultado como reproducción del mismo experimento.
3. EXP-170: dependencia histórica Naibbe y selección exacta siguen sin quedar reproducidas por esta revisión. La PR de auditoría de estadísticas archivadas es un bloque distinto, no una ejecución del mecanismo histórico.
4. Archivo: cotejo completo de equivalencia/procedencia entre Biblioteca y GitHub y resolución de referencias numéricas ambiguas. Esta sesión no ha leído ni certificado todos los archivos de Biblioteca.
5. Propuestas abiertas: PR 2, 5, 6, 7 y 8 observadas al empezar. No se fusionan ni se reinterpretan como parte de master en esta revisión; sus evidencias corresponden a sus commits.
6. Revisión científica de conclusiones antiguas: las probabilidades, exclusiones de teorías y etiquetas VALID de los checkpoints históricos no quedan confirmadas por pruebas técnicas.

No se ha terminado de corregir todo el historial. El cierre exige evidencias por resultado afectado, no una declaración de perfección. No existe traducción validada.

## Autoauditoría del alcance

No se ajustan modelos, corpus ni umbrales a resultados deseados. No se ejecuta nueva prueba lingüística ni se actualizan compromisos o hallazgos científicos. Las comprobaciones técnicas y la coincidencia de snapshot no se usan como prueba de una teoría. Se conservan fallos y resultados negativos. Los textos históricos se preservan y la corrección se limita a su presentación y uso actual.
