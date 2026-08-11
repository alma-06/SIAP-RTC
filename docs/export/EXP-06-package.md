# EXP-06 — Paquete ejecutivo y manifiesto

## Objetivo
Generar en una sola operación los entregables XLSX, DOCX y PPTX derivados del mismo `ExportPayload`.

## Salidas
- `siap_rtc_ejecutivo.xlsx`
- `siap_rtc_ejecutivo.docx`
- `siap_rtc_ejecutivo.pptx`
- `manifest.json`

## Manifiesto
Registra título, periodo, Evidence ID, nombres de archivos y SHA-256 de cada entregable.

## Trazabilidad
El `Evidence ID` es común a los tres formatos. El hash permite verificar posteriormente que el archivo no fue alterado desde su generación.

## Regla
El orquestador no modifica los datos de negocio. Coordina exportadores y registra la identidad de los archivos producidos.
