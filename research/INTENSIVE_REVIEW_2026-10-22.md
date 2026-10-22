# Revisión intensiva de reproducibilidad — 22-10-2026

Base revisada: `93a0fda3fcc58b564a2ec324ee7cb8a67b8638e8`. Este ciclo repara código y añade evidencia; no asigna un EXP ni modifica transcripciones o resultados científicos históricos.

## Reparaciones completadas

### 1. Portabilidad de 474 scripts históricos

Se sustituyeron 491 literales que apuntaban al ordenador del autor (`/Users/asash/voynich-cryptanalyst` o `~/voynich-cryptanalyst`) por rutas resueltas desde el propio script. Se conservan los sufijos y los tipos de cadena que esperaba el código.

Para cada archivo se conservaron SHA-256 antes/después y una firma AST que ignora exclusivamente la sustitución de raíz y el import añadido. Las 474 firmas coinciden: no se alteraron filtros, modelos, semillas, parámetros, fuentes relativas ni fórmulas. Además se evaluaron las expresiones de ruta reparadas para comprobar que resuelven al checkout actual. Esto verifica portabilidad y conservación del algoritmo; no constituye ejecución ni validación científica de los 474 experimentos.

- Herramienta reproducible: `scripts/repair_legacy_paths.py` (previsualiza; solo escribe con `--apply`).
- Verificación: `python scripts/audit_legacy_portability.py`.
- Evidencia: [manifiesto](maintenance/2026-10-22-intensive/path-migration.json) y [resultado](maintenance/2026-10-22-intensive/portability-result.json).

La CI exige esta conservación para la migración registrada. Una modificación algorítmica futura de estos archivos requiere revisar explícitamente su recibo de mantenimiento; no debe actualizarse la firma para ocultar un cambio.

### 2. Cobertura de la auditoría de metadatos

`audit_ivtff_metadata.py` solo reconocía páginas sin subdivisión: inspeccionaba 184 cabeceras de ZL3b y veía 102 etiquetas A y 72 B. Ahora inspecciona las 227 cabeceras: 114 A, 83 B y 30 sin etiqueta A/B. También funciona fuera del directorio raíz y rechaza asignaciones contradictorias de `$L`.

El defecto estaba en la auditoría auxiliar. El cargador productivo EXP-590 ya tenía cobertura ampliada; sus métricas se comprobaron idénticas al JSON versionado. No se atribuye la corrección del auditor a un cambio científico en Currier.

### 3. Capa léxica sin pérdida de información

Nuevo módulo `scripts/ivtff_lossless.py`: conserva todos los caracteres del payload y offsets, distingue espacios ciertos/inciertos, comentarios, ligaduras, alternativas, caracteres ilegibles, códigos extendidos y marcadores de continuación. Las vistas analíticas declaran sus políticas y rechazan entradas sin resolver. Los códigos extendidos se conservan opacos, sin inventar qué glifo representan.

La referencia es René Zandbergen, **documento IVTFF issue 2.0.2**, 08-07-2025, relativo al formato 2.0.1: https://www.voynich.nu/software/ivtt/IVTFF_format.pdf, §§5.6, 6.6–6.8. Se contrastaron directamente las reglas relevantes: whitespace de presentación; códigos extendidos de tres cifras en rango 128–255; alternativas con separadores; ligaduras distintas de comentarios. No se afirma conformidad integral ni validación del alfabeto completo.

Hay 16 fixtures identificadas, más pruebas de políticas, entradas malformadas, offsets y continuaciones emparejadas. Las pruebas históricas de compatibilidad siguen separadas: que un parser antiguo acepte un caso no certifica que ese caso cumpla la norma.

## Auditoría de las tres transcripciones

Se verificaron reconstrucción exacta y offsets anidados de **15.989 registros**. Ninguna de las tres fuentes mostró diagnósticos de las categorías léxicas implementadas. Este hecho no certifica otras reglas documentales o semánticas del formato.

| Fuente | Registros | Listas de tokens distintas frente al filtro histórico | `daiin` histórico | Vista candidata |
|---|---:|---:|---:|---:|
| ZL3b | 5.385 | 1.170 | 853 | 848 |
| ZL3a | 5.389 | 1.178 | 853 | 849 |
| IT2a | 5.215 | 115 | 865 | 863 |

La comparación usa los mismos registros. La candidata elige primera alternativa, separa comas, expande ligaduras, conserva códigos e ilegibles y trata whitespace como presentación. Varios factores cambian simultáneamente: no se adjudica la diferencia a uno solo. No se reemplazó el tokenizador productivo ni se reescribieron sus resultados. ZL3a/ZL3b/IT2a son transcripciones del mismo manuscrito, no muestras independientes.

[Salida reproducible con hashes, políticas y ejemplos](maintenance/2026-10-22-intensive/readiness.json). El lector permite representar las nueve filas de códigos extendidos antes vacías bajo el filtro ASCII.

## Referencias ausentes: impacto verificado

