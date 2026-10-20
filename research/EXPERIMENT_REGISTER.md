# Registro de numeracion de experimentos

Actualizado: 2026-10-20.

## Regla
Los identificadores EXP son unicos. Las fases, los experimentos y las ejecuciones de Actions son series distintas. Un reintento no crea un EXP nuevo. No borrar resultados antiguos: registrar conflictos y conservar los artefactos.

## Conflictos conocidos
- EXP-590: los archivos creados el 20-10-2026 pueden colisionar con numeracion previa; no asumir que sean el EXP-590 historico. Además, la primera versión del script leía `$Q` como Currier; el script se corrigió el 20-10-2026 para usar `$L`. Los JSON/MD anteriores a la nueva ejecución siguen siendo inválidos para resultados por clase hasta confirmar que Actions los regeneró.
- EXP-591: existe un experimento previo de analisis held-out folio (commit e00b3f8) y un script posterior de variantes creado el mismo dia. El script de variantes no puede usar el identificador 591.
- EXP-592: existe un analisis max-T previo (commits 70db96a y a74cff7).
- EXP-593: script canonico scripts/exp593_daiin_variants.py; ejecucion completada y resultados guardados en research/experiments/2026-10-20-exp593.md y .json. Fuente SHA-256: bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc. El identificador aun debe cotejarse con el indice historico completo.

## EXP-593 — salida anterior y reproducción pendiente tras unificación del parser
- 4.188 lineas parseadas y 32.732 tokens.
- 5.000 permutaciones con semilla 20261021.
- `daiin`: 726 ocurrencias, 133 inicios de linea; p empirico y ajustado reportado 0,000200.
- `dain`: 198 ocurrencias; p ajustado 1,000.
- `daiiin`: 19 ocurrencias; p ajustado 1,000.
- **Incidencia detectada el 20-10-2026:** la versión inicial del script extraía la clase desde `$Q` (quire) en vez de `$L` (lengua Currier). Los resultados A/B y la cifra de 607 desconocidos del JSON EXP-590 original no son fiables. El script EXP-593 ya corregido genera A=440, B=278 y unknown=8 para `daiin` (726 ocurrencias totales), usando `$L`; este resultado de archivo es correcto en cuanto a su regla de metadatos, pero la ejecución de Actions debe confirmarse antes de declarar CI verificada. El nulo permuta tokens dentro de cada línea y la señal posicional no demuestra traducción.

## Auditoría estructural del repositorio (20-10-2026)
- Inventario recursivo de GitHub: 2.085 rutas, 624 carpetas `experiments/exp_NNN_*`, 617 IDs únicos y 7 grupos de colisión de carpeta (177, 594, 596, 597, 600, 601, 602); el detalle y las limitaciones están en [auditoría de inventario](repository_inventory_audit_2026-10-20.md).
- Se identificaron 31 workflows y 62 carpetas que requieren clasificación porque no contienen a la vez un script y un resultado reconocibles. No se etiquetan automáticamente como defectos.
- No asignar IDs nuevos hasta reconciliar el registro y el archivo maestro histórico.

La salida `2026-10-20-exp593.json` registra la ejecución anterior. El 20-10-2026 se unificó el lector de metadatos con `parse_currier_language` para aceptar consistentemente `$L=A/B` antes de `>` y se configuraron rutas nuevas `2026-10-20-exp593-corrected-L-metadata.json/.md`; esa reproducción debe terminar y compararse antes de etiquetar la salida nueva como `REPRODUCED`. La salida anterior no se sobrescribe.

## Auditoria tecnica (20-10-2026)
- Corregido `scripts/exp593_daiin_variants.py`: la clase Currier ahora se extrae de `$L=A/B`, no de `$Q`.
- Añadido `scripts/audit_ivtff_metadata.py`, sin identificador EXP, para validar que la transcripcion contiene ambas clases y contar cabeceras clasificadas.
- El workflow ejecuta esta auditoria antes de los experimentos. La nueva salida de EXP-593 debe sustituir/actualizar los artefactos con los resultados corregidos al ejecutarse Actions; hasta entonces, los resultados publicados arriba solo describen la ejecucion inicial y sus estadisticas globales deben volver a verificarse.
- Fuente del formato: IVTFF define `$L` como lengua Currier y `$Q` como cuaderno/quire.

## Siguiente accion
Recuperar el archivo maestro historico y enumerar todos los scripts, informes y JSON EXP-* antes de asignar nuevos numeros. El ultimo identificador libre no esta confirmado todavia.

## Conflicto con exportaciones de la Biblioteca ChatGPT
- Dos informes guardados en `/Investigación Voynich/` usan `EXP-623` para controles de orden de palabras; en este repositorio, `EXP-623` es la sensibilidad de la interacción ch/sh en IT2a. Son sistemas de numeración incompatibles. No fusionar, sobrescribir ni reasignar estos archivos sin un inventario de sus scripts y resultados asociados.
- La discrepancia entre parsers de EXP-602 sigue abierta: 1.466 diferencias de listas de tokens en ZL3b y 1.472 en ZL3a. El arreglo de metadatos `$L` no resuelve la tokenización.

## Errata enlazada
- EXP-590: consultar [errata de clasificación Currier](experiments/2026-10-20-exp590-erratum.md). El artefacto histórico se conserva; las tablas por clase requieren regeneración con el script corregido.
