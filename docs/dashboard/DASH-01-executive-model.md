# DASH-01 — Modelo del tablero ejecutivo

## Objetivo
Definir el modelo de datos que consumirá la interfaz ejecutiva del SIAP-RTC, sin recalcular indicadores en la capa de presentación.

## Fuente
El modelo consume exclusivamente:
- `PeriodReconciliation`, producido por la conciliación histórica;
- `ReconciliationEvidence`, producido por CON-09.

## Contenido por periodo
- total comparado;
- adiciones;
- remociones/ausencias;
- permanencias;
- modificaciones;
- tasas de coincidencia, cambio, adición y remoción;
- estado de comparabilidad;
- advertencias;
- identificador de evidencia.

## Regla de integridad
No se construye un periodo de tablero sin evidencia asociada. La función de construcción genera un error explícito cuando falta la evidencia.

## Regla de presentación
El tablero debe mostrar las advertencias de comparabilidad junto con el periodo y no debe ocultar un estado `comparable=False`.

## Principio arquitectónico
La interfaz visual es consumidora de datos validados. Los cálculos y reglas metodológicas permanecen en las capas de conciliación.
