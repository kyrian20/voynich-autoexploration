# Ejecución real del candidato f65r y rechazo del recorte
25-10-2026. Preparación operativa con resultado desfavorable; no EXP ni contraste semántico.

## Qué se ejecutó
Código de PR #59 fijado a 73e9729b5ecd2649a3239b83a5c031f3dcf91a54, en directorio aislado. No se fusionó PR #59; export_mask_candidate.py no estaba disponible en master al consultarlo.
Se recuperaron export_mask_candidate.py, render_coordinator_mask_preview.py, test_mask_candidate.py y region-proposals.json de ese mismo SHA.
Python 3.12.14 / Pillow 12.3.0. Cuatro pruebas de test_mask_candidate.py aprobadas.
Se ejecutó export_mask_candidate.py con fuente Yale f65r.jpg verificada, folio f65r y plan existente.
[Recibo exacto](f65r-mask-execution-receipt.json). No se publican imágenes binarias ni un paquete de anotador.

## Resultado técnico
PNG RGB 2450×3590, SHA256 a91482b46bc86c73b9481a6a7d6f01b151369bbac72f25bb5ab7403ad13fe886.
Comparación independiente por matrices: todos los píxeles coinciden exactamente con el recorte de fuente y los dos rectángulos negros esperados; 99.150 píxeles enmascarados. Metadatos reportados por Pillow vacíos.
Eso comprueba la transformación definida, no que el plan o el dibujo sean adecuados.

## Resultado visual y decisión
Se abrió el PNG con detalle original. El recorte [120,30,2450,3590] corta parte del dibujo de una hoja en su borde izquierdo; conserva además menos contexto que la fuente completa.
**REJECTED_CURRENT_CROP_CLIPS_DRAWING. No apto para anotación con el plan actual.**
La revisión previa ya advertía posible pérdida por recorte; esta ejecución la hace visible en el PNG real.
No se certifica ausencia de todo glifo residual ni preservación anatómica. La revisión fue del coordinador expuesto, no de un anotador independiente.

## Consecuencia
Mantener annotation_ready=false y no usar este hash en anotaciones.
No aprobar el plan por superar tests. Corregir primero el recorte para preservar el objeto y revisar también texto de páginas vecinas y las marcas superiores; ampliar sin más el recorte podría reincorporar información que debe ocultarse.
Conservar plan y hash rechazados para no repetir la misma propuesta como nueva.
No modificar transcripciones, datos científicos o committed_claims.md. La cola sigue bloqueada.

## Reproducción
Desde checkout del SHA de PR #59:
`python -m unittest discover -s tests -p test_mask_candidate.py -v`
`python scripts/export_mask_candidate.py --plan research/decipherment/2026-10-25-visual-annotation/region-proposals.json --folio f65r --source /ruta/f65r.jpg --out /ruta/nueva/f65r.png`
La salida debe ser nueva: el script rechaza sobrescritura. No se ejecutó suite global ni se verificó CI actual.

## Autoauditoría
Conciencia del objetivo: se eligió f65r por tener plan ejecutable existente; no muestra aleatoria ni nueva evidencia de taxón.
Destrucción de rasgos: se detectó corte de dibujo y por ello se rechazó el candidato. No interpretar una anotación posterior sobre él.
Extrapolación: comprobación de un plan y una fuente; no valida máscaras de otros folios.
Negativos: fallo del plan, no ausencia de significado.
Controles: se esperaba igualdad exacta de todos los píxeles con transformación definida y metadatos vacíos; ambos se observaron. El hallazgo visual adverso prevalece sobre la corrección mecánica.
