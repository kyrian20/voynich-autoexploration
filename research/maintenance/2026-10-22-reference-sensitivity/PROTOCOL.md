# Sensibilidad de la comparación de EXP259 a la referencia

Fecha 22-10-2026. Diagnóstico de mantenimiento, sin EXP nuevo. No se repite el parser del manuscrito ni se valida su asignación Currier.

Antes de ejecutar: reproducir solo las columnas de referencia de EXP259 con sus funciones aisladas; verificar las entropías mediante cálculo directo independiente de H(Y|X), sin la resta H(X,Y)-H(X). Comparar la entrada histórica bilingüe con dos vistas de César latino: archivo completo y cuerpo con los límites ya declarados en el bloque integrado. Mantener tokenización ASCII y 12 posiciones de EXP259 para no mezclar cambios de métrica.

Archivar todos los conteos, hashes y diferencias por posición. Criterio funcional: diferencia entre ambas implementaciones <=1e-12 bits, misma cantidad de tokens que el lector histórico, coincidencia con las columnas archivadas a su precisión impresa si los valores son reproducibles. Una discrepancia archivada se declara; no se ajusta el método para ocultarla.

La sustitución de Cicero bilingüe por César cambia simultáneamente idioma, autor, obra, tamaño y composición editorial: es una sensibilidad, no una estimación causal de contaminación. El contraste cuerpo/archivo de César sí aísla la exclusión editorial declarada dentro de ese archivo. No habrá p-valores ni afirmaciones de descifrado. En posiciones tardías cambian los supervivientes por longitud; no equivalen a posiciones relativas al final.
