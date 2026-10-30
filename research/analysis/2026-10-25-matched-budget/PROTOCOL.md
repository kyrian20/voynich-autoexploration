# Sensibilidad del predictor V2 a presupuestos iguales

25-10-2026. Diagnóstico exploratorio del modelo existente; sin EXP nuevo ni prueba confirmatoria. Fijado antes de ejecutar este diagnóstico, tras observar resultados V2 históricos. No se afirma novedad externa.

Pregunta: ¿persiste descriptivamente la diferencia de ganancia de identidad cuando las seis vistas reciben exactamente el mismo número de transiciones por partición? Alternativas limitadas: diferencia sensible al tamaño disponible frente a diferencia que persiste en estas submuestras. Ninguna distingue lengua/cifrado/generador por sí sola.

Entradas: research/analysis/2026-10-22-residual-order/inputs.json, SHA256 c069548868854c29d294efbc3da891a0f5cf7c62878786be78fa13ce5ba5225d. Reutilizar residual_order.py y residual_order_calibrated.py de ese directorio. Antecedentes cotejados: REPORT.md V2, diagnóstico de soporte de identidad del 23-10 y backlog actual. Este contraste iguala presupuestos; no repite memoria de dos tokens ni ch/sh EXP-622/623. La revisión Gemini v2 archivada se usa críticamente; no se solicita otra respuesta ni se adopta su nulo de plantillas.

Mantener bucket SHA256 por grupo: train>=2, dev=1, test=0. Presupuestos mínimos de las seis fuentes: train=10653, dev=3761, test=3590 transiciones. Dentro de cada partición ordenar registros de longitud>=2 por SHA256 de semilla/índice original; tomar registros hasta el presupuesto y truncar solo el último a transiciones restantes+1 tokens. No concatenar líneas. Las unidades físicas no cruzan particiones, aunque esta selección dentro de partición no es un muestreo por conglomerados completo.

Semillas fijadas 2026102501..2026102505, publicar todas. Cap=2000+UNK, tau=20, alpha=.1, rejilla y calibración V2 sin cambios, vocabulario solo train. Treinta ajustes. Publicar EL-W, pesos, UNK, grupos, hashes de registros seleccionados y número de registros truncados. Comprobar cantidades exactas y ausencia de solapamiento de grupos.

No calcular p, equivalencia ni intervalos de confianza a partir de cinco submuestras solapadas. Rangos son sensibilidad, no incertidumbre poblacional. Si controles naturales pierden su ganancia, declarar que la comparación previa depende de estas condiciones y bloquear una lectura lingüística negativa. Si conservan ganancia, solo se debilita la explicación simple por cantidad de transiciones: género, vocabulario, representación, dependencia y elección histórica siguen confundidos. No optimizar semillas ni umbrales tras observar resultados.

Limitación intencional: se pierde material y se trunca una línea; puede degradar dependencias. No se prueba igualdad de diversidad ni equivalencia estadística. Los controles son textos, no demostraciones de recuperación de contenido. IT2a split/join idénticos no son réplicas independientes. La extracción desde fuentes originales no se regenera aquí.
