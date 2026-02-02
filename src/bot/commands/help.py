"""Help command handler."""

from telegram import Update
from telegram.ext import ContextTypes

from src.config import strings
from src.bot.keyboards import KeyboardBuilder


class HelpCommand:
    """Handle /help command."""

    def __init__(self):
        """Initialize help command handler."""
        self.keyboard_builder = KeyboardBuilder()

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /help command.

        Args:
            update: Telegram update object
            context: Context for the handler
        """
        reply_markup = self.keyboard_builder.build_back_to_menu()

        if update.message:
            await update.message.reply_text(
                strings.HELP_MESSAGE,
                reply_markup=reply_markup
            )
        elif update.callback_query:
            await update.callback_query.edit_message_text(
                strings.HELP_MESSAGE,
                reply_markup=reply_markup
            )

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle help button callback.

        Args:
            update: Telegram update object
            context: Context for the handler
        """
        query = update.callback_query
        await query.answer()

        reply_markup = self.keyboard_builder.build_back_to_menu()

        await query.edit_message_text(
            strings.HELP_MESSAGE,
            reply_markup=reply_markup
        )
