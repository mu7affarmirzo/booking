from decouple import config
from pydantic import PostgresDsn, BaseConfig


class DatabaseSettings(BaseConfig):
    url: PostgresDsn
    pool_size: int = 5
    max_overflow: int = 10


class AuthSettings(BaseConfig):
    secret_key: str
    algorithm: str
    token_expire_minutes: int = 30


class Settings(BaseConfig):
    project_name: str = "Booking Stadium"
    env: str = "development"
    debug: bool = False

    database: DatabaseSettings
    auth: AuthSettings

    class Config:
        env_file = ".env"

    @property
    def is_production(self):
        return self.env == "production"

    @property
    def is_testing(self):
        return self.env == config('DEBUG')


