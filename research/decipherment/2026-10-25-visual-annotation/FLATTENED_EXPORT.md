# Exportación aplanada de candidatos — 25-10-2026

Preparación operativa, sin nuevo experimento ni anotaciones. Base revisada:
`980c2e39886d42019d9b1352242f1323f2026ed3`. Su CI de push terminó en
success: https://github.com/kyrian20/voynich-autoexploration/actions/runs/40214892568.
Esa ejecución no valida el código añadido después.

`scripts/export_mask_candidate.py` añade una salida PNG sin capas: los píxeles
de los rectángulos se sustituyen por negro antes de recortar. Una imagen RGB
nueva evita copiar EXIF, comentarios, perfiles y campos de texto de la fuente.
Se verifica SHA256, dimensiones decodificadas, orientación y geometría; una
salida existente se rechaza. El script no modifica la cola ni aprueba máscaras.

Dependencia: Pillow 12.3.0, fijada también en Voynich Check. Ejecución prevista:

```sh
python scripts/export_mask_candidate.py \
  --plan research/decipherment/2026-10-25-visual-annotation/region-proposals.json \
  --folio f65r --source /tmp/voynich-yale-images/f65r.jpg \
  --out /tmp/coordinator-candidate.png
```

Este comando se documenta, pero no se ha ejecutado sobre el manuscrito en esta
continuación. Las pruebas usan una imagen sintética con comentario incrustado:
comprueban todos los píxeles del recorte, bordes exclusivos de máscara,
conservación de píxeles externos, ausencia de metadatos, determinismo y rechazo
de hash, dimensiones, geometría y planes incompletos.

El PNG es un candidato para el coordinador. Aplanarlo no demuestra que todos
los glifos estén cubiertos ni que se conserven los detalles de la ilustración.
La revisión visual a resolución original, la revisión independiente, el
empaquetado con ID opaco y las anotaciones siguen pendientes. No entregar
fuente, SVG, plan con folio ni mapa al anotador. Ninguna tarea pasa a READY.

Comprobaciones locales con Python 3.12.14 y Pillow 12.3.0: suite completa,
auditoría operativa, identidad de corpus y `git diff --check`. El resultado
exacto de la suite y la CI de la propuesta se registran en la PR.
