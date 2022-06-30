import os
import db_helpers as strikerdb

from helpers import validate_arguments
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update
from telegram.ext.updater import Updater

DB_NAME = os.getenv("DB_NAME")
BOT_API_TOKEN = os.getenv("BOT_API_TOKEN")
DB_CONNECTION = strikerdb.check_connection(DB_NAME)

updater = Updater(BOT_API_TOKEN, use_context=True)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello there! I am Striker, and what makes me happy is keeping tabs on "
        "the number of strikes for everyone in this group 😼 Feel free to enter "
        " /help to see the available commands."
    )


def help(update: Update, context: CallbackContext):
    update.message.reply_text(
        """Available commands:
    /status — see overall or user-specific status
    /strike <i>user n</i>  — add n strikes to the user
    /create_user <i>user</i>  — adds a new user to be striken""",
        parse_mode="HTML",
    )


def get_status(update: Update, context: CallbackContext):
    args = validate_arguments(update.message.text)

    update.message.reply_text(
        strikerdb.get_status(DB_NAME, args), parse_mode="Markdown"
    )


def create_user(update: Update, context: CallbackContext):
    args = validate_arguments(update.message.text)
    update.message.reply_text(
        strikerdb.create_user(DB_NAME, args),
        parse_mode="Markdown",
    )


def strike_user(update: Update, context: CallbackContext):
    args = validate_arguments(update.message.text)
    update.message.reply_text(
        strikerdb.strike_user(DB_NAME, args),
        parse_mode="Markdown",
    )


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text("Sorry '%s' is not a valid command" % update.message.text)


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text
    )


updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("help", help))
updater.dispatcher.add_handler(CommandHandler("status", get_status))
updater.dispatcher.add_handler(CommandHandler("create_user", create_user))
updater.dispatcher.add_handler(CommandHandler("strike", strike_user))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(
    MessageHandler(Filters.command, unknown)
)  # Filters out unknown commands

# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()
