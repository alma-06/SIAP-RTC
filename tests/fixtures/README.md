# Fixtures de Excel RTC

Esta carpeta está reservada para archivos Excel sintéticos o anonimizados que reproduzcan la estructura publicada por RTC.

## Casos mínimos

- `valid_single_sheet.xlsx`: estructura válida y registros CAM. SEN.
- `extra_columns.xlsx`: columnas adicionales no relevantes.
- `missing_required_column.xlsx`: falta una columna obligatoria.
- `blank_rows.xlsx`: filas vacías intercaladas.
- `mixed_dates.xlsx`: fechas Excel y fechas de texto equivalentes.
- `duplicate_rows.xlsx`: duplicados dentro del archivo.
- `duplicate_across_files_a.xlsx` / `duplicate_across_files_b.xlsx`: duplicados entre archivos.
- `other_dependencies.xlsx`: dependencias distintas de CAM. SEN.
- `empty_workbook.xlsx`: libro sin registros.

No se deben incorporar al repositorio archivos institucionales que contengan información sensible. Los fixtures deben ser sintéticos o previamente anonimizados.
