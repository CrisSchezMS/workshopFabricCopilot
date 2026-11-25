"""SCD2 para instantáneas de claves únicas con un único escritor por tabla."""

import re
from datetime import date
from functools import reduce
from operator import or_

VERSION = "1.0.0"
IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")


def validate_config(target, keys, attributes, effective_date):
    if not isinstance(target, str) or len(target.split(".")) != 3:
        raise ValueError("El destino debe tener tres identificadores: catálogo.esquema.tabla")
    if any(not IDENTIFIER.fullmatch(part) for part in target.split(".")):
        raise ValueError("Identificador de destino no admitido")
    if not isinstance(keys, (list, tuple)) or not keys:
        raise ValueError("Se necesita al menos una clave")
    if not isinstance(attributes, (list, tuple)) or not attributes:
        raise ValueError("Se necesita al menos un atributo histórico")
    names = [*keys, *attributes]
    if any(not isinstance(name, str) or not IDENTIFIER.fullmatch(name) for name in names):
        raise ValueError("Nombre de columna no admitido")
    lowered = [name.lower() for name in names]
    if (len(set(lowered)) != len(lowered)
            or any(name in ("valid_from", "valid_to") or name.startswith("__scd2_")
                   for name in lowered)):
        raise ValueError("Columnas duplicadas o reservadas")
    if type(effective_date) is not date:
        raise ValueError("La fecha efectiva debe ser datetime.date")


def _any_row(frame):
    return bool(frame.limit(1).count())


def apply_snapshot(spark, snapshot, target, keys, attributes, effective_date):
    """Requiere origen inmutable y un único escritor durante toda la ejecución."""
    validate_config(target, keys, attributes, effective_date)
    from delta.tables import DeltaTable
    from pyspark.sql import Window
    from pyspark.sql import functions as F
    from pyspark.sql.types import (
        BooleanType, ByteType, DateType, DecimalType, DoubleType, FloatType,
        IntegerType, LongType, ShortType, StringType, TimestampType,
    )

    names = [*keys, *attributes]
    target_names = [*names, "valid_from", "valid_to"]
    if len(snapshot.columns) != len(names) or set(snapshot.columns) != set(names):
        raise ValueError("La instantánea debe contener exactamente claves y atributos")
    if len({name.lower() for name in snapshot.columns}) != len(snapshot.columns):
        raise ValueError("Columnas ambiguas en la instantánea")
    if not spark.catalog.tableExists(target):
        raise ValueError("La tabla destino no existe; no se crea automáticamente")
    history = spark.table(target)
    if len(history.columns) != len(target_names) or set(history.columns) != set(target_names):
        raise ValueError("El esquema del destino no coincide con el contrato")
    if len({name.lower() for name in history.columns}) != len(history.columns):
        raise ValueError("Columnas ambiguas en el destino")
    scalar = (StringType, BooleanType, ByteType, ShortType, IntegerType, LongType,
              FloatType, DoubleType, DecimalType, DateType, TimestampType)
    for name in names:
        if not isinstance(snapshot.schema[name].dataType, scalar):
            raise ValueError(f"Tipo de columna no admitido: {name}")
        if snapshot.schema[name].dataType != history.schema[name].dataType:
            raise ValueError(f"Tipo incompatible en origen y destino: {name}")
    if any(not isinstance(history.schema[name].dataType, DateType) for name in ("valid_from", "valid_to")):
        raise ValueError("valid_from y valid_to deben ser DATE")

    source = snapshot.select(*[F.col(f"`{name}`") for name in names])
    null_source_key = reduce(or_, (F.col(f"`{key}`").isNull() for key in keys))
    if _any_row(source.filter(null_source_key)):
        raise ValueError("La instantánea contiene una clave nula")
    duplicates = source.groupBy(*[F.col(f"`{key}`") for key in keys]).agg(
        F.count(F.lit(1)).alias("__scd2_count"))
    if _any_row(duplicates.filter(F.col("__scd2_count") > 1)):
        raise ValueError("La instantánea contiene claves duplicadas")

    invalid_key = reduce(or_, (F.col(f"`{key}`").isNull() for key in keys))
    invalid_interval = (F.col("valid_from").isNull()
                        | (F.col("valid_to").isNotNull()
                           & (F.col("valid_to") <= F.col("valid_from"))))
    if _any_row(history.filter(invalid_key | invalid_interval)):
        raise ValueError("El destino contiene claves o intervalos inválidos")
    active_counts = history.groupBy(*[F.col(f"`{key}`") for key in keys]).agg(
        F.sum(F.when(F.col("valid_to").isNull(), 1).otherwise(0)).alias("__scd2_active"))
    if _any_row(active_counts.filter(F.col("__scd2_active") != 1)):
        raise ValueError("Cada clave del destino debe tener una única versión vigente")
    window = Window.partitionBy(*[F.col(f"`{key}`") for key in keys]).orderBy("valid_from")
    ordered = history.select(
        F.col("valid_from"),
        F.row_number().over(window).alias("__scd2_order"),
        F.lag("valid_to").over(window).alias("__scd2_previous_end"),
    )
    overlap = ((F.col("__scd2_order") > 1)
               & (F.col("__scd2_previous_end").isNull()
                  | (F.col("valid_from") < F.col("__scd2_previous_end"))))
    if _any_row(ordered.filter(overlap)):
        raise ValueError("El destino contiene intervalos solapados o varias versiones vigentes")

    current = history.filter(F.col("valid_to").isNull())
    join = [F.col(f"s.`{key}`") == F.col(f"t.`{key}`") for key in keys]
    joined = source.alias("s").join(current.alias("t"), join, "left")
    exists = F.col(f"t.`{keys[0]}`").isNotNull()
    changed = reduce(or_, (~F.col(f"s.`{name}`").eqNullSafe(F.col(f"t.`{name}`"))
                             for name in attributes))
    effective = F.lit(effective_date)
    if _any_row(joined.filter(exists & (effective < F.col("t.valid_from")))):
        raise ValueError("La fecha efectiva es anterior a la versión vigente")
    if _any_row(joined.filter(exists & changed & (effective == F.col("t.valid_from")))):
        raise ValueError("Cambio contradictorio en la misma fecha")

    selected = [F.col(f"s.`{name}`").alias(name) for name in names]
    inserts = joined.filter(~exists | changed).select(*selected, F.lit(True).alias("__scd2_insert"))
    closes = joined.filter(exists & changed).select(*selected, F.lit(False).alias("__scd2_insert"))
    staged = inserts.unionByName(closes)
    if not _any_row(staged):
        return False
    comparison = " AND ".join(f"t.`{key}` = s.`{key}`" for key in keys)
    match = f"NOT s.`__scd2_insert` AND t.`valid_to` IS NULL AND {comparison}"
    values = {name: f"s.`{name}`" for name in names}
    values.update({"valid_from": f"DATE '{effective_date.isoformat()}'", "valid_to": "CAST(NULL AS DATE)"})
    (DeltaTable.forName(spark, target).alias("t")
     .merge(staged.alias("s"), match)
     .whenMatchedUpdate(set={"valid_to": f"DATE '{effective_date.isoformat()}'"})
     .whenNotMatchedInsert(condition="s.`__scd2_insert`", values=values)
     .execute())
    return True
