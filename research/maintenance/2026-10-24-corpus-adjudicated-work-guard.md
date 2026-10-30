# Identidad de obra en el registro de exclusiones — 24-10-2026

**Tipo:** corrección de integridad de metadatos históricos; sin nuevo EXP.  
**Base examinada:** `master` `561a5f9d4b9af0ae35260c6a89b6e297e0276431`.  
**Estado inicial de este documento:** propuesta; verificar CI de la rama y después CI de `master` si se fusiona.

## Defecto concreto

El auditor `scripts/audit_corpus_identity_overlay.py` comprobaba que `adjudicated_work` fuera una cadena no vacía, pero no que coincidiera con la identidad de obra registrada para cada una de las seis exclusiones. Por tanto, un cambio de `The Bible, Douay-Rheims, Complete` a `Invented work`, o incluso a `The Book of Mormon #17`, no activaba esa comprobación, aunque los bytes, hashes, cabeceras y demás evidencias fueran idénticos. Se trata de un fallo de detección de deriva documental, **no** de una nueva identificación independiente de textos.

## Reparación acotada

Se fijan las seis cadenas `adjudicated_work` ya existentes en `research/CORPUS_IDENTITY_REVIEW.json` mediante `EXPECTED_WORKS`, sin modificar el registro, los corpus ni los resultados originales. La función `audit` rechaza ahora un valor distinto para cualquiera de las seis rutas. Una nueva adjudicación legítima requeriría una revisión explícita y coordinada de la evidencia y de esta puerta, no un cambio silencioso.

Se añade `test_changed_adjudicated_work_rejected_even_if_nonempty`, con dos variantes deterministas: obra inventada y obra real de otro corpus. **Semilla:** no aplica; fixtures temporales sin aleatoriedad. **Criterio de aceptación:** las dos variantes deben producir el error `Historical adjudicated work changed`, y las pruebas previas y los seis registros congelados deben seguir pasando.

## Procedimiento de comprobación

```sh
python -m unittest discover -s tests -p 'test_corpus_identity_overlay.py' -v
python scripts/audit_corpus_identity_overlay.py
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

El workflow `.github/workflows/voynich-check.yml` ejecuta el auditor y las regresiones en la PR. Los hashes SHA-256 y tamaños de los corpus siguen en `research/CORPUS_INPUT_MANIFEST.json`; las identidades y sus evidencias siguen en `research/CORPUS_IDENTITY_REVIEW.json`. El SHA Git de los archivos modificados y los logs remotos quedan vinculados a la PR. No se recalculan ni sustituyen resultados históricos.

## Límites

Esta reparación garantiza consistencia de las **etiquetas de obra registradas**, no demuestra que dichas etiquetas sean científicamente correctas ni que los experimentos antiguos utilizaran esos bytes. Tampoco resuelve los lectores históricos bilingües, las entradas exactas de Naibbe, la adjudicación IVTFF ni la conciliación de artefactos. No se ejecuta ningún ciclo científico nuevo. El resultado de las pruebas debe documentarse después de su ejecución real, nunca presumirse.
