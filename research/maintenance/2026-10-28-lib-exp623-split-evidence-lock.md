# LIB-ORDER-2026-10-19-A/B — bloqueo de identidad de particiones (28-10-2026)

**Tipo:** reparación acotada de integridad de evidencia; no es un EXP nuevo ni una reproducción de puntuaciones históricas. **Estado del defecto:** corregido en esta rama, pendiente de verificación de CI e integración. La decisión científica de [la adjudicación anterior](2026-10-28-lib-exp623-physical-leaf-leakage.md) no cambia: INVALID_FOR_CLAIM para generalización a hojas físicas completamente reservadas.

## Defecto reproducido

El comprobador `check_expected` de `scripts/audit_library_exp623_leaf_leakage.py` contrastaba **solo el número** de hojas físicas compartidas en cada una de 60 particiones. Sustituir una hoja compartida por otra, conservando la longitud de la lista, pasaba ese contrato. También podían cambiar silenciosamente la semilla o los tamaños de entrenamiento/prueba. Una demostración sintética sobre el JSON archivado sustituyó el identificador de la primera hoja compartida sin alterar su recuento.

## Corrección y procedencia

Se conserva el contrato de los 60 recuentos y se añade SHA-256 de la serialización JSON canónica de **cada serie completa de filas** (`sort_keys=True`, `separators=(',', ':')`, `ensure_ascii=False`, UTF-8). Quedan protegidas las identidades exactas de hojas compartidas, semillas, tamaños de train/test y cantidad/orden de filas. Se compara contra el artefacto de CI **posterior a la integración de PR #126**, no contra valores reconstruidos ahora.

- Run fuente: https://github.com/kyrian20/voynich-autoexploration/actions/runs/40695242744
- Artefacto: `library-exp623-leaf-leakage-40695242744`, ID `12819575881`, ZIP de 4188 bytes.
- SHA-256 del ZIP descargado y cotejado con el metadato de GitHub: `57fbae626ca3bdbc7f00d04c386ebcbcc59e3ab679611178fa6480614f0f6de7`.
- Miembro `library-exp623-leaf-leakage.json`: 55062 bytes, SHA-256 `4ed3ca9b595a511c27ce172e913f4c6f3b6b1a136117ef8c202fb5c2cda421bf`.

| Corpus | Serie | SHA-256 de filas canónicas |
| --- | --- | --- |
| ZL3b | A_all_tokens (20) | `cf0300ffdc468930c99c1e4e6622611062467eff9c9a524390bf6dd508f4415d` |
| ZL3b | B_interior_tokens (10) | `07d3fbfeafdacfa4c8c801ee19fe188ac5d312f3f73b0c0ef302ee031d6435df` |
| IT2a | A_all_tokens (20) | `48bea7c3f3e07df730ce08830ce4b1f7a6f48ca808b144bb176e6995a144d6b8` |
| IT2a | B_interior_tokens (10) | `07d3fbfeafdacfa4c8c801ee19fe188ac5d312f3f73b0c0ef302ee031d6435df` |

La coincidencia entre las dos series B refleja la misma elegibilidad de caras en las dos transcripciones, **no independencia** de las fuentes. Los hashes de corpus y scripts originales, las semillas y los 60 recuentos siguen fijados en el informe previo y el código; no se han modificado.

## Verificación y regresiones

Comprobación local sobre el ZIP descargado: los cuatro hashes canónicos coinciden exactamente; tres mutaciones sintéticas (identidad de hoja sin cambiar recuento, semilla, tamaño train) producen un hash distinto. Las pruebas automatizadas se amplían para rechazar esas tres mutaciones y conservar el rechazo por deriva de recuentos.

Comandos para reproducir en el árbol completo (CI debe ejecutarlos antes de declarar éxito):
```sh
python -m unittest discover -s tests -p 'test_library_exp623_leaf_leakage.py' -v
python -O -m unittest discover -s tests -p 'test_library_exp623_leaf_leakage.py' -v
python scripts/audit_library_exp623_leaf_leakage.py --check --out library-exp623-leaf-leakage.json
```

## Límites y decisión

Esta es una **reparación del control de integridad**, no una reparación de la fuga histórica. La fuente de referencia es un artefacto previo generado por nuestro propio auditor, no una reproducción independiente de las implementaciones originales de Biblioteca. Una reconstrucción equivocada pero estable también puede superar estos hashes. No se han reentrenado modelos, puntuado tokens ni utilizado los folios reservados para seleccionar hipótesis. Ningún significado ni traducción está validado. La adjudicación de IVTFF y la reproducción de las puntuaciones históricas permanecen bloqueadas.

**Siguiente paso:** una evaluación nueva, preregistrada y agrupada por hoja física, únicamente después de resolver los bloqueos metodológicos y disponer de las entradas exactas; mantener separado el alias LIB-ORDER del GH-EXP-623.
