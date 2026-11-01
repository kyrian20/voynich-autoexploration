# LIB-ORDER EXP-623 — recibos de auditoría con creación exclusiva

**Fecha:** 2026-11-01. **Clase:** reparación operativa de preservación de evidencia, sin EXP nuevo ni ejecución de modelos. **Base inspeccionada:** `master` `0dc1e00ded45071051f2620e498f6442867adcf1`. **Estado de la reproducción histórica exacta:** no acreditada. **Estado de CI:** pendiente de verificar por SHA de PR y de `master` posterior; este documento no afirma ejecución exitosa.

## Defecto concreto, delimitación y prueba falsable

`scripts/audit_library_exp623_leaf_leakage.py::main` escribía `--out` mediante `Path.write_text(...)`, que **trunca silenciosamente un fichero preexistente**. El auditor guarda las identidades de hojas físicas compartidas, semillas y tamaños por partición de los pilotos de Biblioteca LIB-ORDER-2026-10-19-A/B. Reutilizar por error una ruta de recibo o apuntar a un enlace simbólico podía destruir evidencia de una auditoría anterior. La ruta de salida de los auditores de holdout prospectivo ya se protegió por separado el 31-10-2026; **este auditor de Biblioteca seguía sin esa protección**. No se ha observado una destrucción real de archivos históricos.

**Criterio de aceptación fijado antes de ejecutar CI:** (1) `--out` crea un JSON válido con terminador LF si la ruta no existe; (2) una ruta preexistente provoca `FileExistsError` y conserva exactamente sus bytes; (3) un enlace simbólico a un recibo existente provoca `FileExistsError` sin modificar destino ni enlace; (4) los 60 recuentos y hashes congelados de la auditoría existente permanecen iguales; (5) CI de PR y, si se integra, CI del SHA exacto de `master` terminan satisfactoriamente.

## Reparación y regresiones

- `scripts/audit_library_exp623_leaf_leakage.py`: sustituir la escritura destructiva por `Path.open("x", encoding="utf-8", newline="\\n")`. Se mantiene el JSON serializado (`indent=2`, `ensure_ascii=False`, `sort_keys=True`) y el terminador LF; no se cambian elegibilidad, LCG, Mulberry32, semillas, particiones, controles ni interpretación.
- `tests/test_library_exp623_leaf_leakage.py`: dos nuevas regresiones llaman al `main()` real con corpus y repartos **sintéticos** (el analizador está simulado) para verificar preservación de recibo, creación nueva y rechazo de enlace simbólico. La suite existente también verifica fuentes, RNG, particiones, recuentos y SHA-256 de series de reparto.
- La CI ya ejecuta esa suite con Python normal y `-O` y ejecuta el auditor sobre ZL3b/IT2a congelados con `--check`; no se crea otro workflow ni se duplican ejecuciones científicas.

Comandos de verificación desde la raíz del repositorio:

```sh
python -m unittest discover -s tests -p 'test_library_exp623_leaf_leakage.py' -v
python -O -m unittest discover -s tests -p 'test_library_exp623_leaf_leakage.py' -v
python scripts/audit_library_exp623_leaf_leakage.py --check --out /tmp/lib-exp623-evidencia-NUEVA.json
```

El último comando necesita una ruta que no exista; la segunda invocación a la misma ruta **debe fallar** sin truncarla. Para la aceptación de la PR, inspeccionar el log del paso de CI correspondiente y el resultado de la auditoría, no inferirlo de este informe.

## Identidades conservadas y límites

Los corpus originales permanecen congelados: ZL3b SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`; IT2a `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`. Scripts originales de Biblioteca: A SHA-256 `c4bb8e7fb44632b93979a26bb88c49264c3fb7c4c2d3685a59d72958f902b070`; B `ea51e67e6f36b8c651231262cb22ebbb5ef9f98cd31c4673924e33d6a3627010`. Las copias de GitHub difieren únicamente por el LF final, según la conciliación de la PR #208. No se cambian esos bytes ni sus registros.

**No se rehabilitan** las afirmaciones de independencia por hoja física: los pilotos A/B compartían hojas entre entrenamiento y prueba; su evaluación sobre hojas físicas completamente reservadas sigue `INVALID_FOR_CLAIM`. El auditor de este bloque solo reconstruye metadatos de reparto, no puntuaciones predictivas ni traducciones. No se han cambiado corpus, manifiestos, scripts históricos, resultados negativos, semillas, hashes fijados, folios reservados ni `state/committed_claims.md`. No se ha ejecutado un ciclo científico prohibido. La reparación previene futuras sobrescrituras, no certifica ausencia de alteraciones anteriores.

**Pendientes separados:** entradas históricas exactas de EXP-170, adjudicación IVTFF completa, conciliación global de artefactos y PR científicas #7/#138. Próximo paso tras CI: inspeccionar los recibos de esta auditoría y continuar una incidencia concreta de procedencia, sin reutilizar el holdout como confirmación ciega. Evaluación general: 22-11-2026, sin prometer descifrado.
