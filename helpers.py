def validate_username(message):
    user = message.split()[1]
    return user.lower()
