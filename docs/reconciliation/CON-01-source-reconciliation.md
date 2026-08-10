# CON-01 — Conciliación de fuente contra histórico

## Objetivo
Determinar qué registros de un archivo RTC son nuevos respecto del histórico y cuáles ya existen, sin modificar el histórico.

## Clasificaciones
- `NEW`: identidad canónica no encontrada previamente.
- `EXISTING`: identidad canónica ya presente en el histórico.
- `duplicate_source_count`: repeticiones de una identidad dentro del propio archivo de entrada.

## Principio
La conciliación es una operación de solo lectura. La decisión de insertar o auditar pertenece al motor transaccional de importación.

## Salida
El motor devuelve el detalle por identidad y un resumen con:

- total de registros de la fuente;
- nuevos;
- existentes;
- duplicados internos de la fuente.

## Alcance de esta entrega
Esta versión concilia identidades canónicas. La detección de registros faltantes, diferencias de atributos para una misma identidad y conciliación temporal serán fases posteriores.
