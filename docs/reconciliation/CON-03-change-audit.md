# CON-03 — Auditoría de cambios

## Objetivo
Registrar de manera explícita cualquier cambio detectado entre un registro histórico y una nueva publicación de RTC.

## Regla principal
Un cambio detectado no sobrescribe silenciosamente el histórico.

## Cada evento conserva
- identidad canónica;
- archivo nuevo;
- archivo anterior, cuando se conoce;
- fecha y hora de detección;
- campo modificado;
- valor anterior;
- valor nuevo;
- tipo de cambio;
- lote de importación, cuando existe.

## Granularidad
Se genera un evento por campo modificado. Esto permite reconstruir exactamente qué cambió.

## Integración
`CON-01` determina si la identidad existe; `CON-02` determina si cambió el contenido; `CON-03` convierte esas diferencias en eventos de auditoría.

## Próxima etapa
La auditoría deberá persistirse en una tabla histórica inmutable o append-only y vincularse al lote de importación.
