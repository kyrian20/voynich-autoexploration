# Auditoría acotada: etiquetas físicas indentadas en el censo de holdout (31-10-2026)

## Defecto y alcance

En `scripts/audit_holdout_locus_coverage.py`, `inspect_source` solo procesaba filas que empezaban literalmente por `<f`. Una cabecera ` <f2r>` o un locus `\t<f1r.2,@P0>` desaparecían del censo sin diagnóstico. El lector estricto `audit_ivtff_page_locus_ids.py` ya detecta algunos de estos casos y el crosswalk también puede detenerlos; el censo independiente, ejecutado por separado, no debía certificarlos. **Defecto de cobertura del lector**, demostrado con fixtures sintéticos, no alteración demostrada de los corpus.

## Corrección y prueba falsable

El lector de cobertura rechaza ahora una fila cuyo primer carácter estructural `<f` esté precedido por espacios o tabuladores. La comprobación precede al descarte de filas no estructurales; no interpreta texto ni cambia la selección de hojas. Las pruebas `test_indented_structural_tags_are_rejected` y `test_matching_hash_cannot_hide_indented_locus` verifican (1) cabecera indentada, (2) locus indentado y (3) que actualizar deliberadamente el SHA-256 del fixture y su manifiesto no evita el rechazo.

**Criterio de aceptación**: ambas regresiones pasan en Python normal y optimizado; la CI de la rama ejecuta el censo de fuentes originales y el crosswalk, compara byte a byte el snapshot congelado y termina en verde. Se exige comprobación posterior en `master` si se integra. No equiparar un estado pendiente con éxito.

## Reproducibilidad y límites

Comandos: `python -m unittest discover -s tests -p 'test_holdout_locus_coverage.py' -v` y `python -O -m unittest discover -s tests -p 'test_holdout_locus_coverage.py' -v`. El workflow canónico `.github/workflows/voynich-check.yml` ya contiene ambos comandos y la auditoría de los corpus originales. Sin aleatoriedad ni semillas; unidad = fila física con etiqueta estructural. El código usa los bytes originales en la auditoría de corpus; los casos adversariales son fuentes sintéticas. No se modifican corpus, particiones, manifiestos, snapshots históricos ni `state/committed_claims.md`.

**Limitaciones**: esta comprobación no certifica conformidad IVTFF integral, ni detecta todas las variantes posibles de etiquetas dañadas, ni verifica semántica, folios ciegos o descifrado. No reejecuta simulaciones EXP-170 ni resuelve su procedencia. La corrección es independiente de las PR de investigación #7 y #138.

## Autoauditoría metodológica

- **Calibración contra el objetivo**: ninguna; no hay métricas lingüísticas ni calibración Voynich.
- **Destrucción de la característica**: ninguna tokenización o transformación de tokens; se comprueba la visibilidad de filas físicas.
- **Extrapolación**: únicamente los casos de indentación ASCII probados, sin afirmación de limpieza global.
- **Resultado negativo**: los fixtures malformados deben ser rechazados; no se infiere mecanismo lingüístico.
- **Controles**: filas sintéticas válidas ya cubiertas por la suite; se espera que se acepten. El control adversarial se espera rechazado por indentación; verificar ejecución CI antes de registrar el resultado observado.

**Pendientes científicos**: procedencia exacta de EXP-170, adjudicación IVTFF completa, conciliación de artefactos y revisión de borradores #7/#138. Evaluación general: 22-11-2026, sin prometer traducción.
