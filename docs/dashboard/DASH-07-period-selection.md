# DASH-07 — Selector de periodo y corte de referencia

## Objetivo
Definir una selección explícita de periodo actual, periodo de referencia y rango histórico para el tablero ejecutivo.

## Reglas
- El periodo actual debe existir.
- El periodo de referencia, si se proporciona, debe existir.
- Actual y referencia no pueden ser el mismo periodo.
- Los periodos históricos solicitados deben existir.
- Los duplicados del rango histórico se eliminan conservando el primer orden solicitado.

## Principio
La selección no modifica los datos ni recalcula indicadores. Únicamente determina qué resultados validados serán presentados.

## Flujo previsto
`Periodo actual → referencia → histórico → comparativo → ficha/gráficas/alertas`.

## Control metodológico
La selección no anula la validación de comparabilidad. Un periodo seleccionado conserva su estado y advertencias originales.
