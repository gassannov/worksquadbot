"""Sticker pack creation and management."""

import time
from typing import List
from telegram import Bot, InputSticker
from telegram.constants import StickerFormat


class StickerPackCreator:
    """Handles creation of custom emoji sticker packs."""

    def __init__(self, bot: Bot):
        """
        Initialize sticker pack creator.

        Args:
            bot: Telegram bot instance
        """
        self.bot = bot

    async def create_emoji_pack(
        self,
        user_id: int,
        emoji_files: List[str],
        pack_title: str = None
    ) -> str:
        """
        Create custom emoji sticker pack.

        Args:
            user_id: Telegram user ID
            emoji_files: List of paths to emoji images
            pack_title: Custom pack title

        Returns:
            URL to the created emoji pack
        """
        timestamp = int(time.time())
        pack_name = f"emoji_{user_id}_{timestamp}_by_{self.bot.username}"

        if not pack_title:
            pack_title = f"Emoji Pack {timestamp}"

        stickers = []
        for emoji_path in emoji_files:
            with open(emoji_path, "rb") as img_file:
                sticker = InputSticker(
                    sticker=img_file.read(),
                    emoji_list=["😀"],
                    format=StickerFormat.STATIC
                )
                stickers.append(sticker)

        await self.bot.create_new_sticker_set(
            user_id=user_id,
            name=pack_name,
            title=pack_title,
            stickers=stickers,
            sticker_type="custom_emoji"
        )

        return f"https://t.me/addemoji/{pack_name}"
