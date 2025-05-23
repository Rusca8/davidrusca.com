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
    def get_clues_on_interval(start, end):
        """Returns list of dates and quotes in date, between two given dates"""
        db = get_db()
        entries = db.execute(
            """
            SELECT * FROM diacriptic_arxiu
            WHERE date_published >= ? AND date_published <= ?
            """,
            (start, end,)
        )
        archive_clues = {}
        for row in entries:
            date_published = row["date_published"]
            if date_published not in archive_clues:
                archive_clues[date_published] = []
            archive_clues[date_published].append(
                [DiacripticArxiu(
                    id_=row["id"], date_published=date_published, clue_id=row["clue_id"], num=row["num"]
                )
                ])
        return archive_clues

    @staticmethod
    def get_queue():
        """Returns list of future dates with a clue assigned to them.
           Will check against calendar to detect holes near today.
        """
        db = get_db()
        queue = db.execute(
            """
            SELECT date_published FROM diacriptic_arxiu
            WHERE date_published > strftime('%Y-%m-%d','now')
            ORDER BY date_published ASC
            """
        ).fetchall()
        return (row["date_published"] for row in queue)
