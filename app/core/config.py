from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "TenantCore"
    environment: str = "development"
    debug: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
