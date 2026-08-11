# INT-06 — Conciliación RTC entre periodos

## Objetivo
Comparar dos universos consolidados y clasificar cada identidad de registro como `unchanged`, `added`, `removed` o `modified`.

## Identidad de comparación
La identidad operativa utiliza Orden, Fecha, Clave, Campaña, Versión y Canal Base.

## Importante
La identidad de conciliación no elimina registros. La deduplicación ya ocurrió en INT-04.

## Modificaciones
Cuando una identidad aparece en ambos periodos pero alguno de sus campos difiere, se registra como `modified` y se conserva la lista de campos modificados.

## Interpretación
- `unchanged`: misma identidad y mismos valores.
- `added`: aparece en el periodo actual y no en el anterior.
- `removed`: aparece en el anterior y no en el actual.
- `modified`: misma identidad operativa, pero con cambios en los valores.

## Próxima etapa
Derivar indicadores de volumen, altas, bajas, permanencias y cambios a partir de la conciliación.
