---
name: scd2-databricks
description: Diseña y revisa historificación Slowly Changing Dimension tipo 2 para Databricks, Delta y PySpark con pruebas y reglas explícitas.
---

Lee `standards/scd2.md`, `corporate_scd2/delta.py` y
`examples/databricks_scd2_standard_demo.py`. Identifica el origen, destino,
claves, atributos, tipo de entrada y fecha efectiva. Comprueba permisos,
versión y que se garantice un único escritor. Si el origen son eventos, define
y valida cómo formar cada instantánea; si falta una decisión, pregúntala.

Usa `corporate_scd2.delta.apply_snapshot` versión 1.0.0 para el contrato
compatible: instantánea con claves únicas, fechas de negocio, rechazo de
duplicados y llegadas tardías, y sin bajas por ausencia. No sustituyas la
biblioteca por un `MERGE` generado ad hoc. Si el caso requiere CDC,
retroactividad o concurrencia no controlada, detente y propone una extensión
revisada: esta versión no lo soporta.

Antes de escribir presenta destino, creación, cambios, cómputo y coste y
solicita aprobación. Nunca elimines ni sobrescribas datos para probar.
Ejecuta los controles aplicables de la demo Delta y las pruebas locales;
documenta resultados, límites y cómo se asegura el único escritor. Ni la
skill ni la mera existencia del pipeline garantizan cumplimiento.
