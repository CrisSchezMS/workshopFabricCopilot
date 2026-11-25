# Databricks notebook source
# MAGIC %md
# MAGIC # SCD2 con datos sintéticos
# MAGIC
# MAGIC Ejemplo didáctico para generar linaje observado. Construye la historia
# MAGIC a partir de versiones de origen conocidas; no es una solución productiva
# MAGIC de CDC, llegadas tardías ni concurrencia.

# COMMAND ----------

catalog = "demo_catalogo"
schema = "copilot_data_workshop"
clientes = f"`{catalog}`.`{schema}`.`clientes`"
historico = f"`{catalog}`.`{schema}`.`clientes_historico`"
spark.sql(f"""CREATE TABLE IF NOT EXISTS {clientes}
    (customer_id BIGINT, region STRING, effective_date DATE) USING DELTA""")
spark.sql(f"""CREATE TABLE IF NOT EXISTS {historico}
    (customer_id BIGINT, region STRING, valid_from DATE, valid_to DATE) USING DELTA""")

# COMMAND ----------

spark.sql(f"""
MERGE INTO {clientes} t
USING (
  SELECT 1L AS customer_id, CAST(NULL AS STRING) AS region, DATE'2026-01-01' AS effective_date
  UNION ALL SELECT 1L, 'norte', DATE'2026-02-01'
  UNION ALL SELECT 2L, 'sur', DATE'2026-01-01'
) s
ON t.customer_id = s.customer_id AND t.effective_date = s.effective_date
WHEN NOT MATCHED THEN INSERT *
""")

# COMMAND ----------

spark.sql(f"""
MERGE INTO {historico} t
USING (
  SELECT customer_id, region, effective_date AS valid_from,
         LEAD(effective_date) OVER (PARTITION BY customer_id ORDER BY effective_date) AS valid_to
  FROM {clientes}
) s
ON t.customer_id = s.customer_id AND t.valid_from = s.valid_from
WHEN NOT MATCHED THEN INSERT *
""")

# COMMAND ----------

rows = spark.sql(f"SELECT customer_id, region, valid_from, valid_to FROM {historico} ORDER BY customer_id, valid_from").collect()
assert len(rows) == 3
assert sum(row.valid_to is None for row in rows) == 2
assert rows[0].region is None and str(rows[0].valid_to) == "2026-02-01"
display(spark.sql(f"SELECT * FROM {historico} ORDER BY customer_id, valid_from"))
print("VALIDADO: 3 versiones y 2 clientes vigentes.")
