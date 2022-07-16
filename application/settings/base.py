from pydantic import BaseSettings, Field
from typing import Optional


class ApplicationSettings(BaseSettings):
    application_name: Optional[str] = 'Vehicle Manager'
    debug: Optional[bool] = False
    secret_key: str

    class Config:
        env_file = '.env'


settings = ApplicationSettings()
