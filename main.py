import os
import db_helpers as strikerdb

from helpers import validate_arguments
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update
from telegram.ext.updater import Updater

DB_NAME = f"db/{os.getenv('DB_NAME')}"
BOT_API_TOKEN = os.getenv("BOT_API_TOKEN")
DB_CONNECTION = strikerdb.check_connection(DB_NAME)
ALLOWED_GROUPS = [int(id) for id in os.getenv("ALLOWED_GROUPS").split(",")]

updater = Updater(BOT_API_TOKEN, use_context=True)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello there! My name is *Striker*, and what makes me happy is keeping tabs on "
        "the number of strikes for everyone in this group 😼\nType /rules to find out what "
        "this means and /help to see the available commands.",
        parse_mode="Markdown",
    )


def help(update: Update, context: CallbackContext):
    update.message.reply_text(
        """Available commands:
    /rules — what this is all about
    /status — see overall or user-specific status
    /strike <i>user n</i>  — add n strikes to the user
    /brought_pastries <i>user</i>  — substracts an owed pastry when the user settles a pastry debt
    /create_user <i>user</i>  — adds a new user to be striken""",
        parse_mode="HTML",
    )


def get_rules(update: Update, context: CallbackContext):
    update.message.reply_text(
        f"<i>Sup</i>, {update.message.from_user.first_name}? The rules are simple:"
        "\n\n<strong>Every time you screw something up, you get a strike ⚡</strong>\n\n"
        "Every time your strike counter reaches 5, it resets back to 0, and your pastries 🥐 counter increases by one.\n\n"
        "Having a positive pastries counter means you'll have to live with a veil of shame until you bring pastries* "
        "for the team to the office and somebody runs /brought_pastries on your username.\n\n"
        "If somebody thinks you deserve it, they can give you negative strikes, and you can have up to 5 negative strikes, "
        "but the only way to decrease your pastries counter is by bringing food to the office.\n\n"
        "* <i>pastries</i> stands for <i>edible things that can be shared with my colleagues at the office</i>, not only "
        "pastries, so you can cook your specialties too!\n\n"
        "All set? Let the game begin 👹\nType /help to see the list of available commands.",
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


def substract_pastry(update: Update, context: CallbackContext):
    args = validate_arguments(update.message.text)
    update.message.reply_text(
        strikerdb.substract_pastry(DB_NAME, args),
        parse_mode="Markdown",
    )


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        f"Sorry '{update.message.text}' is not a valid command. Try again."
    )


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        f"Sorry '{update.message.text}' is not a valid command. Try again."
    )


updater.dispatcher.add_handler(
    CommandHandler("start", start, filters=Filters.chat(ALLOWED_GROUPS))
)
updater.dispatcher.add_handler(
    CommandHandler("help", help, filters=Filters.chat(ALLOWED_GROUPS))
)
updater.dispatcher.add_handler(
    CommandHandler("rules", get_rules, filters=Filters.chat(ALLOWED_GROUPS))
)
updater.dispatcher.add_handler(
    CommandHandler("status", get_status, filters=Filters.chat(ALLOWED_GROUPS))
)
updater.dispatcher.add_handler(
    CommandHandler("create_user", create_user, filters=Filters.chat(ALLOWED_GROUPS))
)
updater.dispatcher.add_handler(
    CommandHandler("strike", strike_user, filters=Filters.chat(ALLOWED_GROUPS))
)
updater.dispatcher.add_handler(
    CommandHandler(
        "brought_pastries", substract_pastry, filters=Filters.chat(ALLOWED_GROUPS)
    )
)

updater.dispatcher.add_handler(
    MessageHandler(
        Filters.text & Filters.chat(ALLOWED_GROUPS),
        unknown,
    )
)
updater.dispatcher.add_handler(
    MessageHandler(
        Filters.command & Filters.chat(ALLOWED_GROUPS),
        unknown,
    )
)
updater.dispatcher.add_handler(
    MessageHandler(
        Filters.text & Filters.chat(ALLOWED_GROUPS),
        unknown_text,
    )
)


updater.start_polling()
