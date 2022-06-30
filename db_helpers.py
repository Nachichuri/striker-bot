import sqlite3
import queries


def get_connection(db_name):

    conn = sqlite3.connect(db_name)

    cursor = conn.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS strikes (
            name text PRIMARY KEY,
            strikes integer NOT NULL,
            pastries integer NOT NULL
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


def get_status(db_name, user: None):

    conn = sqlite3.connect(db_name)

    with conn as claw:
        cursor = claw.cursor()

        if user is None:
            return "Sarasa"
        else:
            print(user)
            print(queries.get_status_from_user)
            cursor.execute(queries.get_status_from_user, (user,))
            asd = cursor.fetchall()
            print(asd)
            return f"Strikes de *{user}*"