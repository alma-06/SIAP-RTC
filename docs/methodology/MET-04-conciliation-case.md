# MET-04 — Expediente metodológico de conciliación

## Objetivo
Conservar en una sola estructura los elementos necesarios para reconstruir un cálculo del Criterio 78.

## Componentes
Cada caso identifica:

- `case_id`;
- periodo;
- archivo fuente;
- hash del archivo fuente;
- universo de radiodifusoras;
- impactos considerados;
- duración estándar;
- resultado en segundos;
- resultado `[h]:mm:ss`;
- interpretación y notas.

## Principio de reproducibilidad
Un caso no depende únicamente del resultado final. Debe conservar los parámetros y referencias que permiten repetir el cálculo.

## Hash
El hash identifica el archivo utilizado y permite detectar sustituciones posteriores del archivo fuente.

## Ejemplo
El caso `C78-2026-Q2-001` puede vincular una pauta, el universo `CRT-2026-Q2`, 10 impactos y 30 segundos por impacto. El resultado se reconstruye como `413,100` segundos, equivalente a `114:45:00`.

## Limitación
La ficha documenta un cálculo metodológico. No convierte automáticamente una pauta en evidencia de transmisión efectiva.

## Próxima etapa
Esta estructura será utilizada por `EXP-01` para generar un expediente legible y exportable, incluyendo resumen, parámetros, fórmula, resultado y advertencias metodológicas.
