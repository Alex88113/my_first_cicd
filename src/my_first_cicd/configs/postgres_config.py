from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()

class DataBaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore',
        case_sensitive=True
    )
    PSQL_USER: str
    PSQL_PASSWORD: str
    PSQL_PORT: str
    PSQL_HOST: str
    DATABASE_PATH: str


config_db = DataBaseConfig()