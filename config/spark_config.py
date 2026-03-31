# config/spark_config.py
# SparkSession factory with full Hadoop/HDFS support.
# All settings are driven by environment variables so no code changes are needed
# when switching between local mode and a real Hadoop cluster.
#
# ── Quick-start ──
# Local (default):
#   SPARK_MASTER=local[*]
#
# Hadoop YARN cluster:
#   SPARK_MASTER=yarn
#   HDFS_NAMENODE=hdfs://namenode:9000
#   SPARK_DRIVER_MEMORY=4g
#   SPARK_EXECUTOR_MEMORY=4g
#   SPARK_EXECUTOR_CORES=2
#   SPARK_NUM_EXECUTORS=4
#
# Standalone cluster:
#   SPARK_MASTER=spark://master-host:7077

import os
from pyspark.sql import SparkSession

_spark: SparkSession | None = None


def get_spark_session() -> SparkSession:
    """
    Return a cached SparkSession.
    Configuration is read from environment variables so the same code works
    in local dev AND on a Hadoop/YARN cluster.
    """
    global _spark
    if _spark is not None:
        return _spark

    master            = os.getenv("SPARK_MASTER",          "local[*]")
    driver_mem        = os.getenv("SPARK_DRIVER_MEMORY",   "2g")
    executor_mem      = os.getenv("SPARK_EXECUTOR_MEMORY", "2g")
    executor_cores    = os.getenv("SPARK_EXECUTOR_CORES",  "2")
    num_executors     = os.getenv("SPARK_NUM_EXECUTORS",   "2")
    shuffle_parts     = os.getenv("SPARK_SHUFFLE_PARTITIONS", "4")
    hdfs_namenode     = os.getenv("HDFS_NAMENODE",         "")   # e.g. hdfs://namenode:9000
    yarn_rm           = os.getenv("YARN_RESOURCE_MANAGER", "")   # e.g. resourcemanager:8032
    app_name          = os.getenv("SPARK_APP_NAME",        "AIDataEngineerAssistant")

    builder = (
        SparkSession.builder
        .appName(app_name)
        .master(master)
        .config("spark.driver.memory",              driver_mem)
        .config("spark.executor.memory",            executor_mem)
        .config("spark.executor.cores",             executor_cores)
        .config("spark.sql.shuffle.partitions",     shuffle_parts)
        .config("spark.sql.repl.eagerEval.enabled", True)
        # Performance / compatibility
        .config("spark.sql.legacy.timeParserPolicy",        "LEGACY")
        .config("spark.sql.adaptive.enabled",               "true")
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
    )

    # ── YARN / HDFS cluster settings ──────────────────────────────────────────
    if master == "yarn":
        builder = builder.config("spark.submit.deployMode", "client")
        builder = builder.config("spark.executor.instances", num_executors)

    if hdfs_namenode:
        builder = builder \
            .config("spark.hadoop.fs.defaultFS", hdfs_namenode) \
            .config("spark.hadoop.dfs.client.use.datanode.hostname", "true")

    if yarn_rm:
        builder = builder.config(
            "spark.hadoop.yarn.resourcemanager.address", yarn_rm
        )

    # ── YARN JAR caching — avoids re-uploading Spark JARs on every run ─────────
    # Upload JARs once with: hdfs dfs -put $SPARK_HOME/jars/*.jar /spark-jars/
    # Then set SPARK_YARN_JARS=hdfs://localhost:9000/spark-jars/* in .env
    yarn_jars = os.getenv("SPARK_YARN_JARS", "")
    if yarn_jars:
        builder = builder.config("spark.yarn.jars", yarn_jars)

    # ── Network & task timeouts (critical for YARN cold start) ────────────────
    network_timeout = os.getenv("SPARK_NETWORK_TIMEOUT", "300s")
    builder = builder         .config("spark.network.timeout",                    network_timeout)         .config("spark.executor.heartbeatInterval",         "60s")         .config("spark.yarn.submit.waitAppCompletion",      "false")         .config("spark.yarn.am.waitTime",                   "300s")

    # ── SPARK_LOCAL_IP fix for WSL2 hostname resolution issues ───────────────
    local_ip = os.getenv("SPARK_LOCAL_IP", "")
    if local_ip:
        builder = builder.config("spark.driver.host", local_ip)

    # ── Hive metastore (optional, enable when hive-site.xml is present) ───────
    if os.getenv("SPARK_ENABLE_HIVE", "false").lower() == "true":
        builder = builder.enableHiveSupport()

    _spark = builder.getOrCreate()
    _spark.sparkContext.setLogLevel("ERROR")
    return _spark


def get_hdfs_path(relative_path: str) -> str:
    """
    Convert a relative path to an absolute HDFS path when HDFS_NAMENODE is set,
    otherwise return the local path unchanged.

    Usage:
        path = get_hdfs_path("data/raw/sales.csv")
        sdf  = spark.read.csv(path, header=True, inferSchema=True)
    """
    namenode = os.getenv("HDFS_NAMENODE", "")
    if namenode:
        clean = relative_path.lstrip("/")
        return f"{namenode.rstrip('/')}/{clean}"
    return relative_path


def reset_spark():
    """Stop and reset the cached SparkSession (useful for config changes)."""
    global _spark
    if _spark is not None:
        _spark.stop()
        _spark = None