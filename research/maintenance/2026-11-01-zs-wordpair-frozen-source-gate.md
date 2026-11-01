# Reparación acotada: procedencia de entradas en la auditoría Zhang–Sheng

**Fecha:** 2026-11-01  
**Alcance:** control operativo de procedencia; no es reproducción del artículo ni nuevo experimento científico.  
**Estado inicial:** propuesto en PR; la integración y la CI se deben verificar por commit.

## Defecto demostrado en el código previo

En `research/maintenance/2026-11-01-zs-wordpair-audit/wordpair_audit.py`, `main()` publicaba el SHA Git de ZL3b/IT2a como **constante**, mientras que calculaba un SHA-256 de los bytes efectivamente presentes **sin exigir que coincidiera con la entrada congelada**. Un fichero sustituido conservando su nombre podía alimentar nuevas métricas bajo un recibo que seguía atribuyendo el SHA Git histórico. Además, cada política abría de nuevo la ruta después del cálculo del digest, dejando una ventana entre la verificación y el análisis. No hay evidencia de que se hayan sustituido los corpus en la ejecución archivada; es un defecto de validación de entradas, no una refutación de sus números.

## Reparación

- `load_verified_source()` acepta exclusivamente `eva_zl3b.txt` e `eva_it2a.txt`; comprueba SHA-256 y SHA Git calculados sobre **los mismos bytes**, frente a los dos pares congelados publicados en el informe original. Si difieren, lanza `ValueError` antes de cualquier cálculo.
- Se rechazan rutas con enlaces simbólicos, incluido un directorio padre. La lectura de la fuente se realiza una sola vez; las políticas `split`, `join` y `legacy_ascii` consumen el texto verificado en memoria.
- El import de NumPy pasa a la función que lo necesita, de forma que las regresiones de procedencia se puedan ejecutar sin instalar las dependencias numéricas del experimento.
- Se incorporan seis tests `unittest`: los dos corpus reales, mutación adversarial, nombre no autorizado, enlace al fichero, enlace en el directorio y lector que no reabre la ruta. La CI los ejecuta con Python normal y optimizado (`-O`).

**Entradas congeladas:**

| Fuente | SHA-256 | Git blob SHA |
|---|---|---|
| ZL3b | `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc` | `2a4533ab9bdfa85db9bad602d590978953055df1` |
| IT2a | `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5` | `4d6d3f2537b1f507a257529b49c94af7d6e03446` |

**Comandos de regresión:**

```sh
python -m unittest discover -s tests -p 'test_zs_wordpair_source_lock.py' -v
python -O -m unittest discover -s tests -p 'test_zs_wordpair_source_lock.py' -v
```

## Alcance científico y límites

Esta reparación no cambia la fórmula de correlación, el conjunto de pares, las semillas 20261101–20261103, los barajados, el corpus original ni el JSON archivado. Tampoco reejecuta la auditoría completa: el valor del preprint continúa **no reproducido**, en particular por la fórmula de corrección de propensión y las diferencias de población. Una prueba de fuente inmutable no valida una métrica. La ejecución completa requiere NumPy y debe auditarse por separado antes de promover afirmaciones científicas.

**Verificación:** consultar los checks y logs de la PR correspondiente y la ejecución posterior de `master` si llega a integrarse; no inferir éxito de este documento.
