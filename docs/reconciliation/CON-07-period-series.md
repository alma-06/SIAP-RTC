# CON-07 — Serie histórica de conciliaciones por periodo

## Objetivo
Conservar los resultados de conciliación de varios cortes en una estructura única, inmutable y apta para reportes.

## Unidad de la serie
Cada periodo contiene:
- identificador del periodo;
- resumen de conciliación producido por CON-06.

## Diseño
La serie no recalcula indicadores. Consume `ReconciliationSummary` ya validado por el motor de conciliación.

## Uso previsto
La serie será la fuente para:
- tablas históricas;
- gráficas de tendencia;
- comparativos entre periodos;
- resumen ejecutivo.

## Regla metodológica
Los periodos representan cortes comparables; no deben mezclarse cortes con universos o criterios metodológicos incompatibles sin dejar constancia de ello.
