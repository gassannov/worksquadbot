"""Main entry point for the emoji cropper bot."""

import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

from src.config.settings import settings
from src.bot.handlers import BotHandlers


async def main():
    """Start the bot."""
    settings.validate()

    application = Application.builder().token(settings.BOT_TOKEN).build()

    handlers = BotHandlers()

    application.add_handler(CommandHandler("start", handlers.start))
    application.add_handler(CommandHandler("help", handlers.help_command))
    application.add_handler(CommandHandler("emoji_cropper", handlers.emoji_cropper))
    application.add_handler(MessageHandler(filters.PHOTO, handlers.handle_photo))
    application.add_handler(
        CallbackQueryHandler(handlers.handle_command_callback, pattern="^cmd_")
    )
    application.add_handler(
        CallbackQueryHandler(handlers.handle_grid_selection, pattern="^grid_")
    )
    application.add_handler(
        CallbackQueryHandler(handlers.handle_padding_selection, pattern="^padding_")
    )

    await application.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
