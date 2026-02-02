"""Telegram bot handlers."""

import os
import shutil
from telegram import Update
from telegram.ext import ContextTypes

from src.config import strings, settings
from src.bot.keyboards import KeyboardBuilder
from src.emoji.processor import ImageProcessor
from src.emoji.sticker import StickerPackCreator


class BotHandlers:
    """Handlers for bot commands and callbacks."""

    def __init__(self):
        """Initialize bot handlers."""
        self.processor = ImageProcessor(settings.EMOJI_SIZE)
        self.keyboard_builder = KeyboardBuilder()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        await update.message.reply_text(strings.START_MESSAGE)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        await update.message.reply_text(strings.HELP_MESSAGE)

    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming photos."""
        photo = update.message.photo[-1]
        file = await photo.get_file()

        user_id = update.effective_user.id
        temp_dir = f"{settings.TEMP_DIR_PREFIX}{user_id}"
        os.makedirs(temp_dir, exist_ok=True)

        image_path = os.path.join(temp_dir, "input.jpg")
        await file.download_to_drive(image_path)

        context.user_data["image_path"] = image_path
        context.user_data["temp_dir"] = temp_dir

        width, height = self.processor.get_image_dimensions(image_path)
        suggested_grids = self.processor.suggest_grid_sizes(width, height)

        reply_markup = self.keyboard_builder.build_grid_selection(suggested_grids)

        await update.message.reply_text(
            strings.ASK_GRID_SIZE.format(width=width, height=height),
            reply_markup=reply_markup
        )

    async def handle_grid_selection(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):
        """Handle grid size selection."""
        query = update.callback_query
        await query.answer()

        grid_data = query.data.replace("grid_", "")
        cols, rows = map(int, grid_data.split("x"))

        context.user_data["grid_size"] = (cols, rows)

        reply_markup = self.keyboard_builder.build_padding_selection()

        await query.edit_message_text(
            strings.ASK_PADDING,
            reply_markup=reply_markup
        )

    async def handle_padding_selection(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):
        """Handle padding selection and process image."""
        query = update.callback_query
        await query.answer()

        padding = int(query.data.replace("padding_", ""))

        await query.edit_message_text(strings.PROCESSING)

        image_path = context.user_data.get("image_path")
        temp_dir = context.user_data.get("temp_dir")
        grid_size = context.user_data.get("grid_size")
        user_id = update.effective_user.id

        if not image_path or not grid_size:
            await query.edit_message_text(strings.ERROR_PROCESSING)
            return

        try:
            output_dir = os.path.join(temp_dir, "emojis")
            cropped_files = self.processor.crop_to_grid(
                image_path,
                output_dir,
                grid_size,
                padding
            )

            await query.edit_message_text(strings.CREATING_PACK)

            sticker_creator = StickerPackCreator(context.bot)
            emoji_link = await sticker_creator.create_emoji_pack(
                user_id=user_id,
                emoji_files=cropped_files
            )

            await query.edit_message_text(
                strings.SUCCESS.format(link=emoji_link)
            )

            shutil.rmtree(temp_dir, ignore_errors=True)

        except Exception as e:
            print(f"Error: {e}")
            await query.edit_message_text(strings.ERROR_CREATING_PACK)

            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
