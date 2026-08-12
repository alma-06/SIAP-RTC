# F3-08 — Dictamen técnico de validación

## Naturaleza
Este documento establece el marco para emitir el dictamen técnico de una corrida o versión del SIAP-RTC. No sustituye la validación del área responsable ni declara aprobación cuando faltan archivos RTC reales o evidencia documental.

## Preguntas de decisión
1. ¿Los archivos de entrada están identificados y tienen huella SHA-256?
2. ¿La estructura real fue diagnosticada?
3. ¿La corrida se ejecutó de forma aislada y reproducible?
4. ¿Las pruebas críticas de aceptación están aprobadas?
5. ¿Los hallazgos bloqueantes están cerrados o justificados?
6. ¿Los ajustes están respaldados por evidencia y pruebas?
7. ¿La reejecución demuestra el efecto esperado del ajuste?
8. ¿Las cifras relevantes están conciliadas con su evidencia?
9. ¿El Criterio 78 tiene parámetros y cálculo reproducibles?
10. ¿Las limitaciones restantes están documentadas?

## Estados posibles
- `NO_VALIDADO`: faltan datos o evidencia suficiente.
- `VALIDADO_CON_OBSERVACIONES`: los controles críticos cumplen y existen observaciones no bloqueantes.
- `VALIDADO`: controles críticos, conciliación y evidencia suficientes para el alcance evaluado.
- `RECHAZADO`: existe una falla crítica o discrepancia no resuelta.

## Regla de prudencia
Una versión no se declara `VALIDADO` por el solo hecho de que el software ejecute correctamente. La validación requiere evidencia del comportamiento, de los datos y de la metodología dentro del alcance declarado.

## Condición actual del proyecto
Mientras no se incorporen y revisen archivos RTC reales representativos, el dictamen técnico debe permanecer en `NO_VALIDADO`. La arquitectura y los controles pueden estar preparados, pero eso no equivale a validación de resultados reales.

## Firma y trazabilidad
La emisión definitiva deberá identificar versión, corrida, periodo, archivos fuente, SHA-256, fecha, responsable de la revisión y estado final.
