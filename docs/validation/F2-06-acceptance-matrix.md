# F2-06 — Matriz de pruebas de aceptación

## Criterio de salida
La versión candidata no se libera mientras exista una prueba crítica fallida o una discrepancia metodológica sin resolver.

| ID | Escenario | Resultado esperado | Criticidad |
|---|---|---|---|
| AT-01 | Un archivo RTC válido | Preflight OK y pipeline ejecutado | Alta |
| AT-02 | Varios archivos RTC | Consolidación en un único resultado | Alta |
| AT-03 | Hoja con columnas faltantes | Procesamiento detenido | Alta |
| AT-04 | Hoja vacía | Advertencia controlada | Media |
| AT-05 | Sin registros CAM. SEN. | Advertencia; no inventar registros | Alta |
| AT-06 | Registro de otra dependencia | Fuera del universo analítico | Alta |
| AT-07 | Duplicado canónico | Duplicado identificado y trazable | Alta |
| AT-08 | Registro modificado | Cambio detectable en conciliación | Alta |
| AT-09 | Primer periodo | Resultado sin dependencia de histórico | Alta |
| AT-10 | Periodo ya registrado | Histórico no sobrescrito | Alta |
| AT-11 | Criterio 78 | Cálculo reproducible con parámetros registrados | Alta |
| AT-12 | Cambio de parámetros C78 | Huella digital diferente | Alta |
| AT-13 | Evidencia/paquete alterado | Verificación SHA-256 fallida | Alta |
| AT-14 | Generación XLSX/DOCX/PPTX | Entregables generados desde resultado integrado | Alta |
| AT-15 | Paquete final | ZIP y manifiesto consistentes | Alta |
| AT-16 | Advertencias no críticas | Resultado utilizable y advertencias visibles | Media |

## Evidencia de prueba
Cada ejecución debe conservar: fecha, versión/código, archivos de entrada, periodo, resultado esperado, resultado observado y estado PASS/FAIL.

## Regla metodológica
Una prueba técnica aprobada no sustituye la validación documental de la fuente. Las pruebas de aceptación verifican comportamiento del sistema; la evidencia RTC acredita el dato de origen.
