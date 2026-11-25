# Contexto, normas y DevOps

## ¿Es correcto usar Azure DevOps Repos?

Sí. Copilot en VS Code trabaja con los archivos del workspace abierto,
independientemente de que Git se aloje en Azure Repos o GitHub. Clonar un repo
no integra automáticamente Copilot con sus work items, builds o Wiki. Git y
MCP tienen autenticación y permisos propios. Una organización GitHub Copilot
puede controlar licencias, políticas y exclusiones aunque el código esté en
Azure Repos; comprobar la política vigente.

El contexto depende del cliente, versión, modelo, instrucciones disponibles,
archivos abiertos o adjuntos, búsqueda/indexación, límites y herramientas.
El agente puede buscar archivos accesibles; no asumas que lee **todo** el repo,
que ve ramas/remotos no descargados, ni que cada chat recoge documentos lejanos.
Datos fuera del workspace o de la sesión necesitan adjuntarse o conectarse
con una herramienta autorizada. Exclusiones y permisos pueden limitar acceso.
Usa «cita archivo y línea» y contrasta en lugar de confiar en una promesa.

## ¿Cómo compartimos contexto?

| Nivel | Qué guardar | Distribución |
|---|---|---|
| Corporativo | Seguridad, clasificación, nomenclatura consensuada, arquitectura de referencia y skills genéricas | Repo de estándares versionado; plantillas aprobadas, paquete/plugin o copia sincronizada con versión |
| Proyecto | Objetivos, comandos, contrato de datos, decisiones y restricciones locales | `.github/copilot-instructions.md`, README y archivos `*.instructions.md` por patrón |
| Tarea | Pregunta concreta, archivos o datos autorizados y criterios | Prompt reutilizable o contexto añadido a ese chat |
| Herramientas | Capacidades externas, credenciales y permisos | MCP configurado y aprobado; secretos en gestor seguro, no en Git |

Una biblioteca central de estándares **sí tiene sentido**, pero Copilot no
la consulta automáticamente por existir o por enlazar una URL. Distribuye una
versión explícita a cada proyecto (por ejemplo, plantilla o copia mediante PR),
revisa conflictos con normas locales y prueba descubrimiento en VS Code. El
submódulo necesita checkout/actualización y una ubicación soportada para
instrucciones/skills: no presupongas carga automática. Un MCP o documento
corporativo son otra opción con autorización y alcance explícitos.

Promueve una versión con changelog, revisión, tests y responsables. Cada repo
recibe PR de actualización y valida antes de adoptar. Mantén pocas reglas
concretas, rutas/ejemplos, criterios comprobables, fuentes y fecha; evita
documentos enormes, información confidencial y contradicciones. Combina
instrucciones automáticas con lint, CI y políticas de rama: las instrucciones
son contexto, no un motor de cumplimiento.

## Evolución y agentes

Un agente especializado combina instrucciones, skills, contexto y herramientas
con límites de permisos y revisión. Hoy puede acelerar desarrollo, documentación
y análisis de impacto; no es responsable autónomo de seguridad o producción.
Como evolución, prueba agentes por tarea con fuentes verificables, trazas,
evaluaciones, aprobaciones y protección frente a instrucciones maliciosas
en datos externos. No prometas futuras funciones o disponibilidad de preview.
