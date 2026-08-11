# INT-08 — Evidencia y trazabilidad metodológica

## Objetivo
Vincular cada resultado con sus fuentes, huellas SHA-256, periodo, metodología y advertencias.

## Estructura
`EvidenceManifest` contiene:
- `evidence_id`;
- métrica;
- metodología aplicada;
- fuentes con nombre, periodo y SHA-256;
- advertencias.

## Principio de trazabilidad
Un indicador debe poder remontarse desde el resultado hasta los archivos fuente que lo sustentan.

## Limitación metodológica
La evidencia de pauta RTC acredita programación publicada. El manifiesto no transforma esa evidencia en prueba de transmisión efectiva.

## Integridad
Las fuentes se identifican mediante SHA-256 para detectar modificaciones posteriores.

## Próxima etapa
Integrar INT-02 a INT-08 en el orquestador y generar un paquete ejecutivo que incluya la evidencia metodológica.
