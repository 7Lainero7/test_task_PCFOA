import subprocess
import time
import sys
import os

def log(msg: str):
    print(f"[entrypoint] {msg}", flush=True)

def run(cmd: list[str], check: bool = True):
    log(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=check)

def main():
    log("Waiting for PostgreSQL...")
    time.sleep(3)

    log("Running Alembic migrations...")
    run(["alembic", "upgrade", "head"])

    log("Starting FastAPI app...")
    run([
        "uvicorn",
        "src.app.main:app",
        "--host", "0.0.0.0",
        "--port", "8000"
    ])

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        log(f"Command failed: {e}")
        sys.exit(e.returncode)
