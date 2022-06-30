def validate_arguments(message):

    if len(message.split()) == 1:
        return []

    arguments = message.split()[1:]

    return arguments
