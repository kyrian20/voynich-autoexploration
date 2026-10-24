# Errata de alcance — EXP-260 (24-10-2026)

**Estado: INVALID_FOR_CLAIM** para interpretar las cifras A=1,815, B=2,087 y «Latin»=0,781 como información mutua de Shannon de caracteres adyacentes, y para el cociente 2,3–2,7× como contraste validado frente a latín monolingüe.

La función histórica `compute_pmi` usa frecuencias globales de caracteres en vez de los marginales de pares `(c_i,c_{i+1})`, y suma únicamente bigramas que alcanzan `min_count=20`. Es una estadística heredada, no la MI estándar. Además, el archivo llamado `cicero_de_officiis_latin.txt` contiene **latín e inglés**, no un control latino puro.

Conservar sin cambios `script.py` y `result.md`. El auditor corregido y las pruebas, los hashes y la ejecución verificada se enlazan desde [el informe de adjudicación](../../research/maintenance/2026-10-24-exp260-mi-scope.md). Esta errata no invalida automáticamente las frecuencias de pares VMS ni aporta significado a ninguna secuencia.
