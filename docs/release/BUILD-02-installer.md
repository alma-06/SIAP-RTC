# BUILD-02 — Instalador Windows

## Objetivo

Generar un instalador reproducible de SIAP-RTC para Windows mediante Inno Setup 6.

## Flujo

1. Construir `dist/SIAP-RTC` con el proceso BUILD-01.
2. Instalar Inno Setup 6 en el equipo de construcción.
3. Ejecutar `build/build_installer.ps1`.
4. Verificar el instalador en `installer/output/`.
5. Realizar instalación limpia y actualización sobre una instalación existente.

## Datos de usuario

Los datos se ubican bajo `%APPDATA%\SIAP-RTC` y se separan de los binarios:

- `data` — SQLite y configuración persistente.
- `imports` — archivos fuente procesados.
- `reports` — reportes generados.
- `logs` — registros técnicos.
- `backups` — respaldos.

## Requisito de actualización

Una actualización no debe sobrescribir ni eliminar los datos históricos del usuario.

## Verificación

La prueba mínima de instalación debe comprobar:

- acceso directo creado;
- aplicación inicia;
- directorios de datos creados;
- SQLite persiste después de reiniciar;
- importación y reporte funcionan;
- desinstalación no elimina datos sin consentimiento.
