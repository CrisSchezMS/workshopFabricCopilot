# Guion para enseñar la demo

## Antes de la reunión

Reserva 60–75 minutos. Comprueba VS Code, Copilot, Python y Azure CLI. Abre el
repo y revisa `docs/conexiones.md`. Para conexión real identifica un workspace
de prueba, organización de Azure DevOps, y workspace/SQL warehouse Databricks
con permisos apropiados. Comprueba herramientas MCP y licencia, sin grabar
tokens en el repo. No enciendas compute hasta que se apruebe su coste.
Si falta un servicio, enseña la alternativa local; no llames «resultado real»
a un ejemplo ficticio. No muestres correos, secretos o información de cliente
en pantalla compartida.

### 1. Inicio y workspace — 5 min

1. Abre Copilot Chat en Agent. Pide: **«Usa inicio-workshop para preparar una
   demo conectada; pregúntame el workspace antes de actuar»**.
2. Introduce el nombre del workspace de prueba. Acepta el descubrimiento de
   lectura y enseña `python tools\preflight.py`. Si una capacidad está
   suspendida, explícalo: no la activa el script. Muestra qué se pudo leer,
   qué permisos faltan y que no se ha escrito nada.
3. Si la skill no aparece, abre **Chat: Open Customizations**, verifica Skills
   y abre una sesión nueva; también puedes ejecutar el script manualmente.

### 2. DevOps y contexto común — 10 min

1. Enseña la URL de clonación de un repo Azure Repos ficticio/autorizado en
   DevOps, clónalo con Git y abre la **carpeta raíz** en VS Code
   ([pasos](conexiones.md)). Muestra `git remote -v` sin datos sensibles.
2. En este repo muestra `.github/copilot-instructions.md`, una instrucción
   por patrón `.github/instructions/python.instructions.md` y una skill.
   Pregunta: «¿Qué reglas compartidas aplican a Python y en qué archivos
   están? Cita rutas». Verifica las referencias; no garantices que Copilot
   haya leído todo el repositorio ni que siempre seleccione los mismos archivos.
3. Explica que un repo DevOps es Git como otro, pero Copilot no entra
   automáticamente a la Wiki, pipelines u otros repos; MCP y permisos son
   independientes. Para probar reproducción, abre un chat nuevo y pide las
   reglas sin volver a explicarlas. Confirma la configuración de instrucciones
   de VS Code y el alcance en el panel de personalización.

### 3. Nomenclatura y revisión — 10 min

1. Muestra `standards/nomenclatura.md` y la skill `nomenclatura-datos`.
   Pide: **«Usa nomenclatura-datos para revisar examples/nombres.json y
   muéstrame los incumplimientos y cómo corregirlos»**.
2. Comprueba en terminal `python tools\check_names.py examples\nombres.json`.
   La salida debe señalar `VentasFinal` y `silver_`; exit 1 es deliberado.
3. Pide: **«Usa revision-notebook para revisar examples/scd2_reference.py:
   documenta contratos y enumera solo problemas verificables, con líneas»**.
   Contrasta el análisis y enseña `standards/revision.md`.

### 4. Historificación SCD2 — 10 min

1. En Azure DevOps o GitHub abre el PR del estándar corporativo. Plantea:
   «Todos los proyectos deben historificar igual, sin copiar lógica distinta
   en cada notebook». Enseña la skill y el contrato que se revisan en el PR.
2. En Copilot pide: **«Usa scd2-databricks para adaptar este estándar al
   origen de clientes; explica garantías, pruebas y límites. No modifiques
   tablas»**. Contrasta la propuesta con el contrato y el código del PR.
3. En Databricks abre el notebook `copilot_data_workshop_scd2_estandar` y
   muestra la salida de una ejecución validada. En Catalog Explorer abre la
   tabla dedicada `clientes_scd2_estandar_demo` y comprueba sus tres versiones
   y dos vigentes. Contrasta el rechazo de claves nulas, duplicados, llegadas
   tardías y cambios contradictorios, y la reejecución sin cambios.
4. Explica cómo otro proyecto adoptaría una versión revisada de la biblioteca
   y skill mediante un PR, configurando su origen, claves y atributos. El
   notebook usa datos ficticios; no borra ni sobrescribe tablas. Para retomar
   explícitamente una tabla de demo vacía tras una ejecución fallida existe
   el parámetro `resume_empty_demo_table`, desactivado por defecto.

