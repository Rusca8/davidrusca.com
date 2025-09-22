from database.db import get_db


class DiacripticSolve:
    sql_filter_recent = """
        WHERE date_solved IS NOT NULL AND date_solved > strftime('%s', 'now', '-7 day')
        """

    def __init__(self, clue_id, user_id, date_solved=None, help_used=""):
        self.clue_id = clue_id
        self.user_id = user_id
        self.date_solved = date_solved
        self.help_used = help_used

    @property
    def help_dots(self):
        return "".join("d" if h == "?" else "l" for h in self.help_used)

    @staticmethod
    def get(clue_id, user_id):
        db = get_db()
        solve = db.execute(
            """
            SELECT * FROM diacriptic_solve
            WHERE clue_id = ? AND user_id = ?
            """,
            (clue_id, user_id)
        ).fetchone()
        if not solve:
            return None
        return DiacripticSolve(
            clue_id=clue_id, user_id=user_id, date_solved=solve["date_solved"], help_used=solve["help_used"]
        )

    @staticmethod
    def create(clue_id, user_id, date_solved=None, help_used=""):
        db = get_db()
        try:
            db.execute(
                """
                INSERT INTO diacriptic_solve (clue_id, user_id, date_solved, help_used)
                VALUES (?, ?, ?, ?)
                """,
                (clue_id, user_id, date_solved, help_used)
            )
            db.commit()
        except Exception as e:
            print(e)
            return False
        return True

    @staticmethod
    def add_help(clue_id, user_id, help_char):
        db = get_db()
        # picking it if in case it exists
        solve = DiacripticSolve.get(clue_id, user_id)
        if solve:  # existed previous progress
            help_used = solve.help_used
            if help_char in help_used:
                print("help already exists")
                return help_used
            help_used += help_char
            db.execute(
                """
                UPDATE diacriptic_solve SET help_used = ? 
                WHERE clue_id = ? AND user_id = ?
                """,
                (help_used, clue_id, user_id,)
            )
            db.commit()
        else:  # start anew
            help_used = help_char
            DiacripticSolve.create(clue_id, user_id, help_used=help_used)
        return help_used

    @staticmethod
    def solved(clue_id, user_id, date_solved):
        db = get_db()
        solve = DiacripticSolve.get(clue_id, user_id)
        if solve:
            if solve.date_solved:
                print("solve already exists")
                return False
            db.execute(
                """
                UPDATE diacriptic_solve SET date_solved = ?
                WHERE clue_id = ? AND user_id = ?
                """,
                (date_solved, clue_id, user_id,)
            )
            db.commit()
        else:
            DiacripticSolve.create(clue_id, user_id, date_solved=date_solved)
        return True

    @staticmethod
    def count_solves_per_person(only_recent=False):
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
                ON user.id = diacriptic_solve.user_id"""
            + (DiacripticSolve.sql_filter_recent if only_recent else '') +
            """
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

    @staticmethod
    def get_solves_by_user(user_id, start, end):
        """Returns solves by user in a given period"""
        db = get_db()
        entries = db.execute(
            """
            SELECT * FROM diacriptic_arxiu 
              LEFT JOIN diacriptic_solve
                ON diacriptic_arxiu.clue_id = diacriptic_solve.clue_id
            WHERE user_id = ? AND date_published > ? AND date_published < ? 
            """,
            (user_id, start, end,)
        )
        solves = {}
        for row in entries:
            date_published = row["date_published"]
            if date_published not in solves:
                solves[date_published] = []
            solves[date_published].append(
                DiacripticSolve(
                    clue_id=row["clue_id"], user_id=user_id, date_solved=row["date_solved"], help_used=row["help_used"]
                )
            )
        return solves
