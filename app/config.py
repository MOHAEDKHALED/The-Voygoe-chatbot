"""
config.py – All settings come from .env (never hard-coded in code)
"""

from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra="ignore")

    # ── Voyago API ────────────────────────────────────────────────────────
    VOYAGO_API_BASE: str = "http://voyagoo.runasp.net"
    HOTELS_ENDPOINT: str = "/hotels"
    ATTRACTIONS_ENDPOINT: str = "/Attractions"
    RESTAURANTS_ENDPOINT: str = "/Restaurants"
    TOURGUIDES_ENDPOINT: str = "/TourGuides"

    # ── Gemini AI ─────────────────────────────────────────────────────────
    GEMINI_API_KEY: str = ""  # Get free key: https://aistudio.google.com/apikey

    # ── CORS ──────────────────────────────────────────────────────────────
    ALLOWED_ORIGINS: List[str] = ["*"]   # change to your domain in production

    # ── Context (short-term memory) ───────────────────────────────────────
    CONTEXT_MAX_TURNS: int = 5

    # ── Data ─────────────────────────────────────────────────────────────
    DATASET_PATH: str = "data/voyago_dataset.csv"


settings = Settings()
