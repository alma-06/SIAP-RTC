# EXP-07 — Verificación de integridad del paquete

## Objetivo
Comprobar que los archivos registrados en `manifest.json` existen y conservan exactamente el SHA-256 generado al crear el paquete.

## Resultado
La verificación devuelve un estado global `valid` y un resultado individual por archivo.

## Casos
- Paquete íntegro: todos los archivos existen y sus hashes coinciden.
- Paquete alterado: al menos un archivo existe pero su hash no coincide.
- Manifiesto inexistente: el paquete se considera no válido.

## Alcance
La verificación comprueba integridad de los entregables; no determina por sí misma la validez metodológica de los datos RTC.
