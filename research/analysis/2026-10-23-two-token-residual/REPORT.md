# Predictor con dos predecesores — 23-10-2026

Estado: **REPRODUCED**, alcance exploratorio. No hay recuperación semántica. Se extiende el predictor V2 de orden residual sin modificar sus entradas, resultados o transcripciones.

## Resultado principal

El predictor calibrado en desarrollo eligió **peso cero para la identidad del segundo token anterior en las cuatro vistas Voynich**. Por tanto, añadir esa capa no cambia su pérdida de evaluación. Esto es una decisión de este modelo bajo esta partición, no prueba de que el manuscrito carezca de dependencias de dos palabras o de lengua.

Los controles naturales tampoco muestran una ganancia residual clara de esa identidad adicional: César da una diferencia pequeña negativa y Dante una pequeña positiva, con ambos intervalos exploratorios incluyendo cero. En consecuencia, el ensayo **no proporciona una discriminación fiable entre Voynich y estos textos naturales en la métrica primaria**. No se transforma esa falta de discriminación en un argumento a favor de generación sin significado.

| Fuente | Tripletas de evaluación | Peso H2 / W2 | Ganancia H2−W2, bits/tripleta | Intervalo exploratorio por grupos, 95 % | Media de 16 controles |
|---|---:|---|---:|---|---:|
| ZL3b split | 4.927 | 0,025 / 0 | 0 | [0; 0] | 0,000002275 |
| ZL3b join | 4.457 | 0,025 / 0 | 0 | [0; 0] | 0,000027689 |
| IT2a split | 4.848 | 0,025 / 0 | 0 | [0; 0] | 0,000005230 |
| IT2a join | 4.848 | 0,025 / 0 | 0 | [0; 0] | 0,000005230 |
| César latino | 3.065 | 1 / 0,5 | −0,000034477 | [−0,000160378; 0,000055913] | 0,000002484 |
| Dante italiano | 6.075 | 0,5 / 1 | 0,000126872 | [−0,000098910; 0,000375731] | 0,000002563 |

**Los intervalos [0;0] de Voynich son consecuencia algebraica del peso cero fijado en desarrollo. No representan certeza de efecto poblacional cero**: el remuestreo no repite selección de pesos ni incorpora incertidumbre de entrenamiento/desarrollo o decisiones históricas. Las cuatro vistas son del mismo manuscrito; las dos IT2a son idénticas para esta entrada y no aportan réplicas independientes.

La capa H2 de bordes/longitud del segundo token anterior sí mejora la pérdida respecto a W1 en los controles naturales: +0,0178971 bits/tripleta en César y +0,0122081 en Dante. En Voynich, esos incrementos van de −0,0001927 a +0,0002002. Son diagnósticos del modelo, sin contraste confirmatorio o atribución lingüística.

## Error detectado y corregido antes del análisis real

La primera implementación añadía otra capa de suavizado y recuperaba una ganancia de 0,0000410788 bits incluso en datos construidos sin dependencia residual. Falló el umbral negativo fijado (<1e-10); la ejecución se detuvo antes de procesar las seis fuentes reales. El error era atribuir automáticamente a identidad una mejora marginal producida por suavizado adicional.

Se conservan el [protocolo inicial](PROTOCOL_V1.md) y [fuente inicial íntegra](v1-source.py.txt), estado **INVALID_FOR_CLAIM** para esa atribución. Para reproducir el aborto, copiar esa fuente a un nombre temporal dentro de scripts de un checkout desechable y ejecutar con --output. La reparación se fijó después de examinar exclusivamente los controles sintéticos, sin consultar evaluación real ni relajar el criterio negativo.

La capa corregida usa un cociente centrado entre distribución por identidad y distribución agrupada. Cuando ambas son proporcionales, el multiplicador es uno y el predictor no gana automáticamente por añadir suavizado. Se normaliza sobre todos los eventos; las probabilidades siguen sumando uno en contextos vistos y no vistos.

