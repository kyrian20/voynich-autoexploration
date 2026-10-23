# Auditoría descriptiva del denominador de EXP-173

Estado inicial: PROPOSED. Fecha: 23-10-2026. Base: c70a0ba5a97276edce09d7bfe7b8dc88514a2881.

Se conserva exactamente el lector histórico ya cotejado y se seleccionan exclusivamente sus líneas con $L=B explícito. No se crea EXP, no se cambia tokenización ni se reinterpreta C005/C006. Es una auditoría retrospectiva del denominador, no una prueba confirmatoria.

Para cada línea i, n_i es su longitud y k_i la cantidad de tokens con el rasgo (-am o inicio y). Bajo permutación uniforme de tokens dentro de cada línea, la esperanza de presencia del rasgo en un extremo es k_i/n_i. La suma de esas fracciones es la esperanza exacta del conteo total, sin simulación ni supuesto de independencia entre líneas para calcular esa esperanza. La distribución conjunta, los intervalos y los valores p no se calculan.

Publicar para ambos rasgos: observado O; esperanza histórica L*K/N; esperanza por línea sum(k_i/n_i); cocientes O/E; cantidad de folios numéricos y páginas; número de líneas unitarias, donde el extremo no puede moverse. Las fracciones se conservarán como racionales exactos. No elegir umbral según resultados. Ningún cociente constituye identificación lingüística.

Control sintético previo: líneas [yam,x], [a,b,c,d,e,xxam]. Para -am se espera 1/2+1/6=2/3 en el extremo final; para inicio y se espera 1/2 en el inicial. Exhaustar los 2!*6! órdenes debe coincidir. El control conserva inventario y longitud por línea; destruye deliberadamente orden y vecindad, por lo que no contrasta hipótesis que los requieran. El lector IVTFF completo y la incertidumbre por folio siguen pendientes.
