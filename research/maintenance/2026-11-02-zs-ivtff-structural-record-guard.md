# Reparación acotada: contrato estructural IVTFF en lectores Zhang–Sheng

**Fecha:** 2026-11-02. **Tipo:** corrección de integridad de lectores, sin EXP nuevo ni traducción.
**Base inspeccionada:** master bb62736ed60d657c5817e600137e3c97af127449.
**Referencia interna:** scripts/audit_ivtff_page_locus_ids.py (contrato de identificadores ya adjudicado); norma research/RESEARCH_INTEGRITY_STANDARD.md.
**Alcance:** research/maintenance/2026-11-01-zs-wordpair-audit/wordpair_audit.py y tests/test_zs_wordpair_source_lock.py.

## Defecto comprobable

Los lectores read_pages y read_pages_legacy aceptaban una etiqueta sin separación del cuerpo, por ejemplo <f1r.1,@P0>daiin, y descartaban silenciosamente una etiqueta estructural desplazada con espacio o tabulación inicial. Una etiqueta de página sin < podía desaparecer como si fuese un comentario. Además, el patrón de locus anterior aceptaba códigos de localización con espacios, Unicode, tabulaciones o sufijos de transcriptor arbitrarios; una fila excluida por categoría podía ocultar el defecto. El auditor estructural del repositorio ya exigía códigos de tres caracteres ASCII imprimibles y sufijo opcional de un carácter.

Estos son **fallos potenciales de aceptación/omisión en entradas malformadas**, no evidencia de corrupción de las transcripciones congeladas. No atribuirles un cambio observado de puntuación sin recalcularlo y documentarlo.

## Corrección y falsación

En el iterador físico compartido se rechazan etiquetas <f...> con sangría, cuerpo pegado tras > y prefijos estructurales sin < que correspondan a página o locus reconocible. Se limita la gramática de locus a un índice de 1–3 dígitos ASCII, coma, código de tres caracteres ASCII imprimibles sin delimitadores y transcriptor opcional de un carácter ASCII. Se mantienen los controles existentes de duplicados, página activa y línea cero.

**Criterio previo a CI:** cuatro regresiones nuevas deben rechazar en ambos lectores los casos adversariales descritos y aceptar las filas válidas con separación por tabulación, @P0;A y +P0. Deben seguir pasando la auditoría de las transcripciones originales, la reproducción acotada de 2/54 filas archivadas y la CI del commit exacto. No se altera el universo P/C/R ni se ajustan parámetros mirando la puntuación.

Comandos de comprobación desde la raíz:

    python -m unittest discover -s tests -p 'test_zs_wordpair_source_lock.py' -v
    python -O -m unittest discover -s tests -p 'test_zs_wordpair_source_lock.py' -v
    python -m unittest discover -s tests -p 'test_zs_wordpair_archive_contract.py' -v
    python scripts/audit_repository_operations.py
    python scripts/check_corpus_integrity.py

## Preservación y límites

No se modifican data/transcriptions/, results.json (54 filas), semillas 20261101–20261103, controles, manifiestos reservados, resultados negativos ni state/committed_claims.md. Las entradas fijadas conservan sus hashes SHA-256: ZL3b bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc e IT2a 7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5.

Esta reparación **no certifica conformidad IVTFF completa**, no reproduce el preprint Zhang–Sheng, no valida independencia física de las mitades históricas ni desbloquea EXP-170. El estado de sus 54 resultados sigue siendo una auditoría descriptiva parcial; 52 filas no están cubiertas por el replay de CI. El control adversarial es sintético. No hay recuperación de texto plano.

**Cierre condicionado:** comprobar la ejecución de la PR y, si se integra, el run posterior de master, sus logs y el contenido de los artefactos pertinentes. Sin esas pruebas no afirmar reparación integrada ni resultados históricos reproducidos.
