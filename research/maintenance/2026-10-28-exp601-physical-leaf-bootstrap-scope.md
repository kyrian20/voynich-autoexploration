# EXP-601: corrección de alcance del bootstrap histórico por «folio»

**Fecha:** 2026-10-28. **Tipo:** adjudicación retrospectiva de la unidad de remuestreo, sin experimento nuevo. **Estado:** INVALID_FOR_CLAIM únicamente para intervalos descritos como agrupados por **hoja física** y sensibilidad de exclusión de **hoja física**. La prueba histórica y sus resultados permanecen congelados.

## Defecto verificable

En `experiments/exp_601_folio_clustered_confirmation/script.py`, la función `parse` guarda como `folio` la cabecera `fNNr`, `fNNv` o `fNNv3`. El bootstrap agrupa por ese identificador completo y remuestrea los elementos de `folio_rows` de manera independiente. No agrupa las dos caras ni los paneles que pertenecen a una misma hoja numerada. La función leave-one-out excluye también una **cara/panel**, no la hoja física.

El JSON archivado identifica **81 unidades de remuestreo** pero solamente **40 hojas físicas numeradas**. De estas, 36 contienen las dos caras en el conjunto histórico; 35 hojas tienen dos unidades, dos hojas tienen cuatro unidades (86: cuatro paneles v; 95: dos r y dos v), y tres hojas tienen una sola unidad (57, 85 y 116). Se puede verificar la identidad de cada grupo en el JSON derivado de la auditoría. Una hoja con varias unidades puede entrar repetidamente de forma parcial en una réplica bootstrap, en vez de entrar/salir completa como conglomerado.

Por tanto, el intervalo histórico `[2.115596, 3.59317]` de 20.000 réplicas con semilla `60120261019` **no debe citarse como intervalo bootstrap por hoja física**. Tampoco el rango leave-one-out `[2.640358, 2.930637]` debe presentarse como sensibilidad a excluir una hoja física completa. No se ha demostrado que los intervalos corregidos cambien de signo o que el efecto desaparezca: **no se ha recalculado un bootstrap físico**.

La tasa descriptiva histórica `88/31.279224 = 2.813369` se conserva como dato del lector histórico. El p de aleatorización uniforme *dentro de cada línea* `0.00005` responde a un nulo distinto y no depende de la afirmación de bootstrap físico; su interpretación continúa condicionada por el tokenizador y la selección histórica.

## Identidad y protección de originales

- Script congelado Git blob SHA-1: `1bdb44324c0e27483d0e57fbc7ec37795745d2a8`.
- Resultados congelados Git blob SHA-1: `485e489c2552d4b492ae11a51f063cdea8524de7`.
- Corpus ZL3b SHA-256: `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- Semilla: `60120261019`; réplicas: 20.000; líneas elegibles: 2.325.
- Auditor nuevo: `scripts/audit_exp601_physical_leaf_cluster_scope.py`; pruebas: `tests/test_exp601_physical_leaf_cluster_scope.py`.
- El lector `scripts/audit_exp601_paired_reader_bootstrap.py` usa la misma definición histórica de `folio` al reproducir el intervalo y comparar dos políticas de lectura. **Su comparación no certifica agrupación por hoja física**; no se ha modificado ni vuelto a ejecutar como un experimento nuevo.

## Cierre verificable

La CI debe ejecutar las pruebas normales y con `-O`, ejecutar el auditor de solo lectura con salida exclusiva y publicar el JSON y su SHA-256. La auditoría exige las identidades congeladas y detecta alteraciones de unidades, semillas y tamaños. Hasta verificar una ejecución real, la reparación es una propuesta.

```sh
python -m unittest discover -s tests -p 'test_exp601_physical_leaf_cluster_scope.py' -v
python -O -m unittest discover -s tests -p 'test_exp601_physical_leaf_cluster_scope.py' -v
python scripts/audit_exp601_physical_leaf_cluster_scope.py --out exp601-physical-leaf-scope.json
sha256sum exp601-physical-leaf-scope.json
```

**Autoauditoría:** no se calibran parámetros mirando un resultado objetivo; no se destruyen tokens ni rasgos porque no se reprocesa el texto; la invalidación se limita a la afirmación de unidad de remuestreo; no se niega el resultado descriptivo ni se transforma un negativo en positivo. El control sintético agrupa `f86v3/f86v4` y `f95r1/f95v2` por número físico, y rechaza identidades malformadas. No se asigna significado a `daiin`.

**Siguiente paso:** tras CI y revisión, estudiar por separado un nuevo intervalo con conglomerados por hoja física (y controles de verdad conocida), preregistrado y sin reetiquetarlo como reproducción del intervalo histórico. Mantener los bloqueos IVTFF y de compromisos contradictorios. Evaluación general: 2026-11-22, sin promesa de descifrado.
