# LIB-ORDER-2026-10-19-A/B — contaminación por hoja física (28-10-2026)

**Decisión:** INVALID_FOR_CLAIM **exclusivamente para la afirmación de evaluación en hojas físicas enteramente reservadas**. No se modifica el estado exploratorio de los resultados históricos ni se ejecutan nuevas pruebas de descifrado. No es un nuevo EXP. La revisión de integridad se basa en las dos implementaciones originales conservadas en Biblioteca y en sus corpus exactos.

## Incidencia

Los dos análisis de Biblioteca denominados EXP-623 separaban las unidades identificadas como fNNr y fNNv de forma independiente, aunque son caras de la **misma hoja física**. En A se baraja una lista de identificadores de página extraída de loci; en B se estratifica por $L pero se barajan igualmente identificadores de cara. Ambos procedimientos permiten que entrenamiento y prueba contengan caras de una misma hoja. La afirmación «folios reservados completos» es inválida para una partición por hoja física. No se atribuye este defecto al EXP-623 de GitHub, que investiga ch/sh y es otro experimento.

Los dos nulos tampoco son intercambiables: A permuta todas las palabras de los loci de prueba con el modelo entrenado sin cambios; B conserva los extremos, permuta **tanto entrenamiento como prueba** y vuelve a entrenar para cada control. Además, A usa todos los loci aceptados y B restringe a P0. Sus resultados negativos/positivos no forman una contradicción sobre un mismo contraste.

## Identidad de seis archivos originales de Biblioteca

Bytes materializados de Biblioteca y SHA-256 calculados de nuevo el 28-10-2026. Se verificaron sintaxis Python y JSON; los originales no se modificaron ni se incorporaron al repositorio.

| Alias | Archivo | Bytes | SHA-256 |
|---|---|---:|---|
| A | Informe_Voynich_exp623_Control_orden_palabras_2026-10-19.md | 8916 | d64bd77fc1e7fab4fe5b3d691f36b442ef878833723ca1aeeb6f0caed37f055d |
| A | exp623_shuffle_holdout.py | 8563 | c4bb8e7fb44632b93979a26bb88c49264c3fb7c4c2d3685a59d72958f902b070 |
| A | exp623_resultados_2026-10-19.json | 2633 | f46390e0f3a467f6327c1120c8a8a3eeddf707dc387bb5e6be8d4461780d618b |
| B | Informe_Voynich_exp623_control_orden_2026-10-19.md | 8752 | 7d8d794f36a2da83d4e6886d9986d9f42478ad999cde6ce1aeec3ad4c133af16 |
| B | exp623_order_null.py | 11137 | ea51e67e6f36b8c651231262cb22ebbb5ef9f98cd31c4673924e33d6a3627010 |
| B | exp623_order_null_summary.json | 2960 | 841425ae5668b9094d61b63d7290b57f4cc821e1b8acecbc7715a8ead555e692 |

Los hashes de los archivos ya estaban en research/library_artifact_sha256_manifest_2026-10-22.md; la **nueva evidencia** es la reconstrucción de las particiones y la cuantificación del solapamiento físico. Los JSON son registros de pilotos, no resultados regenerados.

Transcripciones inmutables: ZL3b SHA-256 bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc (Git blob 2a4533ab9bdfa85db9bad602d590978953055df1); IT2a SHA-256 7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5 (Git blob 4d6d3f2537b1f507a257529b49c94af7d6e03446). Son transcripciones del mismo manuscrito, no réplicas independientes.

## Auditoría de asignaciones (sin puntuaciones ni tokens reservados)

El nuevo script scripts/audit_library_exp623_leaf_leakage.py reconstruye exclusivamente elegibilidad y reparto de identificadores mediante LCG, Mulberry32, semillas, filtros y orden de los dos programas hash-identificados. Una hoja se cuenta como compartida cuando su número aparece en ambos grupos, aunque mediante caras distintas.

| Método / edición | Particiones | Caras elegibles | Caras train/test | Hojas compartidas por partición |
|---|---:|---:|---:|---|
| A / ZL3b | 20 | 227 | 158/69 | **41–57**; semilla 623101: **51** |
| A / IT2a | 20 | 225 | 157/68 | **38–53**; semilla 623102: **45** |
| B / ZL3b | 10 | 203 | 143/60 | **31–48**; semilla 623: **44** |
| B / IT2a | 10 | 203 | 143/60 | **31–48**; semilla 623: **44** |

En B con semilla 623, las hojas compartidas incluyen 1, 3, 4, 6, 9, 13, 14, 19, 21 y 23. Se cuentan **hojas distintas**, no tokens; esto no estima cuánto cambian las métricas. Las 60 cifras exactas de solapamiento están fijadas en EXPECTED_OVERLAP y el auditor emite la lista completa por semilla en JSON. La reconstrucción inicial independiente se realizó sobre los dos Git blobs con una implementación JS de los RNG; los primeros ocho valores de cada RNG se cotejaron con los programas Python originales y coinciden. Las cinco regresiones sintéticas pasaron localmente en Python normal y -O.

## Regresión y CI

Comandos desde la raíz del repositorio:

- python -m unittest discover -s tests -p 'test_library_exp623_leaf_leakage.py' -v
- python -O -m unittest discover -s tests -p 'test_library_exp623_leaf_leakage.py' -v
- python scripts/audit_library_exp623_leaf_leakage.py --check --out library-exp623-leaf-leakage.json

El script falla ante cambios en los SHA-256 de los corpus o en cualquiera de los 60 recuentos fijados. Los tests verifican RNG, elegibilidad, agrupación de caras/paneles, fuente sustituida y recuento alterado. Sin dependencias externas, sin aleatoriedad nueva, sin entrenamiento ni inferencia lingüística. El JSON de CI conserva semillas y listas de hojas; el informe conserva el resultado y los hashes tras expirar los artefactos.

## Autoauditoría y decisión

**Target-awareness:** se investigó retrospectivamente una afirmación de holdout, no se eligió un contraste para obtener significación. **Rasgos destruidos:** no se altera el corpus ni se permutan palabras; se reconstruye el reparto histórico. **Control positivo:** caras opuestas de una hoja repartidas entre train/test producen intersección; **control negativo:** caras agrupadas en el mismo conjunto producen cero. **Alcance:** dos pilotos de Biblioteca, no el conjunto del proyecto. **Resultado negativo:** no puede utilizarse su holdout por cara como prueba de generalización a hojas físicas completamente no vistas.

No se afirma que la ganancia de B desaparezca ni que A cambie de signo. El p=0,010 histórico de B no se promueve a confirmación independiente: la selección del control fue exploratoria y el holdout por hoja física no se cumple. La equivalencia exacta entre scripts Python y ejecuciones piloto JavaScript no está acreditada; esta auditoría verifica el reparto reconstruido, no reproduce puntuaciones históricas. No se modifican committed_claims.md, corpus, scripts históricos, JSON antiguos, semillas ni manifiestos.

**Próximo paso:** prerregistrar una evaluación agrupada por hoja física y controles de fuga, con una población de folios verdaderamente nueva si se pretende confirmación ciega. No usar las hojas test actuales para elegir reglas. Fecha de evaluación global: 22-11-2026, sin prometer descifrado.
