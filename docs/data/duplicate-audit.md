# DATA-03 — Auditoría de duplicados

## Objetivo
Conservar evidencia de cada registro que el motor identifica como duplicado durante una importación.

## Tabla
`duplicate_audit` registra:

- `identity_hash` del registro;
- lote que detectó el duplicado;
- archivo de origen;
- identificador del registro histórico existente, cuando esté disponible;
- fecha y hora de detección.

## Unicidad de la evidencia
La combinación `identity_hash + batch_id + source_filename` evita registrar repetidamente la misma detección dentro del mismo archivo y lote.

## Relación con histórico
La auditoría documenta el intento de incorporación; no modifica ni elimina el registro histórico existente.

## Consultas previstas
La capa de persistencia permite obtener el número de duplicados detectados por lote y, mediante `identity_hash`, localizar todas las detecciones de un mismo registro.

## Criterio de trazabilidad
Un registro no incorporado por duplicidad debe ser explicable a partir de su identidad, lote y archivo de procedencia.
