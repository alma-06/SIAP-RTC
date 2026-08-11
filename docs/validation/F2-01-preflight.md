# F2-01 — Validación preliminar de archivos RTC

## Objetivo
Comprobar la compatibilidad estructural de los libros RTC antes de ejecutar el pipeline analítico.

## Comprobaciones
- existencia de hojas;
- presencia de las diez columnas requeridas;
- conteo de filas de datos;
- conteo de filas de Cámara de Senadores;
- filas completamente vacías;
- advertencia cuando una hoja no contiene registros identificables de Cámara de Senadores.

## Columnas esperadas
`Pauta de transmisión`, `Estado`, `Tiempo Fiscal`, `Canal Base`, `Orden`, `Fecha`, `Dependencia CAM. SEN.`, `Clave`, `Campaña`, `Versión`.

## Regla de seguridad
Un libro con columnas faltantes se marca como inválido para el preflight; no se debe interpretar como un resultado analítico.

## Relación con INT-02
F2-01 es una barrera previa a la ingesta. INT-02 continúa siendo responsable de producir los registros normalizados de entrada al pipeline.

## Próximo paso
Aplicar el preflight a los archivos representativos reales del periodo y registrar las excepciones encontradas antes de modificar reglas de negocio.
