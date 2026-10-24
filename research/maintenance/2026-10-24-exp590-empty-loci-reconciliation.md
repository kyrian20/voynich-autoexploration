# Conciliación de nueve loci sin tokens ASCII en EXP-590 (24-10-2026)

**Tipo:** reparación de trazabilidad de entradas; **no** es un EXP nuevo ni una traducción.  
**Estado del alcance:** `RECONCILED_INPUT_SELECTION_ONLY` en la CI de la rama; integración en master y CI posterior deben verificarse por separado.

## Incidencia y criterio de cierre

El inventario de ZL3b registra 5.385 loci con cuerpo crudo no vacío; el lector de cobertura ampliada de EXP-590 selecciona 5.376 con al menos un token ASCII. La diferencia de nueve no debe confundirse con nueve palabras Voynich perdidas. El criterio fue identificar todos los loci, conservar sus cuerpos y hashes, reproducir la selección del lector real y verificar el vector congelado sin modificar los artefactos históricos.

- Fuente inmutable: `data/transcriptions/eva_zl3b.txt`; SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- Implementación: `scripts/audit_exp590_empty_loci.py`; pruebas: `tests/test_exp590_empty_loci.py`; CI: `.github/workflows/voynich-check.yml`.
- Comando ejecutado por CI: `python -m unittest discover -s tests -p 'test_exp590_empty_loci.py' -v` y `python scripts/audit_exp590_empty_loci.py --check-canonical --out "$RUNNER_TEMP/exp590-empty-loci.json"`.
- Política: eliminar etiquetas IVTFF, anotaciones entre llaves y corchetes; contar secuencias ASCII `[a-z]+` en minúsculas, de acuerdo con la vista histórica específica auditada.
- Sin aleatoriedad ni semilla; el cotejo es determinista y no ejecuta simulaciones/permutaciones.

## Evidencia efectivamente inspeccionada

Ejecución de la rama, commit `4c5d22328dab43afba1e9cbab59d6b0cbbeb2739`: [Voynich Check 40076747686](https://github.com/kyrian20/voynich-autoexploration/actions/runs/40076747686), conclusión `success`. Las dos regresiones sintéticas constan como `ok` en el log. El log imprimió el vector `(5385, 5376, 9, 39594, 853)`, cotejado con el lector real de EXP-590.

Se descargó e inspeccionó el ZIP del artefacto [`exp590-empty-loci-40076747686`](https://github.com/kyrian20/voynich-autoexploration/actions/runs/40076747686/artifacts/12553244083), conservado 90 días. SHA-256 del ZIP: `51c7a7f3e0a06aae8ff600fdcc57aaeec74fc32a5ae15f083968363c6b2307be`; SHA-256 del JSON interno: `48ec75b77b14e3810143a0720bf8390b182a98843fe6439903fed12df0b8fb46`. El JSON contiene los siguientes **nueve loci** y números de línea de la fuente:

| Locus | Línea fuente | Cuerpo crudo |
| --- | ---: | --- |
| `f49v.11,*L0` | 2143 | `@140;` |
| `f49v.21,*L0` | 2153 | `@192;` |
| `f49v.27,*L0` | 2160 | `@140;` |
| `f49v.29,*L0` | 2162 | `@164;` |
| `f49v.35,*L0` | 2169 | `@192;` |
| `f49v.41,*L0` | 2175 | `@140;` |
| `f66r.24,+L0` | 2722 | `@169;` |
| `f66r.38,+L0` | 2736 | `@172;<!cf f57v?>` |
| `f66r.42,+L0` | 2740 | `@195;` |

Los nueve cuerpos carecen de secuencias `[a-z]+` **después del filtrado histórico**; la anotación `<!cf f57v?>` del octavo se elimina por esa política. El JSON conserva también el SHA-256 individual de cada cuerpo. La diferencia de denominadores queda conciliada para esta vista, no para todas las políticas IVTFF.

## Límites y estado científico

No se modificaron corpus originales, resultados congelados ni la definición de EXP histórico. No se han recuperado palabras en claro, validado equivalencias semánticas, adjudicado todos los casos de IVTFF ni reproducido las simulaciones históricas. El recuento de `daiin` (853) es de la vista ampliada y **no** debe confundirse con las 726 ocurrencias de la selección restringida histórica. Las transcripciones alternativas son testigos del mismo manuscrito, no replicaciones independientes. El ZIP expira según la política de retención; este informe preserva los IDs, hashes y criterios mínimos de verificación.

## Siguiente comprobación

Verificar que el código se integra sin conflictos con las correcciones históricas posteriores a la base de la rama y que una **nueva CI sobre el commit de integración de master** termina en `success`. Mantener la adjudicación IVTFF completa y los problemas de identidad de corpus como incidencias independientes, sin abrir experimentos confirmatorios hasta cerrar los bloqueos metodológicos.
