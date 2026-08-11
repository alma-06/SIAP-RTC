# DASH-06 — Comparativo ejecutivo

## Objetivo
Presentar varios periodos en una estructura única para análisis histórico, conservando el estado de comparabilidad de cada corte.

## Contenido por periodo
- total comparado;
- adiciones;
- modificaciones;
- permanencias;
- remociones/ausencias;
- tasa de coincidencia;
- tasa de cambio;
- estado de comparabilidad;
- evidencia asociada.

## Regla metodológica
El comparativo no transforma un periodo no comparable en comparable. Si al menos un corte tiene `comparable=False`, el conjunto se marca como no comparable y conserva la advertencia correspondiente.

## Uso previsto
La estructura alimentará tablas y visualizaciones históricas. La interfaz podrá mostrar los periodos comparables y, al mismo tiempo, advertir sobre los cortes que no deben interpretarse como parte de una tendencia homogénea.
