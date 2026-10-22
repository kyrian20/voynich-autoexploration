# BC-2026-10-22

Comparación nueva de lenguaje conocido, cifrado Naibbe y generación propia, con originales EXP-170 intactos.

- [Protocolo previo](PROTOCOL.md), [informe y autoauditoría](result.md), [verificación](VERIFICACION.md).
- `freeze.json`: hashes previos de fuentes/código externo/parser y protocolo.
- `implementation-freeze.json`: código de ejecución fijado antes de simular.
- `data/run-01` y `run-02`: intentos fallidos antes de simulaciones, conservados.
- `data/run-03`: resultados y SHA256 publicados; selección cruda, vistas y secuencias ausentes por bloqueo (véase PUBLICACION.md).

Desde la raíz del repositorio, con Python 3.12:

```sh
python -m pip install -r experiments/common_battery_2026_10_22/requirements.txt
python experiments/common_battery_2026_10_22/script.py --out work/bateria-nueva
python tests/test_common_battery.py
```

El script rechaza sobrescribir directorios no vacíos y cambios de fuentes congeladas. El archivo gzip contiene JSONL, un registro por brazo/semilla con `train` y `test`: permite métricas nuevas sin fingir que existían tokens históricos. La prueba automatizada reconstruye las métricas archivadas; no valida una conclusión científica.

Naibbe original, tablas y licencia del commit 719f2f4c4d1eacf95fabf48381cd84fc6cd94279 de greshko/naibbe-cipher. Cita: Greshko (2025), Cryptologia, DOI 10.1080/01611194.2025.2566408. Generadores de copia propios inspirados en controles previos, sin afirmar réplica del programa Timm/Schinner.

**Publicación parcial:** consultar PUBLICACION.md. La entrega anterior declaró tokens y vistas conservados localmente; no se han localizado en el entorno de continuación. Siguen pendientes de recuperación y de autorización específica exigida por revisión automática. No se han repetido experimentos. La PR contiene sus hashes, código y métricas; CI omite explícitamente el replay del archivo ausente.
