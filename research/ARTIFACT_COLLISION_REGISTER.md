# Registro de colisiones y alias de artefactos

Fecha de auditoría: 20-10-2026  
Estado: inventario parcial; no equivale a una auditoría completa de los más de 2.000 paths de GitHub ni de todos los ficheros de la Biblioteca.

## Reglas

- Los nombres históricos se conservan por trazabilidad.
- No fusionar artefactos por compartir EXP ID o similitud de nombre.
- Los alias técnicos se añaden en este registro; el renombrado físico solo se hará después de localizar referencias y comparar hashes.
- Un resultado se marca inválido solo para las afirmaciones afectadas por su defecto; no se borra.

## Conflictos confirmados

| Nombre histórico | Ubicación | Contenido/alcance | Acción segura |
|---|---|---|---|
| EXP-623 | GitHub: informe de interacción ch/sh | Sensibilidad de una interacción contextual entre transcripciones ZL3b/IT2a; interacción no significativa, cambia de signo | Conservar como GH-EXP-623; no usar para afirmaciones de orden de palabras |
| EXP-623 control de orden, variante A | Biblioteca: Informe_Voynich_exp623_Control_orden_palabras_2026-10-19.md | Bigramas en folios reservados, control que baraja todas las palabras dentro del locus; el orden real no supera al control en la métrica reportada | Alias de inventario LIB-ORDER-2026-10-19-A; no renumerar hasta comparar el script y el JSON |
| EXP-623 control de orden, variante B | Biblioteca: Informe_Voynich_exp623_control_orden_2026-10-19.md | Modelo de bigramas en folios reservados; control que permuta palabras interiores y mantiene extremos; informa ventaja predictiva frente a ese nulo, con limitaciones exploratorias | Alias de inventario LIB-ORDER-2026-10-19-B; no fusionar con A ni con GitHub |
| EXP-590 | GitHub: scripts/exp590_daiin_position.py y resultados JSON/MD del 20-10-2026 | El script original usaba $Q para clase Currier; el script se corrigió para usar $L. Resultados antiguos por clase siguen pendientes de regeneración/verificación | Alias GH-EXP-590-OLD-Q; conservar el output histórico y marcar las tablas por clase como INVALID_FOR_CLAIM hasta repetición |
| EXP-593 | GitHub: scripts/exp593_daiin_variants.py y JSON/MD | Se corrigió extracción de clase a $L; el registro advierte que hay conflictos históricos de numeración y que debe verificarse la ejecución CI | Mantener ID con advertencia; no reasignar hasta revisar el índice histórico completo |

## Parser y corpus

- La auditoría histórica de protocolo v1 registra 1.466 desacuerdos de listas de tokens para ZL3b y 1.472 para ZL3a. Tras corregir el terminador de comentarios IVTFF en protocolo v2, el recuento actualizado es 792 para ZL3b y 805 para ZL3a. El protocolo v1 se conserva en `experiments/exp_602_independent_ivtff_parser_audit/archive/results_pre_terminator_fix_2026-10-20.json`; la salida v2 está en `experiments/exp_602_independent_ivtff_parser_audit/results_v2.json`. La discrepancia sigue abierta.
- Los conteos anteriores deben conservarse como evidencia histórica de discrepancia, no como una medida de que un parser concreto sea correcto.
- ZL3a, ZL3b e IT2a son transcripciones alternativas del mismo manuscrito y no deben contarse como réplicas independientes.

## Inventario estructural actualizado

La auditoría de árbol del 20-10-2026 cuenta 2.085 rutas, 624 carpetas `experiments/exp_NNN_*`, 617 IDs únicos, siete grupos de colisión de IDs de carpeta y 31 workflows. El informe [repository inventory audit](repository_inventory_audit_2026-10-20.md) detalla los grupos y evita etiquetar automáticamente como defectuosas las carpetas históricas sin script o salida convencional.

## Próxima auditoría de colisiones

1. Enumerar todos los archivos cuyo nombre contenga EXP, exp, fase, vNNN o checksum en GitHub y Biblioteca.
2. Extraer el ID del contenido, no solo del nombre.
3. Calcular SHA-256 de cada script, JSON, informe y fuente.
4. Agrupar coincidencias exactas y detectar pares con mismo ID pero distinta pregunta, script o resultado.
5. Resolver cada grupo con un alias estable, una relación de sustitución y referencias cruzadas.
6. No borrar ni sobrescribir artefactos históricos durante el proceso.
