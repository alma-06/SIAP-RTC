# EXP-01 — Contrato común de exportación

## Objetivo
Definir una representación neutral al formato para que Excel, Word y PowerPoint reciban exactamente los mismos resultados validados.

## Contenido
- título;
- subtítulo;
- periodo;
- estado de comparabilidad;
- indicadores ejecutivos;
- alertas;
- identificador de evidencia.

## Formatos previstos
- XLSX;
- DOCX;
- PPTX.

## Regla de fuente única
Los exportadores no deben recalcular indicadores ni consultar directamente los archivos RTC. Reciben únicamente `ExportPayload`.

## Ventaja
La modificación de una plantilla de salida no altera la metodología ni genera diferencias entre formatos.

## Siguiente paso
Implementar adaptadores concretos para cada formato manteniendo este contrato como interfaz estable.
