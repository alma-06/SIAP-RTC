# F3-01 — Diagnóstico de archivos RTC reales

## Objetivo
Definir el procedimiento de recepción y diagnóstico previo al procesamiento de archivos RTC reales.

## Regla principal
Los archivos reales deben diagnosticarse antes de modificar reglas de negocio. Las diferencias observadas se registran como hallazgos y no se convierten automáticamente en nuevas reglas.

## Diagnóstico mínimo
1. Nombre, extensión y tamaño del archivo.
2. Número y nombre de hojas.
3. Fila de encabezados y columnas detectadas.
4. Número de filas de datos y filas vacías.
5. Valores observados en `Dependencia CAM. SEN.`.
6. Formatos de `Fecha` y cobertura temporal.
7. Formatos y valores de `Tiempo Fiscal`.
8. Registros con `Orden` o `Clave` vacíos.
9. Duplicidades potenciales.
10. Variaciones estructurales entre archivos del mismo periodo.
11. Huella SHA-256 de cada archivo recibido.

## Clasificación de hallazgos
- BLOQUEANTE: impide interpretar o procesar de forma segura.
- ADVERTENCIA: permite continuar, pero requiere revisión.
- INFORMATIVO: diferencia registrada sin impacto analítico conocido.

## Evidencia
Cada archivo debe conservar su nombre original, SHA-256 y diagnóstico asociado. No se deben alterar los archivos fuente durante esta etapa.

## Salida
El diagnóstico produce una ficha técnica por archivo y una consolidación del periodo. La decisión de procesar se toma después del diagnóstico.

## Estado
Este protocolo está listo para ejecutarse cuando se incorporen los archivos RTC reales; no declara que dichos archivos hayan sido validados mientras no estén disponibles.
