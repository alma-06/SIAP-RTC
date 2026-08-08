# UAT-03 — Escenario operativo semanal completo

## Objetivo
Validar de extremo a extremo el procedimiento que seguirá la Coordinación de Comunicación Social para procesar una publicación semanal del sistema RTC.

## Precondiciones
- SIAP-RTC instalado o ejecutándose en entorno de prueba.
- Base histórica inicializada.
- Archivos de prueba disponibles y hash registrados.
- Usuario con permisos para seleccionar archivos y generar reportes.

## Flujo principal

1. Recibir uno o varios archivos RTC.
2. Identificar periodo y archivos mediante nombre, fecha y SHA-256.
3. Seleccionar los archivos en SIAP-RTC.
4. Validar estructura y encabezados.
5. Ejecutar importación.
6. Homologar campos.
7. Filtrar exclusivamente `CAM. SEN.`.
8. Detectar duplicados intraarchivo e interarchivo.
9. Incorporar únicamente registros nuevos al histórico.
10. Actualizar indicadores.
11. Generar Excel ejecutivo.
12. Ejecutar conciliación independiente.
13. Registrar resultado de la prueba y cualquier incidencia.

## Flujos alternos y errores

| ID | Situación | Comportamiento esperado |
|---|---|---|
| ALT-01 | Archivo inválido | Rechazar archivo, informar causa y conservar trazabilidad del intento |
| ALT-02 | Encabezado faltante | Detener procesamiento del archivo afectado y mostrar campo requerido |
| ALT-03 | Archivo ya procesado | No duplicar registros; informar coincidencia con lote previo |
| ALT-04 | Registro duplicado | Excluir del conteo único y registrar incidencia/auditoría |
| ALT-05 | Semana ya importada | Mantener histórico; permitir revisión sin duplicación |
| ALT-06 | Diferencia de conciliación | Marcar prueba como no aprobada y conservar evidencia |
| ALT-07 | Libro sin registros CAM. SEN. | Completar lote con cero aceptados e informar resultado, sin error técnico |
| ALT-08 | Fallo durante persistencia | No declarar importación exitosa; registrar error y evitar estado parcial no trazable |

## Resultado esperado

Al finalizar una ejecución correcta deben existir:

- lote de importación identificado;
- archivos fuente trazables;
- registros CAM. SEN. procesados;
- duplicados identificados;
- nuevos registros históricos incorporados;
- conteo de spots;
- indicadores actualizados;
- Excel ejecutivo generado;
- evidencia de conciliación.

## Criterio de aprobación

El escenario se aprueba cuando el flujo completo produce resultados reproducibles, no existen pérdidas o duplicaciones injustificadas y la conciliación independiente coincide con el resultado del sistema o cualquier diferencia queda formalmente explicada.

## Evidencia

La evidencia de prueba debe almacenarse fuera del repositorio cuando contenga información institucional. El repositorio conservará únicamente fixtures sintéticos, plantillas, scripts y documentación.
