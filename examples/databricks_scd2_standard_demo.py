# Databricks notebook source
# MAGIC %md
# MAGIC # Estándar SCD2: ejecución y controles
# MAGIC
# MAGIC Datos ficticios, tabla dedicada y un único escritor. No ejecutar en
# MAGIC producción sin las garantías y revisiones de `standards/scd2.md`.

# COMMAND ----------

from datetime import date
from pyspark.sql import Window
from pyspark.sql import functions as F
from corporate_scd2.delta import VERSION, apply_snapshot

DEMO_CATALOG = "demo_catalogo"
DEMO_SCHEMA = "copilot_data_workshop"
source_table = f"{DEMO_CATALOG}.{DEMO_SCHEMA}.clientes"
target_table = f"{DEMO_CATALOG}.{DEMO_SCHEMA}.clientes_scd2_estandar_demo"
first_date = date(2026, 1, 1)
second_date = date(2026, 2, 1)
dbutils.widgets.dropdown("resume_empty_demo_table", "false", ["false", "true"])

events = spark.table(source_table).select("customer_id", "region", "effective_date")
duplicates = events.groupBy("customer_id", "effective_date").count().filter("count > 1")
assert not duplicates.limit(1).count(), "Eventos duplicados por clave y fecha"


def snapshot_as_of(day):
    ordering = Window.partitionBy("customer_id").orderBy(F.col("effective_date").desc())
    return (events.filter(F.col("effective_date") <= F.lit(day))
            .withColumn("_rank", F.row_number().over(ordering))
            .filter(F.col("_rank") == 1)
            .select("customer_id", "region"))


def history_rows():
    return [(row.customer_id, row.region, row.valid_from, row.valid_to)
            for row in spark.table(target_table).orderBy("customer_id", "valid_from").collect()]


expected = [
    (1, None, first_date, second_date),
    (1, "norte", second_date, None),
    (2, "sur", first_date, None),
]
created = not spark.catalog.tableExists(target_table)
if created:
    spark.sql(f"""CREATE TABLE {target_table}
        (customer_id BIGINT, region STRING, valid_from DATE, valid_to DATE) USING DELTA""")
existing_rows = history_rows()
resume_empty = not existing_rows and dbutils.widgets.get("resume_empty_demo_table") == "true"
if created or resume_empty:
    assert apply_snapshot(spark, snapshot_as_of(first_date), target_table,
                          ["customer_id"], ["region"], first_date)
    assert apply_snapshot(spark, snapshot_as_of(second_date), target_table,
                          ["customer_id"], ["region"], second_date)
else:
    assert existing_rows == expected, "La tabla existente no coincide con esta demo; no se modificará"

assert history_rows() == expected
assert not apply_snapshot(spark, snapshot_as_of(second_date), target_table,
                          ["customer_id"], ["region"], second_date)

# COMMAND ----------

schema = "customer_id LONG, region STRING"
bad_inputs = [
    ([(1, "sur")], first_date, "anterior"),
    ([(1, "sur")], second_date, "misma fecha"),
    ([(1, "sur"), (1, "norte")], date(2026, 3, 1), "duplicadas"),
    ([(None, "sur")], date(2026, 3, 1), "nula"),
]
for data, day, reason in bad_inputs:
    before = history_rows()
    try:
        apply_snapshot(spark, spark.createDataFrame(data, schema), target_table,
                       ["customer_id"], ["region"], day)
    except ValueError as error:
        assert reason in str(error), f"Error inesperado: {error}"
    else:
        raise AssertionError(f"Se esperaba rechazo: {reason}")
    assert history_rows() == before, f"La validación {reason} modificó el destino"

print(f"Estándar {VERSION}: cambio, nulo, reejecución y rechazos validados.")
display(spark.table(target_table).orderBy("customer_id", "valid_from"))
