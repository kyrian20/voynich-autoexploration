# Loci IVTFF no interpretables: barrera de continuidad P-to-P (30-10-2026)

**Estado:** corrección técnica acotada, no EXP nuevo; integración y CI pendientes de verificación. **Base:** PR #138, SHA `68b113d4bef5a30c1707d2377b115bdd15ee1ba2`; `master` observado en `342b4dd0eaf36e4b2ee94cc2628378b0ae47320b`. PR abiertas comprobadas: #5, #7, #13, #66, #82 y #138. PR #2, #8 y #10 constan fusionadas. Se trabaja en rama separada para evitar sobrescribir la investigación concurrente.

## Defecto reproducible y regla falsable

En `line_boundary_replication.parse()`, una fila física que empieza con un identificador de locus del mismo folio pero carece de coma de tipo o de cierre `>` se ignoraba. Si aparece entre `<f1r.P.1,P0> alpha` y `<f1r.P.2,P0> beta`, el constructor `candidates()` puede generar un positivo de límite de línea, aunque existe un registro intermedio no interpretado. El control de ordinales consecutivos no detecta ese caso: 1 y 2 siguen siendo consecutivos.

**Criterio previo:** cualquier fila que comience por `<fNNr.`, `<fNNv.`, sus paneles 1–6, o `<fRos.` y no pueda interpretarse como locus completo con coma, debe anotar `UNPARSED_LOCUS` sobre la última fila P conocida de esa página. No se inventan tokens ni se corrige el locus. El siguiente P no puede constituir una adyacencia positiva con el anterior. Los negativos interiores de filas P bien formadas siguen siendo válidos. Un encabezado `<f1r>`, un comentario `#` o un locus inválido de otra página no deben bloquear la transición.

**Pruebas sintéticas:** tres formas de fila defectuosa (coma ausente, cierre ausente, cierre/coma ausentes), una cabecera y comentario válidos, y un locus inválido de otro folio. El comportamiento anterior produciría un positivo espurio en las tres variantes; el corregido debe producir únicamente los dos negativos intralínea. El control válido conserva un positivo.

## Fuentes, alcance y controles

- Corpus originales congelados: ZL3b `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`; IT2a `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5` (SHA-256 esperados en el lector). El test exige ambos hashes antes del censo.
- Una lectura textual preliminar del repositorio, antes de la CI, no encontró filas de esta clase en los dos corpus. **No se atribuye a ello una reproducción científica:** el test en Python comprobará los hashes y la ausencia exacta. No se modifica ningún corpus.
- Script reparado: `research/analysis/2026-10-28-line-boundary-reproduction/line_boundary_replication.py`. Regresiones ampliadas: `tests/test_line_boundary_interposed_loci.py`.
- Comandos previstos en CI: `python -m unittest discover -s tests -p 'test_line_boundary_interposed_loci.py' -v` y `python -O -m unittest discover -s tests -p 'test_line_boundary_interposed_loci.py' -v`, además del workflow `Voynich Check`. Python 3.12. Sin dependencias nuevas, aleatoriedad, semillas, ajuste de modelos ni folios reservados.
- Cualquier ejecución fallida debe quedar enlazada; no declarar éxito sin consultar el run exacto y su SHA. Se conserva la implementación histórica en el historial Git; los resultados científicos congelados permanecen intactos.

## Autoauditoría y límites

1. **Target-awareness:** el cambio responde a la integridad del registro físico IVTFF, no a una métrica de rendimiento, palabra objetivo o selección de umbrales.
2. **Feature-destroying:** se eliminan conservadoramente posibles adyacencias si un locus no puede interpretarse; eso puede reducir cobertura legítima. No es una prueba justa de un mecanismo lingüístico ni una interpretación del contenido.
3. **Extrapolación:** solo se protege esta clase de fila con identificador de página reconocible; no se certifica conformidad completa IVTFF ni detección de todas las formas de corrupción.
4. **Resultado negativo:** si los corpus congelados contienen cero filas afectadas, eso no demuestra que los demás defectos del parser estén resueltos. No se reejecutan métricas.
5. **Control:** sin barrera, tres fixtures con registro intermedio producirían un falso positivo; con barrera se esperan cero positivos, dos negativos. Con cabecera, comentario y locus de otro folio se espera un positivo; se contrastará en CI.

**Limitación científica:** las puntuaciones históricas del predictor de PR #138 siguen `INVALID_FOR_CLAIM` para el lector combinado corregido. Siguen pendientes adjudicación IVTFF, procedencia exacta EXP-170 y conciliación de artefactos. No se inicia un nuevo ciclo científico ni se modifica `state/committed_claims.md`.

**Siguiente paso:** abrir PR hacia la rama de #138, comprobar CI y regresiones, verificar que la cabeza de destino no haya avanzado antes de integrar y registrar la evidencia posterior. No se declara limpieza global.
