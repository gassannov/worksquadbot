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
        from src.config.logger import get_logger
        logger = get_logger()

        logger.info("Validating application settings")
        logger.debug(f"BOT_TOKEN present: {bool(cls.BOT_TOKEN)}")
        logger.debug(f"EMOJI_SIZE: {cls.EMOJI_SIZE}")
        logger.debug(f"TEMP_DIR_PREFIX: {cls.TEMP_DIR_PREFIX}")

        if not cls.BOT_TOKEN:
            logger.error("BOT_TOKEN not found in environment variables")
            raise ValueError("BOT_TOKEN not found in environment variables")

        logger.info("Settings validation successful")


settings = Settings()
