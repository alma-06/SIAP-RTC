# INT-03 — Normalización RTC

## Objetivo
Convertir los registros filtrados de CAM. SEN. a una representación canónica antes de deduplicar o conciliar.

## Reglas
- Texto: espacios redundantes se eliminan y se normaliza a minúsculas para comparación.
- Fecha: se convierte a ISO `YYYY-MM-DD` cuando el valor es reconocible.
- Tiempo Fiscal: `HH:MM[:SS]` se convierte a segundos.
- Valores no reconocibles se conservan como texto para revisión, no se inventan datos.
- Campos vacíos generan advertencia, pero no eliminan automáticamente el registro.

## Principio metodológico
Normalizar no significa corregir el dato fuente. La representación canónica sirve para comparar y detectar inconsistencias sin perder el valor original de procedencia.

## Próxima etapa
La deduplicación utilizará esta representación normalizada y deberá distinguir duplicados exactos de registros legítimamente repetidos.
