# Conexiones y seguridad

## Azure Repos en VS Code

1. En Azure DevOps abre **Repos > Files > Clone** y copia la URL HTTPS del
   repositorio autorizado. Necesitas acceso a la organización, proyecto y repo.
2. En VS Code usa **Git: Clone** o `git clone <url-copiada>`; abre la carpeta
   clonada y selecciona la rama adecuada. Utiliza Entra ID y Git Credential
   Manager cuando estén disponibles. No guardes PAT en la URL o el repositorio.
3. Inicia sesión en GitHub Copilot y comprueba licencia/política. Abre Chat y
   solicita las instrucciones del proyecto con rutas. La conexión Git da
   acceso al código clonado, no automáticamente a la Wiki ni a otros proyectos.
4. Si falla: comprueba la URL, organización, permisos, sesión y configuración
   de proxy/red; no pegues tokens ni datos de autenticación en el chat.

## MCP en VS Code

Abre la documentación de cada servidor y verifica disponibilidad, versión,
alcance y permisos. En VS Code, configura un servidor desde el catálogo o
`.mcp.json` con la sintaxis vigente; usa entradas de configuración
locales para URLs privadas y el flujo de inicio de sesión del servidor.
Inspecciona la lista de herramientas antes de aceptar llamadas. Los MCP
heredan los permisos de la identidad, no conceden acceso adicional y pueden
tener herramientas de escritura; pedir «solo lectura» en el prompt no es un
control de seguridad. Usa permisos RBAC y políticas del servidor.

Para el harness Copilot actual, `.mcp.json` en la raíz usa `mcpServers`;
este repositorio lo excluye de Git para evitar publicar destinos privados. La
configuración heredada `.vscode/mcp.json` usa `servers` y puede requerir
compatibilidad del editor. Revisa la [referencia vigente](https://code.visualstudio.com/docs/agents/reference/mcp-configuration).
Añadir un endpoint no equivale a autenticarlo ni a validar una llamada.

**Fabric Core MCP**: endpoint oficial
`https://api.fabric.microsoft.com/v1/mcp/core`, Streamable HTTP y autenticación
Entra. Consulta la [guía del servidor](https://learn.microsoft.com/en-us/rest/api/fabric/articles/mcp-servers/core-remote/get-started-core)
para configurar y autenticarlo. Descubre sus herramientas reales antes de
prometer operaciones. Core no es FabricIQ, ni el SQL endpoint, ni un servidor
de modelado: capacidades, licencias y permisos varían por servidor.

**Azure DevOps MCP**: el [servidor remoto oficial](https://learn.microsoft.com/en-us/azure/devops/mcp-server/remote-mcp-server)
usa `https://mcp.dev.azure.com/{organization}`; sustituye el marcador por tu
organización localmente, sin publicarla. Autentica con tu identidad y descubre
las herramientas. El servidor remoto admite `X-MCP-Readonly: true` y
`X-MCP-Toolsets: repos,wiki,wit` para limitar herramientas; conserva permisos
adecuados. Para Wiki, habilita solo los permisos necesarios. Para
mantenerla actualizada, detecta cambios mediante pipeline/PR, genera un
borrador y pide revisión antes de publicar; conectar MCP no automatiza eventos.

**Databricks**: sigue la [guía de MCP SQL](https://learn.microsoft.com/en-us/azure/databricks/agents/mcp-tools/databricks-sql)
para el endpoint de tu workspace, autenticación, warehouse y permisos.
Herramientas SQL pueden escribir: utiliza una identidad y un entorno
restringidos a lectura y revisa las herramientas expuestas. El servidor
dispone de `execute_sql_read_only`; limitar herramientas en el cliente no
sustituye los permisos del servidor. Puede haber coste
al iniciar un SQL warehouse. Un workspace existente no demuestra acceso al
data plane ni habilitación de Unity Catalog.

## Databricks: lineage

`system.access.table_lineage` recoge eventos de linaje capturados por Unity
Catalog. Con una tabla de prueba y acceso a la tabla de sistema, consulta
escrituras observadas en una ventana; reemplaza el nombre ficticio y fechas
solo en el entorno autorizado:

```sql
SELECT event_time, source_table_full_name, target_table_full_name,
       entity_type, entity_id, entity_run_id, entity_metadata.notebook_id AS notebook_id
FROM system.access.table_lineage
WHERE target_table_full_name = 'catalogo.esquema.tabla'
  AND event_date >= current_date() - INTERVAL 30 DAYS
ORDER BY event_time DESC
LIMIT 100;
```

Consulta al administrador los permisos, habilitación y cobertura de system
tables. El resultado representa **eventos registrados**, no todos los
notebooks que podrían escribir: una ejecución por job puede identificar el
notebook en `entity_metadata.notebook_id` incluso si `entity_type` es JOB;
el campo puede no estar disponible. La retención predeterminada documentada
es una ventana móvil de 395 días para system tables de linaje: confirma
políticas vigentes antes de fijar la ventana. Complementa con búsqueda de
código, jobs y metadatos de modelos/informes. No extrapoles dependencias
entre Databricks y Fabric sin evidencia. Un registro de fuente vacía, permisos
insuficientes o ausencia de eventos no prueba ausencia de impacto.

## Azure Data Factory: ejecuciones fallidas

Un MCP puede consultar ADF **si** expone la operación adecuada y la identidad
tiene acceso; descubre herramientas antes de prometerlo. Como alternativa,
usa la [API oficial de consulta de pipeline runs](https://learn.microsoft.com/en-us/rest/api/datafactory/pipeline-runs/query-by-factory)
con Entra y permisos de lectura en la factory:

```http
POST https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DataFactory/factories/{factoryName}/queryPipelineRuns?api-version=2018-06-01
Content-Type: application/json

{
  "lastUpdatedAfter": "2026-01-01T00:00:00Z",
  "lastUpdatedBefore": "2026-02-01T00:00:00Z",
  "filters": [{"operand": "Status", "operator": "Equals", "values": ["Failed"]}]
}
```

Sustituye fechas y destino por los autorizados; pagina con `continuationToken`
según API, sin imprimir tokens. Si no hay fallos, enséñalo como resultado
vacío para esa ventana, no como prueba de que jamás fallaron. El monitor de
ADF es otra forma de contrastar.

## Diagnóstico

Una respuesta vacía puede deberse a filtros, cobertura o permisos; 401 suele
requerir inicio de sesión o audiencia correcta, y 403 revisar autorización,
políticas y acceso de red. Comprueba tenant, identidad, permisos y documentación.
No registres credenciales ni datos de clientes en este repo público.
