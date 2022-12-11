import re
import subprocess
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Callable
from uuid import uuid4

import nmap3

from app.enum import PortStatus, Protocol
from app.schemes import Service


def get_proto(proto: str) -> Protocol:
    try:
        return Protocol(proto)
    except ValueError:
        return Protocol.tcp


def get_status(status: str) -> PortStatus:
    try:
        return PortStatus(status)
    except ValueError:
        return PortStatus.open


@dataclass
class NmapService:
    ip: str
    ports: str
    handle_progress_logs: Callable[[str, float], None] = None

    @cached_property
    def filename(self) -> str:
        folder = Path("./nmap_output/")
        folder.mkdir(exist_ok=True)
        return str(folder / f"{uuid4()}.xml")

    def _parse_result(self) -> list[Service]:
        parser = nmap3.NmapCommandParser(None)
        services = []
        with open(self.filename) as xml_output:
            parsed_output = nmap3.Nmap().get_xml_et(xml_output.read())
            scan_result = parser.filter_top_ports(parsed_output)
            for entry in scan_result.values():
                for port_info in entry.get("ports", []):
                    service_name = None
                    service_product = None
                    service_version = None
                    if "service" in port_info:
                        service_name = port_info["service"]["name"]
                        service_product = port_info["service"].get("product", None)
                        service_version = port_info["service"].get("version", None)

                    services.append(
                        Service(
                            port=port_info["portid"],
                            proto=get_proto(port_info["protocol"]),
                            name=service_name,
                            status=get_status(port_info["state"]),
                            product=service_product,
                            version=service_version,
                        )
                    )
        return services

    def start_scan(self) -> list[Service]:
        pid = subprocess.Popen(
            [
                "nmap",
                "-v2",
                "-p",
                self.ports,
                "-sT",
                "-T4",
                "-sV",
                "--version-trace",
                "-Pn",
                "--stats-every",
                "10s",
                "-oA",
                self.filename,
                str(self.ip),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )
        progress = 0
        for line in iter(pid.stdout.readline, ""):
            m = re.search(r"About (.+)% done", line)
            if m:
                try:
                    self.scan.progress = float(m.group(1)) * 0.01 / 2
                except Exception:
                    pass
            if callable(self.handle_progress_logs):
                self.handle_progress_logs(line, progress)
        pid.stdout.close()

        return self._parse_result()