Explica que un único MERGE agrupa cierres e inserciones, pero **el único
escritor debe garantizarlo el orquestador** y el origen debe permanecer
inmutable durante validación y MERGE: esta demo no valida concurrencia, CDC,
borrados ni recuperaciones retroactivas. Los tests locales comprueban el
contrato; la validación Delta se ejecuta en Databricks, no en la CI local.
El archivo `azure-pipelines.yml` es una definición manual y todavía no activa
un pipeline ni políticas de rama; configurarlos requiere autorización.

### 5. Impacto y MCPs — 20 min

1. Pide: **«Usa impacto-datos para analizar el cambio de
   demo.silver.ventas y cita las rutas de evidencia local»**. Contrasta con
   `python tools\impact.py examples\lineage.json demo.silver.ventas`.
   Es un grafo de ejemplo, no linaje conectado.
2. Con Fabric Core MCP configurado y autenticado, pide **«Para el workspace
   indicado, enumera los items visibles de solo lectura y cita su tipo»**.
   Contrasta con el portal y preflight. El descubrimiento no crea nada.
3. Con Azure DevOps MCP conectado a una organización de prueba, pide listar
   proyectos, repos y Wikis visibles. Después pide **un borrador** de la página
   afectada por un cambio. La publicación precisa revisión/aprobación;
   una wiki no se actualiza automáticamente por conectar MCP.
4. Con Databricks SQL MCP y Unity Catalog autorizados, solicita ejecutar la
   consulta de [conexiones.md](conexiones.md#databricks-lineage) en modo
   solo lectura para una tabla de prueba. Contrasta eventos con búsqueda en
   repos y Catalog Explorer: una ejecución observada no prueba todas las
   referencias posibles. Si el servidor, warehouse o tabla no existen, muestra
   el ejemplo local e indica el bloqueo.
5. Si existe una Azure Data Factory autorizada, consulta fallos por ventana con
   una herramienta MCP que lo soporte; si no está disponible utiliza la ruta
   REST oficial descrita en `conexiones.md`. Nunca dispares un fallo real para
   la demo sin aprobación.

**Demo conectada de Databricks:** abre el notebook de prueba
`copilot_data_workshop_scd2` y muestra su ejecución y las tablas `clientes` y
`clientes_historico` dentro del esquema de demostración. Pregunta al MCP:
«Con `execute_sql_read_only`, cuenta las versiones históricas y las vigentes
en la tabla de demostración». Después pregunta por los notebooks que hayan
escrito esa tabla y verifica los eventos mediante la consulta de linaje. El
ejemplo devuelve tres versiones y dos vigentes; una consulta vacía de linaje
no confirma que no existan dependencias. El código portátil es
`examples/databricks_scd2_notebook.py`: hay que sustituir el catálogo de
ejemplo y aprobar el destino antes de ejecutarlo. Es un ejemplo acotado, no
un MERGE SCD2 de producción para cambios posteriores ni datos tardíos.

**Demo conectada de ADF:** en Monitor, filtra la factory de prueba y abre la
ejecución `demo_fallo_intencional`; su actividad `fallo_demo` falla a
propósito con código `DEMO`. Contrasta con la API de consulta por ventana y
estado descrita en conexiones. La definición genérica está en
`examples/adf_pipeline_fallo.json`; desplegarla o ejecutarla consume recursos.

### 6. Cierre — 5 min

Resume corporativo frente a proyecto con `docs/contexto.md`: estándares y
controles centrales, instrucciones y datos propios del proyecto, skills
versionadas, MCP con permisos mínimos, revisión humana y CI. Detén sesiones
de cómputo y anota quién apaga capacidades. No borres recursos sin aprobación.
Si creaste un cambio de ejemplo, revísalo y no lo apliques en producción.

## Resultado esperado

Una demo no queda validada porque un asistente diga «hecho». Muestra el
comando, fuente y salida real. Si no hay MCP autenticado, no se puede afirmar
que se haya consultado Azure DevOps o Databricks. Si el workspace está
suspendido, preflight puede listar metadatos pero no demuestra que Spark,
modelos o SQL puedan ejecutar. Documenta cada rama como **validada** o
**bloqueada** y la causa concreta.
