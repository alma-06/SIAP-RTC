# PIPE-02 — Lector y homologador RTC

## Objetivo
Transformar hojas Excel RTC en registros normalizados, conservando la procedencia de cada fila.

## Comportamiento
- Lee libros XLSX/XLSM mediante `openpyxl`.
- Recorre las hojas del libro.
- Identifica encabezados mediante una tabla de homologación tolerante a mayúsculas, acentos y espacios.
- Ignora filas completamente vacías.
- Normaliza cadenas y fechas.
- Conserva número de fila y nombre de hoja de origen.

## Encabezados homologados

- Pauta de transmisión → `pauta_transmision`
- Estado → `estado`
- Tiempo Fiscal → `tiempo_fiscal`
- Canal Base → `canal_base`
- Orden → `orden`
- Fecha → `fecha`
- Dependencia CAM. SEN. → `dependencia_cam_sen`
- Clave → `clave`
- Campaña → `campana`
- Versión → `version`

## Separación de responsabilidades
El lector solo interpreta y normaliza el archivo. El filtrado de `CAM. SEN.`, identidad, deduplicación y persistencia pertenecen a etapas posteriores del pipeline.

## Procedencia
Cada registro conserva `source_sheet` y `source_row` para facilitar conciliación y diagnóstico.

## Siguiente integración
El orquestador PIPE-01 deberá consumir `NormalizedRTCRecord.values` y encadenar el filtrado, identidad y persistencia.
