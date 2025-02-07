from flask_login import UserMixin

from database.db import get_db
from secretos import oauth_yo


class User(UserMixin):
    username_pattern = r"^[a-zà-öø-ý][a-zà-öø-ý0-9_.]{2,29}$"  # js validation picks from here

    def __init__(self, user_id, name, fallback_email, profile_pic, date_joined=None, username=None, login_details=None):
        self.id = user_id
        self.name = name
        self.fallback_email = fallback_email
        self.profile_pic = profile_pic
        self.date_joined = date_joined
        self.username = username
        self.login_details = login_details

    @property
    def user_id(self):
        return self.id

    @staticmethod  # adapted from realpython's
    def get(user_id):
        db = get_db()
        user_data = db.execute(
            """
            SELECT user_id, name, fallback_email, profile_pic, date_joined, username, sub, provider, email 
            FROM user 
            LEFT JOIN login_details 
              ON login_details.user_id = user.id 
            WHERE id = ?;
            """, (user_id,)
        ).fetchall()

        if not user_data:
            return None

        login_details = []
        for row in user_data:
            login_details.append({"provider": row["provider"], "sub": row["sub"], "email": row["email"]})
        user = User(
            user_id=user_data[0]["user_id"],
            name=user_data[0]["name"],
            fallback_email=user_data[0]["fallback_email"],
            profile_pic=user_data[0]["profile_pic"],
            date_joined=user_data[0]["date_joined"],
            username=user_data[0]["username"],
            login_details=login_details
        )
        return user

    @staticmethod
    def get_from_oauth(provider, sub):
        db = get_db()
        user_data = db.execute(
            """
            SELECT user_id, name, fallback_email, profile_pic, date_joined, username, sub, provider, email 
            FROM user 
            LEFT JOIN login_details 
              ON login_details.user_id = user.id 
            WHERE id = (
              SELECT user_id FROM login_details 
              WHERE provider = ? AND sub = ? 
            );
            """,
            (provider, sub)
        ).fetchall()

        if not user_data:
            return None

        login_details = []
        for row in user_data:
            login_details.append({"provider": row["provider"], "sub": row["sub"], "email": row["email"]})
        user = User(
            user_id=user_data[0]["user_id"],
            name=user_data[0]["name"],
            fallback_email=user_data[0]["fallback_email"],
            profile_pic=user_data[0]["profile_pic"],
            date_joined=user_data[0]["date_joined"],
            username=user_data[0]["username"],
            login_details=login_details
        )
        return user

    @staticmethod  # from realpython's
    def create(name, email, provider, sub, profile_pic=""):
        print(f"Inserting new user into db: {name}")
        db = get_db()
        # main user data
        db.execute(
            "INSERT INTO user (name, fallback_email, profile_pic) "
            "VALUES (?, ?, ?) ",  # Els ? són per evitar SQL injection, diu (prohibit f"" %s etc)
            (name, email, profile_pic),
        )
        # Pick id from the email, since PythonAnywhere doesn't let me use RETURNING clauses
        user_id = db.execute(
            "SELECT id FROM user WHERE fallback_email = ?",
            (email,)
        ).fetchone()
        # adding login_details [this should happen in the same transaction, since it's not commited yet]
        user_id = user_id["id"]
        print(f"· Adding login_details (user_id={user_id})")
        db.execute(
            "INSERT INTO login_details (sub, provider, user_id, email) "
            "VALUES (?, ?, ?, ?)",
            (sub, provider, user_id, email)
        )
        db.commit()
        print("New user commited.")
        return User.get(user_id)

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

    @property
    def is_admin(self):
        if self.login_details is not None:
            for ld in self.login_details:
                if ld.get("provider") == "google" and ld.get("sub") == oauth_yo:
                    return True
        return False
