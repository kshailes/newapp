import functools

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",extra = "ignore")
    DATABASE_URL: str
    BASE_URL: str = "https://jsonplaceholder.typicode.com/"


@functools.lru_cache
def get_settings():
    return Settings()
