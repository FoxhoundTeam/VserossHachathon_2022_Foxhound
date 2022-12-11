import re
import subprocess
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Callable
from uuid import uuid4

from app.schemes import Service


def skip_line(line: str) -> bool:
    return line.startswith("#") or not line


def make_service(line: str) -> Service:
    state, proto, port, _, _ = line.split()
    return Service(port=port, proto=proto, state=state)


@dataclass
class MasscanService:
    ip: str
    handle_progress_logs: Callable[[str, float], None] = None

    @cached_property
    def filename(self) -> str:
        folder = Path("./masscan_output/")
        folder.mkdir(exist_ok=True)
        return str(folder / f"{uuid4()}.txt")

    def _parse_result(self) -> list[Service]:
        with open(self.filename, "r") as result_file:
            services = [make_service(line) for line in result_file if not skip_line(line)]
        return services

    def start_scan(self) -> list[Service]:
        pid = subprocess.Popen(
            [
                "masscan",
                "--rate",
                "5000",
                "--ports",
                "0-65535",
                "-oL",
                self.filename,
                str(self.ip),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )
        progress = 0
        for line in iter(pid.stdout.readline, ""):
            match = re.search(r"(\d+\.\d+)%\sdone.*found=(\d+)", line)
            if match:
                try:
                    current_progress = float(match.group(1))
                    if current_progress == 100.0 and "waiting" in line:
                        progress = 0.99
                    else:
                        progress = float(match.group(1)) * 0.01
                except Exception:
                    pass
            if callable(self.handle_progress_logs):
                self.handle_progress_logs(line, progress)
        pid.stdout.close()
        pid.wait()
        return self._parse_result()
