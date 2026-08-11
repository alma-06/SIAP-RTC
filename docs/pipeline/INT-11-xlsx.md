# INT-11 — Excel ejecutivo institucional

## Objetivo
Generar un libro XLSX desde el resultado integrado, manteniendo una única fuente de verdad.

## Hojas
- `Resumen`: métricas ejecutivas y advertencias.
- `Base Consolidada`: registros depurados con periodo y archivo fuente.
- `Conciliación`: clasificación y campos modificados, cuando existe periodo anterior.
- `Indicadores`: métricas derivadas de la conciliación, cuando existe comparación.
- `Fuentes`: archivo, periodo y SHA-256.
- `Advertencias`: limitaciones y observaciones del procesamiento.

## Reglas de presentación
Se congelan encabezados, se agregan filtros y se ajustan anchos de columna de forma conservadora.

## Principio
El libro es una representación del `IntegratedPipelineResult`; no recalcula la lógica analítica.

## Próxima etapa
Agregar generación de DOCX y PPTX usando el mismo resultado integrado.
