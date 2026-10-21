# Síntesis crítica reproducible — EXP-604 a EXP-611
Fecha: 2026-10-21
Repositorio: `kyrian20/voynich-autoexploration`, rama `master`

## Estado de reproducibilidad

Los últimos runs correctos observados para EXP-604–611 ejecutaron los scripts y el paso `Commit results` con éxito:
- [EXP-604, run 39673400827](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39673400827)
- [EXP-605, run 39673408627](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39673408627)
- [EXP-606, run anterior 39673413204](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39673413204) — **obsoleto para interpretación**: después se detectó que su script confundía el campo IVTFF `$Q` (quire/cuaderno) con Currier; se corrigió para usar `$L` mediante `parse_currier_language`. La ejecución de esa corrección está pendiente en el momento de redactar esta síntesis.
- [EXP-607, run 39673423239](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39673423239)
- [EXP-608, run 39673435096](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39673435096)
- [EXP-609, run 39673443142](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39673443142)
- [EXP-610, run 39673449155](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39673449155)
- [EXP-611, run 39673455023](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39673455023)

La primera edición del bloque de reintentos tuvo un error de indentación YAML; esos runs fallaron antes de ejecutar los trabajos. La indentación se corrigió y los runs enumerados arriba para EXP-604, 605, 607, 608, 609, 610 y 611 terminaron en verde. EXP-606 está siendo regenerado después de corregir un error semántico del parser. Se conserva esta incidencia en el registro para que no se confundan los fallos intermedios con resultados científicos.

## Hallazgos y límites

### EXP-604 — Replicación posicional de `daiin` en IT2a

- Protocolo declarado: Currier B, posición P0 exacta, líneas con al menos dos tokens limpios; permutación de una posición uniforme por línea, 20.000 remuestreos bootstrap por folio y 20.000 permutaciones.
- Muestra: 2.324 líneas elegibles, 81 folios; 84 apariciones de `daiin` iniciales observadas frente a 32,28 esperadas por el inventario; 301 tokens `daiin` en total.
- Razón de enriquecimiento: **2,60×**; IC bootstrap agrupado por folio al 95%: **1,94–3,34×**; permutación unilateral con corrección +1: **p ≈ 0,00005**, cero excedencias en 20.000 permutaciones.
- Sensibilidad leave-one-folio-out: razón entre **2,43× y 2,71×**.
- **Lectura prudente:** evidencia fuerte de posición inicial no uniforme bajo este nulo en esta transcripción. No es una clave semántica ni desciframiento; IT2a puede compartir convenciones editoriales con otras transcripciones.

### EXP-605 — Auditoría de cabeceras y lagunas de foliación

- ZL3b e IT2a reflejan la lista predeclarada de 14 números de folio ausentes; ninguno de esos números aparece inesperadamente.
- Ambas transcripciones contienen 92 números de folio únicos, de 1 a 116. ZL3b tiene 184 cabeceras de lado y no muestra folios con un único lado; IT2a tiene 183 y señala `f116` con solo lado `r` (posible lado `v` ausente en esa transcripción).
- **Lectura prudente:** confirma consistencia de cabeceras de texto con la lista conocida, no prueba que no se hayan perdido hojas no numeradas. La anomalía de `f116` requiere contraste con facsímiles y convenciones editoriales.

### EXP-606 — Distancia léxica en límites de lagunas

- **Error detectado y corregido:** el script anterior leía `$Q` como si fuese la etiqueta Currier; IVTFF usa `$L=A/B` para Currier y `$Q` para cuaderno. Los resultados antiguos de EXP-606 no deben citarse como comparación por Currier.
- Se cambió el script para reutilizar `parse_currier_language` de `scripts/audit_ivtff_metadata.py`, que lee `$L=A/B`, nunca `$Q`. También se corrigió el resumen para comparar solo los tres bordes disponibles cuyas dos caras tienen la misma etiqueta Currier no nula.
- Run corregido: [39673786598](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39673786598), `success`; el paso de commit terminó correctamente.
- ZL3b: media JSD de los 3 bordes elegibles **0,6914 bits**, frente a **0,7019** en 147 transiciones de control de misma clase. IT2a: **0,6734**, frente a **0,7107** en 147 controles. Los otros dos bordes disponibles no tienen la misma clase Currier a ambos lados y quedan fuera de esta comparación; `f90v→f93r` no está disponible en las transcripciones.
- **Lectura prudente:** no aparece una distancia léxica media mayor en los bordes de lagunas que en los controles emparejados por Currier. La muestra es de solo tres bordes elegibles, no está emparejada por ilustración, mano, longitud ni tema, y no permite concluir nada firme sobre pérdida de hojas.

