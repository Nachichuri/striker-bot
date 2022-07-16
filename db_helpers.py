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
        return helpers.more_than_one_user_message
    if len(args) == 1 and args[0].isnumeric():
        return "✋ The user name should have at least one letter."

    user = args[0]
    user_display = user.capitalize()

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

            if len(all_status) == 0:
                return (
                    "Seems like there aren't any users yet!\n\n"
                    "You can add a new user running /create\_user _user_"
                )

            return (
                f"Here's a report on everyone's current status:\n\n{all_status_results}"
            )

        if len(args) > 1:
            return helpers.more_than_one_user_message

        user = args[0]

        cursor.execute(queries.get_status_from_user, (user,))
        user_status = cursor.fetchall()

        user_display = user.capitalize()

        if len(user_status) == 0:
            return helpers.user_not_found_message % user_display

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


def strike_user(db_name, args, pastry_treshold):

    if len(args) == 0 or (len(args) > 1 and args[0].isnumeric()):
        return (
            "✋ After the _/strike_ command, tell me the name of the person we're striking first, "
            "and then optionally the number of strikes to add/substract\n( ͡° ͜ʖ ͡°)"
        )

    user = args[0]
    user_display = user.capitalize()

    conn = sqlite3.connect(db_name)

    try:
        int(pastry_treshold)
    except ValueError:
        return (
            "✋ Whoops! Looks like I can't record the strikes since the value I've been given"
            f" for my pastries threshold is _{pastry_treshold}_, which is not a valid integer."
            "\n\nPlease report this error to the bot owner 🙃"
        )

    with conn as claw:
        cursor = claw.cursor()

        cursor.execute(queries.get_status_from_user, (user,))
        user_status = cursor.fetchall()

        if len(user_status) == 0:
            return helpers.user_not_found_message % user_display

        current_user_strikes = int(user_status[0][1])
        current_user_pastries = int(user_status[0][2])

        if len(args) == 1:
            strikes_to_add = 1
            updated_user_status = helpers.compute_new_values(
                current_user_strikes,
                current_user_pastries,
                strikes_to_add,
                pastry_treshold,
            )
        else:
            try:
                strikes_to_add = int(args[1])
                updated_user_status = helpers.compute_new_values(
                    current_user_strikes,
                    current_user_pastries,
                    strikes_to_add,
                    pastry_treshold,
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


def substract_pastry(db_name, args):

    if len(args) == 0:
        return "Please tell me who brought pastries to the office so I can decrease his/her pastries counter."

    if len(args) > 1:
        return helpers.more_than_one_user_message

    user = args[0]
    user_display = user.capitalize()

    conn = sqlite3.connect(db_name)

    with conn as claw:
        cursor = claw.cursor()

        cursor.execute(queries.get_status_from_user, (user,))
        user_status = cursor.fetchall()

        if len(user_status) == 0:
            return helpers.user_not_found_message % user_display

        current_user_strikes = user_status[0][1]
        current_user_pastries = user_status[0][2]

        if current_user_pastries == 0:
            return (
                f"Hmmm... looks like *{user_display}* didn't owe any pastries.\n\n"
                "If he/she did something good and you want to praise the effort, "
                "you can add negative strikes for the screwups to come.\n\n"
                "But pastries are *non negotiable*."
            )

        new_user_pastry_count = current_user_pastries - 1

        cursor.execute(
            queries.update_user_pastries,
            (new_user_pastry_count, user),
        )

        updated_status_answer = (
            f"Here's where *{user_display}* stands now:\n\n"
            f"{helpers.get_strike_reaction(current_user_strikes)}\n\n"
            f"{helpers.get_pastries_reaction(new_user_pastry_count)}"
        )

        if new_user_pastry_count == 0:
            updated_pastries_prelude = (
                f"Ok, *{user_display}* has settled the ancestral debt.\n"
                "He/She can walk without shame now."
            )

            return "\n\n".join(
                [
                    updated_pastries_prelude,
                    updated_status_answer,
                ]
            )

        updated_pastries_prelude = (
            f"Ok, *{user_display}* has settled the ancestral debt.\n"
            f"BUT WAIT! The good news is *{new_user_pastry_count}* pastries are still owed by him/her!"
            "\n( ͡° ͜ʖ ͡°)"
        )

        return "\n\n".join(
            [
                updated_pastries_prelude,
                updated_status_answer,
            ]
        )
