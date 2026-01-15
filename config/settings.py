from typing import ClassVar
from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # --- Project Metadata ---
    PROJECT_NAME: str = "Smart HSRP"
    VERSION: str = "1.0.0"

    # --- Model Paths ---
    HELMET_MODEL_PATH: str
    PLATE_MODEL_PATH: str
    HSRP_MODEL_PATH: str

    # --- Security ---
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # --- Business Rules ---
    HELMET_CONF_THRESHOLD: float
    HSRP_CONF_THRESHOLD: float = 0.5
    OCR_CONF_THRESHOLD: float

    # --- Database & Storage ---
    DATABASE_URL: str
    STORAGE_DIR: str

    # --- API ---
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DEBUG: bool = True

    # --- Non-settings (computed / helpers) ---
    BASE_DIR: ClassVar[Path] = BASE_DIR

    DB_CONFIG: ClassVar[dict] = {}

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
    }


settings = Settings()
