# EXP-001 — alcance de la afirmación sobre entropía inicial (23-10-2026)

**Estado:** adjudicación metodológica y control matemático sintético. No se crea EXP ni se reproduce el cálculo del Voynich. Base consultada: 465b2cf05ce1d5715f93894e16dd5c9b5d9753af. Continuación de los cuatro lectores ya reproducidos, sin repetirlos. El informe original, script y corpus permanecen intactos.

## Hallazgo delimitado

El informe histórico de EXP-001 presenta H_initial=3,137 y h2=2,341 bits para el manuscrito y afirma «The pure glossographic model is contradicted». La diferencia H_initial-h2=0,796 compara dos cantidades distintas: entropía marginal del primer carácter de cada palabra frente a entropía condicional entre caracteres adyacentes en una cadena de palabras concatenadas sin separadores. Por sí sola **no demuestra existencia de léxico semántico ni descarta una familia general de generadores sin significado**. Tampoco prueba que un modelo específico de restricciones uniformes sea compatible: esa hipótesis estrecha necesita un generador explícito y predicciones comprobables.

Se ejecutó un **control adversarial sintético**, sin ajustar parámetros al manuscrito: 128 ciclos deterministas de cuatro palabras con inicio a/b/c/d y ocho letras z. Produce 512 palabras sin contenido semántico, H_initial=2,000000000, h2=0,704577821 y una diferencia **+1,295422179 bits** con las fórmulas estadísticas de EXP-001 reimplementadas de forma independiente. Por tanto, una diferencia positiva, incluso mayor que la histórica, es compatible con un mecanismo explícito no léxico. No es un ajuste a la distribución del Voynich ni un modelo plausible de todos sus rasgos. SHA-256 de la secuencia sintética con palabras separadas por salto de línea y salto final: edd63e1a21774aa14e2ba7d9729f41baaed58b6abd90e252adbc412cd36fb075.

El lector de EXP-001 toma **991.553 tokens** de data/reference_corpora/latin/vulgate.txt, cuya identidad ya fue adjudicada como **traducción inglesa Douay-Rheims**, no Vulgata latina. La cifra histórica «Latin Vulgate» (H_initial=3,978) **no sirve como control monolingüe latino**. Esto ya estaba identificado en el manifiesto y en la auditoría de lectores; aquí se enlaza a la afirmación concreta, sin presentar la identidad como descubrimiento nuevo.

## Trazabilidad y comprobaciones

- Fuentes primarias internas: experiments/exp_001_word_initial_entropy/script.py (SHA-256 91cb9febee7752d56fe91eeaa43155590b405b46cdd18330acb9271fd7816f59), result.md (blob Git SHA-1 2feb8c7dbb268f46d6a7995ddd2c15a76f6bd907), research/maintenance/2026-10-22-remaining-readers/results.json y research/CORPUS_IDENTITY_REVIEW.json.
- Corpus de referencia: SHA-256 d63b1b81824e259b1cf92ba8a6e5cbbf783e2a83214cf2c3db2ecd1459165bfe, recuperado del snapshot del lector reproducido, **no recalculado en este entorno**.
- Código: scripts/audit_exp001_claim_scope.py; salida congelada results.json; pruebas tests/test_exp001_claim_scope.py. Python estándar. Parámetros: repeats=128, suffix_length=8, orden abcd, sin semilla ni aleatoriedad.
- Comandos desde checkout completo: python tests/test_exp001_claim_scope.py y python scripts/audit_exp001_claim_scope.py --check research/maintenance/2026-10-23-exp001-claim-scope/results.json. El segundo comprueba hashes del script y corpus, blob del informe, identidad y salida sintética; falla ante divergencia.
- **Ejecutado localmente:** 5/5 pruebas puras correctas y cálculo del control sintético. **No ejecutado aquí:** auditor integral sobre checkout completo, métricas históricas, control latino adjudicado. La CI del commit debe comprobarse por separado; la CI principal puede limitarse a sintaxis.

## Autoauditoría (skills/audit_experiment.md)

**Target-awareness:** no se calibran símbolos, longitud, repeticiones ni parámetros al manuscrito; el ejemplo prueba solo la no implicación lógica. Comparación con el valor histórico retrospectiva y exploratoria.

**Feature-destroying implementation:** se reproduce la convención histórica de concatenar palabras sin marcadores al calcular h2, que incluye transiciones de frontera. No se cambia el parser original.

**Extrapolación:** un contraejemplo invalida la implicación universal «brecha positiva implica léxico o excluye generadores sin significado», pero no demuestra que cualquier generador sea compatible ni refuta modelos particulares definidos.

**Negative-result scope:** solo se limita una interpretación de EXP-001 y la validez del control mal rotulado. No se infiere nada sobre traducción o ausencia de significado.

**Control behavior:** se espera H_initial=log2(4)=2 bits por cuatro onsets equiprobables y se observa 2. Se espera h2<2 por las ocho z deterministas y se observa 0,704577821. Es un control constructivo, no un test estadístico sobre el manuscrito.

## Próximo paso falsable

No repetir EXP-001 sin justificación. Preregistrar dos modelos generativos concretos, entrenar solo en folios de desarrollo y evaluar predicción de primeras letras en folios retenidos, con controles de longitud, sección y transcripción. Comparar con baseline de distribución de inicios y generador sintético con estructura conocida. Informar efectos e intervalos por folio y sensibilidad al parser. Resolver primero dependencias IVTFF y colisiones de IDs. No interpretar mejoras como traducción.
