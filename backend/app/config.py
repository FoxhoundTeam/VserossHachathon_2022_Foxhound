from typing import Any, Optional

from pydantic import AmqpDsn, BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    project_name: str = "FoxInt"

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expires_s: int = 60 * 60 * 60

    broker_server: str = "broker"
    broker_port: str = "5672"
    broker_user: str = "guest"
    broker_pass: str = "guest"
    postgres_server: str = "db"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "app"
    database_uri: Optional[PostgresDsn] = None
    broker_uri: Optional[AmqpDsn] = None

    @validator("database_uri", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("postgres_user"),
            password=values.get("postgres_password"),
            host=values.get("postgres_server"),
            path=f"/{values.get('postgres_db') or ''}",
        )

    @validator("broker_uri", pre=True)
    def assemble_broker_connection(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return AmqpDsn.build(
            scheme="amqp",
            host=values.get("broker_server"),
            user=values.get("broker_user"),
            password=values.get("broker_pass"),
            port=values.get("broker_port"),
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