Cuatro referencias faltantes aparecen en tres scripts. Se revisó su uso y se ejecutaron los dos scripts que no necesitan todas esas referencias:

| Script | Referencia ausente e impacto |
|---|---|
| EXP-031 `qo_stripping` | `data/reference_corpora/latin_vulgate.txt`: constante LATIN sin uso; no bloquea |
| EXP-170 `naibbe_simulation` | `data/derived/naibbe-cipher` y su ejemplo `divina_commedia.txt`: requeridos; bloquean |
| EXP-436 `latin_hapax_length` | `data/reference_corpora/italian/dante_divine_comedy_italian.txt`: rama opcional protegida por exists; comparación italiana omitida |

Estado de EXP-170: **BLOCKED_MISSING_INPUT**. EXP-031 y la parte latina de EXP-436 se ejecutaron desde `/tmp` con retorno cero: [logs de ejecución](maintenance/2026-10-22-intensive/historical-smoke-results.json). La comparación italiana opcional de EXP-436 sigue ausente. No se sustituyeron fuentes por textos de nombre parecido. Recuperar Naibbe y su versión exacta exige verificar procedencia. El inventario no cubre todas las dependencias Python o externas de cada experimento histórico.

## Validación y alcance

- 592 archivos Python analizados sintácticamente, sin errores.
- Ocho suites de regresión ejecutadas con retorno cero.
- 474 firmas AST y expresiones de ruta verificadas.
- Metadatos completos de ZL3b e igualdad de métricas del EXP-590 vigente comprobados.
- Las nuevas auditorías y fixtures quedan incorporadas a Voynich Check, con artefacto de diagnóstico.
- No se repitieron los 34 comandos del saneamiento operativo anterior: su código científico no cambió. Tampoco se ejecutaron los 624 directorios históricos completos.

[Pruebas](maintenance/2026-10-22-intensive/test-results.json) · [invariantes](maintenance/2026-10-22-intensive/active-invariants.json) · [metadatos](maintenance/2026-10-22-intensive/metadata-result.json).

## Evitar repetir investigación ya hecha

El test de predicción por orden de palabras ya existe en `experiments/exp_607_heldout_bigram_prediction/`, además de los dos protocolos LIB-EXP-623 reproducidos. La propuesta conversacional de hacer otro test genérico de orden sería una repetición. EXP-607 conserva un patrón de página restringido y tokenización simplificada: antes de ampliar conclusiones, hay que evaluar sensibilidad bajo un universo y políticas explícitos, sin ajustar el modelo a los resultados ya observados.

Las dos pruebas LIB-EXP-623 usan controles diferentes y muestran comportamientos diferentes; no deben promediarse ni presentarse como confirmación mutua. Véase [comparación de reproducción](reproduction/EXP623_REPRODUCTION_COMPARISON_2026-10-22.md).

## Autoauditoría

- **Conocimiento del objetivo:** la política léxica se fijó por reglas documentadas, sin escoger variantes por su recuento de `daiin`; la comparación es descriptiva.
- **Pérdida de características:** se conserva la capa bruta y se evita que los caracteres extendidos desaparezcan. La vista candidata sigue siendo una elección de análisis, no una lectura lingüística.
- **Extrapolación:** las firmas AST prueban una migración mecánica y las fixtures una cobertura finita; no validan todos los experimentos ni todo IVTFF.
- **Resultados negativos:** una dependencia requerida ausente bloquea su ejecución; una referencia opcional o sin uso no permite esa conclusión. Ninguno de esos casos refuta una hipótesis. No se cambió `committed_claims.md`, `findings.md` ni `failed_approaches.md`.
- **Controles:** no se introdujeron nulos estadísticos ni nuevas afirmaciones inferenciales. La igualdad EXP-590 se comprobó bajo su tokenizador existente; no se traslada esa validación a la candidata.

## Estado para continuar

La infraestructura operativa se conserva. La revisión cierra las rutas de máquina conocidas en 474 scripts y la cobertura del auditor de metadatos, y entrega una capa léxica comprobable para la siguiente integración. Continúan abiertos: EXP-170 con inputs requeridos ausentes y la comparación italiana opcional, validación documental/alphabet-specific del lector, sensibilidad científica antes de migrar resultados y cotejo completo Biblioteca/GitHub. No se declara la investigación entera validada.

## Verificación de integración

Voynich Check [39748431050](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39748431050) terminó en `success` para el commit `83b0875841b3cbdb83c4ffa661e55abfb5b98fa4`, incluyendo portabilidad, capa léxica, auditoría de tres transcripciones, metadatos y regresiones existentes. Artefacto `intensive-readiness-39748431050`, ID `12412790780`, digest ZIP `sha256:9b970f70a2eae45b4fcf7053164543ea457c54760a4b768a222f2fbab8cb6065`. La clasificación posterior de referencias se conserva en el manifiesto; cualquier commit posterior requiere su propia comprobación de CI.
