# hadoop/hdfs_client.py
# ─────────────────────────────────────────────────────────────────────────────
# Low-level HDFS operations using the `hdfs` CLI command.
# All functions read HDFS_NAMENODE from environment / .env automatically.
#
# Usage:
#   from hadoop.hdfs_client import HdfsClient
#   client = HdfsClient()
#   client.put("data/raw/sales.csv", "/data/raw/sales.csv")
#   client.ls("/data/raw/")
#   client.rm("/data/raw/old_file.csv")
# ─────────────────────────────────────────────────────────────────────────────

import os
import subprocess
import shutil
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class HdfsClient:
    """
    Wrapper around the `hdfs dfs` CLI.
    Requires Hadoop to be installed and HDFS_NAMENODE set in .env.
    """

    def __init__(self, namenode: Optional[str] = None):
        self.namenode = (namenode or os.getenv("HDFS_NAMENODE", "")).rstrip("/")
        if not self.namenode:
            raise EnvironmentError(
                "HDFS_NAMENODE not set in .env\n"
                "Add:  HDFS_NAMENODE=hdfs://localhost:9000"
            )
        if not shutil.which("hdfs"):
            raise EnvironmentError(
                "hdfs command not found on PATH.\n"
                "Make sure Hadoop is installed and HADOOP_HOME/bin is on PATH."
            )

    # ── Internal helper ───────────────────────────────────────────────────────
    def _run(self, args: list[str], timeout: int = 60) -> subprocess.CompletedProcess:
        result = subprocess.run(
            ["hdfs", "dfs"] + args,
            capture_output=True, text=True, timeout=timeout
        )
        return result

    # ── Public API ────────────────────────────────────────────────────────────

    def put(self, local_path: str, hdfs_path: str, overwrite: bool = True) -> dict:
        """Upload a local file to HDFS."""
        local_path = str(local_path)
        if not Path(local_path).exists():
            return {"ok": False, "error": f"Local file not found: {local_path}"}

        # Ensure parent directory exists
        parent = "/".join(hdfs_path.rstrip("/").split("/")[:-1])
        if parent:
            self._run(["-mkdir", "-p", parent])

        flags = ["-put", "-f", local_path, hdfs_path] if overwrite else ["-put", local_path, hdfs_path]
        result = self._run(flags, timeout=120)

        if result.returncode != 0:
            return {"ok": False, "error": result.stderr.strip()}
        return {"ok": True, "hdfs_path": hdfs_path, "local_path": local_path}

    def get(self, hdfs_path: str, local_path: str) -> dict:
        """Download a file from HDFS to local disk."""
        result = self._run(["-get", hdfs_path, local_path], timeout=120)
        if result.returncode != 0:
            return {"ok": False, "error": result.stderr.strip()}
        return {"ok": True, "local_path": local_path}

    def rm(self, hdfs_path: str, skip_trash: bool = True) -> dict:
        """Delete a file from HDFS."""
        # Safety: only allow deleting inside /data/ or /spark-jars/
        if not (hdfs_path.startswith("/data/") or hdfs_path.startswith("/spark-jars/")):
            return {"ok": False, "error": f"Refusing to delete outside /data/ or /spark-jars/: {hdfs_path}"}

        flags = ["-rm", "-skipTrash", hdfs_path] if skip_trash else ["-rm", hdfs_path]
        result = self._run(flags, timeout=30)
        if result.returncode != 0:
            return {"ok": False, "error": result.stderr.strip()}
        return {"ok": True, "deleted": hdfs_path}

    def mkdir(self, hdfs_path: str) -> dict:
        """Create a directory (and parents) on HDFS."""
        result = self._run(["-mkdir", "-p", hdfs_path])
        if result.returncode != 0:
            return {"ok": False, "error": result.stderr.strip()}
        return {"ok": True, "path": hdfs_path}

    def ls(self, hdfs_path: str = "/data/", recursive: bool = True) -> list[dict]:
        """List files in an HDFS directory. Returns list of file dicts."""
        flag = "-ls -R" if recursive else "-ls"
        result = self._run(flag.split() + [hdfs_path], timeout=15)
        if result.returncode != 0:
            return []

        files = []
        for line in result.stdout.strip().splitlines():
            parts = line.split()
            if len(parts) < 8:
                continue
            permissions, _, owner, group, size, date, time_, path = parts[:8]
            files.append({
                "permissions": permissions,
                "owner":       owner,
                "size":        size,
                "modified":    f"{date} {time_}",
                "path":        path,
                "name":        path.split("/")[-1],
            })
        return files

    def exists(self, hdfs_path: str) -> bool:
        """Check if a path exists on HDFS."""
        result = self._run(["-test", "-e", hdfs_path])
        return result.returncode == 0

    def count_files(self, hdfs_path: str = "/data/") -> int:
        """Count files in an HDFS directory."""
        return sum(1 for f in self.ls(hdfs_path) if not f["permissions"].startswith("d"))

    def cat(self, hdfs_path: str, max_bytes: int = 4096) -> str:
        """Read file content from HDFS (first max_bytes bytes)."""
        result = self._run(["-cat", hdfs_path], timeout=15)
        if result.returncode != 0:
            return ""
        return result.stdout[:max_bytes]


# ── Convenience functions (used by app.py) ───────────────────────────────────

def upload_to_hdfs(local_path: str, hdfs_path: str) -> dict:
    """
    Push a local file to HDFS. Silently skips if HDFS_NAMENODE not set.
    Used by app.py on every file upload.
    """
    namenode = os.getenv("HDFS_NAMENODE", "")
    if not namenode:
        return {"ok": False, "skipped": True, "reason": "HDFS_NAMENODE not set"}
    try:
        client = HdfsClient(namenode)
        return client.put(local_path, hdfs_path)
    except EnvironmentError as e:
        return {"ok": False, "error": str(e)}
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "HDFS upload timed out after 120s"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def get_hdfs_or_local(local_path: str) -> str:
    """
    Return HDFS path if HDFS_NAMENODE configured, else return local path.
    Used by _load_spark() in app.py to decide where to read data from.
    """
    namenode = os.getenv("HDFS_NAMENODE", "").rstrip("/")
    if not namenode:
        return str(local_path)
    # Convert  data/raw/sales.csv  →  hdfs://localhost:9000/data/raw/sales.csv
    relative = str(local_path).lstrip("/")
    return f"{namenode}/{relative}"


if __name__ == "__main__":
    # Quick smoke test
    try:
        client = HdfsClient()
        files = client.ls("/data/")
        print(f"✅ HDFS connected — {len(files)} items in /data/")
        for f in files[:5]:
            print(f"   {f['permissions']}  {f['size']:>10}  {f['path']}")
    except EnvironmentError as e:
        print(f"❌ {e}")