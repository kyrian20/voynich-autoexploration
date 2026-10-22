# Lista de aceptación antes de integrar PR #6

Estado: pendiente de ejecución y comprobación, no aprobado automáticamente.

1. Confirmar que el flujo de pruebas aparece en GitHub Actions y registrar URL, SHA, fecha y conclusión.
2. Ejecutar tests de contrato y parser en Python 3.12; no fusionar si falla cualquiera.
3. Revisar manualmente los fixtures del parser: son pruebas de humo, NO validación IVTFF exhaustiva.
4. Verificar que el PR modifica solo documentación, pruebas y workflow de comprobación; no datos ni resultados históricos.
5. Comprobar que no hay ejecuciones de investigación en curso que escriban simultáneamente a master.
6. No activar reintentos de workflows fallidos sin diagnosticar el error exacto.
7. Si el workflow no arranca por restricciones de permisos o GitHub, registrar bloqueo y no afirmar que CI ha pasado.
8. Mantener la rama y PR abiertos hasta revisión satisfactoria.
9. Conservar hashes de entradas y artefactos para experimentos futuros.
10. No declarar traducción sin clave explícita y validación fuera de muestra.

Esta lista es una puerta de control, no un certificado de que se hayan superado las pruebas.
