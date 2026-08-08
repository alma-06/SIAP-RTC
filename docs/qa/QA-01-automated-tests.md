# QA-01 — Pruebas automatizadas iniciales

## Objetivo
Establecer una primera barrera automatizada sobre las reglas críticas del núcleo SIAP-RTC antes de ampliar el sistema.

## Cobertura incorporada
- identidad canónica independiente de mayúsculas y espacios exteriores;
- normalización y aceptación de `CAM. SEN.`;
- rechazo de una dependencia distinta;
- creación y cierre de lote transaccional;
- inserción de un registro nuevo;
- detección y auditoría de duplicados.

## Alcance pendiente
Se requieren pruebas adicionales con libros XLSX reales o fixtures generados durante la fase de integración, incluyendo múltiples hojas, encabezados variables, fechas, filas vacías, errores de lectura y rollback provocado.

## Criterio de avance
No considerar el pipeline listo para producción únicamente por tener estas pruebas. La cobertura debe ampliarse y ejecutarse en CI antes del hito de aceptación técnica.
