# Auditoría descriptiva de sensibilidad de ligaduras IVTFF y cobertura del parser

Fecha: 2026-10-22  
Estado: **reproducida en CI; auditoría descriptiva, no EXP registrado**  
Workflow validado: [run 563](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39738683050)  
Script: `scripts/audit_ivtff_ligature_views.py`  
Pruebas: `tests/test_ivtff_ligature_views.py`

## Resumen ejecutivo

La auditoría compara tres vistas de los spans entre llaves: la política histórica que los elimina, una vista que conserva cada ligadura como unidad tipada, y una vista derivada que expande el contenido interno. No modifica transcripciones ni resultados históricos.

Se han detectado **dos efectos diferentes que no deben confundirse**:

1. **Sensibilidad de las ligaduras:** en la vista de expansión, una ocurrencia exacta de `daiin` deja de aparecer en ZL3b y ZL3a, mientras que las unidades y tokens totales cambian.
2. **Cobertura del parser de línea:** el patrón de línea heredado de EXP-590 solo reconoce IDs del tipo `f1r.1`; excluye IDs IVTFF como `f67r1.5` y `fRos.23`. El conteo más amplio reconoce 5.385 registros en ZL3b, coherente con el recuento de registros del protocolo independiente de EXP-602. La línea base histórica de EXP-590 se reproduce exactamente con su patrón antiguo, pero sus cifras no deben compararse directamente con el recuento amplio sin explicar esa diferencia de cobertura.

## Resultados de sensibilidad con cobertura amplia

Fuentes y SHA-256:

- ZL3b: `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`
- ZL3a: `56419297682d338ff1a0a17f5ae251e3ee3e2c5bf05a62db04c5385ef30b36a2`
- IT2a: `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`

| Medida | ZL3b | ZL3a | IT2a |
|---|---:|---:|---:|
| Registros de texto no vacíos | 5.385 | 5.389 | 5.215 |
| Spans entre llaves en el archivo (líneas no editoriales) | 446 | 444 | 0 |
| Líneas con ligaduras visibles tras quitar anotaciones cuadradas | 371 | 369 | 0 |
| Ligaduras visibles en esas líneas | 402 | 399 | 0 |
| Ligaduras ocultas al eliminar anotaciones cuadradas | 44 | 45 | 0 |
| Unidades en vista histórica | 39.594 | 39.596 | 37.945 |
| Unidades en vista de ligadura atómica | 39.996 | 39.995 | 37.945 |
| Tokens en vista expandida | 39.512 | 39.513 | 37.945 |
| Ocurrencias exactas de `daiin`, vista histórica/atómica | 853 | 853 | 865 |
| Ocurrencias exactas de `daiin`, vista expandida | 852 | 852 | 865 |
| Líneas que comienzan por `daiin`, las tres vistas | 161 | 161 | 157 |

Las 44/45 ligaduras ocultas por anotaciones cuadradas no se expanden en estas tres vistas: se mantiene la política histórica de retirar la anotación incierta completa. Se informan aparte para no confundirlas con ligaduras ordinarias fuera de corchetes. Su tratamiento exige una decisión independiente sobre alternativas inciertas.

## Comparación con la cobertura histórica de EXP-590

La función de compatibilidad reproduce el patrón de línea heredado de EXP-590. No modifica el script ni sus JSON/MD históricos.

| Métrica | EXP-590 / patrón heredado ZL3b | Cobertura amplia ZL3b | Diferencia |
|---|---:|---:|---:|
| Líneas con al menos un token | 4.188 | 5.385 registros de texto | +1.197 registros |
| Tokens/unidades de la vista histórica | 32.732 | 39.594 | +6.862 |
| Ocurrencias exactas de `daiin` | 726 | 853 | +127 |
| Líneas iniciales de `daiin` | 133 | 161 | +28 |

La comparación de líneas tiene una pequeña diferencia de definición: EXP-590 cuenta solo líneas que producen al menos un token; la cobertura amplia cuenta registros de texto no vacíos, incluso si después una vista de análisis no produce tokens. Por eso no debe interpretarse la diferencia de 1.197 como un recuento exacto de registros perdidos sin aplicar el mismo filtro de tokens a ambas vistas.

El origen técnico principal identificado es el patrón de ID: la expresión antigua `f(\\d+[rv])` no admite sufijos de subdivisión como `f67r1.5`. La documentación oficial IVTFF da nombres de página como `f102r2`, por lo que el parser debe poder representar esos sufijos ([fuente oficial](https://www.voynich.nu/extra/sta-aaa.html); [formato IVTFF 2.0.2](https://www.voynich.nu/software/ivtt/IVTFF_format.pdf)). También aparece el ID especial `fRos.23` en la transcripción, que la auditoría amplia registra por separado. No se ha cambiado el parser productivo ni se ha regenerado EXP-590. Antes de actualizar cualquier análisis, hay que declarar qué familias de registros pertenecen al universo analítico.

## Interpretación y límites

- ZL3a y ZL3b son transcripciones alternativas del mismo manuscrito; no son muestras independientes.
- IT2a no tiene spans entre llaves en este inventario.
- La vista atómica conserva la ligadura como unidad separada; no afirma que sea una palabra léxica.
- La vista expandida conserva los caracteres internos en una vista derivada, pero no conserva necesariamente los límites de palabra históricos.
- Las cifras de `daiin` describen la sensibilidad de la tokenización, no prueban significado ni desciframiento.
- No se ejecutaron pruebas de significación ni permutaciones nuevas.
- Ningún resultado histórico fue sobrescrito.

## Próximas puertas de validación

1. Consultar la gramática oficial de los identificadores de línea IVTFF y documentar qué registros especiales deben incluirse.
2. Añadir una prueba que reproduzca el recuento de registros del parser independiente EXP-602.
3. Separar en la siguiente versión las anotaciones cuadradas con ligaduras internas, sin inferir automáticamente cómo deben interpretarse.
4. Crear un experimento nuevo solo después de reconciliar el registro de IDs EXP; conservar las salidas actuales como auditoría técnica sin número EXP.
