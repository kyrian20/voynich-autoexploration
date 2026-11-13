# Errata de alcance — EXP-436 (9-11-2026)

**Estado:** comparación con controles lingüísticos `INVALID_FOR_CLAIM` hasta verificar las fuentes. Se conserva intacto `result.md` y el script histórico. Esta revisión no recalcula sus estadísticas ni crea un EXP nuevo.

## Incidencias confirmadas en el repositorio

1. El script de EXP-436 usa `data/reference_corpora/latin/caesar_gallic_wars.txt` como “Latin (Caesar)”. El registro congelado identifica esos mismos bytes como una **traducción inglesa** de *De Bello Gallico and Other Commentaries* (SHA-256 `eaa456256c46507f872efd965335b370605e6d323ca89ef2012cb71b516183d7`, 964,557 bytes). Por ello, los 23,274 tokens y la razón 1.79× archivados no son una medición de un corpus latino y no respaldan la conclusión de que el gradiente sea universal o mayor en latín que en Voynich.

2. El script busca el control italiano en `data/reference_corpora/italian/dante_divine_comedy_italian.txt`, ruta que no existe en el árbol actual. El manifiesto sí contiene `data/reference_corpora/italian/dante_divina_commedia.txt` (SHA-256 `76a06f77ea52d4c815f27251fa253ddc8383dfdae49a44065e45a15adec828a6`), pero no hay evidencia de que sean los mismos bytes que produjeron la fila italiana del informe. Como el script solo analiza esa fila si la ruta existe, el informe italiano tampoco se puede atribuir al script y a una entrada identificada del checkout actual.

## Alcance conservado

Los cocientes VMS A/B copiados de F435 no quedan automáticamente refutados por estas dos incidencias, pero esta auditoría no los reproduce ni valida. Tampoco se puede concluir lo contrario sobre latín o italiano: sus comparaciones quedan sin resolver hasta fijar y documentar entradas apropiadas y trazables. No se sustituyen corpus, no se modifican resultados históricos ni `state/committed_claims.md`.

La pregunta abierta Q022 registra el siguiente paso de procedencia. La eventual comparación con latín auténtico y una entrada italiana identificada debe tratarse en una revisión separada, con salidas nuevas y sin reutilizar las cifras históricas como si fueran reproducidas.

## Divergencia adicional del script consultado — 13-11-2026

La revisión de `script.py` en `master` muestra ahora `LATIN_CORPUS` apuntando a `data/reference_corpora/latin/caesar_de_bello_gallico_latin.txt`, **no** a `caesar_gallic_wars.txt` como describe la instantánea histórica anterior. La primera incidencia de esta errata documenta la identidad del control inglés del archivo histórico, pero **no** demuestra que el script actualmente consultado haya generado la fila archivada de 23.274 tokens ni que la ruta nueva contenga el mismo texto. Son afirmaciones diferentes: identidad de la entrada inglesa archivada y linaje de ejecución del script presente.

**Regla de integridad:** conservar ambos nombres de archivo, los números originales y esta discrepancia; no ejecutar el script actual y denominarlo «reproducción» de EXP-436 sin recuperar la versión exacta del código, entradas, parámetros y logs de aquella ejecución. El estado de las filas latina e italiana permanece `INVALID_FOR_CLAIM`. Una ejecución nueva con fuentes adjudicadas deberá publicarse por separado, con hashes y resultados propios. Esta nota no modifica `script.py`, `result.md`, los corpus ni los compromisos científicos.
