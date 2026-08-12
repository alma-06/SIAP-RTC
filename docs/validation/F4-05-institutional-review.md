# F4-05 — Revisión institucional

## Objetivo
Establecer el punto de control previo a la liberación de un expediente, separando la revisión institucional de la ejecución técnica.

## Controles críticos
La revisión comprueba:
- expediente técnico completo;
- expediente documental completo;
- integridad del paquete;
- conciliación terminada;
- Criterio 78 sustentado y reproducible cuando aplique;
- hallazgos críticos resueltos.

## Estados
- `PENDING`: revisión no concluida.
- `OBSERVED`: controles críticos cumplen, pero existen observaciones documentadas.
- `CONFORMING`: controles críticos cumplen y no existen observaciones.
- `BLOCKED`: falta un control crítico.

## Regla de independencia
La revisión institucional no modifica directamente cálculos, reglas o resultados técnicos. Una inconsistencia debe convertirse en observación o hallazgo y regresar al flujo controlado de ajuste y reejecución.

## Regla de liberación
`BLOCKED` impide liberar el expediente. `OBSERVED` requiere que las observaciones queden registradas y asignadas antes de determinar la liberación conforme al alcance institucional.
