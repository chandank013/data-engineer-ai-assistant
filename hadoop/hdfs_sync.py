# hadoop/hdfs_sync.py
# ─────────────────────────────────────────────────────────────────────────────
# Bulk sync local data/ folder → HDFS /data/
# Run this once after setting up Hadoop to push existing files.
#
# Usage:
#   python hadoop/hdfs_sync.py             # sync both raw and processed
#   python hadoop/hdfs_sync.py --dry-run   # show what would be synced
#   python hadoop/hdfs_sync.py --folder raw
# ─────────────────────────────────────────────────────────────────────────────

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).parent.parent))
load_dotenv()

from hadoop.hdfs_client import HdfsClient

# File types to sync (PDFs and databases stay local)
SYNC_EXTENSIONS = {".csv", ".xlsx", ".xls", ".json", ".parquet", ".txt"}


def sync_folder(client: HdfsClient, local_folder: Path, hdfs_folder: str,
                dry_run: bool = False) -> dict:
    """Sync all eligible files from local_folder to hdfs_folder."""
    if not local_folder.exists():
        return {"skipped": True, "reason": f"{local_folder} does not exist"}

    files = [f for f in local_folder.iterdir()
             if f.is_file() and f.suffix.lower() in SYNC_EXTENSIONS]

    if not files:
        print(f"  ℹ️  No eligible files in {local_folder}")
        return {"synced": 0, "failed": 0}

    synced = 0
    failed = 0

    for f in files:
        hdfs_path = f"{hdfs_folder}/{f.name}"
        if dry_run:
            print(f"  [DRY RUN] would upload: {f} → {hdfs_path}")
            synced += 1
            continue

        print(f"  ↑ {f.name} → {hdfs_path} ...", end=" ", flush=True)
        result = client.put(str(f), hdfs_path)
        if result["ok"]:
            print("✅")
            synced += 1
        else:
            print(f"❌  {result.get('error','')}")
            failed += 1

    return {"synced": synced, "failed": failed}


def main():
    parser = argparse.ArgumentParser(description="Sync local data/ → HDFS /data/")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be synced without uploading")
    parser.add_argument("--folder", choices=["raw", "processed", "both"], default="both")
    args = parser.parse_args()

    namenode = os.getenv("HDFS_NAMENODE", "")
    if not namenode:
        print("❌ HDFS_NAMENODE not set in .env — cannot sync")
        sys.exit(1)

    print(f"🐘 Connecting to HDFS at {namenode}")
    try:
        client = HdfsClient(namenode)
    except EnvironmentError as e:
        print(f"❌ {e}")
        sys.exit(1)

    project_root = Path(__file__).parent.parent
    total_synced = 0
    total_failed = 0

    folders_to_sync = []
    if args.folder in ("raw", "both"):
        folders_to_sync.append((project_root / "data" / "raw", "/data/raw"))
    if args.folder in ("processed", "both"):
        folders_to_sync.append((project_root / "data" / "processed", "/data/processed"))

    for local_dir, hdfs_dir in folders_to_sync:
        print(f"\n📂 Syncing {local_dir} → {hdfs_dir}")
        if not args.dry_run:
            client.mkdir(hdfs_dir)
        result = sync_folder(client, local_dir, hdfs_dir, dry_run=args.dry_run)
        total_synced += result.get("synced", 0)
        total_failed += result.get("failed", 0)

    print(f"\n{'─'*50}")
    if args.dry_run:
        print(f"[DRY RUN] Would upload {total_synced} file(s)")
    else:
        print(f"✅ Synced: {total_synced}  ❌ Failed: {total_failed}")
        if total_synced:
            print("   Files are now available in Spark Analytics ⚡")


if __name__ == "__main__":
    main()