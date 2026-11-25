# Diseño y ciclo de vida de skills

Usa **ambos niveles**: instrucciones generales y conocimiento del proyecto
para contexto transversal; skills específicas para tareas repetibles. Una
skill única para todas las herramientas suele ser demasiado extensa; una por
producto sin un objetivo puede duplicar documentación. Empieza por una tarea,
define entradas, flujo, herramientas, ejemplos, validación y qué no hacer.
Usa documentación de herramienta como referencia progresiva, no copies
manuales completos. El `description` de `SKILL.md` debe explicar cuándo usarla.

| Skill del taller | Cuándo | Evidencia / límite |
|---|---|---|
| `inicio-workshop` | Arrancar | Pregunta workspace, preflight, autorización |
| `nomenclatura-datos` | Validar nombres | Script local, no SQL dinámico |
| `scd2-databricks` | Historificar | Contrato y tests, no MERGE productivo listo |
| `revision-notebook` | Documentar/revisar | Hallazgos con archivo y evidencia |
| `impacto-datos` | Cambio de tabla | Grafos, código y linaje observado, sin afirmar exhaustividad |

En `.github/skills/<nombre>/SKILL.md`, define frontmatter `name` y
`description`, instrucciones concisas y referencias relativas. Revisa
descubrimiento con **Chat: Open Customizations** y una sesión nueva. La
selección automática no garantiza que una skill se cargue en todos los
clientes; para la demo pide explícitamente que la use y verifica sus pasos.
No ejecutes scripts ajenos sin revisarlos.

Para otros proyectos: calidad de datos, contratos, migración, modelado,
diagnóstico de fallos, pruebas, documentación, evaluación de cambios y
checklists de despliegue. Empieza con un conjunto pequeño, ejemplos y tests.
La salida debe indicar qué hizo, qué no pudo comprobar y cómo se valida.
