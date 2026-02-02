"""Start command handler with main menu."""

from telegram import Update
from telegram.ext import ContextTypes

from src.config import strings
from src.bot.keyboards import KeyboardBuilder


class StartCommand:
    """Handle /start command and main menu."""

    def __init__(self):
        """Initialize start command handler."""
        self.keyboard_builder = KeyboardBuilder()

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /start command and show main menu.

        Args:
            update: Telegram update object
            context: Context for the handler
        """
        reply_markup = self.keyboard_builder.build_main_menu()

        await update.message.reply_text(
            strings.START_MESSAGE,
            reply_markup=reply_markup
        )

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle main menu button callback.

        Args:
            update: Telegram update object
            context: Context for the handler
        """
        query = update.callback_query
        await query.answer()

        reply_markup = self.keyboard_builder.build_main_menu()

        await query.edit_message_text(
            strings.START_MESSAGE,
            reply_markup=reply_markup
        )
