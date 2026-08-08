# QA-09 — Cierre de calidad y preparación de versión candidata

## Propósito
Formalizar la decisión de paso de desarrollo a construcción de una versión candidata instalable.

## Criterios de entrada

- Suite unitaria disponible.
- Pruebas de integración disponibles.
- Pruebas históricas disponibles.
- Benchmarks opt-in disponibles.
- Exportación ejecutiva cubierta.
- Auditoría de lotes cubierta.

## Criterios de salida

| Área | Estado requerido |
|---|---|
| Importación | Sin defectos críticos/altos abiertos |
| Filtrado CAM. SEN. | Verificado |
| Deduplicación | Verificada intra/interarchivo |
| Histórico | Verificado en múltiples lotes |
| Reportes | Verificados |
| Auditoría | Verificada |
| CI | Suite normal en verde |
| Rendimiento | Línea base documentada |
| Seguridad de datos | Sin datos institucionales en fixtures |

## Defectos y riesgos

Los defectos deben registrarse como incidencias antes de declarar una versión candidata. Los riesgos aceptados deben documentarse con responsable y mitigación.

## Evidencia mínima de release

- commit de versión;
- resultado de CI;
- reporte de pruebas;
- resultados de benchmark;
- hash del artefacto instalable;
- notas de versión;
- instrucciones de instalación y reversión.

## Decisión

La etiqueta de versión candidata solo debe emitirse cuando todos los criterios de salida estén satisfechos o exista una aceptación formal documentada de las excepciones.
