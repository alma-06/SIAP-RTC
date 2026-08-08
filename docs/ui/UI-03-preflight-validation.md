# UI-03 — Validación previa de archivos RTC

## Objetivo
Evitar que un archivo RTC inválido llegue al motor de procesamiento o modifique el histórico.

## Validaciones

1. Existencia del archivo.
2. Extensión XLSX/XLSM.
3. Apertura correcta del libro.
4. Lectura de encabezados de la primera hoja.
5. Presencia de los campos RTC requeridos.
6. Cálculo de SHA-256 para trazabilidad.

## Resultado por archivo

Cada archivo obtiene un estado `VÁLIDO` o `INVÁLIDO`, junto con tamaño, SHA-256, encabezados detectados y causa de rechazo.

## Campos mínimos

- Pauta de transmisión
- Estado
- Tiempo Fiscal
- Canal Base
- Orden
- Fecha
- Dependencia CAM. SEN.
- Clave
- Campaña
- Versión

## Regla de seguridad

Un archivo marcado como inválido no debe enviarse al pipeline de importación ni producir cambios en la base histórica.
