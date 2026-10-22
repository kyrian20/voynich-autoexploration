# Cierre de cuatro lectores de referencia — 22-10-2026

Estado: **REPRODUCED**, limitado a selección de entradas. Fuente congelada: `aa9ec5399e7a5cdf8d1b2890fa657f1358825b41`. Continúa la [auditoría anterior](../2026-10-22-loader-audit/REPORT.md); no crea un EXP ni valida simulaciones históricas.

## Resultado verificable

Se extrajeron mediante AST únicamente las funciones o sentencias lectoras de cuatro scripts pendientes. No se importaron los módulos de experimentos ni se ejecutaron sus cálculos sobre el manuscrito. Una reconstrucción independiente coincide con cada secuencia completa; [results.json](results.json) conserva hashes de script, AST, corpus y secuencia, conteos y ejemplos.

| Consumidor histórico | Entrada efectiva según revisión de identidad | Selección reproducida |
|---|---|---:|
| EXP-267 | Cicero bilingüe, sin separar idiomas | 105.892 tokens ASCII de longitud ≥2, conservando mayúsculas |
| EXP-288 | Cicero bilingüe, sin separar idiomas | 87.754 registros de palabras ASCII de longitud ≥3, en minúsculas |
| EXP-001 | Archivo `vulgate.txt`: Biblia Douay-Rheims en inglés | 991.553 tokens ASCII tras recorte histórico |
| EXP-170 | Mismo archivo inglés | 97.164 líneas con al menos tres caracteres alfabéticos |

Las identidades no son un descubrimiento nuevo: proceden del manifiesto canónico `research/CORPUS_IDENTITY_REVIEW.json`, cuyos hashes se verifican antes de ejecutar. El avance es demostrar exactamente la selección realizada por estos cuatro lectores. Una reproducción sobre el árbol actual no prueba qué bytes utilizó cada ejecución histórica.

## Defecto de coordenadas en EXP-001

El lector calcula el índice del marcador final sobre el texto completo, elimina el prefijo inicial y reutiliza el índice antiguo sobre el texto acortado. En este archivo el prefijo eliminado mide 832 caracteres. El recorte histórico conserva 832 caracteres adicionales después de la posición correcta del marcador final.

Conservando la misma política ASCII, corregir solo las coordenadas da 991.420 tokens, frente a 991.553: diferencia de 133 tokens. No se estima aquí su impacto en entropías. El recorte corregido sigue conservando parte de la línea del marcador inicial; no constituye una edición limpia del cuerpo. Corregir este recorte tampoco convierte una traducción inglesa en latín.

Se preserva el lector histórico: cambiarlo ahora alteraría la reproducción de sus salidas anteriores. Las comparaciones monolingües latinas afectadas requieren una entrada adjudicada y nuevas salidas identificadas, sin sobrescribir originales.

## Cobertura y límites

Quedan reproducidos los dos consumidores en línea de Cicero y los dos lectores activos del archivo llamado Vulgata que la auditoría anterior dejaba pendientes. EXP-266, EXP-577 y EXP-031 conservan su clasificación estática de variable declarada sin carga AST; no se convierten en lectores activos por aparecer en el inventario.

La selección de onset de EXP-288 se reconstruye literalmente: omite vocales iniciales antes de buscar un grupo consonántico. Se reproduce su comportamiento; no se certifica su adecuación lingüística. Los conteos de tokens, registros y líneas de la tabla tienen unidades diferentes y no se suman.

No se auditan aquí accesos transitivos o dinámicos, el agrupado posterior de EXP-170, parsers del manuscrito, resultados estadísticos completos ni compromisos históricos. La auditoría global y la conformidad IVTFF siguen abiertas. No hay traducción verificada.

## Reproducción e integración

Desde cualquier directorio, con Python 3 y sin dependencias nuevas:

```sh
python /ruta/al/repositorio/tests/test_remaining_reference_loaders.py
python /ruta/al/repositorio/scripts/audit_remaining_reference_loaders.py --check /ruta/al/repositorio/research/maintenance/2026-10-22-remaining-readers/results.json
```

La CI existente ejecuta ambos comandos con permisos de lectura. El inventario histórico excluye explícitamente este nuevo diagnóstico, igual que el auditor anterior: sus referencias de prueba no son usos históricos. El primer ensayo de integración detectó esas dos referencias añadidas; se corrigió el alcance explícito del inventario, sin cambiar su snapshot ni omitir comparaciones de resultados. `--check` compara la estructura completa y no escribe resultados. `--out` genera un diagnóstico nuevo en una ruta explícita. Seis pruebas cubren exclusión del cuerpo del módulo, selección bilingüe sin filtro, reconstrucción del onset, filtro Unicode de líneas, fallo de coordenadas, ausencia de marcadores y rechazo de lector ausente. La primera ejecución de pruebas detectó un conteo esperado incorrecto en el fixture de longitud mínima (seis palabras, no siete); se corrigió el fixture esperado, sin modificar el algoritmo histórico.

## Autoauditoría según skills/audit_experiment.md

1. **Conocimiento del objetivo:** no se ajusta ninguna selección a métricas del Voynich. Se reproducen lectores preexistentes; selección retrospectiva explícita de cuatro pendientes.
2. **Destrucción de rasgos:** ASCII, filtros por longitud, eliminación de vocales iniciales y coordenadas defectuosas se conservan para diagnosticar el comportamiento original. No se usan para rechazar una hipótesis lingüística.
3. **Extrapolación:** coincidencia de cuatro lectores sobre dos archivos congelados. No equivale a reproducción completa de cuatro experimentos ni de sus ejecuciones antiguas.
4. **Alcance negativo:** no se infiere ausencia de lenguaje, significado o posibilidad de desciframiento. Las etiquetas históricas de latín no justifican una interpretación monolingüe con estas entradas.
5. **Controles:** se espera igualdad exacta entre lector extraído y reconstrucción; coinciden las cuatro secuencias. El fixture del recorte predice retención de material posterior al marcador y la prueba la confirma. No hay contraste de métricas del manuscrito con una distribución nula en este diagnóstico.

## Siguiente acción concreta

Relacionar las afirmaciones históricas que usaron estas selecciones con sus salidas y calcular su sensibilidad sobre corpus correctamente adjudicados. No sustituir corpus silenciosamente ni repetir simulaciones que no dependan de estas entradas.
