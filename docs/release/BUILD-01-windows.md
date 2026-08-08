# BUILD-01 — Construcción Windows

## Objetivo

Generar una versión ejecutable de SIAP-RTC para pruebas en equipos Windows sin instalar el entorno de desarrollo completo.

## Requisitos de construcción

- Windows 10/11 x64.
- Python 3.11, 3.12 o 3.13 dentro del rango del proyecto.
- Git.
- acceso al repositorio.

## Procedimiento

Desde PowerShell en la raíz del repositorio:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\build\build_windows.ps1
```

El script instala dependencias, instala PyInstaller y genera `dist/SIAP-RTC`.

## Separación programa/datos

El artefacto no debe contener una base institucional. La base SQLite, importaciones, reportes, logs y respaldos deben ubicarse en directorios de datos del usuario.

## Verificación mínima

1. Ejecutar el binario en un equipo limpio de desarrollo.
2. Abrir la aplicación.
3. Confirmar creación de directorios de datos.
4. Importar un fixture de prueba.
5. Reiniciar la aplicación.
6. Confirmar persistencia.
7. Generar un reporte.
8. Registrar versión y SHA-256 del artefacto.

## Nota

Este entregable genera el ejecutable preliminar. No constituye todavía el instalador institucional; ese trabajo corresponde a BUILD-02.
