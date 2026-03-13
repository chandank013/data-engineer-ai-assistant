# hadoop/yarn_monitor.py
# ─────────────────────────────────────────────────────────────────────────────
# Check YARN ResourceManager status and list running / recent applications.
#
# Usage:
#   python hadoop/yarn_monitor.py
#   from hadoop.yarn_monitor import get_yarn_status, list_apps
# ─────────────────────────────────────────────────────────────────────────────

import os
import subprocess
import shutil
import json
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


def get_yarn_status() -> dict:
    """
    Returns YARN cluster status using `yarn node -list`.
    """
    if not shutil.which("yarn"):
        return {"ok": False, "error": "yarn command not found on PATH"}

    try:
        result = subprocess.run(
            ["yarn", "node", "-list"],
            capture_output=True, text=True, timeout=15
        )
        lines   = result.stdout.strip().splitlines()
        nodes   = [l for l in lines if "RUNNING" in l or "UNHEALTHY" in l]
        running = sum(1 for n in nodes if "RUNNING" in n)
        return {
            "ok":           True,
            "total_nodes":  len(nodes),
            "running_nodes":running,
            "output":       result.stdout[:2000],
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "YARN command timed out"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def list_apps(state: str = "ALL", limit: int = 10) -> list[dict]:
    """
    List YARN applications.
    state: ALL | RUNNING | FINISHED | FAILED | KILLED
    """
    if not shutil.which("yarn"):
        return []
    try:
        result = subprocess.run(
            ["yarn", "application", "-list", "-appStates", state],
            capture_output=True, text=True, timeout=15
        )
        apps = []
        for line in result.stdout.strip().splitlines():
            if line.startswith("application_"):
                parts = line.split()
                apps.append({
                    "app_id":   parts[0] if len(parts) > 0 else "",
                    "name":     parts[1] if len(parts) > 1 else "",
                    "state":    parts[5] if len(parts) > 5 else "",
                    "progress": parts[8] if len(parts) > 8 else "",
                })
        return apps[:limit]
    except Exception:
        return []


def kill_app(app_id: str) -> dict:
    """Kill a running YARN application."""
    if not shutil.which("yarn"):
        return {"ok": False, "error": "yarn not found"}
    try:
        result = subprocess.run(
            ["yarn", "application", "-kill", app_id],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode != 0:
            return {"ok": False, "error": result.stderr.strip()}
        return {"ok": True, "killed": app_id}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def get_rm_url() -> str:
    """Return the YARN ResourceManager web UI URL."""
    rm = os.getenv("YARN_RESOURCE_MANAGER", "localhost:8032")
    host = rm.split(":")[0]
    return f"http://{host}:8088"


if __name__ == "__main__":
    print("── YARN Status ───────────────────────────────────")
    status = get_yarn_status()
    if status["ok"]:
        print(f"✅ YARN running — {status['running_nodes']} node(s) active")
        print(f"   Web UI: {get_rm_url()}")
    else:
        print(f"❌ {status['error']}")

    print("\n── Recent Applications ───────────────────────────")
    apps = list_apps("ALL", limit=5)
    if apps:
        for app in apps:
            print(f"   {app['app_id']}  {app['state']:10}  {app['name']}")
    else:
        print("   No recent applications")