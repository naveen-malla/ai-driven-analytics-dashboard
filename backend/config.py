from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_PATH: str = "data/who_health.duckdb"
    ANTHROPIC_API_KEY: str
    PORT: int = 8000
    SCHEMA_REGISTRY_PATH: str = "data/schema_registry.json"
    PROVENANCE_PATH: str = "data/provenance.json"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
