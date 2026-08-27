from config import MAX_MESSAGE_LENGTH, MAX_USERNAME_LENGTH


def validate_username(value):
    if not isinstance(value, str):
        raise ValueError("username must be a string.")

    value = value.strip()

    if not value:
        raise ValueError("username is required.")

    if len(value) > MAX_USERNAME_LENGTH:
        raise ValueError("username is too long.")

    return value


def validate_message(value):
    if not isinstance(value, str):
        raise ValueError("message must be a string.")

    value = value.strip()

    if not value:
        raise ValueError("message is required.")

    if len(value) > MAX_MESSAGE_LENGTH:
        raise ValueError("message is too long.")

    return value
