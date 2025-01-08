import sqlite3
import os


def get_users():
    root = os.path.dirname(__file__)
    path = os.path.join(root, "sqlite_db")
    con = sqlite3.connect(path)
    cur = con.cursor()

    users = cur.execute('SELECT * FROM user').fetchall()
    con.close()
    return users


if __name__ == "__main__":
    print(get_users())
