from flask_login import UserMixin

from database.db import get_db


class User(UserMixin):
    username_pattern = r"^[a-zà-öø-ý][a-zà-öø-ý0-9_.]{2,29}$"  # js validation picks from here

    def __init__(self, id_, name, email, profile_pic, date_joined=None, username=None):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic
        self.date_joined = date_joined
        self.username = username

    @staticmethod  # adapted from realpython's
    def get(user_id):
        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            return None

        user = User(
            id_=user[0], name=user[1], email=user[2], profile_pic=user[3], date_joined=user[4], username=user[5]
        )
        return user

    @staticmethod  # from realpython's
    def create(id_, name, email, profile_pic):
        print(f"Inserting new user into db: {name}")
        db = get_db()
        db.execute(
            "INSERT INTO user (id, name, email, profile_pic) "
            "VALUES (?, ?, ?, ?)",  # Els ? són per evitar SQL injection, diu (prohibit f"" %s etc)
            (id_, name, email, profile_pic),
        )
        db.commit()

    @staticmethod
    def is_username_taken(username):
        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        return True if user else False

    @staticmethod
    def change_username(id_, username):
        import re
        print("username change requested")
        if re.match(User.username_pattern, username, re.IGNORECASE):
            print(f"new username ({username}) for {id_}")
            db = get_db()
            try:
                db.execute(
                    "UPDATE user SET username = ? WHERE id = ?", (username, id_)
                )
                db.commit()
                return True
            except Exception as e:
                print("username update failed", e)
        return False
