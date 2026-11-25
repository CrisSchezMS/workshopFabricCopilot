# Nomenclatura de ejemplo

Convenciones ilustrativas para adaptar y aprobar con el cliente, no una
norma universal ni validación de objetos existentes:

- Tablas en minúsculas `snake_case`, prefijo de capa `bronze_`, `silver_` o
  `gold_`, seguido de al menos una palabra.
- Columnas y variables Python en `snake_case`; clases en `PascalCase`.
- Scripts y notebooks con nombre que describa la responsabilidad.
- No guardar credenciales ni datos personales en nombres.

El verificador solo cubre la lista de nombres de tablas de `examples/nombres.json`.
No detecta SQL dinámico, mayúsculas entrecomilladas, columnas ni convenciones
específicas de cada motor. Las excepciones necesitan revisión humana.
