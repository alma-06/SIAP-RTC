# DASH-04 — Alertas ejecutivas

## Objetivo
Señalar condiciones que ameritan revisión sin convertir automáticamente una diferencia estadística en un error o conclusión administrativa.

## Alertas actuales
- `NON_COMPARABLE`: el periodo no es comparable con la referencia declarada.
- `EVIDENCE_WARNING`: la evidencia contiene advertencias.
- `HIGH_MODIFICATION_RATE`: la tasa de modificación alcanza o supera 25% por defecto.
- `HIGH_REMOVAL_RATE`: la tasa de remoción/ausencia alcanza o supera 25% por defecto.

## Umbrales
Los umbrales de modificación y remoción son parámetros explícitos y pueden modificarse en la llamada al motor. No deben interpretarse como criterios normativos; son umbrales de revisión operativa.

## Principio
Una alerta indica `revisar`, no `error`. El sistema conserva los valores originales y las advertencias que sustentan la alerta.

## Alcance
La primera versión no genera alertas sobre altas porque una adición puede ser un comportamiento esperado del corte y requiere contexto adicional para establecer un umbral útil.
