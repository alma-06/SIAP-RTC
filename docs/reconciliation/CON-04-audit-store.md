# CON-04 — Persistencia de auditoría

## Objetivo
Persistir los cambios detectados por CON-03 en SQLite para que la bitácora sobreviva al proceso de importación.

## Tabla
`change_audit` conserva un evento por campo modificado.

Campos principales:
- identidad;
- archivo nuevo;
- archivo anterior;
- fecha de detección;
- campo;
- valor anterior;
- valor actual;
- tipo de cambio;
- lote de importación.

## Regla de escritura
La capa expuesta por este módulo únicamente agrega eventos. No contiene una operación de actualización o eliminación de eventos históricos.

## Índices
Se crean índices para consultar por identidad y por lote de importación.

## Alcance
Esta entrega cubre la persistencia de la auditoría de cambios. La persistencia de registros históricos, lotes de importación y deduplicación se integrará posteriormente con el repositorio de datos principal.
