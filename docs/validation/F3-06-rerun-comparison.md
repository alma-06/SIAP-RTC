# F3-06 — Reejecución controlada y comparación

## Objetivo
Relacionar una nueva corrida con la corrida anterior y medir el efecto de un ajuste aprobado.

## Identificación
Cada comparación conserva `previous_run_id` y `current_run_id`.

## Métricas
La comparación admite métricas numéricas del resultado, por ejemplo registros, spots, exclusiones, duplicados, tiempo calculado o indicadores, según el alcance de la corrida.

## Delta
Para cada métrica se calcula `current - previous`.

## Regla
Una nueva corrida no sustituye a la anterior. Ambas permanecen disponibles para reconstruir la evolución del resultado.

## Uso metodológico
Un cambio en una métrica no se interpreta automáticamente como mejora. Debe relacionarse con el ajuste que originó la reejecución y con la evidencia correspondiente.

## Salida
La comparación alimenta F3-07 Conciliación y permite determinar si el ajuste resolvió el hallazgo sin introducir efectos no previstos.
