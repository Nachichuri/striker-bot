# General repeated messages, isolated here to prevent cluttering in the main functions.
user_not_found_message = (
    "Whoops! Couldn't find user *%s* 🤔\n"
    "Are you sure it exists?\n"
    "You can see every user using /status, and create new users using /create\_user"
)
more_than_one_user_message = (
    "✋ Please enter command followed only by a *single* user name."
)


def validate_arguments(message):
    """Returns a lowercase list of all the words inputted in the message by the user after the command.

    Args:
        message (string): message sent by the user.

    Returns:
        list: list of words the user inputted.
    """

    if len(message.split()) == 1:
        return []

    arguments = [x.lower() for x in message.split()[1:]]

    return arguments


def get_strike_reaction(strike_count, pastry_threshold):
    """Replies with a custom message which changes with the amount of strikes.

    Args:
        strike_count (int): number of strikes.

    Returns:
        string: message to be returned by the bot.
    """
    if strike_count < 0:
        return f"⚡ Strikes: *{strike_count}* (Hey! Don't think for a second this'll let you break the production environment next friday!)"

    if strike_count == 0:
        return "⚡ Strikes: *0* (For now)"
    if strike_count == 1:
        return f"⚡ Strikes: *{strike_count}* (Only {strike_count}? Are we sure?)"
    if strike_count >= 2:
        return (
            f"⚡ Strikes: *{strike_count}* (Better watch your step, only {int(pastry_threshold) - strike_count} "
            f"{'strike' if int(pastry_threshold) - strike_count == 1 else 'strikes'} left to reach the _pastries tier_!)"
        )


def get_pastries_reaction(pastries_count):
    """Replies with a custom message which changes with the amount of pastries.

    Args:
        pastries_count (int): number of pastries owed.

    Returns:
        string: message to be returned by the bot.
    """
    if pastries_count == 0:
        return "🥐 Pastries: *0* (Somebody's been cautious lately...)"
    if pastries_count == 1:
        return "🥐 Pastries: *1* (Pastries eaters lurking at the office, rejoice!)"
    if pastries_count == 2:
        return "🥐 Pastries: *2* (Hey, staking? Is that even allowed?)"
    if pastries_count >= 3:
        return f"🥐 Pastries: *{pastries_count}* (What? {pastries_count}???? I'd start looking into some kind of personal loan by now...)"


def compute_new_values(
    current_strikes, current_pastries, strikes_to_add, pastry_threshold
):
    """Takes the user current status and the strikes to add, and applies the logic
    updating the corresponding values (albeit strikes or pastries).

    Args:
        current_strikes (_type_): current user strikes.
        current_pastries (_type_): current user pastries counter.
        strikes_to_add (_type_): how many strikes have to be added to the user.
        pastry_threshold (_type_): how many strikes are required to increase the pastry counter.

    Returns:
        updated_strikes (int): updated number of strikes.
        updated_pastries (int): updated number of pastries.
    """

    pastry_threshold = int(pastry_threshold)
    new_strikes = current_strikes + strikes_to_add

    if new_strikes > (pastry_threshold - 1):
        updated_strikes = new_strikes % pastry_threshold
        updated_pastries = current_pastries + new_strikes // pastry_threshold
    elif new_strikes < 0:
        updated_strikes = new_strikes if new_strikes > -6 else -5
        updated_pastries = current_pastries
    else:
        updated_strikes = new_strikes
        updated_pastries = current_pastries

    return updated_strikes, updated_pastries
