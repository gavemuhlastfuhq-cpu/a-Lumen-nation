import datetime


def process_message(username, message):
    response = {
        "user": username,
        "message": message,
        "response": f"Hello {username}, your message was received.",
        "timestamp": str(datetime.datetime.now())
    }

    return response


if __name__ == "__main__":
    test = process_message(
        "Rocky",
        "Build Lumen Nation"
    )

    print(test)