### EXP-607 — Predicción de siguiente token en folios retenidos

- División por folio basada en SHA-256, bucket 0/5 como test; transiciones no cruzan líneas; modelo interpolado 50% unigramas + 50% bigramas, α=0,1; control con orden de tokens barajado en entrenamiento.
- ZL3b: mejora del modelo real frente a unigramas de **0,2668 bits/token**, pero el control barajado mejora **0,2109**; diferencia real–control **0,0559 bits/token**.
- IT2a: mejora real **0,3410 bits/token**, control **0,2860**; diferencia real–control **0,0550 bits/token**.
- **Lectura prudente:** hay una pequeña señal de orden local por encima del control, pero el efecto residual es modesto y depende de un tokenizador simple; no identifica idioma ni significado. Las dos transcripciones no son testigos independientes.

### EXP-608 — Auditoría descriptiva del carácter siguiente a `ch/sh`

- Se cuentan contextos dentro de tokens limpios; no se aplica modelo por plantilla ni se atribuyen etiquetas Currier. En ZL3b: 13.083 contextos en 183 folios; tasa global de vocal después del dígrafo **86,34%**. En IT2a: 13.258 contextos en 182 folios; tasa **85,87%**.
- **Lectura prudente:** el agregado muestra una tasa alta de vocales, pero por sí solo no valida la hipótesis de Parisel ni su mezcla Beta-Binomial; hace falta un modelo condicionado por plantilla/folio y controles de dependencia.

### EXP-609 — Comparación pareada de tasa vocálica después de `ch` y `sh`

- ZL3b: 181 folios pareados; diferencia media por folio `ch - sh` **−6,24 puntos porcentuales**, IC bootstrap 95% **−7,81 a −4,68 pp**, permutación sign-flip bilateral **p ≈ 0,00005**.
- IT2a: 182 folios pareados; diferencia media **−5,49 pp**, IC 95% **−7,34 a −3,53 pp**, p ≈ 0,00005.
- **Lectura prudente:** diferencia descriptiva consistente entre las dos transcripciones, pero no independiente entre fuentes y sin ajuste por plantilla, sección o mano. El mínimo p estimado es consecuencia del límite de 20.000 permutaciones, no una precisión infinita.

### EXP-610 — Estratificación por longitud de token

Diferencia media por folio en tasa vocálica `ch - sh`:
- Longitud 2–4: ZL3b **−7,47 pp**; IT2a **−7,34 pp**.
- Longitud 5–7: ZL3b **−6,49 pp**; IT2a **−5,09 pp**.
- Longitud 8+: ZL3b **−1,57 pp**; IT2a **−0,75 pp**.

**Lectura prudente:** el contraste se reduce notablemente en tokens largos. La longitud explica parte de la diferencia bruta; las tasas siguen siendo descriptivas y no son una réplica del modelo de Parisel.

### EXP-611 — Emparejamiento por longitud exacta y posición del dígrafo

- ZL3b: 32 estratos longitud/posición, 1.134 pares folio-estrato; tasas agrupadas de contexto emparejado: `ch` **84,61%**, `sh` **90,44%**; diferencia media dentro de estratos por folio **−6,65 pp**.
- IT2a: 31 estratos, 1.153 pares folio-estrato; `ch` **83,84%**, `sh` **90,06%**; diferencia media **−7,13 pp**.
- No se calculó p-valor; hay estratos escasos y los tipos de palabra se solapan.
- **Lectura prudente:** la diferencia descriptiva persiste después de controlar longitud exacta y posición, pero eso no descarta plantilla, sección, mano, convenciones de transcripción o dependencia de las fuentes.

## Conclusión operativa

La señal más estable en este bloque es una diferencia descriptiva en el carácter siguiente a `ch` frente a `sh` que persiste en emparejamientos simples, pero se reduce en tokens largos. Esto justifica una siguiente prueba **predeclarada** con modelo por plantilla y efectos por folio/segmento, no una afirmación de desciframiento. EXP-607 da una señal residual modesta de secuencia; EXP-604 ofrece evidencia posicional clara para `daiin` bajo su nulo específico. EXP-606 queda en espera de resultados regenerados por la corrección de metadatos.

## Fuentes y hashes

- ZL3b `data/transcriptions/eva_zl3b.txt`: SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- IT2a `data/transcriptions/eva_it2a.txt`: SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.

Este informe resume artefactos generados por los scripts registrados; no sustituye los `results.json`, los protocolos ni la inspección de los facsímiles.
