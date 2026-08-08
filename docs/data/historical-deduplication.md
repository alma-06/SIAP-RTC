# Histórico y deduplicación persistente

## Objetivo
Mantener un histórico acumulativo de registros RTC sin duplicar registros cuya identidad canónica ya exista.

## Tabla funcional
`historical_records` conserva el registro consolidado y su procedencia.

## Unicidad
`identity_hash` tiene restricción `UNIQUE`. La base de datos constituye la segunda barrera de protección contra duplicaciones, además de la lógica de aplicación.

## Procedencia
Cada registro conserva:
- `source_batch_id`;
- `source_filename`;
- `created_at`.

Esto permite reconstruir el origen de cada registro aceptado.

## Inserción
El método `insert_if_new()` calcula la identidad canónica y utiliza `INSERT OR IGNORE`. El resultado booleano distingue entre registro nuevo y registro ya existente.

## Integridad
La clave foránea `source_batch_id` vincula el histórico con el lote de importación. La aplicación no debe insertar registros históricos asociados a lotes inexistentes.

## Alcance de la primera implementación
La tabla contiene los campos operativos definidos para la identidad RTC. La ampliación a columnas adicionales deberá preservar la regla de identidad y documentarse mediante migración de esquema.

## Próxima evolución
La auditoría deberá registrar explícitamente los intentos de inserción que resulten duplicados, incluyendo identidad, lote y archivo de origen, para conservar evidencia aun cuando el registro no sea insertado nuevamente.
