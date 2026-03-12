# hadoop/setup_hdfs_dirs.py
# ─────────────────────────────────────────────────────────────────────────────
# One-time setup: create required HDFS directories.
# Run this once after installing Hadoop, before starting Flask.
#
# Usage:
#   python hadoop/setup_hdfs_dirs.py
# ─────────────────────────────────────────────────────────────────────────────

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))
load_dotenv()

from hadoop.hdfs_client import HdfsClient

# Directories to create on HDFS
HDFS_DIRS = [
    "/data",
    "/data/raw",
    "/data/processed",
    "/spark-jars",
    "/tmp/spark-logs",
]


def main():
    namenode = os.getenv("HDFS_NAMENODE", "")
    if not namenode:
        print("❌ HDFS_NAMENODE not set in .env")
        print("   Add: HDFS_NAMENODE=hdfs://localhost:9000")
        sys.exit(1)

    print(f"🐘 Setting up HDFS directories on {namenode}\n")

    try:
        client = HdfsClient(namenode)
    except EnvironmentError as e:
        print(f"❌ {e}")
        sys.exit(1)

    for hdfs_dir in HDFS_DIRS:
        print(f"  📁 Creating {hdfs_dir} ...", end=" ", flush=True)
        result = client.mkdir(hdfs_dir)
        if result["ok"]:
            print("✅")
        else:
            # mkdir -p doesn't fail if dir exists, so this is a real error
            print(f"⚠️  {result.get('error', '')}")

    print(f"\n✅ HDFS directory setup complete!")
    print(f"   Next step: python hadoop/upload_spark_jars.py")


if __name__ == "__main__":
    main()