# PIPE-04 — Integración del pipeline RTC

## Objetivo
Conectar el lector Excel, el filtro CAM. SEN., la identidad y la persistencia transaccional dentro del orquestador.

## Flujo implementado

1. Prevalidación de archivos.
2. Lectura y normalización mediante `RTCExcelReader`.
3. Filtrado de registros mediante `CamSenFilter`.
4. Cálculo de identidad dentro de la capa transaccional.
5. Inserción de registros nuevos en `historical_records`.
6. Registro de duplicados en `duplicate_audit`.
7. Cálculo de métricas por archivo.
8. `COMMIT` o `ROLLBACK` del lote.
9. Construcción de `ImportBatchResult`.

## Responsabilidades
El orquestador coordina el flujo; el lector interpreta Excel, el filtro aplica la regla CAM. SEN. y la infraestructura administra la persistencia.

## Estado
PIPE-04 constituye la primera integración funcional del pipeline. El siguiente paso es validar el comportamiento con fixtures Excel controlados y pruebas automatizadas antes de considerar estable el procesamiento.

## Riesgo conocido
La creación del lote y la inserción de sus datos de auditoría requieren que el `batch_id` exista en `import_batches` antes de insertar registros históricos. La capa de aplicación deberá completar esta inicialización al integrar el flujo de ejecución definitivo.
