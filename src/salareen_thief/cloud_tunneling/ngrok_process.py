"""Safe ngrok subprocess operations with no credential argument."""

import subprocess
from dataclasses import dataclass


@dataclass(slots=True)
class NgrokProcess:
    process: subprocess.Popen[bytes]

    def running(self) -> bool:
        return self.process.poll() is None

    def terminate(self) -> None:
        if self.running():
            self.process.terminate()

    def wait(self, timeout: float) -> None:
        self.process.wait(timeout=timeout)

    def kill(self) -> None:
        if self.running():
            self.process.kill()


def start_ngrok(port: int, public_url: str) -> NgrokProcess:
    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    process = subprocess.Popen(
        ["ngrok", "http", str(port), "--url", public_url],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=creationflags,
    )
    return NgrokProcess(process)


def command_ok(*arguments: str) -> bool:
    completed = subprocess.run(
        ["ngrok", *arguments],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=10,
        check=False,
    )
    return completed.returncode == 0
