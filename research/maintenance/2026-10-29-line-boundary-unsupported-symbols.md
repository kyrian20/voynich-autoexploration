# Corrección acotada: caracteres EVA no adjudicados no son separadores de palabra

**Fecha:** 2026-10-29. **Estado de este documento:** parche propuesto; **CI y fusión pendientes de verificación posterior**. No se asigna EXP. Base congelada: PR #138 `codex/line-boundary-leaf-replication-20261028`, SHA `7cb3242691fdb5579f3c16506c0fcdae6300b140`. `master` comprobado: `1bce529f2dd4f572f05489443c7a4579e9c0894f`. PR abiertas antes de actuar: #5, #7, #13, #66, #82, #138. Se crea rama separada para no sobrescribir trabajo concurrente.

## Incidencia y regla falsable

El tokenizador de la réplica empleaba `re.findall(r"[A-Za-z]+", x)` después de separar por espacios IVTFF. Por ello, `qo'ky` se convertía en `["qo","ky"]`, como si el apóstrofo fuera un espacio. En ZL3b se observa, por ejemplo, `<f2r.10,+P0> qo'ky...`. La especificación IVTFF 2.0.2, §§6.6–6.7, enumera los cuatro separadores de palabra: punto, coma, `<->` y `<~>`; **no** el apóstrofo. No se asigna interpretación gráfica a `'`.

**Regla de seguridad:** después de procesar anotaciones y separadores IVTFF admitidos, cada unidad que no sea una secuencia completa `[A-Za-z]+` se conserva como `None` para la construcción de candidatos. No se divide silenciosamente por apóstrofos, dígitos u otros caracteres no adjudicados. La misma regla preserva las barreras ya establecidas para `?`, ligaduras, códigos `@nnn;` y continuaciones. Es una **cuarentena conservadora**, no una transcripción nueva ni una lectura lingüística.

**Hipótesis técnica falsable:** el lector anterior generaba candidatos de adyacencia que cruzaban unidades con `'`; el lector reparado no los genera. **Control negativo:** pares separados por punto y comentarios libres correctamente formados siguen su contrato anterior. El lector conserva filas y hojas, no reentrena modelos.

## Población, contrafactual y expectativas fijadas antes de CI

- Corpus originales sin modificar: ZL3b SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`; IT2a SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.
- Unidad: filas P aceptadas por el lector de la PR #138, bajo `primary` y `drop_uncertain_word`; el contrafactual reproduce **solo** el tokenizador de la cabeza anterior, manteniendo los otros guardias de candidatos. No es reproducción histórica de `results.json`.
- Una inspección independiente de las cadenas IVTFF en la conexión de GitHub (previa a ejecutar Python CI) encontró 21 filas P con apóstrofos no contenidos en comentarios/ligaduras en ZL3b y 0 en IT2a. Una implementación de censo en JavaScript, siguiendo el contrato del lector, prevé: ZL3b `primary` 9 positivos y 55 negativos menos; `drop_uncertain_word` 9 positivos y 53 negativos menos; IT2a cero diferencias. **Estas cifras son expectativas sujetas a la regresión Python, no resultados CI verificados en el momento de crear este documento.**
- Semilla: no aplicable (censo determinista). Sin dependencias nuevas; Python 3.12 de CI. Se guarda el contrafactual `previous_tokens()` en `tests/test_line_boundary_unsupported_symbols.py` y se comprueba el hash antes de leer cada fuente.
- Comandos: `python -m unittest discover -s tests -p 'test_line_boundary_unsupported_symbols.py' -v` y `python -O -m unittest discover -s tests -p 'test_line_boundary_unsupported_symbols.py' -v`. Ambos quedan exigidos por `.github/workflows/voynich-check.yml`.

## Integridad, autoauditoría y límites

1. **Sin calibración al resultado:** la regla de admisión procede de los separadores del formato, no de AUC, significación ni vocablos objetivo. El censo posterior no altera la regla.
2. **Sin prueba de idioma:** al retirar por precaución unidades desconocidas, se pueden perder también adyacencias auténticas a su alrededor. Los candidatos excluidos **no son todos errores demostrados**. Una decodificación autorizada de esos caracteres podría recuperar cobertura.
3. **Sin extrapolación:** no se ejecuta el predictor ni se consumen hojas reservadas. No se recalculan AUC/AP/log-loss, intervalos, modelos ni baselines. Los resultados antiguos siguen `INVALID_FOR_CLAIM` para el lector reparado.
4. **Sin resultados negativos ocultos:** IT2a se espera sin cambio, pero esto no certifica conformidad IVTFF. Una eventual discrepancia con las expectativas se debe registrar sin retocar silenciosamente los criterios.
5. **Sin sobrescrituras:** se conservan `results.json`, corpus, particiones, semillas, logs y correcciones anteriores. No se modifica `state/committed_claims.md`; no se inicia ciclo científico mientras la adjudicación IVTFF y la conciliación de artefactos sigan pendientes.

**Siguiente paso:** verificar las regresiones y la CI en el SHA exacto; si pasan, integrar solo en la rama de PR #138 tras comprobar que no haya avanzado y verificar CI posterior. Si falla, conservar el fallo y corregir únicamente con causa demostrada. No declarar limpieza global.

**Referencia normativa:** R. Zandbergen, *IVTFF – Intermediate Voynich MS Transliteration File Format*, issue 2.0.2 (08/07/2025), §§6.6–6.7: https://voynich.nu/software/ivtt/IVTFF_format.pdf.


## Primera ejecución CI fallida y corrección de la expectativa (sin ocultarla)

La CI de la PR #152, **run [40918358778](https://github.com/kyrian20/voynich-autoexploration/actions/runs/40918358778)** sobre SHA `095bd094e09ff676743f838797e0e1ab000327c7`, falló en la regresión de alcance: `ZL3b primary: changed=22`, frente a la expectativa inicial de 21. Los controles sintéticos pasaron; el test `drop_uncertain_word` registró 21 filas, 9 positivos y 53 negativos excluidos; IT2a registró cero diferencias. El workflow terminó `failure`; no se considera validado.

**Causa examinada en la fuente:** además de las 21 filas con apóstrofo visible fuera de anotaciones, la fila `<f34v.1,@P0>` contiene `k[e':s]chdy`. La lectura **primaria** selecciona `e'`, por lo que la unidad resultante también incluye un apóstrofo; la política de exclusión sustituye el corchete por `?` y ya la trataba como barrera. El censo inicial de cadenas había eliminado por completo los corchetes y omitió este caso. La regla de código no cambia: solo se corrige la expectativa de **filas afectadas** a 22 en `primary` y 21 en `drop_uncertain_word`; las expectativas de candidatos (9/55 y 9/53) no se retocan. Se conserva este fallo y la explicación para evitar ajustar silenciosamente el protocolo.

La ejecución posterior a esta corrección de expectativas requiere verificación nueva; no se afirma CI verde por anticipado.
