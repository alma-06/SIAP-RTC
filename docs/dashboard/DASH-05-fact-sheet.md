# DASH-05 — Ficha ejecutiva del periodo

## Objetivo
Crear una representación compacta y reutilizable de un periodo conciliado para exportarla posteriormente a Word, Excel, PowerPoint o una interfaz web.

## Contenido
- KPIs ejecutivos de DASH-02;
- alertas de DASH-04;
- etiqueta explícita de comparabilidad.

## Regla de fuente única
La ficha se construye a partir de `DashboardPeriod`. No recalcula indicadores ni modifica resultados.

## Estado
Los estados permitidos en esta versión son:
- `COMPARABLE`;
- `NO COMPARABLE`.

## Uso futuro
La ficha será el contrato de datos para plantillas institucionales y reportes ejecutivos. El diseño visual y la exportación a formatos concretos se implementarán en capas posteriores.
