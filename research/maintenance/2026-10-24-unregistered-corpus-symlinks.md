# Auditoría de enlaces no registrados en árboles de corpus — 24-10-2026

**Tipo:** reparación operativa acotada; no EXP. **Base fijada:** `83a44ef433ce89c519c7ea0532e054b3c0413a1b` (`master` tras PR #20). **Estado:** propuesta de revisión, no cierre ni validación científica.

## Defecto y demostración aislada

El inventario `scripts/check_corpus_integrity.py` construía `actual` exclusivamente con `rglob('*.txt')` y `p.is_file()`. Un enlace simbólico nuevo a un `.txt` inexistente devuelve `False` en `is_file()`, por lo que no figuraba en el inventario. Un directorio simbólico no registrado tampoco se inventariaba, pues `rglob('*.txt')` no lo incluía. Estos cambios en el árbol de datos podían pasar inadvertidos cuando existía al menos un corpus válido y no cambiaba su manifiesto.

Demostración sintética independiente en Python 3 (directorio temporal, sin corpus real): un `dangling.txt` y un `linked-dir` apuntando a destinos inexistentes dieron `set()` con el inventario antiguo, y aparecieron ambos con `rglob('*')` + `is_symlink()`. Esta prueba verifica la causa concreta, **no** la batería completa del repositorio.

## Reparación y criterio de aceptación

El auditor sigue calculando hashes/tamaños de archivos ordinarios exactamente como antes y conserva la prohibición de enlaces en rutas ya registradas. Añade un inventario independiente de enlaces simbólicos bajo `data/transcriptions` y `data/reference_corpora`, sin seguir sus destinos; rechaza los enlaces no registrados, incluidos los rotos y los directorios. Comprueba también si las dos raíces de corpus son enlaces.

Regresiones deterministas en `tests/test_corpus_integrity.py`:
1. Corpus normal con manifiesto válido debe pasar antes de añadir enlaces.
2. Un `dangling.txt` no registrado debe producir `Unregistered symlink in corpus tree`.
3. Un directorio simbólico no registrado debe producir el mismo error.
4. Las pruebas previas de enlaces registrados, hashes, vacíos y manifiestos deben seguir pasando.

**Sin semillas, azar ni llamadas de red.** No se cambian transcripciones, manifiestos, experimentos históricos, resultados negativos ni compromisos científicos. No se infiere que existieran estos enlaces en el repositorio: los casos son sintéticos.

## Puerta de cierre

Ejecutar `python tests/test_corpus_integrity.py`, `python scripts/check_corpus_integrity.py`, `python -m unittest discover -s tests -v` y `python scripts/audit_repository_operations.py`, además de `Voynich Check` sobre el SHA final de esta rama. Verificar después los resultados remotos y cualquier CI de `master` si se integra. Hasta entonces, la corrección permanece propuesta.

**Limitaciones:** solo se inventarían enlaces simbólicos bajo las raíces designadas; no se certifican procedencia científica, licencias, contenido semántico, conformidad IVTFF ni equivalencia con los archivos de Biblioteca. Las identidades históricas mal atribuidas y la conciliación de resultados siguen bloqueadas.
