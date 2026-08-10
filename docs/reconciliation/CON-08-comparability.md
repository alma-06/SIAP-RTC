# CON-08 — Validación de comparabilidad

## Objetivo
Impedir que una serie histórica sea presentada como tendencia cuando los cortes fueron obtenidos con universos, metodologías o campos comparables incompatibles.

## Validaciones
Para comparar varios periodos se verifica la igualdad de:

- `universe_id`;
- `methodology_id`;
- `comparable_fields`.

## Resultado
La validación devuelve:
- `comparable=True` cuando no existen incompatibilidades;
- `comparable=False` y una lista de razones cuando existe al menos una diferencia.

## Regla de presentación
Una serie no comparable debe generar advertencia y no debe alimentar automáticamente una visualización de tendencia como si fuera homogénea.

## Alcance
La validación no decide si dos metodologías son equivalentes desde el punto de vista jurídico o sustantivo. Solamente detecta diferencias declaradas en los metadatos metodológicos.
