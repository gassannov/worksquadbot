"""Application settings and configuration."""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application configuration settings."""

    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    EMOJI_SIZE: int = int(os.getenv("EMOJI_SIZE", "100"))
    TEMP_DIR_PREFIX: str = "temp_"

    @classmethod
    def validate(cls):
        """Validate required settings."""
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN not found in environment variables")


settings = Settings()
