# UI-04 — Integración de validación en Importador RTC

## Objetivo
Integrar la prevalidación de UI-03 en el flujo de importación para impedir que archivos inválidos lleguen al procesamiento.

## Estados por archivo

- `PENDIENTE`
- `VALIDANDO`
- `VÁLIDO`
- `INVÁLIDO`
- `PROCESANDO`
- `PROCESADO`
- `ERROR`

## Regla de procesamiento

El comando **Procesar archivos válidos** solo puede habilitarse cuando todos los archivos seleccionados estén en estado `VÁLIDO`. Los archivos inválidos no deben ser enviados al pipeline.

## Información visible

Para cada archivo se debe mostrar:

- nombre;
- tamaño;
- estado;
- SHA-256 abreviado;
- campos faltantes, si aplica;
- mensaje de error, si aplica.

## Resultado global

La pantalla debe mostrar al menos:

- archivos seleccionados;
- válidos;
- inválidos;
- pendientes;
- acción disponible.

## Seguridad de datos

La validación es previa a la persistencia. Un archivo inválido no puede crear ni modificar lotes históricos.
