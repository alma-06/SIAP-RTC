# UI-05 — Resultado y auditoría de importación

## Objetivo
Presentar un resultado consolidado por lote y conservar la trazabilidad de la ejecución.

## Identificador de lote
Cada ejecución obtiene un identificador único con formato `RTC-XXXXXXXXXXXX`.

## Métricas del lote
- archivos procesados;
- registros leídos;
- registros CAM. SEN.;
- duplicados;
- rechazados;
- registros nuevos;
- spots contabilizados;
- estado final.

## Resultado por archivo
Cada archivo conserva nombre, SHA-256, estado, conteos y error, si existe.

## Estados del lote
- `INICIADO`
- `PROCESADO`
- `ERROR`

## Regla de auditoría
El resultado debe permitir reconstruir qué archivos participaron en una ejecución y qué resultado produjo cada uno. El identificador de lote será la referencia primaria para reportes y consultas posteriores.

## Integridad
Un lote con error no debe presentarse como procesado correctamente. Las cifras agregadas se calculan a partir de los resultados individuales para evitar discrepancias de interfaz.
