from pydantic_settings import BaseSettings, SettingsConfigDict


class settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    STMP_USER: str
    STMP_PASS: str

    SECRET_KEY: str |None = None
    ALGORITHM: str |None = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int |None = None


    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_psycopg(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    

model_config = SettingsConfigDict(env_file=".env")

settings = settings()