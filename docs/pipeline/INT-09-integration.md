# INT-09 — Integración del pipeline RTC

## Objetivo
Ejecutar en una sola operación las etapas de ingesta, normalización, deduplicación, consolidación, conciliación opcional, indicadores y evidencia.

## Flujo
`Excel RTC → ingesta CAM. SEN. → normalización → deduplicación → consolidación → conciliación opcional → indicadores → EvidenceManifest`

## Diseño
La conciliación se activa únicamente cuando se proporciona el universo del periodo anterior. Esto permite procesar el primer periodo sin inventar una comparación.

## Advertencia permanente
El pipeline conserva la advertencia de que la pauta RTC no acredita por sí misma transmisión efectiva.

## Trazabilidad
El resultado integrado conserva los objetos de cada etapa para auditoría y pruebas, en lugar de devolver únicamente cifras agregadas.

## Próximo hito
Conectar `IntegratedPipelineResult` con el paquete ejecutivo de INT-01 y realizar pruebas de integración sobre archivos RTC representativos.
