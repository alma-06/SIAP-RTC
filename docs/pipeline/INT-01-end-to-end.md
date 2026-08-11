# INT-01 — Orquestador SIAP-RTC de extremo a extremo

## Objetivo
Encadenar los componentes validados del proyecto para convertir un resultado de periodo en un paquete ejecutivo verificable.

## Flujo
`resultado validado → ficha ejecutiva → ExportPayload → XLSX/DOCX/PPTX → manifest → verificación`

## Principio
El orquestador coordina componentes existentes; no duplica reglas de negocio ni implementa cálculos alternativos.

## Punto de integración
El parámetro opcional `prepare` permite conectar posteriormente el lector/consolidador/conciliador real sin modificar la capa de exportación.

## Históricos
`run_history` genera un paquete independiente por periodo, conservando la separación de evidencias y resultados.

## Próxima integración
Conectar este orquestador al pipeline real de archivos RTC: selección, lectura de Excel, normalización, filtrado CAM. SEN., deduplicación, conciliación, validación y construcción de `DashboardPeriod`.
