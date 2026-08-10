# CON-02 — Diferencias de contenido

## Objetivo
Distinguir un registro completamente idéntico de uno que conserva la misma identidad canónica pero presenta cambios en sus atributos.

## Clasificaciones
- `IDENTICAL`: no existen diferencias en los campos comparables.
- `CHANGED`: existe al menos una diferencia.

## Detalle
Cada diferencia conserva:
- nombre del campo;
- valor anterior;
- valor actual.

## Regla
Los campos utilizados para identificar el registro no deben compararse como contenido. La identidad ya fue resuelta por CON-01.

## Ejemplo
Una identidad `A` puede permanecer igual mientras `version` cambia de `01` a `02`. CON-02 clasifica el registro como `CHANGED` y conserva ambos valores.

## Próxima evolución
La comparación deberá integrarse con el modelo de importación para producir una auditoría de cambios, sin sobrescribir silenciosamente el histórico.
