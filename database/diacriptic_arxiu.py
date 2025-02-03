from database.db import get_db


class DiacripticArxiu:
    def __init__(self, id_, date_published, clue_id, num=None):
        self.arxiu_id = id_
        self.date_published = date_published
        self.num = num
        self.clue_id = clue_id

    @staticmethod
    def get_all():
        db = get_db()
        archive_data = db.execute(
            "SELECT * FROM diacriptic_arxiu"
        ).fetchall()
        arxiu = {}
        for da in archive_data:
            date = da["date_published"]
            if date not in arxiu:
                arxiu[date] = []
            arxiu[date].append(
                DiacripticArxiu(
                    id_=da["id"], date_published=da["date_published"], clue_id=da["clue_id"], num=da["num"]
                )
            )
        return arxiu

    @staticmethod
    def create(date_published, clue_id):
        db = get_db()
        try:
            db.execute(
                """
                INSERT INTO diacriptic_arxiu (date_published, clue_id) 
                VALUES (date(?), ?)
                """,
                (date_published, clue_id,)
            )
            db.commit()
        except Exception as e:
            print(e)
            return False
        return True

    @staticmethod
    def assign_num(clue_id, num):
        db = get_db()
        # check for usage
        num_is_used = db.execute(
            """
            SELECT num FROM diacriptic_arxiu
            WHERE clue_id != ? AND num = ?
            """,
            (clue_id, num,)
        ).fetchall()
        if num and num_is_used:
            return False
        db.execute(  # swapping num for all appearances of the clue
            """
            UPDATE diacriptic_arxiu SET num = ?
            WHERE clue_id = ?
            """,
            (num, clue_id)
        )
        db.commit()
        return True

    @staticmethod
    def remove(date_published, clue_id):
        db = get_db()
        try:
            db.execute(
                "DELETE FROM diacriptic_arxiu "
                "WHERE clue_id = ? AND date_published = ?",
                (clue_id, date_published)
            )
            db.commit()
        except Exception as e:
            print(e)
            return False
        return True

    @staticmethod
    def get_clues_on_date(date):
        """returns list of clue_id for each clue on given date"""
        db = get_db()
        entries = db.execute(
            """
            SELECT clue_id FROM diacriptic_arxiu 
            WHERE date_published = ?
            """,
            (date,)
        )
        return [row["clue_id"] for row in entries]

    @staticmethod
    def count_solves_per_person():
        """returns list of how many solves by each solver"""
        db = get_db()
        solves = db.execute(
            """
            SELECT user_id, name, username, count(user_id) as solves, 
                CASE WHEN date_solved IS NULL THEN 'PENDING'
                ELSE 'SOLVED'
                END AS 'solve_status'
            FROM diacriptic_solve 
            LEFT JOIN user
                ON user.id = diacriptic_solve.user_id
            GROUP BY user_id, solve_status
            ORDER BY solves DESC
            """
        ).fetchall()

        solves_count = {}
        for row in solves:
            user_id = row["user_id"]
            if user_id not in solves_count:
                solves_count[user_id] = {"name": row["name"], "username": row["username"]}
            if row["solve_status"] == "PENDING":
                solves_count[user_id]["pending"] = row["solves"]
            else:
                solves_count[user_id]["solved"] = row["solves"]
        return solves_count

