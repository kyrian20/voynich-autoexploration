# Auditoría del paquete de Matthew Dominik — 2026-11-06

**Clase:** auditoría externa de reproducibilidad; no es un EXP nuevo ni una validación de traducción.

## Alcance y procedencia

Se inspeccionaron los registros Zenodo [10.5281/zenodo.22049207](https://zenodo.org/records/22049207) y [10.5281/zenodo.23444474](https://zenodo.org/records/23444474).

El ZIP de 22049207 tiene 2.871.699 bytes. Su MD5 local coincide con el publicado por Zenodo: `6cc444416d57698775c40bcb7f2e1786`; SHA-256 local: `b428c0f28215f5c2f50878d3ea84321cadde54d4751ed1238b543e3f2fb116a1`. **Todos los hashes** enumerados en `SHA256SUMS.txt` pasaron `sha256sum -c`.

## Reproducción ejecutada: transferencia R2

Se ensamblaron únicamente los inputs incluidos en el depósito: estado Cycle28, ZL3b, RF1b, salida R1 de segmentación, protocolo R2 y motor congelado. El script R2 usa rutas absolutas `/mnt/data/voynich_r1` y `/mnt/data/voynich_r2`; en una copia local se cambiaron solo esas rutas para ejecutar el mismo código sobre el paquete extraído. El script terminó con código 0.

El resumen numérico y estructural resultante coincide con el JSON R2 depositado:

- fidelidad del parser: **4.258/4.258 = 100 %**;
- cobertura RF1b con espacios inciertos separados: **29.590/34.381 = 86,065 %**, frente al 85,748 % del lookup exacto;
- recuperación de la brecha respecto al ZL3b canónico: **15,4 %**, clasificada por el protocolo como **LITTLE/NO RECOVERY**;
- no se promovió ninguna regla semántica.

Una lista de ejemplos de CONTENT-L difiere solo en el orden. Sus recuentos y todos los demás campos del resumen coinciden; el cambio es compatible con iteración no determinista de conjuntos y no altera las métricas.

## Límite reproducible del informe R1

El auditor `Voynich_Draft2_Reproducibility_Adversary_v1.py` no se puede ejecutar íntegramente desde el ZIP tal como está depositado. Además del estado Cycle28 incluido, requiere cinco tablas de entrada que no aparecen en el ZIP ni en sus paquetes R1/R2:

1. `Voynich_FINAL_Controlled_SourceOrder_Audit_v1.csv`
2. `Voynich_Cycle36_ContentL_StateR_OperationHistory_Audit_v1.csv`
3. `Voynich_Cycle37_QO_AN_Relation_Role_Audit_v1.csv`
4. `Voynich_Cycle39_D_OS_OM_OperationHistory_Audit_v1.csv`
5. `Voynich_Campaign4_Sealed_Folio_Split_v1.csv`

El depósito incluye un CSV de auditoría con otro nombre, además de resultados derivados; eso no proporciona los cinco ficheros que el script intenta leer. Por tanto, los cuadros de split, multiplicidad y contraste del informe R1 siguen siendo **resultados declarados por el autor**, no reproducidos de forma independiente en esta pasada. R2 sí se pudo reproducir con los archivos presentes.

## Qué significa la partición de validación

El propio informe adversarial corrige que el holdout original es por página/panel, no por hoja física: cinco caras físicas mezclan Discovery y Holdout, y 37 hojas tienen unidades en ambos grupos. Al excluir todas las hojas presentes en Discovery quedan solo **36 líneas y 290 tokens** del benchmark, demasiado pocos para varias comparaciones.

La partición por caras físicas del paquete R1 se presenta como sensibilidad/robustez y reconoce que no es un holdout genuinamente intacto, porque el material y las hipótesis ya habían sido examinados. Los resultados y p-valores asociados no se han vuelto a calcular aquí. El informe declara que 10/21 pruebas sobreviven BH y 2/21 Holm; quedan como cifras del informe hasta disponer de sus inputs.

## Nuevo endpoint estructural: cinco posiciones aún sin ledger

El PDF de 23444474 (163.508 bytes; MD5 Zenodo verificado: `c7d56f0d87122337ac38495b83253d81`) explica el cambio desde **12.294/12.495 (98,3914 %; 201 opacas)** en la entrega anterior a **12.299/12.495 (98,4314 %; 196 opacas)**: cuatro ocurrencias ARODY y una AIRODY promovidas a un papel derivacional amplio.

El texto delimita la cifra correctamente: es naturalizabilidad de papeles funcionales en un benchmark seleccionado, no exactitud de traducción, recuperación léxica ni porcentaje del manuscrito traducido. Sin embargo, el registro Zenodo 23444474 contiene solo ese PDF. El propio artículo recomienda acompañarlo de un endpoint ledger de 196 posiciones, exportaciones legibles por máquina y un mapa de afirmaciones a artefactos. No se adjuntan allí, así que la actualización de cinco posiciones está documentada pero todavía no puede reproducirse desde ese registro. El depósito previo mantiene el endpoint 12.294/12.495.

## Adjudicación

- **Reproducido en esta pasada:** integridad del ZIP y sus hashes internos; salida analítica de R2; desglose del cambio de cinco posiciones según el texto del PDF.
- **No reproducido:** las pruebas y estadísticas R1 dependientes de las cinco tablas ausentes; la asignación y la derivación exacta de las cinco posiciones nuevas sin ledger.
- **No establecido:** significado léxico ordinario, idioma fuente o traducción validada.

## Siguiente paso concreto

Localizar un depósito suplementario que contenga las cinco entradas del auditor R1 y el ledger/exportaciones de 196 posiciones del trabajo estructural. Si no existen públicamente, registrar esas ausencias como bloqueos de reproducibilidad y no reconstruir las tablas desde los valores publicados.

## Seguimiento de búsqueda de suplementos — 2026-11-07

Se comprobó el inventario público de archivos de los tres registros relacionados y se buscaron por nombre los cinco CSV ausentes y el ledger de 196 posiciones en los índices web y en el código del repositorio:

- El registro base [10.5281/zenodo.22049207](https://zenodo.org/records/22049207) enumera la edición, los preprints y el ZIP de 2,9 MB; el catálogo no enumera los cinco CSV como archivos independientes.
- La versión 2 del suplemento [10.5281/zenodo.23444474](https://zenodo.org/records/23444474) contiene un único archivo, el PDF de 163,5 kB.
- La versión 1 relacionada [10.5281/zenodo.23113674](https://zenodo.org/records/23113674) enumera el artículo, un documento de metadatos y otro PDF no relacionado con los datos tabulares; tampoco lista los cinco CSV ni el ledger.
- Las búsquedas exactas de nombres no encontraron una copia pública indexada de esas tablas ni del ledger.

**Adjudicación del seguimiento:** no se localizó un suplemento público que resuelva las entradas ausentes. Esto no demuestra que no existan copias privadas o no indexadas. La reproducción de R1 y el endpoint de 196 posiciones siguen **BLOCKED** por falta de entradas/ledger; el alcance reproducido de R2 no cambia. No se reconstruyen tablas a partir de cifras publicadas ni se afirma que el endpoint nuevo esté validado.
