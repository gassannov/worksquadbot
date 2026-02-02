"""Telegram bot for creating emoji packs from images."""

import os
import asyncio
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputSticker, Bot
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from telegram.constants import StickerFormat
from PIL import Image
import strings
from image_processor import crop_image_to_emojis, suggest_grid_size


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    await update.message.reply_text(strings.START_MESSAGE)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    await update.message.reply_text(strings.HELP_MESSAGE)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming photos."""
    photo = update.message.photo[-1]
    file = await photo.get_file()

    user_id = update.effective_user.id
    temp_dir = f"temp_{user_id}"
    os.makedirs(temp_dir, exist_ok=True)

    image_path = os.path.join(temp_dir, "input.jpg")
    await file.download_to_drive(image_path)

    context.user_data["image_path"] = image_path
    context.user_data["temp_dir"] = temp_dir

    img = Image.open(image_path)
    width, height = img.size
    img.close()

    suggested_grids = suggest_grid_size(width, height)

    keyboard = []
    for cols, rows in suggested_grids:
        text = f"{cols}x{rows} ({cols * rows} эмодзи)"
        callback_data = f"grid_{cols}x{rows}"
        keyboard.append([InlineKeyboardButton(text, callback_data=callback_data)])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        strings.ASK_GRID_SIZE.format(width=width, height=height),
        reply_markup=reply_markup
    )


async def handle_grid_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle grid size selection."""
    query = update.callback_query
    await query.answer()

    grid_data = query.data.replace("grid_", "")
    cols, rows = map(int, grid_data.split("x"))

    context.user_data["grid_size"] = (cols, rows)

    keyboard = [
        [InlineKeyboardButton(strings.PADDING_OPTIONS["1"], callback_data="padding_1")],
        [InlineKeyboardButton(strings.PADDING_OPTIONS["2"], callback_data="padding_2")],
        [InlineKeyboardButton(strings.PADDING_OPTIONS["3"], callback_data="padding_3")],
        [InlineKeyboardButton(strings.PADDING_OPTIONS["4"], callback_data="padding_4")],
        [InlineKeyboardButton(strings.PADDING_OPTIONS["5"], callback_data="padding_5")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        strings.ASK_PADDING,
        reply_markup=reply_markup
    )


async def handle_padding_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        cropped_files = crop_image_to_emojis(
            image_path,
            output_dir,
            grid_size,
            padding
        )

        await query.edit_message_text(strings.CREATING_PACK)

        pack_name = f"emoji_{user_id}_{int(time.time())}_by_{context.bot.username}"
        pack_title = f"Emoji Pack {int(time.time())}"

        stickers = []
        for emoji_path in cropped_files:
            with open(emoji_path, "rb") as img_file:
                sticker = InputSticker(
                    sticker=img_file.read(),
                    emoji_list=["😀"],
                    format=StickerFormat.STATIC
                )
                stickers.append(sticker)

        await context.bot.create_new_sticker_set(
            user_id=user_id,
            name=pack_name,
            title=pack_title,
            stickers=stickers,
            sticker_type="custom_emoji"
        )

        emoji_link = f"https://t.me/addemoji/{pack_name}"

        await query.edit_message_text(
            strings.SUCCESS.format(link=emoji_link)
        )

        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)

    except Exception as e:
        print(f"Error: {e}")
        await query.edit_message_text(strings.ERROR_CREATING_PACK)


async def main():
    """Start the bot."""
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN not found in environment variables")

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(CallbackQueryHandler(handle_grid_selection, pattern="^grid_"))
    application.add_handler(CallbackQueryHandler(handle_padding_selection, pattern="^padding_"))

    await application.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
