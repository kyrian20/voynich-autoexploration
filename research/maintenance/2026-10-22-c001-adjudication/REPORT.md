# Adjudicación acotada de C001 y EXP-170/171/176 — 2026-10-22

**Estado: revisión documental, no EXP nuevo; no reproducción de simulaciones.**
Base de lectura: commit `19994b57027ce45e455c62eee745385c4c320838`.
No se modifica `state/committed_claims.md` (reservado al responsable humano).

## Fuentes internas examinadas
- `research/maintenance/2026-10-22-remaining-readers/REPORT.md` y `research/maintenance/2026-10-22-loader-audit/REPORT.md`.
- `experiments/exp_170_naibbe_simulation/{script.py,result.md}`.
- `experiments/exp_171_timm_simulation/result.md`.
- `experiments/exp_176_timm_parameter_sweep/result.md`.
- `state/committed_claims.md` (C001), `skills/audit_experiment.md`, `research/RESEARCH_INTEGRITY_STANDARD.md`.

## Matriz de adjudicación
| Componente | Resultado histórico reportado | Adjudicación |
|---|---|---|
| EXP-170, condiciones «Lat-A» y «Lat-B» | am_ll 0.625 y 1.008; y_lf 1.117 y 1.011, respectivamente | **INVALID_FOR_CLAIM** cuando se atribuyen a *latín*: el lector toma `data/reference_corpora/latin/vulgate.txt`, identificado en el manifiesto como traducción inglesa Douay-Rheims. No se descartan como simulaciones con entrada inglesa. |
| EXP-170, condiciones italianas | am_ll 1.062 (A), 0.999 (B); y_lf 0.724 (A), 1.011 (B) | Evidencia histórica *reportada* que no depende del archivo Vulgata; requiere comprobar identidad exacta del italiano y reproducción del simulador antes de elevar el estatus. |
| EXP-171, Timm con parámetros fijos | am_ll 0.994; y_lf 1.007 | Resultado histórico independiente de la entrada Vulgata como generación; la tabla comparativa sí incorpora la columna Naibbe «Lat-B». No demuestra imposibilidad universal. |
| EXP-176, rejilla Timm | máximo am_ll 0.572 y máximo y_lf 0.526 en 75 configuraciones | Resultado negativo *reportado* en la rejilla cp={0.3,0.5,0.7,0.85,0.95}, mp={0.1,0.25,0.4,0.6,0.8}, ventana={10,30,50}; no autoriza «todo mecanismo sin posición». |

C001 en `state/committed_claims.md` afirma «No tested position-blind mechanism...» y se apoya en EXP-170/171/176. Su evidencia no debe citarse como **400 simulaciones sobre latín e italiano**: dos brazos usan inglés. No se modifica ni se declara refutada C001; la afirmación histórica requiere una nota pública del responsable antes de nueva difusión, especialmente para la interpretación lingüística.

## Dos confusores adicionales en el código EXP-170
1. `parse_vms` calcula la clase A/B mediante tasa de `edy` por número de folio y umbral 0.05, no mediante la etiqueta IVTFF `$L`. Por tanto, la referencia «VMS B» no puede equipararse automáticamente a la clasificación canónica por línea.
2. `group_latin_paragraphs` segmenta mediante patrones de numeración y encabezados aplicados a un texto inglés. El protocolo A, además, usa longitudes de línea distintas de las del manuscrito, tal como advierte el informe original. Es un control de sensibilidad, no un contraste lingüístico limpio.

## Prueba falsable propuesta (no ejecutada)
**H0:** bajo el simulador Naibbe v2 y una segmentación B fijada antes de ver resultados, cambiar el idioma de entrada no altera materialmente las distribuciones de am_ll e y_lf.
**H1:** al menos uno de los contrastes cambia fuera de la variación entre semillas.

Antes de ejecutarla: fijar hashes SHA-256 y procedencia/licencia de un corpus latino auténtico y del italiano; congelar versión de Naibbe, semilla, política de líneas, versión del parser IVTFF y asignación por `$L`; ejecutar control positivo de identidad (reproducir brazo inglés original), control negativo de permutación con límites de línea preservados, y evaluación en folios reservados. Conservar todos los brazos y resultados negativos sin sobrescribir EXP-170. No asignar EXP nuevo hasta consultar el registro completo y comprobar que no exista trabajo equivalente.

**Criterio:** si un brazo nuevo alcanza am_ll >= 3.0 o y_lf >= 2.0 bajo condiciones predefinidas, se activa la condición explícita de contradicción de C001; si ninguno la alcanza, solo queda sin refutar la implementación y rejilla ensayadas.

## Autoauditoría (skills/audit_experiment.md)
- **Target-awareness:** el umbral 3.0/2.0 procede de C001 y sirve para detectar contradicción, no para ajustar parámetros; cualquier selección posterior basada en él sería exploratoria.
- **Destrucción de rasgos:** segmentación de líneas y corpus de origen pueden suprimir señales posicionales; no inferir incapacidad general del cifrado.
- **Extrapolación:** ninguna conclusión fuera de los cuatro brazos históricos o las 75 configuraciones reportadas.
- **Alcance negativo:** resultados históricos no reproducidos en esta revisión; ningún modelo de escritura ni lenguaje queda descartado.
- **Controles:** no se ejecutaron controles nuevos; por tanto, no hay valores esperados/observados nuevos que interpretar.

**Archivos originales y resultados negativos:** intactos. **Hashes de corpus:** remitidos al manifiesto y auditoría existentes, no recalculados aquí. **CI:** pendiente de confirmación después del commit. **Descifrado:** ninguno.
