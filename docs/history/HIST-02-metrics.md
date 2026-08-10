# HIST-02 — Motor de indicadores históricos

## Objetivo
Transformar el histórico consolidado en agregaciones reproducibles, sin modificar la base de datos.

## Indicadores iniciales
- total de registros;
- registros por periodo `YYYY-MM`;
- registros por campaña;
- registros por versión;
- registros por canal base;
- registros por estado;
- registros por clave;
- registros por lote;
- total de duplicados detectados.

## Filtros
Las agregaciones utilizan los mismos filtros de consulta del histórico, por lo que un indicador puede calcularse sobre un subconjunto definido por fecha, campaña, versión, clave, canal, estado, lote o archivo.

## Arquitectura
`HistoricalMetricsService` expone el caso de uso y `HistoricalRepository` ejecuta las agregaciones SQL parametrizadas.

## Regla de integridad
Los indicadores se calculan exclusivamente sobre `historical_records`. Los duplicados se reportan desde `duplicate_audit` y no incrementan el total histórico.

## Próxima ampliación
Incorporar métricas de duración a partir de `tiempo_fiscal` y `pauta_transmision`, con reglas explícitas de conversión y conciliación antes de utilizarlas en informes institucionales.