Control sintético positivo: ganancia **0,777607579** bits/tripleta, supera el criterio >0,5. Control sintético negativo: ganancia **0**, supera el criterio absoluto <1e-10. Seis pruebas pasan, incluidas normalización, ausencia de cruce entre líneas, rechazo de grupos compartidos y un negativo con tamaños de identidad distintos pero distribuciones proporcionales.

## Método y trazabilidad

W1 reutiliza V2 con vocabulario de 2.000 tipos de entrenamiento más UNK. H2 añade la firma de bordes y longitud del segundo predecesor; W2 añade su identidad dentro de esa firma mediante la corrección centrada. Tau=20, alpha=0,1 y rejilla de pesos heredados. Solo entrenamiento aporta vocabulario/conteos; solo desarrollo selecciona pesos. Los folios físicos se mantienen enteros en la partición V2; evaluación usa las mismas tripletas para las tres capas y nunca cruza líneas.

Se publican las seis fuentes completas, todos los pesos/scores de desarrollo adicionales, 16 barajados por fuente con semillas, pérdidas, UNK, cobertura de contextos y agregados por grupo. Los contextos W2 de evaluación presentes en entrenamiento son 970/4.927, 686/4.457, 896/4.848, 896/4.848, 476/3.065 y 1.957/6.075, respectivamente. La escasez de contextos limita la interpretación de este modelo de identidades exactas.

Los 2.000 bootstrap por grupos usan semilla 2026102301 y pesos fijados. Los controles barajan entrenamiento dentro de línea y recalibran todo en el mismo desarrollo real. Son diagnósticos, no una distribución nula confirmatoria ni una prueba de traducción. Se conservan hashes de entradas, scripts y protocolo en results.json.gz; no se añaden copias de corpus.

```
python tests/test_two_token_residual.py
python scripts/analyze_two_token_residual.py --check research/analysis/2026-10-23-two-token-residual/results.json.gz
```

La comparación exige estructura y enteros exactos y floats finitos con tolerancia 1e-12. El estado CI de este commit se debe comprobar por la colección completa de ejecuciones, según research/CI_VERIFICATION.md.

## Decisión para el desciframiento

No ampliar otra vez este modelo mediante ajuste al test ni atribuir sonidos a partir de sus pesos. Este ensayo no recupera una señal primaria suficientemente clara en los controles naturales para usarla como discriminador de teorías. La siguiente categoría útil es representación/unidades de texto o anclas semánticas externas verificables; no otra búsqueda de variantes favorables de esta misma memoria exacta. Una traducción necesita reglas estables y predicciones semánticas independientes que todavía no se han obtenido.

## Autoauditoría — skills/audit_experiment.md

**Target-awareness:** ampliar memoria se propuso tras observar V2. Fuentes, partición, rejilla y comparación son retrospectivas. La reparación se desarrolló en controles sintéticos antes de observar fuentes reales; se conserva la versión fallida. No se escogió una vista favorable.

**Implementación:** UNK y las firmas pueden agrupar identidades diferentes y absorber información lingüística. La poca cobertura de contextos exactos reduce sensibilidad. La corrección centrada elimina la mejora automática detectada, no certifica un modelo universal de dependencia.

**Extrapolación:** solo esta memoria de dos tokens, estas proyecciones, controles y partición. No se excluyen dependencias largas, segmentaciones distintas o lenguas. Los ceros con peso cero no se interpretan como precisión inferencial.

**Alcance negativo:** no se mejora con identidad adicional bajo la calibración seleccionada en Voynich; no se concluye ausencia de lenguaje. Los controles naturales no respaldan un uso discriminativo fuerte de la métrica primaria.

**Controles:** se esperaba >0,5 bits en el positivo y <1e-10 absoluto en el negativo conocido. V1 produjo 0,778071975 y 0,000041079: falló el negativo y se bloqueó. Tras la corrección fijada sin datos reales, se observan 0,777607579 y 0. Los pequeños valores de barajados reales se publican y no se consideran prueba semántica; la identidad primaria en controles naturales es incierta. No se reajusta para forzar un resultado favorable.

No se editan committed_claims.md, findings.md ni failed_approaches.md. No se asigna EXP ni se sobrescriben intentos anteriores.
