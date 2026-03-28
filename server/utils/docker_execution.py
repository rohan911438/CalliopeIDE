import os
import shutil
import subprocess
import tempfile
import logging
import time
from typing import Dict, Any

logger = logging.getLogger(__name__)

def _docker_available() -> bool:
    """Check if Docker CLI is available on the system."""
    return shutil.which("docker") is not None

def execute_in_docker(code: str, timeout: int = 5) -> Dict[str, Any]:
    """Execute Python code inside an isolated Docker container.

    The function creates a temporary directory, writes the supplied code to a
    ``script.py`` file, and runs it using the official ``python:3.10-slim`` image.
    The container is started with strict security constraints:

    * ``--network none`` – no network access.
    * ``--memory 128m`` – limit RAM usage.
    * ``--cpus 0.5`` – limit CPU share.
    * ``--read-only`` – mount the working directory as read‑only.
    * ``-v <temp>:/app:ro`` – mount only the temporary directory as read‑only.
    * ``--rm`` – container is removed automatically.

    Args:
        code: The Python source code to execute.
        timeout: Maximum execution time in seconds.

    Returns:
        A dictionary compatible with the existing ``secure_execute`` API:
        ``{"status": ..., "output": ..., "error": ..., "execution_time": ...}``
    """
    start_time = time.perf_counter()
    if not _docker_available():
        return {
            "status": "error",
            "output": "",
            "error": "Docker is not installed or not available on this host.",
            "execution_time": 0,
        }
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            script_path = os.path.join(temp_dir, "script.py")
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(code)
            command = [
                "docker", "run", "--rm",
                "--network", "none",
                "--memory", "128m",
                "--cpus", "0.5",
                "--read-only",
                "-v", f"{temp_dir}:/app:ro",
                "-w", "/app",
                "python:3.10-slim",
                "python", "script.py",
            ]
            logger.debug("Running Docker command: %s", " ".join(command))
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            execution_time = time.perf_counter() - start_time
            return {
                "status": "success" if result.returncode == 0 else "error",
                "output": result.stdout,
                "error": result.stderr,
                "execution_time": execution_time,
            }
    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "output": "",
            "error": f"Execution time limit exceeded ({timeout}s)",
            "execution_time": timeout,
        }
    except Exception as e:
        logger.exception("Docker execution failed")
        return {
            "status": "error",
            "output": "",
            "error": str(e),
            "execution_time": 0,
        }
