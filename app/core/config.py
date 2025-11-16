from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Система пожертвований'
    database_url: str = 'sqlite+aiosqlite:///./test.db'
    secret: str = 'SECRET'

    class Config:
        env_file = '.env'


settings = Settings()
