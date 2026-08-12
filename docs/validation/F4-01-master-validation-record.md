# F4-01 — Expediente maestro de validación

## Objetivo
Concentrar la trazabilidad de un periodo de procesamiento en un registro maestro, sin sustituir los archivos de evidencia originales.

## Contenido mínimo
- periodo;
- versión;
- identificador de corrida;
- archivos fuente y SHA-256;
- perfil estructural;
- resultado de preflight;
- reglas aplicadas;
- conciliación;
- Criterio 78;
- indicadores;
- hallazgos;
- ajustes;
- reejecuciones;
- entregables;
- manifiesto de evidencia;
- dictamen técnico;
- notas y limitaciones.

## Regla de trazabilidad
Cada elemento debe apuntar al artefacto o evidencia que lo respalda. El registro maestro funciona como índice de reconstrucción, no como sustituto de la evidencia.

## Regla de integridad
Los archivos fuente y evidencias no se modifican para actualizar el expediente. Si existe una nueva corrida, se agrega una nueva referencia y se conserva la anterior.

## Estado inicial
El campo de dictamen se inicializa como `NO_VALIDADO` y solo cambia conforme al procedimiento F3-08.
