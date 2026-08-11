# F3-05 — Control de ajustes

## Objetivo
Evitar modificaciones directas al motor derivadas de diferencias observadas durante una corrida RC1.

## Registro mínimo
Cada ajuste propuesto debe contener:
- identificador único;
- código del hallazgo que lo origina;
- clasificación: TECHNICAL, DATA o METHODOLOGY;
- justificación;
- evidencia;
- referencia de prueba;
- estado.

## Flujo
`Hallazgo → clasificación → evidencia → propuesta → prueba → revisión → aprobación → nueva RC`

## Regla de integridad
Un ajuste sin evidencia o sin prueba asociada se rechaza.

## Regla de no mutación silenciosa
No se modifica una regla de negocio únicamente para hacer coincidir un resultado observado con una cifra esperada. La diferencia debe explicarse y quedar documentada.

## Estados
- `PROPOSED`: ajuste registrado y pendiente de revisión.
- `TESTED`: ajuste probado técnicamente.
- `APPROVED`: ajuste autorizado para incorporarse a la siguiente RC.
- `REJECTED`: ajuste descartado con justificación.

## Resultado
Cada ajuste aprobado deberá conducir a una nueva corrida candidata, nunca a la modificación retroactiva de una corrida histórica.
