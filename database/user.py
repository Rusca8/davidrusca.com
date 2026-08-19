from flask_login import UserMixin

from sqlite3 import OperationalError

from database.db import get_db
from secretos import oauth_yo, kubb_admins


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

    def sub(self, provider):
        db = get_db()
        sub = db.execute(
            """
            SELECT sub
            FROM user 
            LEFT JOIN login_details 
              ON login_details.user_id = user.id 
            WHERE provider = ? AND user_id = ?;
            """,
            (provider, self.id)
        ).fetchone()["sub"]
        return sub

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

    def is_kubb_admin(self):
        if self.login_details is not None:
            for ld in self.login_details:
                if ld.get("provider") == "google" and ld.get("sub") in kubb_admins:
                    return True
        return False

    def get_footprint(self, user_id=None):
        """Returns a summary of the user's data on the site."""
        if user_id is None:
            user_id = self.user_id
        # get table names list
        db = get_db()
        db_tables = db.execute(
            """
            SELECT name
            FROM sqlite_schema
            WHERE type ='table' AND name NOT LIKE 'sqlite_%';
            """
        ).fetchall()
        footprint = {"user": 1}
        for table in db_tables:
            name = table["name"]
            try:
                amount = db.execute(
                    """
                    SELECT COUNT(*) AS amount FROM 
                    """ + name +  # table names can't PreparedStatement (NEVER do this UNLESS it's you setting the variable)
                    """ 
                    WHERE user_id = ?;
                    """, (user_id,)
                ).fetchone()
            except OperationalError:  # will give error if column not in table, so we skip it
                continue
            footprint[name] = amount["amount"]
        return footprint

    def self_destruct(self):
        print(f"Deleting user #{self.id} from the database...")
        db = get_db()
        peek = db.execute(
            """
            SELECT COUNT(*) FROM user
            WHERE id = ? AND fallback_email = ? 
            """, (self.id, self.fallback_email)
        ).fetchall()

        print(f"Safety peek found {len(peek)} items.")
        if len(peek) == 1:
            print("Single Deletion OK. Proceeding...")

            deleted = db.execute(
                """
                DELETE FROM user
                WHERE id = ? AND fallback_email = ?
                RETURNING id, name
                """, (self.id, self.fallback_email)
            ).fetchall()
            if len(deleted) == 1:
                db.commit()
            print(f"Deleted user: #{deleted[0]['id']} ({deleted[0]['name']})")
            return {"success": True}
        return {"success": False}
