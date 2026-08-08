# Identidad canónica de registros RTC

## Objetivo
Definir una identidad determinista para detectar registros duplicados sin depender del orden de columnas, espacios accidentales o diferencias de mayúsculas/minúsculas.

## Campos de identidad iniciales

1. `pauta_transmision`
2. `estado`
3. `tiempo_fiscal`
4. `canal_base`
5. `orden`
6. `fecha`
7. `dependencia_cam_sen`
8. `clave`
9. `campana`
10. `version`

## Normalización
Antes de construir la identidad:

- valores nulos se convierten en cadena vacía;
- se aplica Unicode NFKC;
- se eliminan espacios al inicio y al final;
- secuencias internas de espacios se reducen a un espacio;
- texto se normaliza a mayúsculas.

## Identificador
Los campos normalizados se concatenan en orden fijo `campo=valor` separados por `|` y se obtiene SHA-256 de la representación canónica.

## Regla de deduplicación
Dos registros se consideran potencialmente duplicados cuando su identidad canónica produce el mismo hash.

## Advertencia de diseño
La identidad es una decisión de negocio y deberá validarse con archivos RTC reales durante UAT. Si se demuestra que alguno de estos campos puede variar sin representar un nuevo spot, se deberá versionar la regla y ajustar la clave antes de declarar estable el motor de deduplicación.

## Principio de seguridad
Nunca se debe eliminar silenciosamente un registro por considerarlo duplicado: el motor deberá conservar evidencia de la decisión de deduplicación para auditoría.
