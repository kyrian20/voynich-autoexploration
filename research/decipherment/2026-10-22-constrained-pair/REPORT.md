# Contraste propio de bordes y revisión externa — 22-10-2026

**Estado: ejecutado, repetido y exploratorio. Sin traducción ni nuevo EXP.** Fuente de continuidad: `d1246fce9991fead2affc9e7f14cb4e192ae53b2`.

## Decisión científica

`daiin→dam` mantiene ocho apariciones, pero el nulo uniforme anterior no separaba identidad de token y estructura de sus bordes. Al fijar primer/último carácter EVA, la esperanza aumenta a 7–7,5 y las colas exactas son 0,25–0,50. Esto limita cuánto apoya aquella asociación una dependencia adicional entre identidades completas.

**Advertencia central:** los controles de bordes son poco informativos: solo uno o dos registros tienen varianza distinta de cero. Seis o siete de las ocho parejas son inevitables bajo esas restricciones. No demuestra que los bordes causen la asociación, ni que la pareja carezca de significado, ni que todo el orden sea puramente gráfico. La conclusión correcta es que aquí faltan oportunidades de intercambio para distinguir esas explicaciones.

## Resultados completos

Todos los contrastes observan ocho parejas. Las esperanzas se cuentan exactamente mediante asignaciones A=daiin, B=dam, O=otros en estratos por registro; la convolución usa fracciones racionales. No se cruzan líneas ni se modifica el corpus.

| Fuente / coma | Control | Esperanza | Registros variables | Cola exacta exploratoria | Holm, 16 vistas |
|---|---|---:|---:|---:|---:|
| ZL3b / split | fixed_endpoints | 2.8093 | 14 | 0.001404 | 0.016851 |
| ZL3b / split | same_initial | 3.1667 | 9 | 0.000611 | 0.009778 |
| ZL3b / split | same_edges | 7.0000 | 2 | 0.250000 | 1.000000 |
| ZL3b / split | same_edges_position | 7.0000 | 2 | 0.250000 | 1.000000 |
| ZL3b / join | fixed_endpoints | 3.4270 | 13 | 0.003428 | 0.037713 |
| ZL3b / join | same_initial | 3.2333 | 9 | 0.000880 | 0.013194 |
| ZL3b / join | same_edges | 7.5000 | 1 | 0.500000 | 1.000000 |
| ZL3b / join | same_edges_position | 7.5000 | 1 | 0.500000 | 1.000000 |
| IT2a / split | fixed_endpoints | 3.6122 | 15 | 0.006456 | 0.064557 |
| IT2a / split | same_initial | 3.2333 | 9 | 0.000880 | 0.013194 |
| IT2a / split | same_edges | 7.5000 | 1 | 0.500000 | 1.000000 |
| IT2a / split | same_edges_position | 7.5000 | 1 | 0.500000 | 1.000000 |
| IT2a / join | fixed_endpoints | 3.6122 | 15 | 0.006456 | 0.064557 |
| IT2a / join | same_initial | 3.2333 | 9 | 0.000880 | 0.013194 |
| IT2a / join | same_edges | 7.5000 | 1 | 0.500000 | 1.000000 |
| IT2a / join | same_edges_position | 7.5000 | 1 | 0.500000 | 1.000000 |

`fixed_endpoints` mantiene primer y último token y baraja el interior. `same_initial` conserva el primer carácter EVA de cada posición. `same_edges` conserva primer y último carácter. `same_edges_position` conserva además primera/interior/última posición. Son proxies de transcripción, no una identificación paleográfica certificada de glifos.

La evidencia bajo `same_initial` persiste en estas vistas; al conservar ambos bordes cae la capacidad de discriminar. El efecto de fijar extremos de línea varía con fuente/política: no se escoge la vista favorable. Holm cubre las 16 vistas nuevas y no las decisiones históricas. No son contrastes confirmatorios ni inferencia de tokens independientes.

## Qué aporta la revisión externa

