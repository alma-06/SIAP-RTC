# UI-06 — Persistencia de auditoría de importación

## Objetivo
Conservar en SQLite la trazabilidad de cada lote y de cada archivo participante.

## Entidades de auditoría

### `import_batches`
- `batch_id`: identificador único del lote.
- `started_at`: fecha y hora de inicio.
- `status`: INICIADO, PROCESADO o ERROR.

### `import_files`
- archivo y SHA-256;
- estado;
- registros leídos;
- registros CAM. SEN.;
- duplicados;
- rechazados;
- registros nuevos;
- mensaje de error.

## Integridad
Los archivos pertenecen a un lote mediante clave foránea. La eliminación de un lote elimina sus detalles de auditoría asociados (`ON DELETE CASCADE`).

## Índices
Se crean índices por lote y SHA-256 para consultas de auditoría y detección de archivos previamente procesados.

## Regla de operación
La persistencia de auditoría no sustituye la persistencia de los datos de negocio. El lote documenta qué ocurrió durante una ejecución; los registros consolidados se mantienen en las tablas funcionales correspondientes.
