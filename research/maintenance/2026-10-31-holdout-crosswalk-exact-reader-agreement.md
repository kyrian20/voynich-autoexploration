# Holdout crosswalk: acuerdo exacto de páginas y registros entre lectores

**Fecha:** 2026-10-31. **Clase:** reparación operativa acotada, sin EXP nuevo. **Base:** `master` `156e1933dfca72a9f5cac6c25ecd6f9dd546ec0e`. **Estado inicial:** PROPOSED; comprobar CI del head y, si se integra, CI del master posterior. Este documento no certifica resultados de ejecución.

## Defecto de contrato comprobable

El crosswalk original contrastaba solo el conjunto de **números de hoja física** de dos lectores IVTFF. Si uno omitía un panel `f67v2` pero seguía reconociendo `f67r1`, la igualdad de hojas `{67}` continuaba cumpliéndose. Tampoco cotejaba el número de loci: una pérdida de un registro con las mismas cabeceras y hojas podía pasar el contraste. Por tanto, la afirmación operacional «dos lectores concuerdan en páginas y registros» era más fuerte que la puerta realmente implementada.

No se ha demostrado una discrepancia de este tipo en las transcripciones congeladas. Los casos son **inyecciones adversariales** que exhiben un fallo del verificador, no un resultado lingüístico ni una alteración histórica.

## Reparación

- `scripts/audit_holdout_locus_coverage.py`: `inspect_source(..., include_page_ids=True)` expone opcionalmente la lista de cabeceras de página, sin añadir campos a los resultados normales del auditor.
- `scripts/audit_holdout_page_crosswalk.py`: compara el conjunto exacto de páginas, los números de cabeceras y los números de registros de los dos lectores **antes** de publicar el crosswalk. Conserva el contraste anterior por hojas y asignaciones.
- `tests/test_holdout_page_crosswalk.py`: dos pruebas adversariales parchean solo la salida del lector estricto, manteniendo intactos el manifiesto y los bytes sintéticos. Una sustituye `f67v2` por `f67v1` sin cambiar la hoja; la otra resta un locus sin cambiar páginas. Ambas deben fallar de forma explícita.

No se modifican `data/transcriptions/`, `manifest-v2.json`, resultados originales, hashes históricos, semillas, sal, asignaciones, folios reservados ni `state/committed_claims.md`. Los ejemplos de prueba son ficticios. No se consulta el contenido léxico de los folios de test.

## Criterios de cierre fijados antes de CI

1. Pasan las pruebas `test_holdout_page_crosswalk.py` en Python normal y optimizado y `test_holdout_locus_coverage.py`.
2. El crosswalk real sigue produciendo exactamente los bytes congelados de `research/maintenance/2026-10-25-holdout-page-crosswalk/results.json`, mediante el `cmp` existente en CI.
3. CI del commit de PR termina `success`; inspeccionar logs y artefactos pertinentes. Solo entonces considerar integración; después verificar CI push del nuevo `master`.
4. Una divergencia real de lectores debe tratarse como bloqueo, no corregirse cambiando el manifiesto ni reinterpretando texto.

Comandos desde la raíz, Python 3.12:

```sh
python -m unittest discover -s tests -p 'test_holdout_page_crosswalk.py' -v
python -O -m unittest discover -s tests -p 'test_holdout_page_crosswalk.py' -v
python -m unittest discover -s tests -p 'test_holdout_locus_coverage.py' -v
python scripts/audit_holdout_page_crosswalk.py --out /tmp/holdout-crosswalk-UNIQUE.json
cmp research/maintenance/2026-10-25-holdout-page-crosswalk/results.json /tmp/holdout-crosswalk-UNIQUE.json
```

**Semilla:** no aplicable; pruebas deterministas. **Unidad:** cabecera de página y registro físico IVTFF. **Resultado esperado de los controles:** fallo cerrado en discrepancias inyectadas y coincidencia exacta del resultado congelado sobre las fuentes reales. **Limitación:** concordancia entre dos lectores no es certificación completa IVTFF ni independencia histórica de los folios; no implica significado o traducción. Pendientes independientes: EXP-170 sin entradas exactas, identidad de corpus históricos y adjudicación IVTFF completa. Evaluación general: 2026-11-22, sin prometer descifrado.

## Refuerzo de la puerta CI (2026-10-31)

La primera CI del head `24c81839bbb2db604f367a8d13bc063024e3507b` terminó `success` (116/116 pasos; run 41152969511) y ejecutó las pruebas de crosswalk **solo con Python normal**. No contenía el comando `python -O` para ese archivo y no conservaba el JSON del crosswalk como artefacto individual. Esta falta de cobertura se corrige añadiendo al workflow la ejecución optimizada, el cotejo `cmp` antes del SHA-256 y la publicación del JSON junto con su suma. El run anterior sigue siendo evidencia válida únicamente para lo que realmente ejecutó. No cambia ninguna fuente ni resultado histórico. El cierre requiere comprobar un nuevo run del commit modificado y su artefacto; esta nota no anticipa su resultado.
