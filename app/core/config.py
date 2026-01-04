from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Application
    app_name: str = "TenantCore"
    environment: str = "development"
    debug: bool = True

    # Database
    db_host: str = Field(default="localhost")
    db_port: int = Field(default=5432)
    db_name: str = Field(default="tenantcore")
    db_user: str = Field(default="tenantcore")
    db_password: str = Field(default="tenantcore")

    # Security / Auth 
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )
    class Config:
        env_file = ".env"


settings = Settings()
