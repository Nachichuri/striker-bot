import sqlite3
import queries


def check_connection(db_name):

    conn = sqlite3.connect(db_name)

    cursor = conn.cursor()

    cursor.execute(queries.create_strikes_table)

    return conn


def create_user(db_name, args):

    conn = sqlite3.connect(db_name)

    if len(args) == 0:
        return "✋ Please enter command followed by the name to be added."
    elif len(args) > 1:
        return "✋ Please enter command followed by a *single* user name."

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
            return "Sarasa"
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
        pastries_count = user_status[0][2]

        if strike_count < 0:
            strikes_status = f"⚡ Strikes: *{strike_count}* (Hey! Don't think for a second this'll let you break the production environment next friday!)"

        match strike_count:
            case 0:
                strikes_status = "⚡ Strikes: *0* (For now)"
            case 1 | 2:
                strikes_status = (
                    f"⚡ Strikes: *{strike_count}* (Only {strike_count}? Are we sure?)"
                )
            case 3:
                strikes_status = "⚡ Strikes: *3* (Oooh, half way there!)"
            case 4 | 5:
                strikes_status = f"⚡ Strikes: *{strike_count}* (Better watch your step, only 1 strike left to reach the _pastries tier_!)"

        if pastries_count == 0:
            pastries_status = "🥐 Pastries: *0* (Somebody's been cautious lately...)"
        if pastries_count == 1:
            pastries_status = (
                "🥐 Pastries: *1* (Pastries eaters around the office, rejoice!)"
            )
        if pastries_count == 2:
            pastries_status = "🥐 Pastries: *2* (Hey, staking? Is that even allowed?)"
        if pastries_count >= 3:
            pastries_status = f"🥐 Pastries: *{pastries_count}* (What? {pastries_count}???? I'd start looking into some kind of personal loan by now...)"

        return (
            f"Here's where *{user_display}* stands:\n\n"
            f"{strikes_status}\n\n"
            f"{pastries_status}"
            f"\n\nDo you happen to remember any recent screwups by {user_display}? "
            f"Keep in mind you can add n strikes using _/strike {user_display} n_"
            "\nψ (｀∇´) ψ"
        )
