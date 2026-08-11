# F3-03 — Ejecución controlada de RC1

## Objetivo
Ejecutar la versión candidata sobre un conjunto de archivos RTC en un entorno aislado, sin modificar los archivos fuente ni sobrescribir el histórico.

## Identificación
Cada ejecución recibe un `run_id` único con el formato `RC1-<periodo>-<id>`. La evidencia recibe un identificador derivado de la ejecución.

## Artefactos mínimos
- `RunMetadata.json`: versión, periodo, fuentes y estado de la ejecución.
- `EvidenceManifest.json`: fuentes y SHA-256 de los archivos de entrada, metodología y advertencias.
- resultado integrado del pipeline en memoria para posteriores exportaciones.

## Regla de aislamiento
Los resultados de la ejecución se escriben en un directorio exclusivo de la corrida. La ejecución no modifica los archivos de origen ni registra automáticamente el periodo en la base histórica.

## Regla de evidencia
El manifiesto registra la huella SHA-256 de cada archivo fuente antes de producir entregables posteriores.

## Importante
La existencia de una ejecución `completed` no significa que los resultados hayan sido aprobados. La aprobación requiere la revisión F3-04 y, posteriormente, la conciliación F3-07.

## Datos reales
Cuando se reciban archivos RTC reales, F3-03 deberá ejecutarse después de F3-01 y F3-02 sobre esos archivos. Los datos de prueba usados en tests no se consideran evidencia institucional.
