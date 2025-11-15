from typing import Optional

from pydantic import EmailStr, BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Система пожертвований'
    database_url: str
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
