from typing import List
from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "postgresql+asyncpg://postgres:025847@localhost:5432/faculdade"
    DBBaseModel = declarative_base()

    JWT_SECRET: str = "Fjocp00o0W8kLUcJxolmvTUbTG2F8HW18srVOWm54KU"
    """
    import secrets
    
    token: str = secrets.token_urlsafe(32)
    print(token)
    """
    ALGORTITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True


settings: Settings = Settings()
