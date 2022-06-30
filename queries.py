create_new_user = "INSERT INTO strikes VALUES (?, ?, ?)"
create_strikes_table = """CREATE TABLE IF NOT EXISTS strikes (
                            name text PRIMARY KEY,
                            strikes integer NOT NULL,
                            pastries integer NOT NULL
                        )"""
get_status_from_user = "SELECT * FROM strikes WHERE name = ?"
