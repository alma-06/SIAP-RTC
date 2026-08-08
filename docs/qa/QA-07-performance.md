# QA-07 — Protocolo de rendimiento

## Objetivo

Establecer una línea base reproducible para el procesamiento de volúmenes representativos del SIAP-RTC antes del empaquetado de producción.

## Escenarios

| Volumen | Propósito |
|---:|---|
| 1,000 | carga pequeña |
| 10,000 | carga media |
| 50,000 | estrés controlado |

## Ejecución

La suite es opt-in para no ralentizar el CI ordinario:

```text
pytest -q tests/performance/test_import_volume.py --run-performance
```

## Medición

Registrar por escenario:

- tiempo de construcción de objetos de dominio;
- tiempo total de importación cuando se habilite el benchmark E2E;
- memoria máxima;
- tiempo de persistencia SQLite;
- tiempo de consulta histórica;
- tiempo de generación del libro Excel.

## Criterio

El límite actualmente codificado de 30 segundos es un **guardrail de regresión**, no un SLA institucional. Los SLA definitivos se fijarán después de obtener mediciones en un entorno representativo de producción.

## Evidencia

Cada ejecución de rendimiento debe conservar fecha, versión/commit, versión de Python, sistema operativo, hardware y resultado por volumen.
