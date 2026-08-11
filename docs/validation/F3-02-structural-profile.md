# F3-02 — Perfil estructural de archivos RTC

## Objetivo
Obtener una ficha técnica reproducible de cada libro RTC antes de ejecutar la lógica analítica.

## Datos por libro
- ruta/nombre;
- SHA-256;
- número de hojas.

## Datos por hoja
- nombre;
- dimensiones reportadas por Excel;
- encabezados detectados;
- columnas requeridas ausentes;
- filas de datos;
- filas completamente vacías;
- registros identificados como CAM. SEN.;
- hasta cinco muestras de fecha;
- hasta cinco muestras de Tiempo Fiscal.

## Regla
El perfil describe lo que contiene el archivo; no modifica el archivo ni decide por sí mismo que una anomalía sea un error metodológico.

## Uso
El perfil alimentará F3-03 y servirá como evidencia del diagnóstico previo a la ejecución de la RC1.

## Nota
La ejecución sobre archivos reales debe conservar el perfil junto con el paquete de evidencia del periodo correspondiente.
