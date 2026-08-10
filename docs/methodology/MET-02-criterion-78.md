# MET-02 — Conciliación metodológica del Criterio 78

## Objetivo
Implementar de forma reproducible el cálculo del tiempo derivado de impactos, universo de radiodifusoras y duración estándar.

## Fórmula

`Tiempo calculado (segundos) = impactos × radiodifusoras × duración estándar (segundos)`

Posteriormente se expresa como `[h]:mm:ss`.

## Parámetros
Los valores son explícitos y no están codificados como constantes de negocio:

- `impacts`: número de impactos considerados;
- `broadcaster_count`: universo de radiodifusoras;
- `standard_spot_seconds`: duración estándar del spot;
- `parameter_source`: fuente documental del universo/parámetros;
- `cutoff_date`: fecha de corte de los parámetros.

## Ejemplo de conciliación
Con 10 impactos, 1,377 radiodifusoras y 30 segundos por impacto:

`10 × 1,377 × 30 = 413,100 segundos = 114:45:00`

## Interpretación y límites
El resultado es **tiempo calculado conforme a la metodología parametrizada**. No debe presentarse automáticamente como tiempo efectivamente transmitido.

La pauta de RTC permite acreditar programación/pautado conforme a la fuente utilizada, pero el cálculo matemático no constituye por sí mismo evidencia de transmisión efectiva en cada estación.

## Regla de trazabilidad
Toda cifra utilizada para `broadcaster_count` deberá conservar su fuente y fecha de corte. Esto permite sustituir 1,377 por otro universo validado sin modificar el algoritmo.

## Siguiente conciliación
El motor deberá complementarse con evidencia del universo de estaciones y con la metodología documental aplicable al periodo específico antes de utilizar el resultado en una cédula oficial.
