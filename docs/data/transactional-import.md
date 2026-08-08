# DATA-04 — Integración transaccional de importación

## Objetivo
Garantizar que la incorporación al histórico y la evidencia de duplicados formen una única unidad transaccional de SQLite.

## Comportamiento
1. Abrir conexión con claves foráneas habilitadas.
2. Iniciar transacción explícita.
3. Intentar insertar el registro histórico mediante `identity_hash`.
4. Si ya existe, registrar la evidencia en `duplicate_audit`.
5. Confirmar (`COMMIT`) únicamente si todas las operaciones del lote transaccional concluyen correctamente.
6. Ante una excepción, ejecutar `ROLLBACK`.

## Invariante
No debe existir un resultado persistido donde el registro histórico haya sido aceptado pero su operación de auditoría correspondiente haya quedado parcialmente aplicada por una misma unidad transaccional.

## Alcance
`ImportTransaction` proporciona la unidad transaccional. La orquestación superior seguirá siendo responsable de crear el lote, validar archivos y decidir el momento de cierre del lote.

## Recomendación para integración
El procesamiento de un lote completo debe ejecutarse en una única transacción cuando el volumen lo permita. Para archivos muy grandes, podrán utilizarse transacciones por bloque, siempre que el diseño de auditoría documente explícitamente el punto de consistencia.
