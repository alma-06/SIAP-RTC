# QA-03 — Integridad de duplicados

## Objetivo
Demostrar que la identidad canónica protege el histórico frente a múltiples intentos de importación del mismo registro.

## Casos automatizados
- duplicado repetido dentro del mismo archivo y lote;
- mismo registro presentado en lotes diferentes;
- conservación de un único registro en `historical_records`;
- generación de evidencia en `duplicate_audit`.

## Invariante de aceptación
Para una misma identidad canónica, `historical_records` debe contener una sola fila, independientemente del número de importaciones posteriores.

## Auditoría
Cada lote/archivo puede conservar su propia evidencia de detección de duplicidad, sin multiplicar el histórico.

## Pendiente
Agregar pruebas de rollback provocado y de importaciones concurrentes antes de declarar cerrado el bloque QA-03.
