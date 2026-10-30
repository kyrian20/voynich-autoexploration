# Reproducción acotada del predictor residual V2
25-10-2026. **REPRODUCED** sobre entradas analíticas congeladas; no evaluación nueva ni réplica por investigador independiente.
[Recibo, hashes y doce filas](2026-10-25-residual-v2-replay.json).

## Trabajo terminado
Se recuperaron código, protocolo V2, inputs.json y snapshot de resultados del commit 17306da2d6d035f4ed564efe0137e9422b82417c en un directorio aislado.
Se verificó coincidencia SHA256 de protocolo, dos scripts e inputs con el manifiesto del snapshot.
Tres pruebas test_calibrated.py aprobadas.
Comprobaciones adicionales: grupos de entrenamiento/desarrollo/prueba disjuntos y tokens no vacíos en las seis fuentes.
Se ejecutó residual_order_calibrated.py completo: doce comparaciones y 192 ajustes de entrenamiento barajado, conservando sus 2000 remuestreos por comparación.
**La salida completa coincide byte por byte con residual_order_calibrated_results.json**: SHA256 d6732aee9024d03fc34a66135c7e2531ee7640859b922b1b36cee1716cc27c32. También coincide el entorno Python 3.12.14 registrado.

## Qué resultado se sostiene
En estas entradas e implementación, añadir identidad del token anterior a bordes y longitud ofrece:
- Cuatro comparaciones de textos naturales con incremento positivo e intervalos exploratorios por encima de cero.
- Ocho vistas Voynich con incrementos de aproximadamente -0,000506 a +0,003669 bits/transición; todos sus intervalos exploratorios incluyen cero.

No son doce muestras independientes: se reutilizan corpus y las vistas IT2a split/join son idénticas.
La ganancia pequeña/incierta no identifica lengua, mecanismo, ausencia de significado o imposibilidad de descifrado.
La comparación positiva de referencias acredita sensibilidad limitada de este instrumento; no representa todas las lenguas, géneros o cifrados.
El estudio sigue exploratorio porque la partición y el desarrollo metodológico tienen exposición previa.

## Qué no se verificó
No se regeneró inputs.json desde los archivos crudos y el lector original en esta continuación. La extracción y conformidad IVTFF no quedan certificadas por este replay.
No se reprodujeron V1, suite global, identidad de todos los corpus o historial del proyecto, ni CI actual.
No se trató el remuestreo con pesos ya fijados como incertidumbre completa de entrenamiento.
Las 192 ejecuciones son controles de un análisis existente, no 192 descubrimientos ni experimentos nuevos.

## Auditor técnico de rótulos
Se volvió a recuperar el script publicado audit_label_metadata_standalone.py del mismo commit y se ejecutó sobre las fuentes de hash conocido. Su JSON coincide byte por byte con la salida ya archivada; controles integrados aprobados. No hay cambio de recuentos ni nueva conclusión semántica.
La utilidad de este recurso sigue siendo técnica; no se establece novedad académica por repetirlo.

## Reproducción del bloque V2
Desde el directorio research/analysis/2026-10-22-residual-order del checkout fijado:
```sh
python -m unittest test_calibrated.py -v
python residual_order_calibrated.py > /tmp/residual-v2.json
cmp residual_order_calibrated_results.json /tmp/residual-v2.json
```
La igualdad byte a byte observada corresponde a este entorno; otras versiones pueden diferir en metadatos Python y aritmética. Conservar diferencias y examinarlas, nunca ignorarlas automáticamente.

## Autoauditoría
Conciencia del objetivo: repetición seleccionada por su relevancia y trazabilidad, después de conocer el resultado. No confirmación prospectiva.
Destrucción de características: método original preservado, incluidas sus limitaciones al condicionar bordes/longitud. No es prueba justa de ausencia universal de gramática.
Extrapolación: solo entradas congeladas, un predictor y dos referencias naturales.
Negativos: ausencia de incremento respaldado bajo esta implementación; no ausencia de contenido.
Controles: se esperaban parámetros, pérdidas, semillas e intervalos idénticos al snapshot y controles naturales positivos; se recuperaron exactamente. No se seleccionaron semillas o variantes favorables.
Próxima acción: el replay queda cerrado; no repetirlo sin cambios o motivo nuevo. Una nueva vía de desciframiento requiere una pregunta discriminante y controles adecuados, no más remuestreos de este mismo análisis.
