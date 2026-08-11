# F2-04 — Base histórica acumulativa

## Objetivo
Conservar los paquetes procesados por periodo sin sobrescribir resultados históricos.

## Identificador de periodo
Cada periodo se registra una sola vez en `HistoricalIndex.json`, junto con Evidence ID, ruta del paquete y SHA-256.

## Regla de no sobrescritura
Intentar registrar nuevamente un periodo existente produce un error. Una corrección de datos debe generar una nueva versión o un nuevo paquete identificable; no se reemplaza silenciosamente el histórico.

## Integridad
`verify()` comprueba la existencia del paquete y su SHA-256 frente al índice histórico.

## Beneficio
Permite construir comparativos y series históricas sin perder la evidencia documental correspondiente a cada corte.

## Próxima etapa
Incorporar consultas históricas y comparativos interperiodo sobre los resultados validados, sin alterar los paquetes originales.
