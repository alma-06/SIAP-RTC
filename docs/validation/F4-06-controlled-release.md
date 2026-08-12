# F4-06 — Liberación controlada

## Objetivo
Establecer las condiciones mínimas para declarar una versión liberada dentro de un alcance determinado.

## Identidad de la liberación
La liberación debe quedar asociada a:
- versión;
- commit;
- identificador de corrida;
- expediente maestro;
- manifiesto verificado;
- dictamen técnico;
- revisión institucional;
- alcance autorizado.

## Condiciones
No se libera una versión si falta cualquiera de los elementos anteriores o si el manifiesto no supera la verificación de integridad.

## Regla de inmutabilidad lógica
Una versión liberada no se corrige retroactivamente. Cualquier modificación posterior debe producir una nueva versión, nueva corrida y nueva trazabilidad.

## Alcance
La liberación es válida únicamente para el alcance declarado. La validación de un periodo o conjunto de archivos no implica automáticamente la validación de otros periodos, fuentes o escenarios.

## Estado actual del proyecto
El mecanismo de liberación está implementado, pero no debe utilizarse para declarar una versión real como liberada hasta que existan archivos RTC reales, evidencia suficiente, dictamen técnico y revisión institucional conforme al procedimiento.
