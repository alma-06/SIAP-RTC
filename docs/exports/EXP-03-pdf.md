# EXP-03 — Expediente de conciliación en PDF

## Propósito
Generar un expediente PDF institucional a partir del mismo modelo canónico utilizado por los demás formatos.

## Arquitectura
`ConciliationCase → ConciliationReport → PdfConciliationDocument → PDF renderer`

La capa PDF no realiza cálculos metodológicos.

## Contenido mínimo
- identificación del caso;
- periodo;
- fuente y hash;
- universo de radiodifusoras;
- parámetros;
- fórmula;
- desarrollo y resultado;
- interpretación;
- limitaciones;
- notas.

## Requisito de integridad
El PDF debe representar exactamente la información del `ConciliationCase` y no introducir cifras calculadas de forma independiente.

## Estado
La entrega actual construye la fuente canónica de contenido UTF-8 y la prueba automatizada. La materialización física del PDF queda separada en el renderer documental para evitar acoplar la lógica de negocio con una biblioteca de presentación.
