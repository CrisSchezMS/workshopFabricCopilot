---
name: impacto-datos
description: Analiza impacto de cambios en tablas, notebooks, vistas y modelos contrastando referencias de código con linaje observado de Fabric o Databricks.
---

Pide tabla y cambio propuesto. Comprueba fuentes disponibles: repositorios,
lineage de Fabric y Unity Catalog; no afirmes cobertura total. Distingue
dependencias estáticas, linaje observado y referencias no verificadas.
Para la demo local ejecuta `python tools/impact.py
examples/lineage.json demo.silver.ventas`. Presenta rutas y evidencia.
Para Databricks descubre herramientas MCP, permisos, catálogo y ventana; usa
lecturas autorizadas de `system.access.table_lineage` cuando esté disponible.
El historial observado solo incluye ejecuciones capturadas y no prueba todos
los notebooks que potencialmente escriben; complementa con búsqueda de código.
Revisa downstream en Fabric y acceso a los modelos/informes. Si no existe
vínculo demostrable entre plataformas, muestra un hueco, no una dependencia.
