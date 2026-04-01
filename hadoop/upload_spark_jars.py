# hadoop/upload_spark_jars.py
# ─────────────────────────────────────────────────────────────────────────────
# One-time setup: upload all PySpark JARs to HDFS /spark-jars/
# This prevents Spark from re-uploading JARs on every YARN job (saves 60s+ per run).
#
# Usage:
#   python hadoop/upload_spark_jars.py
#   python hadoop/upload_spark_jars.py --skip-existing   # skip already uploaded JARs
# ─────────────────────────────────────────────────────────────────────────────

import os
import sys
import argparse
import subprocess
import shutil
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))
load_dotenv()


def find_spark_home() -> Optional[Path]:
    """Find PySpark JAR directory."""
    # 1. SPARK_HOME env var
    spark_home = os.getenv("SPARK_HOME", "")
    if spark_home:
        p = Path(spark_home) / "jars"
        if p.exists():
            return p

    # 2. Find via pyspark package
    try:
        import pyspark
        p = Path(pyspark.__file__).parent / "jars"
        if p.exists():
            return p
    except ImportError:
        pass

    # 3. Find spark-submit on PATH
    spark_submit = shutil.which("spark-submit")
    if spark_submit:
        p = Path(spark_submit).parent.parent / "jars"
        if p.exists():
            return p

    return None


def main():
    parser = argparse.ArgumentParser(description="Upload Spark JARs to HDFS /spark-jars/")
    parser.add_argument("--skip-existing", action="store_true",
                        help="Skip JARs already on HDFS (faster re-run)")
    args = parser.parse_args()

    namenode = os.getenv("HDFS_NAMENODE", "")
    if not namenode:
        print("❌ HDFS_NAMENODE not set in .env")
        sys.exit(1)

    if not shutil.which("hdfs"):
        print("❌ hdfs command not found — make sure Hadoop is installed and on PATH")
        sys.exit(1)

    jars_dir = find_spark_home()
    if not jars_dir:
        print("❌ Could not find PySpark jars directory")
        print("   Set SPARK_HOME in your .env or install pyspark: pip install pyspark")
        sys.exit(1)

    jar_files = list(jars_dir.glob("*.jar"))
    print(f"🔍 Found {len(jar_files)} JARs in {jars_dir}")
    print(f"🐘 Uploading to {namenode}/spark-jars/\n")

    # Create HDFS directory
    subprocess.run(["hdfs", "dfs", "-mkdir", "-p", "/spark-jars/"],
                   capture_output=True)

    if args.skip_existing:
        # Get list of existing JARs on HDFS
        result = subprocess.run(
            ["hdfs", "dfs", "-ls", "/spark-jars/"],
            capture_output=True, text=True
        )
        existing = set()
        for line in result.stdout.splitlines():
            parts = line.split()
            if parts:
                existing.add(parts[-1].split("/")[-1])
        jar_files = [j for j in jar_files if j.name not in existing]
        print(f"   Skipping {len(list(jars_dir.glob('*.jar'))) - len(jar_files)} already-uploaded JARs")
        print(f"   Uploading {len(jar_files)} new JARs\n")

    if not jar_files:
        print("✅ All JARs already on HDFS — nothing to upload")
        print(f"\n   Add to your .env:")
        print(f"   SPARK_YARN_JARS=hdfs://localhost:9000/spark-jars/*")
        return

    uploaded = 0
    failed   = 0

    for i, jar in enumerate(jar_files, 1):
        hdfs_path = f"/spark-jars/{jar.name}"
        print(f"  [{i:3}/{len(jar_files)}] {jar.name[:50]:50s}", end=" ", flush=True)
        result = subprocess.run(
            ["hdfs", "dfs", "-put", "-f", str(jar), hdfs_path],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            print("✅")
            uploaded += 1
        else:
            print(f"❌  {result.stderr.strip()[:60]}")
            failed += 1

    print(f"\n{'─'*60}")
    print(f"✅ Uploaded: {uploaded}   ❌ Failed: {failed}")
    print(f"\nAdd to your .env file:")
    print(f"  SPARK_YARN_JARS=hdfs://localhost:9000/spark-jars/*")
    print(f"\nThis will cut Spark YARN startup from ~60s to ~15s ⚡")


if __name__ == "__main__":
    main()