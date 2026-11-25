# Workshop: GitHub Copilot para equipos de datos

Taller en español para responder preguntas reales de equipos que trabajan con
Azure DevOps, Databricks y Microsoft Fabric. Incluye una **demo guiada**, cinco
skills, instrucciones compartidas y ejercicios reproducibles con datos
ficticios. Un MCP ofrece herramientas; una skill enseña un procedimiento;
ninguno sustituye permisos, pruebas ni revisión humana.

## Empezar

1. Instala VS Code, Git, la extensión GitHub Copilot y Python 3.10+; inicia
   sesión con una cuenta habilitada para Copilot. Para Fabric instala Azure
   CLI, inicia sesión y verifica tu suscripción.
2. Clona y abre este repositorio en VS Code:

   ```powershell
   git clone https://github.com/CrisSchezMS/workshopFabricCopilot.git
   Set-Location workshopFabricCopilot
   code .
   ```

3. En Copilot Chat, modo Agent, escribe:

   ```text
   Usa la skill inicio-workshop. Quiero preparar la demo conectada y el
   guion para enseñarla. Empieza preguntándome el nombre del workspace.
   ```

4. Di el nombre del workspace cuando se pregunte. El descubrimiento es de
   solo lectura; revisa el alcance antes de aceptar acciones. Un MCP o un
   workspace visible no garantizan acceso a todos sus datos.

Alternativa reproducible sin Copilot:

```powershell
python tools\preflight.py
python -m unittest discover -s tests -v
python tools\check_names.py examples\nombres.json
python tools\impact.py examples\lineage.json demo.silver.ventas
```

`check_names.py` devuelve código 1 por los **dos nombres incorrectos
intencionados**. Preflight necesita Azure CLI y acceso a Fabric; no crea ni
enciende recursos. Se pregunta el nombre cada vez que no se pasa
`--workspace`. Las demás pruebas no necesitan nube.

## Recorrido

| Bloque | Qué se enseña | Material |
|---|---|---|
| Contexto y Azure DevOps | Clone, qué puede consultar Copilot, instrucciones comunes | [Conexiones](docs/conexiones.md), [Contexto](docs/contexto.md) |
| Skills | Nomenclatura, SCD2, documentación y revisión, impacto | [Skills](docs/skills.md), [Guion](docs/demo.md) |
| MCP | Fabric, DevOps/Wiki, Databricks/linaje y diagnóstico ADF | [Conexiones](docs/conexiones.md), [Guion](docs/demo.md) |
| Gobierno | Qué es corporativo/proyecto, distribución y evolución | [Recomendaciones](docs/contexto.md) |

El caso de linaje local es ficticio; no se presenta como un workspace real.
Las demostraciones conectadas dependen de permisos, licencias y conectores
aprobados. Consulta [preparación y validación](docs/demo.md). Los datos del
cliente, tokens, nombres internos y resultados reales nunca se publican aquí.

El estándar SCD2 `corporate_scd2` 1.0.0 ofrece un MERGE Delta para
instantáneas y se acompaña de una demo Databricks. Requiere un único escritor
garantizado externamente y revisiones adicionales antes de producción:
[contrato y límites](standards/scd2.md).

[Fuentes oficiales](docs/fuentes.md) · [MIT](LICENSE)
