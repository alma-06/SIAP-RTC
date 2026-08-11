# INT-07 — Indicadores RTC

## Objetivo
Transformar la conciliación entre periodos en indicadores descriptivos y trazables.

## Indicadores
- Total del periodo anterior.
- Total del periodo actual.
- Permanencias.
- Altas.
- Bajas.
- Modificados.
- Variación neta: actual menos anterior.
- Tasa de permanencia: permanencias / periodo anterior.
- Tasa de altas: altas / periodo actual.
- Tasa de bajas: bajas / periodo anterior.
- Tasa de modificación: modificados / periodo actual.

## Criterio de denominadores
Los denominadores están definidos explícitamente para evitar porcentajes ambiguos. Cuando el denominador es cero, el resultado es `None`, no cero.

## Alcance
Estos indicadores describen registros de pauta RTC y cambios entre universos. No deben etiquetarse como transmisión efectiva ni como tiempo consumido sin una fuente o cálculo metodológico adicional.

## Próxima etapa
Construir la capa de evidencia y metadatos que permita vincular cada indicador con sus fuentes, reglas y advertencias.
