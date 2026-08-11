# INT-05 — Consolidación RTC

## Objetivo
Convertir los registros depurados en un universo consolidado que conserve explícitamente periodo y procedencia.

## Alcance
- Consolidación de un periodo.
- Consolidación histórica de múltiples periodos.
- Conservación del archivo fuente por registro.
- Inventario de periodos y archivos de origen.

## Principio
La consolidación no recalcula impactos ni tiempo de transmisión. Tampoco vuelve a deduplicar registros. Consume el universo producido por INT-04.

## Distinción metodológica
Un registro consolidado representa una observación publicada en una pauta RTC. No equivale por sí mismo a una transmisión efectiva.

## Próxima etapa
Construir la conciliación y los indicadores derivados sobre el universo consolidado.
