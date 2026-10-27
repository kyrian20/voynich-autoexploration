# Inventario EXP: enlaces a directorios omitidos — 27-10-2026

**Estado:** corrección propuesta; CI de PR y posterior a integración pendientes de verificación. Sin nuevo EXP, sin experimento científico y sin cambio de corpus.

## Defecto falsable

`scripts/audit_ambiguous_exp_references.py::scan` filtraba extensiones antes de detectar enlaces simbólicos. `Path.rglob("*")` (Python 3.12) enumera el enlace a un directorio, pero no desciende en él; como el enlace a un directorio normalmente carece de extensión `.md/.rst/.txt`, se omitía sin constar en `skipped_symlinks`. Así `coverage_complete_for_selected_files` podía ser `true` aunque una carpeta enlazada contuviera informes EXP no examinados.

Este es un **defecto del indicador de cobertura** de un inventario léxico; no demuestra que ningún informe original estuviera mal atribuido. No cambia las reglas de identificación ni atribuye experimentos por número.

## Reparación y alcance

Comprobar enlaces antes de filtrar extensiones, excluyendo previamente los corpus brutos y directorios de trabajo ignorados. Registrar los enlaces a directorios (y enlaces sin extensión, incluso rotos) como `skipped_symlinks`; mantener fuera del alcance los enlaces a archivos de extensiones no seleccionadas. No seguir enlaces ni leer sus destinos. El informe debe indicar cobertura incompleta cuando existe un enlace de directorio no inspeccionado.

Regresiones en `tests/test_ambiguous_exp_references.py`:
1. Enlace a directorio externo con `archived.md` y `EXP-177`: cero hits observados, enlace registrado, cobertura incompleta.
2. Enlace roto sin extensión: registrado, cobertura incompleta.
3. Enlace a `.py` no seleccionado: no cambia la cobertura de los tipos seleccionados.
4. Mantener los controles anteriores de enlaces a `.txt`, corpus brutos y referencias ambiguas.

**Comando de verificación:** `python -m unittest discover -s tests -p 'test_ambiguous_exp_references.py' -v`. El workflow `voynich-check.yml` ya ejecuta ese comando y publica `ambiguous-exp-references.json`; no es necesario crear otro workflow ni repetir experimentos.

## Integridad y límites

Base comprobada antes de crear rama: `3238c6e9f907024309a52ac2d7260ff079969cf2` (master, CI `40548493782` success). Los archivos de entrada, el registro congelado, los resultados históricos, las semillas y las particiones reservadas no se modifican. Las pruebas usan exclusivamente `TemporaryDirectory`, sin aleatoriedad. La ausencia de enlaces en un checkout no demuestra cobertura sobre Biblioteca ni archivos PDF/JSON excluidos. El indicador sigue siendo **cobertura del subconjunto textual**, no auditoría completa de artefactos ni validación científica.

**Autoauditoría:** no se ajustó ninguna métrica a resultados Voynich; no se destruye la característica medida (detección de enlaces); el control positivo es el directorio enlazado y el negativo un archivo `.py` excluido. Conservar toda ejecución fallida y registrar CI del SHA final antes de fusionar. No modificar `state/committed_claims.md`.
