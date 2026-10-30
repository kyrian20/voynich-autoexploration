# Conciliación de loci IVTFF sin tokens ASCII: high-ASCII frente a lectura ilegible

**Fecha:** 2026-10-30. **Tipo:** reparación acotada de la interpretación de cobertura, sin EXP nuevo. **Estado científico:** descriptivo; no se ejecuta predictor ni se traduce texto. **CI:** verificar en el SHA exacto de la PR antes de declarar éxito.

## Incidencia y antecedente

El inventario previo de EXP-590 (scripts/audit_exp590_empty_loci.py) identificó nueve loci ZL3b con cuerpo no vacío y sin tokens ASCII, pero no clasificó sus símbolos. El informe de ligaduras de 2026-10-22 dejó pendiente su identidad exacta. Esta intervención **no repite** la comparación de 39.594 tokens ni modifica el lector histórico: distingue qué información se pierde y cómo difieren las ediciones.

IVTFF 2.0.2 utiliza códigos high-ASCII de la forma @nnn; y el signo ? para lectura ilegible. Son clases distintas. El lexer existente (scripts/ivtff_lossless.py) y la proyección protegida (scripts/ivtff_rows.py) conservan ambos como unidades opacas. No se atribuye una letra descifrada ni un significado.

## Resultado de datos reales

| Fuente | Registros con cuerpo | Con tokens ASCII | Sin tokens ASCII | Filas con high-ASCII visible | Códigos visibles | Solo high-ASCII | Solo ? |
|---|---:|---:|---:|---:|---:|---:|---:|
| ZL3b | 5.385 | 5.376 | 9 | 122 | 168 | 9 | 0 |
| ZL3a | 5.389 | 5.380 | 9 | 117 | 160 | 8 | 1 |
| IT2a | 5.215 | 5.207 | 8 | 0 | 0 | 0 | 8 |

SHA-256 de entrada: ZL3b bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc; ZL3a 56419297682d338ff1a0a17f5ae251e3ee3e2c5bf05a62db04c5385ef30b36a2; IT2a 7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5.

Los nueve loci ZL3b son f49v.11, f49v.21, f49v.27, f49v.29, f49v.35, f49v.41, f66r.24, f66r.38 y f66r.42. En ZL3a los mismos nueve aparecen sin tokens ASCII, pero f66r.24 es ? en lugar de @169;. En IT2a ocho de ellos son ?, mientras f66r.38 no está entre los registros sin tokens ASCII. **Las ediciones no son muestras independientes; no se fusionan ni se vota para inventar una lectura.**

Los 168/160 códigos son spans visibles en el cuerpo **después de excluir alternativas entre corchetes**, como en la comparación histórica; pueden estar dentro de ligaduras. No son un censo de todas las alternativas. Las nueve filas ZL3b no son texto vacío: contienen códigos opacos. En ZL3a e IT2a, ? sigue siendo incertidumbre, no un glifo descifrado.

## Reparación, pruebas y conservación

El nuevo auditor scripts/audit_ivtff_high_ascii_coverage.py exige los SHA-256 congelados, valida estructura y filas físicas, coteja el tokenizador ASCII histórico con la proyección opaca y conserva locus, línea física, cuerpo y clasificación HIGH_ASCII_ONLY/UNREADABLE_ONLY. Rechaza desviaciones de los recuentos fijados y casos no adjudicados.

La regresión tests/test_ivtff_high_ascii_coverage.py cubre código aislado, código dentro de palabra, comentario, ligadura, alternativa excluida, ?, dígitos Unicode, código fuera de rango y separadores de fila falsos, además de las tres fuentes reales. La CI genera JSON y SHA-256 como artefactos de 90 días.

Comandos desde la raíz:

    python -m unittest discover -s tests -p 'test_ivtff_high_ascii_coverage.py' -v
    python -O -m unittest discover -s tests -p 'test_ivtff_high_ascii_coverage.py' -v
    python scripts/audit_ivtff_high_ascii_coverage.py --out ivtff-high-ascii-coverage.json
    sha256sum ivtff-high-ascii-coverage.json > ivtff-high-ascii-coverage.sha256

La salida se crea exclusivamente en una ruta nueva; no sobrescribe resultados de EXP-590. No hay semillas ni aleatoriedad. No se modifican transcripciones, resultados históricos, particiones prospectivas ni compromisos humanos.

## Limitaciones y autoauditoría

La reparación explica la diferencia entre **registros con cuerpo** y **registros con tokens ASCII**, no valida las métricas históricas ni certifica conformidad IVTFF completa. Los marcadores opacos no pueden introducirse como letras conocidas en un predictor; antes de cualquier nueva evaluación deben congelarse la política de ilegibilidad y la separación por hoja física.

**Target-awareness:** los recuentos se fijan por la sintaxis de los códigos y la selección ASCII previa, no por una métrica optimizada. **Feature-destroying:** se conservan @nnn; y ? sin atribuirles letras. **Extrapolación:** solo tres ediciones, no conformidad universal. **Resultado negativo:** la ausencia de high-ASCII en IT2a no invalida los códigos de ZL3b. **Control:** se espera que la vista ASCII descarte @140; y ?, mientras la vista opaca los conserve como unidades distintas; las pruebas sintéticas contrastan ambas conductas.

Siguen abiertos los asuntos independientes: adjudicación IVTFF completa, EXP-170 exacto, conciliación de artefactos y revisión de PR científicas. Evaluación general prevista para el 22-11-2026, sin garantizar descifrado.
