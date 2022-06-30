from logging import exception
import sqlite3
import queries
import helpers


def check_connection(db_name):

    conn = sqlite3.connect(db_name)

    cursor = conn.cursor()

    cursor.execute(queries.create_strikes_table)

    return conn


def create_user(db_name, args):

    conn = sqlite3.connect(db_name)

    if len(args) == 0:
        return "✋ Please enter command followed by the name to be added."
    if len(args) > 1:
        return "✋ Please enter command followed by a *single* user name."
    if len(args) == 1 and args[0].isnumeric():
        return "✋ The user name should have at least one letter."

    user = args[0]

    with conn as claw:
        cursor = claw.cursor()

        try:
            cursor.execute(queries.create_new_user, (user, 0, 0))
            return (
                f"User *{user}* created successfully.\n"
                "\nPssst! ( ¬ ‿¬)\n"
                "You can start striking him/her using:\n"
                f"_/strike {user} (nstrikes)_"
            )
        except sqlite3.IntegrityError:
            return (
                f"Whoops! Couldn't create user *{user}* 🤔\n"
                "Are you sure it doesn't already exist?\n"
                "You can see every user and their strikes using /status"
            )


def get_status(db_name, args: None):

    conn = sqlite3.connect(db_name)

    with conn as claw:
        cursor = claw.cursor()

        if len(args) == 0:

            cursor.execute(queries.get_all_status)
            all_status = cursor.fetchall()

            all_status_results = "\n".join(
                [
                    f"*{x[0].capitalize()}* has {x[1]} ⚡ and owes {x[2]} 🥐"
                    for x in all_status
                ]
            )

            return (
                f"Here's a report on everyone's current status:\n\n{all_status_results}"
            )

        if len(args) > 1:
            return "✋ Please enter command followed by a *single* user name."

        user = args[0]

        cursor.execute(queries.get_status_from_user, (user,))
        user_status = cursor.fetchall()

        user_display = user.capitalize()

        if len(user_status) == 0:
            return (
                f"Whoops! Couldn't find user *{user_display}* 🤔\n"
                "Are you sure it exists?\n"
                "You can see every user using /status, and "
                "create new users using /create\_user"
            )

        strike_count = int(user_status[0][1])
        pastries_count = int(user_status[0][2])

        strikes_status = helpers.get_strike_reaction(strike_count)
        pastries_status = helpers.get_pastries_reaction(pastries_count)

        return (
            f"Here's where *{user_display}* stands:\n\n"
            f"{strikes_status}\n\n"
            f"{pastries_status}"
            f"\n\nDo you happen to remember any recent screwups by {user_display}? "
            f"Keep in mind you can add n strikes using _/strike {user_display} n_"
            "\nψ (｀∇´) ψ"
        )


def strike_user(db_name, args: None):

    if len(args) == 0 or (len(args) > 1 and args[0].isnumeric()):
        return (
            "✋ After the _/strike_ command, tell me the name of the person we're striking first, "
            "and then optionally the number of strikes to add/substract ( ͡° ͜ʖ ͡°)"
        )

    user = args[0]
    user_display = user.capitalize()

    conn = sqlite3.connect(db_name)

    with conn as claw:
        cursor = claw.cursor()

        cursor.execute(queries.get_status_from_user, (user,))
        user_status = cursor.fetchall()

        user_display = user.capitalize()

        if len(user_status) == 0:
            return (
                f"Whoops! Couldn't find user *{user_display}* 🤔\n"
                "Are you sure it exists?\n"
                "You can see every user using /status, and "
                "create new users using /create\_user"
            )

        current_user_strikes = int(user_status[0][1])
        current_user_pastries = int(user_status[0][2])

        if len(args) == 1:
            strikes_to_add = 1
            updated_user_status = helpers.compute_new_values(
                current_user_strikes, current_user_pastries, strikes_to_add
            )
        else:
            try:
                strikes_to_add = int(args[1])
                updated_user_status = helpers.compute_new_values(
                    current_user_strikes, current_user_pastries, strikes_to_add
                )
            except ValueError:
                return (
                    f"✋ _{args[1]}_ is not a valid number of strikes. "
                    f"Please type an integer representing the number of strikes "
                    f"to add/substract from {user_display}. For example: _/strike {user_display} 1_"
                )

        cursor.execute(
            queries.update_user_status,
            (updated_user_status[0], updated_user_status[1], user),
        )

        updated_status_answer = (
            f"Striking done. Here's where *{user_display}* stands now:\n\n"
            f"{helpers.get_strike_reaction(updated_user_status[0])}\n\n"
            f"{helpers.get_pastries_reaction(updated_user_status[1])}"
        )

        if updated_user_status[1] > current_user_pastries:
            new_pastries_prelude = (
                f"🎉 Great news everyone! {user_display} now owes "
                f"{updated_user_status[1] - current_user_pastries} new pastries."
            )

            updated_status_answer = "\n\n".join(
                [new_pastries_prelude, updated_status_answer]
            )

        return updated_status_answer
