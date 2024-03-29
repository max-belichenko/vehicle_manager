from enum import Enum
from pydantic import BaseSettings
from typing import Optional


class EnvironmentEnum(str, Enum):
    development = 'development'
    production = 'production'


class ApplicationSettings(BaseSettings):
    application_name: Optional[str] = 'Vehicle Manager'
    debug: Optional[bool] = False
    secret_key: str
    allowed_hosts: list[str]
    environment: Optional[EnvironmentEnum] = EnvironmentEnum.development

    class Config:
        env_file = '.env'


settings = ApplicationSettings()
