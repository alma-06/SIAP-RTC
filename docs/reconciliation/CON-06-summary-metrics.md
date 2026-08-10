# CON-06 — Resumen de conciliación

## Objetivo
Convertir los estados producidos por CON-05 en indicadores ejecutivos y comparables entre periodos.

## Indicadores base
- total comparado;
- adiciones;
- remociones/ausencias;
- permanencias;
- modificaciones.

## Tasas
Las tasas se calculan respecto del total comparado:

- `match_rate = persistence / total`;
- `change_rate = modifications / total`;
- `addition_rate = additions / total`;
- `removal_rate = removals / total`.

Cuando el total es cero, las tasas devuelven `0.0` para evitar divisiones inválidas.

## Interpretación
Las tasas describen la comparación entre dos cortes. No deben interpretarse como indicadores operativos distintos de la conciliación sin una definición específica.

## Uso previsto
Estos indicadores alimentarán el resumen ejecutivo, las exportaciones y las visualizaciones del SIAP-RTC.
