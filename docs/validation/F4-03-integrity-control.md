# F4-03 — Control de integridad del expediente

## Objetivo
Verificar que un paquete de evidencia sea completo y conserve exactamente los archivos que fueron registrados en su manifiesto.

## Controles
1. El manifiesto debe existir.
2. Cada archivo manifestado debe existir.
3. El SHA-256 actual debe coincidir con el registrado.
4. No deben existir archivos adicionales no registrados en el manifiesto.

## Estados
- `VALID`: no existen diferencias.
- `INVALID`: existe al menos un archivo faltante, modificado, no manifestado o falta el manifiesto.

## Códigos de incidencia
- `MANIFEST-MISSING`
- `FILE-MISSING`
- `HASH-MISMATCH`
- `FILE-UNMANIFESTED`

## Regla de liberación
Un paquete con estado `INVALID` no puede considerarse íntegro ni liberarse como expediente definitivo.

## Nota técnica
El repositorio ya dispone de `app/export/verify.py` para verificar archivos declarados en un manifiesto. Este control complementa esa capacidad al detectar también archivos no manifestados, cerrando la brecha de integridad del paquete completo.
