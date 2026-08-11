# INT-14 — Ensamblaje y verificación del paquete

## Objetivo
Cerrar la cadena documental con un manifiesto único, verificación de integridad y archivo ZIP reproducible.

## Manifiesto
`PackageManifest.json` registra periodo, Evidence ID, fecha de generación y, para cada archivo, ruta relativa, tamaño y SHA-256.

## Verificación
`verify_package` comprueba existencia, tamaño, SHA-256 y archivos no manifestados. Un cambio posterior en cualquier entregable invalida la verificación.

## Distribución
`zip_package` genera un archivo ZIP que contiene los entregables y el manifiesto.

## Principio
La verificación se realiza sobre los archivos finales, no sobre una representación intermedia.

## Estado
Con INT-14 se completa la primera cadena funcional: procesamiento → evidencia → XLSX/DOCX/PPTX → manifiesto → verificación → paquete.

## Próxima fase
Pruebas con archivos RTC representativos, validación de reglas de negocio y preparación de una interfaz operativa para selección de archivos y ejecución del pipeline.
