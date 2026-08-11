# F3-04 — Revisión técnica de resultados RC1

## Objetivo
Revisar una corrida RC1 antes de modificar reglas o aceptar sus resultados.

## Controles
- conteo de registros de entrada;
- conteo posterior a normalización;
- conteo posterior a deduplicación;
- conteo consolidado;
- hallazgos y severidad;
- consistencia de evidencia;
- conciliación e indicadores cuando exista periodo previo;
- Criterio 78 y sus parámetros cuando aplique.

## Regla de conteos
Las etapas de normalización, deduplicación y consolidación no deben aumentar registros sin una justificación explícita. Un aumento no explicado es bloqueante.

## Regla de revisión
Primero se registra el hallazgo. Después se determina si corresponde a un defecto técnico, una característica de los datos reales o una regla de negocio que deba documentarse. No se modifica el motor únicamente para eliminar una diferencia observada.

## Resultado
La revisión produce hallazgos con código y severidad. Un hallazgo `BLOCKING` impide aceptar la corrida como resultado validado.

## Limitación actual
La revisión automatizada de conteos es un control inicial. La revisión de contenido y la conciliación con evidencia documental requieren datos RTC reales y criterio del área responsable.
