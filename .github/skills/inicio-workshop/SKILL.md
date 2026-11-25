---
name: inicio-workshop
description: Inicia el taller conectado de Copilot, Fabric, Azure DevOps y Databricks; pregunta primero por el workspace y prepara el descubrimiento y la demo.
---

1. Antes de operaciones o preguntas adicionales, solicita el nombre exacto del
   workspace Fabric si no se ha proporcionado en esta conversación.
2. Lee README.md, docs/demo.md y docs/conexiones.md. Descubre qué herramientas
   y skills están disponibles. No inventes resultados ni instalaciones.
3. Con autorización de lectura, ejecuta `python tools/preflight.py` e indica
   el nombre. Si falta `az`, identidad o acceso, explica el bloqueo. Un
   workspace sin resultados no demuestra inexistencia. No cambies capacidad.
4. Presenta lo hallado y elige con la persona los módulos conectados. Antes
   de escrituras solicita aprobación concreta. Usa alternativas locales si
   no hay acceso. El taller tiene datos ficticios; no uses producción.
5. Sigue docs/demo.md. Diferencia lo que es un ejemplo de lo que se ejecutó.
