# Protocolo de cobertura de etiquetas — 25-10-2026

Estado previo: PROPOSED para un diagnóstico descriptivo de metadatos, sin EXP nuevo. Dos comprobaciones preliminares ya vistas: las Lp seleccionadas están en train y 1.024 IDs compartidos mantienen tipo de locus. No se presenta la revisión como confirmatoria ni ciega.

Pregunta: ¿qué registros L/R y hojas físicas aporta cada transcripción a cada partición existente, y qué diferencias de cobertura impiden intercambiar las ediciones sin registro?

Entradas congeladas: inventario de PR #47 y manifest-v2.json de partición prospectiva. Verificar identidad de fuentes frente al manifiesto, particiones disjuntas, unicidad de IDs de ocurrencia y ausencia de duplicados de locus dentro de cada edición. No cambiar particiones para obtener una muestra más favorable.

Medidas: registros y hojas distintas por edición/tipo/partición; unión/intersección de identificadores; registros presentes solo en una edición y clasificación del registro correspondiente en las exclusiones de la otra; proporción de filas por hoja, descriptiva, sin interpretación semántica. Los folios fRos quedan UNASSIGNED, sin asignarles hoja numérica artificial. Recto, verso y paneles de una hoja comparten partición.

No comparar palabras EVA, buscar nombres, entrenar modelos, evaluar resultados semánticos, calcular p-valores, modificar pesos o usar las hojas test para elegir una hipótesis. Las categorías visuales y referentes permanecen desconocidos.

Criterio de decisión: si un subtipo tiene cero hojas en desarrollo/prueba, esa selección no permite evaluar predicción fuera de entrenamiento con esta partición. Tener filas en test no demuestra referentes fiables, independencia, potencia ni elegibilidad semántica. Los mínimos de PR #13 no se adoptan aquí como garantía de potencia.

Antecedentes: Q002 en state/open_questions.md advierte que L0 mezcla funciones; este diagnóstico no resuelve su clasificación visual ni reproduce el porcentaje histórico de EXP-010. Las etiquetas L/R no se convierten en nombres de plantas automáticamente.
