# QA-02 — Pruebas del lector y pipeline integrado

## Objetivo
Validar el tramo XLSX → normalización → filtro CAM. SEN. → persistencia.

## Casos incorporados
- libro con más de una hoja;
- encabezados con acentos y variaciones de formato;
- fila completamente vacía;
- conservación de hoja y fila de origen;
- registro CAM. SEN.;
- registro de otra dependencia;
- persistencia exclusiva del registro aceptado;
- cierre correcto del lote.

## Fixtures
Los libros de prueba se generan en tiempo de ejecución con `openpyxl`, evitando almacenar binarios de prueba en el repositorio mediante la API de contenidos.

## Alcance pendiente
La batería debe ampliarse con duplicación entre archivos, duplicación entre lotes, fechas Excel seriales, encabezados ausentes, columnas desconocidas, archivos corruptos y rollback provocado.

## Criterio de aceptación
La prueba de integración debe demostrar que una fila no perteneciente a CAM. SEN. no llega a `historical_records` y que el lote procesado conserva su estado final.
