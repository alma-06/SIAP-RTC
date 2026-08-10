# EXP-01 — Generador de expediente de conciliación

## Propósito
Transformar un `ConciliationCase` en un documento legible y reproducible, conservando los elementos necesarios para reconstruir el cálculo.

## Secciones
1. Identificación del caso.
2. Fuente y hash del archivo.
3. Universo de radiodifusoras.
4. Parámetros del cálculo.
5. Fórmula.
6. Resultado en segundos.
7. Resultado en `[h]:mm:ss`.
8. Interpretación y limitaciones.
9. Notas.

## Formato inicial
La primera salida es Markdown, por ser texto UTF-8, versionable y fácilmente convertible a otros formatos.

## Principio de trazabilidad
El reporte no recibe cifras independientes: se construye directamente a partir del caso de conciliación y sus objetos de evidencia.

## Próxima evolución
El mismo modelo será utilizado para generar salidas Excel y PDF, manteniendo la misma información y sin duplicar la lógica de cálculo.