[Fuentes y revisión de código](external-review.md). Se ha ejecutado sin modificaciones el driver `revision/token_syntax_test.py` del repositorio externo, fijado al commit `66f8adaadc120f93e8a4c906685ba66a9d3ab847`. La salida coincide byte a byte con la archivada: [stdout](external-token-syntax.stdout.txt), [recibo con 18 entradas y hashes](external-reproduction-receipt.json).

En ese driver concreto, con vocabulario limitado a 2.000 tipos más marcador y 25 barajados, la información excedente de orden es 0,8% de la entropía para Voynich, frente a 2,0–17,0% en sus controles. Es reproducción de implementación ajena, no una réplica independiente ni reproducción integral del preprint. No se compara directamente con EXP-607: selección, tokenizador y estimando son distintos.

La revisión encontró un error de offset en la retirada de pies Gutenberg de tres ficheros completos. Se verificó que **no cambia los primeros 33.582 tokens** utilizados en los dos flujos afectados (Culpeper e italiano combinado), de modo que no se atribuye a ese defecto la diferencia mostrada. [Diagnóstico reproducible](external-loader-check.json). No se modificó código externo ni se incorporaron sus corpus a los nuestros.

## Autoauditoría obligatoria

**Conciencia del objetivo:** la pareja y sus ocho lugares ya eran conocidos. Las cuatro reglas se fijaron antes de ejecutar; su elección está informada por literatura y por el problema observado. No equivalen a una hipótesis semántica preinscrita.

**Destrucción de características:** los nulos conservan bordes o posiciones y destruyen solo intercambios residuales. Pueden condicionar precisamente la estructura que una hipótesis lingüística usa. No son pruebas justas para negar cualquier gramática y, por su escasa varianza, no autorizan una conclusión negativa general.

**Extrapolación:** universo P0, alternativas primarias, dos transcripciones y dos políticas. No se excluyen lenguas, cifrados o mecanismos completos. Los datos son vistas del mismo manuscrito.

**Alcance negativo:** no se demuestra ausencia de significado; no se justifica todavía privilegiar esta pareja como una frase traducible. El protocolo de traducción prospectiva sigue sin completarse.

**Comportamiento del control:** se esperaba que fijar bordes pudiera aumentar la tasa base si la asociación dependía de las clases, pero no se conocía su magnitud. El control uniforme previo esperaba 2,09–2,63 parejas; el de bordes espera 7–7,5. Este aumento se investigó mediante soportes y contribuciones: seis/siete parejas quedan fijas y solo uno/dos registros varían. Se incorpora esta pérdida de discriminación a la interpretación; no se celebra la comparación uniforme como evidencia léxica independiente.

## Verificación y continuidad

Tres pruebas nuevas comparan el conteo de categorías con enumeración independiente de permutaciones de tokens etiquetados por su índice original, además de casos degenerados y con variación. La primera versión del enumerador de prueba confundía posición de origen y destino: se corrigió antes de aceptar resultados. El código de producción conservaba correctamente los estratos; el fallo quedó detectado localmente y no se publicó una prueba fallida como éxito.

Segunda ejecución: estructura exacta e identidades coinciden con el JSON guardado. El script aborta ante cambios de hash, pareja observada o localizaciones respecto al cálculo anterior. Cada registro conserva tokens, número de asignaciones, soporte, esperanza y varianza; los controles degenerados quedan visibles.

Comandos: `python tests/test_constrained_pair.py`; `python scripts/audit_constrained_pair.py`; comparación mediante `scripts/check_audit_snapshot.py`. La reproducción externa se describe en su recibo. CI reproduce el control propio sin red; no depende de descargar el repositorio externo.

**Siguiente dirección:** comparar identidades residuales únicamente donde exista intercambio suficiente entre tokens de iguales bordes, y evaluar la escala de unidades sobre el texto completo antes de asignar valores fonéticos. Se abandona la promoción de `daiin dam` a ancla semántica con la evidencia actual. No se repiten controles de esta pareja sin datos o pregunta nuevos. No se modifica el registro de afirmaciones comprometidas.
