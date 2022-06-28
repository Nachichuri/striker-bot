import sqlite3


def get_connection(db_name):

    conn = sqlite3.connect(db_name)

    cursor = conn.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS strikes (
            name text,
            strikes integer,
            pastries integer
            )"""
    )

    return conn


def create_user(db_name, username):

    conn = sqlite3.connect(db_name)

    with conn as claw:
        cursor = claw.cursor()

        cursor.execute(
            "INSERT INTO strikes VALUES (?, ?, ?)",
            (username, 0, 0),
        )
