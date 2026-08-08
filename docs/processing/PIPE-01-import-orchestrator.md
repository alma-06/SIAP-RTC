# PIPE-01 — Orquestador del pipeline de importación RTC

## Objetivo
Coordinar las etapas del procesamiento sin concentrar en la interfaz la lógica de negocio ni de persistencia.

## Flujo

1. Recepción de archivos.
2. Prevalidación.
3. Creación/identificación del lote.
4. Inicio de transacción.
5. Lectura y homologación mediante el motor especializado.
6. Filtrado de `CAM. SEN.`.
7. Cálculo de identidad canónica.
8. Inserción en histórico o registro de duplicidad.
9. Consolidación de métricas.
10. `COMMIT` o `ROLLBACK`.
11. Construcción del resultado del lote.

## Responsabilidades

El orquestador coordina. No debe convertirse en el lector Excel ni contener reglas específicas de homologación de columnas.

## Estado actual
La implementación inicial deja un punto de integración explícito para el lector/homologador. La extracción real de filas se incorporará en el siguiente incremento del motor de procesamiento.

## Regla de integridad
Un archivo que falle la prevalidación no inicia el pipeline de persistencia.

## Evolución prevista
El pipeline deberá aceptar un adaptador de procesamiento que entregue registros normalizados, permitiendo probar lectura, homologación, filtrado y persistencia por separado.
