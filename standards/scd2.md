# Contrato SCD tipo 2 — estándar de demostración 1.0.0

Se recibe una instantánea completa de entidades existentes, con una clave y
un atributo `region`. Cada ejecución tiene una fecha efectiva. No se
interpretan ausencias como borrado. Una clave puede tener como máximo una
versión vigente. Se usan intervalos `[valid_from, valid_to)` y `None` como
fin abierto. Solo un cambio real de `region`, incluidos cambios con `None`,
cierra la versión vigente y crea otra.

Una instantánea no puede repetir claves ni incluir claves nulas; una fecha
anterior a la versión vigente se rechaza. Si hay un cambio en la misma fecha
que el inicio vigente se rechaza para no generar intervalos vacíos; una
repetición idéntica no cambia la historia.

## Implementación reutilizable

`corporate_scd2.delta.apply_snapshot` acepta claves y atributos configurables,
un DataFrame con esas columnas exactas, fecha `datetime.date` y una tabla
Delta existente de Unity Catalog. El destino contiene exactamente dichas
columnas, `valid_from DATE` y `valid_to DATE`. Se admiten identificadores
simples y tipos escalares; los tipos deben coincidir entre origen y destino.
Rechaza claves nulas, duplicados, tipos incompatibles, intervalos inválidos,
solapes y claves sin exactamente una versión vigente.

```python
from datetime import date
from corporate_scd2.delta import apply_snapshot

changed = apply_snapshot(
    spark, snapshot, "catalogo.esquema.destino",
    ["customer_id"], ["region"], date(2026, 2, 1)
)
```

`changed` es `False` si la instantánea no requiere modificación. El
origen debe mantenerse **inmutable desde las validaciones hasta el final del
MERGE**, ya que se evalúa varias veces y no se materializa internamente.
La tabla destino debe
haberse creado y autorizado previamente. No existe una ruta de sobrescritura
o creación implícita de la tabla.

Cada aplicación válida prepara cierres e inserciones y los realiza mediante
**un único MERGE Delta**. Para un origen de eventos es responsabilidad del
proyecto obtener primero una instantánea inequívoca; el ejemplo verifica
duplicados por clave y fecha. No interpreta ausencias como bajas.

## Condiciones antes de producción

La implementación **no impone un bloqueo**: el orquestador debe asegurar un
único escritor por tabla durante validación y MERGE. No garantiza CDC,
borrados, reprocesamiento retroactivo, ejecución concurrente ni recuperación
de snapshots cambiantes. No constituye una certificación de producción.
Antes de adoptarla, revisar con el equipo las garantías de aislamiento,
controles de concurrencia, integridad de origen, auditoría, alertas,
rendimiento y pruebas de integración propias del entorno.

Distribuye una versión fijada de la biblioteca y skill mediante un paquete o
PR de actualización. Valida en CI el contrato y ejecuta la prueba Delta en un
entorno aislado; los tests Python locales no sustituyen esa prueba. La demo
`examples/databricks_scd2_standard_demo.py` usa una tabla de prueba exclusiva,
no elimina ni sobrescribe tablas y vuelve a comprobar la reejecución.
