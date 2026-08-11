# F2-05 — Interfaz operativa

## Objetivo
Proporcionar una capa de operación sencilla para seleccionar archivos, indicar el periodo y ejecutar el procesamiento sin incorporar lógica de negocio en la interfaz.

## Servicio de operación
`app/ui/operations.py` define `OperationRequest` y `OperationResponse` y orquesta el preflight y el pipeline integrado.

## Flujo
1. El usuario selecciona uno o más archivos RTC.
2. Indica el periodo.
3. Se ejecuta el preflight.
4. Si algún archivo es estructuralmente inválido, el pipeline no se ejecuta.
5. Si el preflight es satisfactorio, se ejecuta el pipeline integrado.
6. La interfaz recibe validaciones y resultado para presentar estado y entregables.

## Separación de responsabilidades
La interfaz no calcula indicadores, no deduplica, no modifica reglas metodológicas y no interpreta transmisión efectiva. Es una capa de entrada y presentación.

## Próxima etapa
Conectar una interfaz gráfica/web al servicio de operación y añadir la generación del paquete final desde la respuesta validada.
