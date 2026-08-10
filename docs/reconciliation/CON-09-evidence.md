# CON-09 — Evidencia de conciliación

## Objetivo
Vincular cada resultado de conciliación con los metadatos que permiten reconstruir su procedencia.

## Contenido mínimo
- identificador de evidencia;
- periodo;
- archivo fuente;
- hash SHA-256;
- universo utilizado;
- metodología;
- número de registros;
- resumen de conciliación;
- estado de comparabilidad;
- advertencias;
- fecha y hora de generación.

## Identificador
El `evidence_id` se deriva del periodo y del hash de la fuente. Esto permite identificar de forma estable una evidencia para un mismo corte y archivo.

## Hash
El módulo incluye una función para calcular SHA-256 directamente sobre el archivo fuente por bloques, evitando cargar archivos grandes completos en memoria.

## Principio de trazabilidad
El indicador ejecutivo debe poder enlazarse con esta evidencia antes de presentarse como resultado validado.

## Alcance
Esta entrega modela y construye el paquete de evidencia. La persistencia de estos paquetes y su asociación con reportes ejecutivos se integrará en la siguiente fase.
