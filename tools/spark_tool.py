# tools/spark_tool.py
# Spark analytics helpers used by /api/spark and /api/stats endpoints.

from __future__ import annotations
from pathlib import Path
import pandas as pd


def load_to_spark(spark, filepath: Path):
    """Load CSV or XLSX into Spark DataFrame; register as 'dataset' temp view."""
    if filepath.suffix == ".csv":
        sdf = (spark.read
               .option("header", "true")
               .option("inferSchema", "true")
               .csv(str(filepath)))
    else:
        pdf = pd.read_excel(filepath)
        sdf = spark.createDataFrame(pdf)
    sdf.createOrReplaceTempView("dataset")
    return sdf


def get_schema_string(sdf) -> str:
    return "\n".join(f"  {f.name}: {f.dataType}" for f in sdf.schema.fields)


def run_spark_sql(spark, sql: str, limit: int = 100) -> pd.DataFrame:
    return spark.sql(sql).limit(limit).toPandas()


def detect_anomalies(spark, filepath: Path) -> dict:
    """Z-score anomaly detection over numeric columns."""
    from pyspark.sql.functions import col, mean, stddev
    from pyspark.sql.functions import abs as spark_abs

    sdf = load_to_spark(spark, filepath)
    numeric_types = {"IntegerType", "LongType", "DoubleType", "FloatType", "DecimalType"}
    numeric_cols = [f.name for f in sdf.schema.fields if str(f.dataType) in numeric_types]

    anomalies = {}
    for c in numeric_cols:
        row = sdf.select(mean(col(c)).alias("m"), stddev(col(c)).alias("s")).first()
        if row["s"] and row["s"] > 0:
            count = sdf.filter(spark_abs((col(c) - row["m"]) / row["s"]) > 3).count()
            if count > 0:
                anomalies[c] = {"outlier_count": count, "mean": float(row["m"]), "std": float(row["s"])}
    return anomalies