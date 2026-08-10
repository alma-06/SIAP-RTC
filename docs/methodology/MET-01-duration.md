# MET-01 — Normalización de duración

## Objetivo
Establecer una representación numérica y auditable para duraciones provenientes de RTC antes de agregarlas.

## Representación interna
La unidad canónica es el segundo entero.

Se aceptan:
- `MM:SS`;
- `HH:MM:SS`;
- `datetime.timedelta`;
- valores numéricos de Excel menores que 1, interpretados como fracción de día;
- valores numéricos enteros/no fraccionarios, interpretados como segundos.

## Salidas
- `seconds_to_hhmmss`: `HH:MM:SS` convencional;
- `seconds_to_excel_elapsed`: `[h]:mm:ss` conceptual, conservando horas superiores a 24.

## Regla metodológica
Este módulo únicamente normaliza duración. No determina si la duración representa tiempo programado, tiempo fiscal, tiempo transmitido o cualquier otra categoría administrativa. Esa interpretación se establecerá en el módulo de conciliación correspondiente.

## Precisión
Los resultados internos se expresan en segundos enteros. Las fracciones de segundo se truncan en esta capa.

## Criterio de aceptación
Una duración válida debe poder convertirse de forma determinista a segundos y volver a una representación legible sin perder horas acumuladas por encima de 24.
