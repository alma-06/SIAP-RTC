# INT-02 — Ingesta RTC y filtrado CAM. SEN.

## Objetivo
Incorporar al pipeline la lectura de múltiples archivos Excel RTC y conservar únicamente los registros correspondientes a la Cámara de Senadores.

## Columnas esperadas
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

## Comportamiento
- Lee todos los archivos proporcionados.
- Recorre todas sus hojas.
- Normaliza encabezados para tolerar diferencias de espacios y mayúsculas/minúsculas.
- Registra advertencias cuando una hoja no contiene las columnas requeridas.
- Filtra registros de CAM. SEN.
- Conserva el archivo fuente en cada registro para trazabilidad.

## Alcance
Esta etapa implementa ingesta y filtrado; todavía no realiza deduplicación, conciliación ni cálculo de indicadores.
