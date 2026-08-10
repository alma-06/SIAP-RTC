# HIST-01 — Consulta del histórico

## Objetivo
Exponer el histórico acumulativo mediante una capa de solo lectura, reutilizable por la interfaz, indicadores y exportaciones.

## Componentes
- `app/domain/query_filters.py`: contrato de filtros y paginación.
- `app/infrastructure/historical_repository.py`: consultas SQLite parametrizadas.
- `app/application/historical_query_service.py`: servicio de aplicación y resultado paginado.

## Filtros
Fecha inicial/final, estado, campaña, versión, clave, canal base, lote y archivo de origen.

## Seguridad de consulta
La columna de ordenamiento se valida contra una lista blanca. Los valores de filtros se envían como parámetros SQLite; no se construye SQL con valores suministrados por el usuario.

## Solo lectura
El repositorio de consulta habilita `PRAGMA query_only = ON` en sus conexiones de búsqueda y no expone operaciones de escritura.

## Paginación
`limit` se restringe a 1–5000 y `offset` no puede ser negativo. El servicio devuelve tanto los registros de la página como el total de coincidencias.

## Siguiente paso
Construir HIST-02: agregaciones e indicadores sobre consultas reproducibles del histórico.
