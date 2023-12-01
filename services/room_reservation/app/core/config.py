from pydantic import BaseSettings, Field


class Settings(BaseException):
    app_author: str = 'Бронирование комнат'
    db_url: str = Field(..., env='DATABASE_URL')


settings = Settings()