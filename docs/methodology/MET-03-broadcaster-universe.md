# MET-03 — Universo de radiodifusoras

## Objetivo
Evitar que el universo de estaciones utilizado en una conciliación sea un número sin procedencia documental.

## Registro mínimo
Cada universo debe conservar:

- identificador único;
- total de estaciones;
- fuente;
- fecha de corte;
- metodología de conteo;
- archivo de origen, cuando exista;
- notas aclaratorias, cuando sean necesarias.

## Ejemplo
El universo utilizado en una conciliación puede registrarse como:

- `universe_id`: `CRT-2026-Q2`;
- `total_stations`: `1377`;
- `cutoff_date`: `2026-06-30`.

El ejemplo no sustituye la evidencia documental: el archivo y la fuente real deberán conservarse como parte del expediente metodológico.

## Integración con Criterio 78
El universo genera los parámetros de Criterio 78 sin duplicar el número en el algoritmo. Esto permite sustituir el universo para otro periodo manteniendo inalterada la fórmula.

## Principio de auditoría
Una cifra utilizada en un indicador institucional debe poder responder cuatro preguntas: **qué valor fue utilizado, de dónde salió, a qué fecha corresponde y cómo se obtuvo**.
