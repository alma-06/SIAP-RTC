# UAT-04 — Matriz de trazabilidad de aceptación

## Objetivo
Relacionar requisitos, procesos, módulos, casos UAT y evidencia para demostrar cobertura verificable antes de la liberación estable.

## Matriz

| Requisito | Proceso | Módulo | Prueba | Evidencia | Criterio |
|---|---|---|---|---|---|
| RF-IMP-001 | Importación | Importador RTC | UAT-01, UAT-02, UAT-03 | lote + log | archivos válidos procesados |
| RF-FIL-001 | Filtrado | Motor de procesamiento | UAT-03 | Excel resultado | solo CAM. SEN. |
| RF-DUP-001 | Deduplicación | Motor de procesamiento | UAT-04, UAT-05 | auditoría + conteo | sin duplicación injustificada |
| RF-HIS-001 | Histórico | Persistencia | UAT-06, UAT-10 | consulta + evidencia | histórico íntegro |
| RF-CNT-001 | Conteo | Indicadores | UAT-07 | conciliación | diferencia cero o explicada |
| RF-REP-001 | Reportes | Reportes ejecutivos | UAT-08 | XLSX | reporte válido |
| RF-IND-001 | Indicadores | Dashboard/indicadores | UAT-09 | tablero | cifras coherentes |
| RF-AUD-001 | Auditoría | Auditoría | UAT-01..03 | lote + log | trazabilidad completa |

## Estados

Cada fila deberá clasificarse como `NO PROBADO`, `EN PRUEBA`, `APROBADO`, `NO APROBADO` o `NO APLICA`.

## Regla de liberación

No se podrá declarar aprobada la RC si un requisito crítico carece de prueba o evidencia, o si existe un defecto crítico/alto abierto asociado.

## Evidencia

La evidencia con datos institucionales deberá conservarse en el expediente de pruebas o repositorio institucional autorizado, no en el repositorio público de código.

## Control de cambios

La matriz deberá actualizarse cuando cambien requisitos, casos de uso, procesos o módulos. Cada versión liberada debe conservar la matriz correspondiente a su commit de referencia.
