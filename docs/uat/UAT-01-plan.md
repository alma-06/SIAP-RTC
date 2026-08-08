# UAT-01 — Plan de Pruebas de Aceptación de Usuario

## 1. Objetivo
Validar que SIAP-RTC satisface el flujo operativo de la Coordinación de Comunicación Social para importar publicaciones RTC, identificar registros de `CAM. SEN.`, consolidarlos, evitar duplicados y generar resultados verificables.

## 2. Alcance
Incluye selección de uno o varios Excel, importación, homologación, filtrado, deduplicación, persistencia histórica, conteo de spots, consulta de indicadores y exportación ejecutiva.

## 3. Condición de prueba
La prueba deberá realizarse con archivos RTC de prueba o copias autorizadas. No deberán incorporarse archivos institucionales al repositorio Git.

## 4. Casos de aceptación

| ID | Caso | Entrada | Resultado esperado | Evidencia |
|---|---|---|---|---|
| UAT-01 | Importación simple | 1 Excel válido | Lote creado y registros procesados | captura + log |
| UAT-02 | Importación múltiple | 2+ Excel válidos | Todos los archivos procesados | reporte de lote |
| UAT-03 | Filtrado | Registros mixtos | Solo `CAM. SEN.` en resultado | Excel resultado |
| UAT-04 | Duplicado intraarchivo | Registro repetido | Un solo registro contabilizado | conteo + auditoría |
| UAT-05 | Duplicado entre archivos | Mismo registro en dos archivos | No se duplica en histórico | conteo histórico |
| UAT-06 | Histórico | Dos lotes semanales | Registros nuevos se agregan | consulta histórica |
| UAT-07 | Conteo | Resultado consolidado | Conteo coincide con conciliación manual | cédula de conciliación |
| UAT-08 | Reporte | Resultado procesado | Excel ejecutivo con filtros | archivo generado |
| UAT-09 | Indicadores | Lote procesado | Indicadores coherentes con base | tablero |
| UAT-10 | Recuperación | Reinicio de aplicación | Datos persisten | evidencia de reinicio |

## 5. Criterio de aceptación
Cada caso se clasifica como `APROBADO`, `NO APROBADO` o `NO APLICA`. Para liberar la versión estable no deben existir casos críticos o altos no resueltos.

## 6. Conciliación independiente
El total de spots debe calcularse también mediante un procedimiento manual independiente sobre una copia de control. La cifra del sistema debe coincidir o cualquier diferencia debe quedar explicada y documentada.

## 7. Evidencia mínima
- identificación de versión/commit;
- archivos de entrada identificados mediante hash cuando proceda;
- resultado de importación;
- conteo manual de control;
- resultado SIAP-RTC;
- Excel exportado;
- incidencias;
- firma o validación del responsable de la prueba.

## 8. No conformidades
Toda diferencia de conteo, pérdida de registros, duplicación no explicada, filtrado incorrecto o corrupción de histórico se considera defecto bloqueante hasta su análisis.
