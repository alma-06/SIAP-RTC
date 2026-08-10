# CON-05 — Conciliación temporal

## Objetivo
Comparar dos cortes de información RTC y clasificar la evolución de cada identidad canónica.

## Estados
- `ADDITION`: la identidad aparece en el corte actual y no en el anterior.
- `REMOVAL`: la identidad estaba en el corte anterior y no aparece en el actual.
- `PERSISTENCE`: aparece en ambos cortes y sus campos comparables no cambiaron.
- `MODIFICATION`: aparece en ambos cortes y al menos un campo comparable cambió.

## Alcance
La función recibe dos mapas indexados por identidad canónica y no modifica ninguno de los dos conjuntos.

## Importancia para el histórico
Esta clasificación permite construir series de evolución entre publicaciones periódicas y separar altas, bajas, permanencias y modificaciones sin confundir una ausencia en un corte con una eliminación definitiva del histórico.

## Regla metodológica
`REMOVAL` significa ausencia en el corte comparado; no debe interpretarse automáticamente como baja administrativa, cancelación o desaparición permanente de una estación/campaña.

## Próxima etapa
Integrar esta clasificación con los lotes de importación y producir indicadores de conciliación por periodo.
