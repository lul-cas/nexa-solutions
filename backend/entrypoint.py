import os
import socket
import subprocess
import sys
import time


def wait_for_postgres():
    host = os.environ.get("POSTGRES_HOST", "db")
    port = int(os.environ.get("POSTGRES_PORT", "5432"))
    deadline = time.time() + 60
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=2):
                return
        except OSError:
            time.sleep(1)
    raise SystemExit("PostgreSQL indisponivel")


def main():
    wait_for_postgres()
    subprocess.check_call([sys.executable, "manage.py", "migrate", "--noinput"])
    os.execvp(
        sys.executable,
        [sys.executable, "manage.py", "runserver", "0.0.0.0:8000"],
    )


if __name__ == "__main__":
    main()
