# INT-04 — Deduplicación conservadora RTC

## Objetivo
Eliminar únicamente duplicados exactos después de la normalización, sin confundir repeticiones legítimas de impactos con duplicados.

## Huella
La huella SHA-256 se construye con los campos normalizados definidos por `REQUIRED_COLUMNS`.

## Regla
- Primera aparición de una huella: `keep`.
- Aparición posterior de la misma huella: `drop` como duplicado exacto.
- Registros con cualquier diferencia en esos campos: no se eliminan automáticamente.

## Auditoría
Cada decisión conserva archivo fuente, huella, acción y motivo.

## Salvaguarda metodológica
Esta etapa no deduplica por campaña, versión, orden, fecha o estación de manera aislada. Hacerlo podría eliminar impactos legítimos.

## Próxima etapa
Consolidación del universo deduplicado y conciliación de resultados.
