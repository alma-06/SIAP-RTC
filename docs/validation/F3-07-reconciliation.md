# F3-07 — Conciliación y trazabilidad del Criterio 78

## Objetivo
Relacionar los datos de origen, parámetros aplicados, cálculo y cifra reportada, conservando la trazabilidad necesaria para una revisión posterior.

## Criterio 78
El modelo registra explícitamente:
- impactos;
- radiodifusoras consideradas;
- segundos por impacto;
- segundos totales;
- conversión a días y a horas:minutos:segundos.

La operación base es `impactos × radiodifusoras × segundos_por_impacto`.

## Ejemplo técnico
Con 10 impactos, 1,377 radiodifusoras y 30 segundos por impacto se obtienen 413,100 segundos, equivalentes a 4 días, 18:45:00.

Este ejemplo valida la aritmética del componente; no afirma que esos parámetros sean los valores definitivos de un periodo real.

## Conciliación
La cifra final deberá vincularse con el archivo fuente, su SHA-256, el periodo, la corrida y los parámetros utilizados. Si el universo de radiodifusoras proviene de una fuente externa, esa fuente debe quedar identificada en la evidencia del periodo.

## Regla metodológica
El sistema distingue entre tiempo programado/pautado y transmisión efectiva. La fuente RTC acredita la programación disponible; cualquier afirmación sobre transmisión efectiva requiere el sustento correspondiente y no debe inferirse únicamente del registro de pauta.
