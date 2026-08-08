# QA-04 — Integridad transaccional

## Objetivo
Demostrar que una falla durante el procesamiento no deja registros parciales ni un lote marcado como procesado.

## Casos automatizados
- excepción provocada después de insertar un registro;
- error SQL durante la misma transacción;
- comprobación de ausencia del lote tras rollback;
- comprobación de ausencia de registros históricos parciales;
- comprobación de ausencia de auditoría parcial.

## Invariante
Una unidad de importación debe ser atómica: ante una excepción, sus cambios persistentes se revierten.

## Observación de diseño
El estado `ERROR` no se persiste en la misma transacción que se revierte. La capa de orquestación puede conservar el resultado de ejecución en memoria/log y, en una futura bitácora independiente, registrar el fallo fuera de la transacción de datos.

## Criterio de avance
El núcleo transaccional se considera consistente respecto de rollback cuando las pruebas confirman que ningún registro ni lote parcialmente creado sobrevive a una excepción.
