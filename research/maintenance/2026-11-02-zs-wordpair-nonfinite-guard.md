# Zhang–Sheng: impedir correlaciones indefinidas en cuadrículas sin soporte (02-11-2026)

**Tipo:** corrección operativa de la reimplementación parcial, sin EXP nuevo. **Estado de descifrado:** sin traducción validada. Base inspeccionada: `master` `b5f585615bde372c46e1d33709078c6c4a3bba20`.

## Defecto y criterio de falsación

La función `metric()` aceptaba vistas sintéticas con un solo bloque de páginas con texto o vocabularios sin parejas elegibles. Un diseño aditivo con dos tipos podía llegar a `numpy.linalg.LinAlgError` sin diagnóstico del contrato científico; una vista con correlaciones constantes devolvía `NaN`, que `json.dumps` serializa por defecto como el valor no estándar `NaN`. Un recibo así no puede interpretarse como correlación válida ni compararse con los 54 registros congelados.

**Criterio antes de ejecutar:** para vistas sin pares admisibles, sin texto en ambas mitades, con diseño aditivo singular o con correlaciones no finitas, abortar con `ValueError` explícito sin devolver un recibo estadístico. Los dos registros históricos ya seleccionados (ZL3b e IT2a, vista split, 150 tipos, semilla 20261101, 20 barajados) deben seguir coincidiendo con el archivo congelado dentro de 1e-9.

## Reparación

- `research/maintenance/2026-11-01-zs-wordpair-audit/wordpair_audit.py`: guardas de pares y cobertura de ambas mitades antes de barajar, traducción de singularidad a fallo explícito, comprobación de finitud de las tres correlaciones. El campo descriptivo `shuffled_expected` refleja el número de barajados realmente solicitado, sin cambiar el algoritmo.
- `tests/test_zs_wordpair_source_lock.py`: dos nuevas regresiones sintéticas para cuatro condiciones adversariales, con separación de páginas por bloques de diez. Las pruebas existentes del contrato y reproducción parcial son la regresión positiva.

## Verificación exigida

```sh
python -m unittest discover -s tests -p 'test_zs_wordpair_source_lock.py' -v
python -O -m unittest discover -s tests -p 'test_zs_wordpair_source_lock.py' -v
python -m unittest discover -s tests -p 'test_zs_wordpair_archive_contract.py' -v
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

La integración y el cierre quedan sujetos a la CI de la PR y a la CI de `master` **posterior** a la fusión; este documento por sí solo no acredita ejecución. No se han editado los corpus originales, las 54 filas archivadas, las semillas históricas, los manifiestos reservados ni las afirmaciones comprometidas.

**Limitaciones:** no se han recalculado las 52 filas restantes ni reproducido la métrica exacta del artículo (la propensión no está especificada suficientemente). Esta reparación no demuestra independencia entre hojas de los bloques históricos ni semántica. EXP-170, adjudicación IVTFF y conciliación global de artefactos siguen pendientes.
