# DASH-03 — Visualizaciones

## Objetivo
Preparar los datos validados para las visualizaciones ejecutivas sin duplicar cálculos en la capa gráfica.

## Visualizaciones iniciales
1. Evolución temporal de adiciones, modificaciones, permanencias y remociones.
2. Calidad de conciliación mediante tasa de coincidencia y tasa de cambio.

## Adaptadores
`build_trend_points` expone únicamente los valores ya contenidos en `DashboardPeriod`.
`build_quality_points` hace lo mismo para las tasas validadas.

## Regla
Los adaptadores no calculan tasas ni reinterpretan estados. La visualización consume directamente los resultados validados.

## Extensión
La composición del periodo puede construirse a partir del `DashboardPeriod` más reciente sin introducir lógica de negocio nueva.
