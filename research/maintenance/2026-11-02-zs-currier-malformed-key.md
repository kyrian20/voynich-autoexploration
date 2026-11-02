# Corrección acotada: claves $L malformadas ignoradas silenciosamente

**Fecha:** 2026-11-02. **Base:** `master` `4a03826ebf4a931143522178d5c811af403720cb`. **Tipo:** defecto de integridad del lector IVTFF; sin nuevo EXP. **Estado:** pendiente de CI y revisión al abrir la PR.

## Incidencia comprobable

La corrección anterior de metadatos Currier (PR #239) introdujo `CURRIER_FIELD = re.compile(r"\\$L(?![A-Za-z0-9_])[^ \\t<>]*")`. Ese lookahead negativo **omite** claves que empiezan por `$L` y siguen con letras, cifras o guion bajo. Por ejemplo, `<! $Lfoo>`, `<! $L1=A>` y `<! $L_foo>` no producían coincidencias; `checked_currier_metadata` devolvía `None` en lugar de rechazar una declaración corrupta. Esto podía convertir silenciosamente un error de entrada en clase Currier desconocida. La PR #239 comprobaba valores malformados, pero no nombres de clave malformados.

## Reparación y prueba falsable

Se elimina el lookahead negativo, capturando **todos** los campos que comienzan por `$L` y delegando la validación al contrato ya existente: exactamente un campo, igual a `$L=A` o `$L=B`. Los campos `$Q` y `$I` no se confunden con Currier. Una regresión nueva exige `ValueError` para seis cabeceras adversariales en **ambos** lectores (`read_pages` y `read_pages_legacy`): doce rechazos esperados. Los tests previos mantienen los casos válidos, los valores malformados y la ausencia legítima de `$L`.

**Antes de cambiar el repositorio** se comprobó localmente con Python que el patrón anterior devolvía `[]` para `$Lfoo`, `$L1=A` y `$L_foo`, pero reconocía `$L=A`. Esto demuestra el defecto del patrón, **no** sustituye la regresión completa en CI.

## Comandos y aceptación

```sh
python -m unittest discover -s tests -p 'test_zs_wordpair_source_lock.py' -v
python -O -m unittest discover -s tests -p 'test_zs_wordpair_source_lock.py' -v
python -m unittest discover -s tests -p 'test_zs_wordpair_archive_contract.py' -v
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

No declarar éxito hasta verificar la ejecución GitHub Actions del SHA exacto y, si se integra, una ejecución posterior de `master`. La reproducción numérica automatizada de la auditoría Zhang–Sheng cubre **solo 2 de 54** filas archivadas; no se extrapola al resto.

## Preservación, alcance y límites

No se editan transcripciones originales, los 54 resultados históricos, particiones, semillas, archivos de EXP-170, `state/committed_claims.md` ni resultados negativos. SHA-256 congelados: ZL3b `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`; IT2a `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`. No se ha encontrado evidencia de estas claves malformadas en los corpus congelados; el defecto se reproduce mediante entradas sintéticas. La métrica de pares actual no usa el valor Currier, por lo que **no se afirma que cambien sus puntuaciones**.

Sigue pendiente la conformidad IVTFF integral, la identidad exacta de las entradas externas de EXP-170, la conciliación general de artefactos y la evaluación científica de PR #7 y #138. Esta reparación no es una traducción. Evaluación global prevista: 2026-11-22, sin garantía de desciframiento.
