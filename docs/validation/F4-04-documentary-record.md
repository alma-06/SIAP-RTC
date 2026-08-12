# F4-04 — Expediente documental institucional

## Objetivo
Separar la evidencia documental oficial de los artefactos técnicos, manteniendo una relación explícita entre ambos.

## Registro mínimo
Cada documento debe identificar:
- identificador de evidencia;
- tipo documental;
- título;
- referencia oficial, cuando exista;
- fecha;
- fuente;
- ruta del archivo;
- SHA-256;
- qué resultado, cálculo o afirmación sustenta;
- observaciones.

## Tipos posibles
El catálogo puede incluir, entre otros, oficios, acuerdos, respuestas oficiales, bases de datos, archivos RTC, disposiciones normativas, reportes y documentos metodológicos.

## Regla de separación
El expediente técnico explica cómo se procesaron los datos. El expediente documental acredita los documentos que sustentan los datos, parámetros y afirmaciones. Ninguno sustituye al otro.

## Criterio 78
Cuando un parámetro del cálculo provenga de una fuente documental externa a la pauta RTC, esa fuente deberá registrarse y vincularse expresamente con el parámetro utilizado.

## Integridad
Todo documento incorporado debe tener ruta y SHA-256. No se aceptan duplicados de `evidence_id`.

## Resultado
El registro documental alimenta el expediente maestro y la futura revisión institucional.
