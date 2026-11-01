# LIB-EXP-624 — asignación conjunta A/B sin fuga de hoja entre estratos

**Fecha:** 2026-11-01. **Tipo:** reparación de una limitación conocida de las particiones derivadas, no experimento lingüístico. **Estado científico:** `BLOCKED` para evaluación confirmatoria. **Base:** `master` `5e81a8240089b11668b26069f5e05caeac3593c5`. **No se asigna EXP nuevo.**

## Incidencia concreta y decisión previa

La reparación del 30-10-2026 `scripts/prepare_library_exp624_leaf_grouped_splits.py` separa por hoja física cada grupo `all`, `A` y `B` **por separado**. Su propio informe advierte que no garantiza independencia física **entre estratos** si un futuro consumidor junta o cruza los modelos A/B. El defecto histórico de partición por página del piloto LIB-EXP-624 permanece documentado en 28/28 semillas; esta intervención no modifica ni rehabilita aquel resultado.

**Criterio falsable previo:** si un mismo número de hoja aporta caras de clases A y B, todas sus caras deben quedar en el mismo lado de una única asignación global, incluso al filtrar las vistas A/B. La unión de las vistas A/B/no clasificadas debe cubrir exactamente los 203 IDs elegibles; los conjuntos de hojas train/test han de ser disjuntos tanto dentro de cada vista como entre vistas. Un reparto adversarial que pase una cara B al test dejando la cara A de la misma hoja en train debe rechazarse.

## Reparación ejecutable propuesta

Se añade `scripts/prepare_library_exp624_joint_strata.py`. **No reemplaza** las 28 asignaciones independientes archivadas ni altera su fichero o su interpretación. Reutiliza las ocho asignaciones `all` por hoja física del script existente, y **después** filtra sus páginas por `$L=A`, `$L=B` o sin clase. La nueva salida `library-exp624-joint-strata.json` enumera por semilla las hojas globales y las páginas/hojas exactas de cada estrato; el auditor rechaza duplicados, faltantes, solapamientos físicos y discrepancias entre páginas y hojas. Ningún modelo se entrena ni evalúa.

Identidad congelada de fuentes:
- ZL3b `data/transcriptions/eva_zl3b.txt`: SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- IT2a `data/transcriptions/eva_it2a.txt`: SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.
- Script histórico de Biblioteca: SHA-256 `1f00846ab8e91cefd07bc2dcd26ad12cf8a7c4bc7b2478d480afec391a13f3a9`.
- JSON histórico: SHA-256 `d6e1b7490e563c96367ff10ab56feb5487d6b2775a885494f249c89f87bd4bab`.
- Informe histórico: SHA-256 `7de18cce59ea21598af7958a7ded3e05b03e305e8a6cc84c0740917b807447c4`.

**Parámetros:** LCG de 32 bits y Fisher–Yates de la auditoría previa; semillas globales `624010 + 7919*i`, `i=0..7`; corte 70/30 por **número de hojas**. Recuentos esperados por edición: 203 páginas elegibles; en ZL3b A=114, B=81, sin etiqueta=8. Las ediciones comparten el split global pero **no son muestras independientes**.

## Pruebas y trazabilidad

La regresión `tests/test_library_exp624_joint_strata.py` utiliza un control sintético con cada hoja dividida entre recto A y verso B: espera intersección física vacía al combinar estratos, rechazo de una fuga adversarial A/B y rechazo de páginas duplicadas o faltantes. La prueba con corpus congelados exige hashes, ocho semillas, cobertura 114/81/8 y estado de no reproducción. Se ejecuta en Python 3.12 normal y optimizado mediante `Voynich Check`, que conserva JSON, SHA-256 y logs como artefacto. Comandos:

```sh
python -m unittest discover -s tests -p 'test_library_exp624_joint_strata.py' -v
python -O -m unittest discover -s tests -p 'test_library_exp624_joint_strata.py' -v
python scripts/prepare_library_exp624_joint_strata.py --out library-exp624-joint-strata.json
sha256sum library-exp624-joint-strata.json
```

**Evidencia pendiente al redactar:** verificar CI de la PR en su SHA, el JSON generado, el hash del artefacto y, si se integra, CI del nuevo `master`. No anticipar un resultado de CI por el mero hecho de publicar este protocolo.

## Autoauditoría y límites

- **Conciencia del objetivo:** no hay calibración contra un valor lingüístico Voynich; la regla se fija por independencia física.
- **Destrucción de característica:** no se cambian tokens ni etiquetas; solo se derivan asignaciones de un split global.
- **Extrapolación:** garantiza disjunción para las ocho semillas y los IDs elegibles bajo el lector histórico; no demuestra independencia estadística general ni validez IVTFF.
- **Resultado negativo:** las 28 asignaciones históricas contaminadas siguen `INVALID_FOR_CLAIM_PHYSICAL_LEAF_HOLDOUT_ONLY`; no se infiere que cualquier modelo falle.
- **Control esperado/observado:** el control sintético con hojas mixtas A/B debe tener 0 hojas compartidas con el split global; las pruebas deben verificar 0. La fuga adversarial introducida debe ser rechazada. El resultado observado solo se declara tras verificar CI.

La conformidad IVTFF completa y el tokenizador permisivo histórico siguen pendientes; estas hojas ya han sido inspeccionadas, de modo que no constituyen una reserva prospectiva ciega. Las puntuaciones originales de ~0,95–0,97 bits/unidad no se rehabilitan. Se conservan corpus, scripts y salidas originales, resultados negativos, semillas, particiones prospectivas, hashes y `state/committed_claims.md`. La reproducción exacta de EXP-170 y la conciliación global de artefactos continúan bloqueadas. **Siguiente paso:** verificar el artefacto de asignación conjunta y adjudicar IVTFF antes de cualquier scoring confirmatorio. Evaluación final: 22-11-2026, sin prometer descifrado.
