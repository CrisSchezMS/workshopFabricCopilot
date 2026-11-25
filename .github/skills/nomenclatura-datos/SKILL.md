---
name: nomenclatura-datos
description: Revisa nomenclatura de tablas, columnas y código de datos y propone correcciones usando las convenciones del proyecto.
---

Lee `standards/nomenclatura.md`, identifica el alcance concreto y las
excepciones justificadas. En esta demo ejecuta `python tools/check_names.py
examples/nombres.json`: es un verificador determinista de la lista JSON, no un
analizador completo de SQL ni un control de toda la plataforma. Presenta
archivo, nombre, regla y corrección propuesta; no renombres tablas remotas
sin analizar impacto y obtener aprobación. Si no puedes comprobar un objeto,
indícalo. Las reglas corporativas son ejemplos, no políticas del cliente.
