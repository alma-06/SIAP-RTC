# EXP-02 — Exportador Excel ejecutivo

## Objetivo
Generar un archivo XLSX de resumen ejecutivo a partir de `ExportPayload`.

## Estructura inicial
- título y subtítulo;
- periodo;
- estado de comparabilidad;
- tabla de indicadores;
- alertas;
- identificador de evidencia.

## Regla
El exportador no accede a archivos RTC ni recalcula indicadores. Su única entrada de negocio es `ExportPayload`.

## Alcance
Esta primera versión establece la salida funcional mínima. El formato institucional, estilos avanzados, hojas de detalle, filtros y gráficos se incorporarán en etapas posteriores.
