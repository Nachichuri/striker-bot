import os
import db_helpers as strikerdb

from helpers import validate_username
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update
from telegram.ext.updater import Updater

DB_NAME = os.getenv("DB_NAME")
BOT_API_TOKEN = os.getenv("BOT_API_TOKEN")
DB_CONNECTION = strikerdb.get_connection(DB_NAME)

updater = Updater(BOT_API_TOKEN, use_context=True)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello there! I am Striker, and what makes me happy is keeping tabs on "
        "the number of strikes of everyone in this chat. Please write /help to "
        "see the commands available."
    )


def help(update: Update, context: CallbackContext):
    update.message.reply_text(
        """Available Commands :-
    /status - see overall or user-specific status
    /create_user - adds a new user to be striken"""
    )


def get_strikes(update: Update, context: CallbackContext):
    update.message.reply_text("Getting strikes...")
    
    user = validate_username(update.message.text)
    
    result = strikerdb.get_status(DB_NAME, user)
    update.message.reply_text(result, parse_mode="Markdown")


def create_user(update: Update, context: CallbackContext):
    if update.message.text == "/create_user":
        update.message.reply_text("What?")
    else:
        update.message.reply_text("Creating user...")
        user = validate_username(update.message.text)
        strikerdb.create_user(DB_NAME, user)
        update.message.reply_text(
            f"User *{user}* created successfully.\n"
            f"You can start striking him/her using _/strike {user} (nstrikes)_",
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
updater.dispatcher.add_handler(CommandHandler("status", get_strikes))
updater.dispatcher.add_handler(CommandHandler("create_user", create_user))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(
    MessageHandler(Filters.command, unknown)
)  # Filters out unknown commands

# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()
