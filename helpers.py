user_not_found_message = "Whoops! Couldn't find user *%s* 🤔\nAre you sure it exists?\nYou can see every user using /status, and create new users using /create\_user"
more_than_one_user_message = (
    "✋ Please enter command followed only by a *single* user name."
)


def validate_arguments(message):

    if len(message.split()) == 1:
        return []

    arguments = [x.lower() for x in message.split()[1:]]

    return arguments


def get_strike_reaction(strike_count):
    if strike_count < 0:
        return f"⚡ Strikes: *{strike_count}* (Hey! Don't think for a second this'll let you break the production environment next friday!)"

    match strike_count:
        case 0:
            return "⚡ Strikes: *0* (For now)"
        case 1:
            return f"⚡ Strikes: *{strike_count}* (Only {strike_count}? Are we sure?)"
        case 2:
            return f"⚡ Strikes: *{strike_count}* (Better watch your step, only 1 strike left to reach the _pastries tier_!)"

def get_pastries_reaction(pastries_count):
    if pastries_count == 0:
        return "🥐 Pastries: *0* (Somebody's been cautious lately...)"
    if pastries_count == 1:
        return "🥐 Pastries: *1* (Pastries eaters lurking at the office, rejoice!)"
    if pastries_count == 2:
        return "🥐 Pastries: *2* (Hey, staking? Is that even allowed?)"
    if pastries_count >= 3:
        return f"🥐 Pastries: *{pastries_count}* (What? {pastries_count}???? I'd start looking into some kind of personal loan by now...)"


def compute_new_values(
    current_strikes, current_pastries, strikes_to_add, pastry_treshold
):

    pastry_treshold = int(pastry_treshold)
    new_strikes = current_strikes + strikes_to_add

    if new_strikes > (pastry_treshold - 1):
        updated_strikes = new_strikes % pastry_treshold
        updated_pastries = current_pastries + new_strikes // pastry_treshold
    elif new_strikes < 0:
        updated_strikes = new_strikes if new_strikes > -6 else -5
        updated_pastries = current_pastries
    else:
        updated_strikes = new_strikes
        updated_pastries = current_pastries

    return updated_strikes, updated_pastries
