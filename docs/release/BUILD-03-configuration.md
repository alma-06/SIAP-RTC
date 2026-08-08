# BUILD-03 — Configuración de producción

## Objetivo

Centralizar las rutas de datos de SIAP-RTC y evitar dependencias de rutas absolutas en los módulos de la aplicación.

## Configuración

`AppPaths.from_environment()` utiliza `SIAP_RTC_DATA_DIR` cuando está definida. Si no existe, utiliza `%APPDATA%\SIAP-RTC` en Windows mediante la variable `APPDATA`.

## Estructura

```text
SIAP-RTC/
├── data/       SQLite y configuración persistente
├── imports/    archivos fuente RTC
├── reports/    reportes Excel generados
├── logs/       registros técnicos
└── backups/    respaldos
```

## Base de datos

La base predeterminada es `data/siap_rtc.db`.

## Principios

- El ejecutable no debe contener datos institucionales.
- Las rutas deben poder cambiarse sin modificar código de dominio.
- La actualización del programa debe conservar `data`, `imports`, `reports`, `logs` y `backups`.
- El directorio debe inicializarse de forma idempotente.
