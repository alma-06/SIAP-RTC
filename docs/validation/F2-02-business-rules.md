# F2-02 — Reglas de negocio definitivas

## 1. Universo
Solo se consideran registros cuya `Dependencia CAM. SEN.` corresponda a una denominación reconocida de Cámara de Senadores.

## 2. Registro válido
Para el universo analítico, el registro debe contener las diez columnas requeridas y contar, como mínimo, con `Clave`, `Orden` y `Fecha` no vacíos.

## 3. Exclusiones
Los registros de otras dependencias no forman parte del universo de Cámara de Senadores. No se eliminan silenciosamente de la evidencia: deben permanecer trazables en el origen y, cuando corresponda, generar advertencia.

## 4. Duplicidad
La clave canónica inicial se construye con `Fecha`, `Orden`, `Clave`, `Versión`, `Canal Base` y `Dependencia CAM. SEN.` normalizados. `Campaña` no forma parte de esta clave inicial porque una diferencia de campaña no debe impedir detectar un posible duplicado operativo.

## 5. Modificaciones
Una modificación se determina durante la conciliación cuando la clave de comparación permanece identificable pero uno o más campos sujetos a comparación cambian.

## 6. Campos vacíos
`Clave`, `Orden` y `Fecha` son campos críticos para el universo analítico. Su ausencia invalida el registro para el cálculo, aunque el registro debe conservarse en la evidencia de entrada.

## 7. Fechas
La fecha debe conservar su valor original y su representación normalizada. No se debe inferir una fecha inexistente a partir del nombre del archivo.

## 8. Clasificación de resultados
- **Programado:** existe en la pauta RTC publicada.
- **Calculado:** resultado derivado mediante una regla explícita sobre datos de pauta y parámetros documentados.
- **Efectivamente transmitido:** solo puede afirmarse cuando existe evidencia independiente suficiente de transmisión.

## 9. Criterio 78
Los cálculos de tiempo derivados de impactos, duración estándar y número de radiodifusoras se presentan como tiempo calculado/estimado conforme a la metodología, no como prueba de transmisión efectiva.

## 10. Trazabilidad
Toda exclusión, advertencia o transformación relevante debe poder relacionarse con el registro de origen y con el archivo fuente correspondiente.
