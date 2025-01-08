from database.db import get_db
from crypto import unidecode_but


class CrypticClue:
    sql_select_clue = """
        SELECT cryptic_clue.clue_id, word, clue, solution, date_created, 
            autor.id AS autor_id, autor.name AS autor 
        FROM cryptic_clue 
            LEFT JOIN autor 
                ON cryptic_clue.autor_id = autor.id 
        """
    sql_select_with_analyses = """
        SELECT cryptic_clue.clue_id, word, clue, solution, date_created, 
            autor.id AS autor_id, autor.name AS autor, 
            cryptic_clue_analysis.analysis_type, 
            analysis_block.block_type, analysis_block.block_start, analysis_block.block_end 
        FROM cryptic_clue 
            LEFT JOIN autor 
                ON cryptic_clue.autor_id = autor.id 
            LEFT JOIN cryptic_clue_analysis 
                ON cryptic_clue.clue_id = cryptic_clue_analysis.clue_id 
            LEFT JOIN analysis_block 
                ON analysis_block.clue_id = cryptic_clue_analysis.clue_id 
                AND analysis_block.analysis_type = cryptic_clue_analysis.analysis_type 
        """

    def __init__(self, clue_id, word, clue, solution="", date_created=None, autor_id=None, autor=None,
                 clue_analysis=None, solution_analysis=None):
        self.clue_id = clue_id
        self.word = word
        self.clue = clue
        self.solution = solution
        self.date_created = date_created
        self.autor_id = autor_id
        self.autor = autor
        self.clue_analysis = clue_analysis
        self.solution_analysis = solution_analysis

    @property
    def n(self):
        return [len(w) for w in self.word.split()]  # llista de quantitats de lletres

    @staticmethod
    def get(clue_id, with_analyses=False):
        if with_analyses:
            db = get_db()
            cclue_data = db.execute(
                CrypticClue.sql_select_with_analyses +
                """WHERE cryptic_clue.clue_id = ? """,
                (clue_id,)
            ).fetchall()
            if not cclue_data:
                return None
            # parsing
            cclue = cclue_data[0]
            analysis = {}
            for row in cclue_data:
                analysis_type = row["analysis_type"]
                block_type = row["block_type"]
                block_start = row["block_start"]
                block_end = row["block_end"]
                if analysis_type not in analysis:
                    analysis[analysis_type] = {}
                if block_type not in analysis[analysis_type]:
                    analysis[analysis_type][block_type] = []
                analysis[analysis_type][block_type].append([block_start, block_end])

            cclue = CrypticClue.from_row(cclue, clue_analysis=analysis["clue"], solution_analysis=analysis["solution"])
            return cclue
        else:
            db = get_db()
            cclue = db.execute(
                CrypticClue.sql_select_clue +
                "WHERE clue_id = ?",
                (clue_id,)
            ).fetchone()
            if not cclue:
                return None

            cclue = CrypticClue.from_row(cclue)

            return cclue

    @staticmethod
    def from_row(row, clue_analysis=None, solution_analysis=None):
        return CrypticClue(
            clue_id=row["clue_id"],
            word=row["word"],
            clue=row["clue"] if "clue" in row.keys() else None,
            solution=row["solution"] if "solution" in row.keys() else None,
            date_created=row["date_created"] if "date_created" in row.keys() else None,
            autor_id=row["autor_id"] if "autor_id" in row.keys() else None,
            autor=row["autor"] if "autor" in row.keys() else None,
            clue_analysis=clue_analysis,
            solution_analysis=solution_analysis
        )

    @staticmethod
    def get_all(with_analyses=False):
        if with_analyses:
            db = get_db()
            cclue_data = db.execute(
                CrypticClue.sql_select_with_analyses
            ).fetchall()
            # parsing
            cclues = {}
            for row in cclue_data:
                # clue setup
                clue_id = row["clue_id"]
                if clue_id not in cclues:
                    cclues[clue_id] = {"row": row, "analysis": {}}
                # clue analysis
                analysis_type = row["analysis_type"]
                block_type = row["block_type"]
                block_start = row["block_start"]
                block_end = row["block_end"]
                if analysis_type not in cclues[clue_id]["analysis"]:
                    cclues[clue_id]["analysis"][analysis_type] = {}
                if not block_type:
                    continue
                if block_type not in cclues[clue_id]["analysis"][analysis_type]:
                    cclues[clue_id]["analysis"][analysis_type][block_type] = []
                cclues[clue_id]["analysis"][analysis_type][block_type].append([block_start, block_end])

            return [CrypticClue.from_row(cclue["row"],
                                         clue_analysis=cclue["analysis"]["clue"],
                                         solution_analysis=cclue["analysis"]["solution"])
                    for cclue in cclues.values()]
        else:
            db = get_db()
            cclues = db.execute(
                CrypticClue.sql_select_clue
            ).fetchall()
            for cclue in cclues:
                print(cclue["clue_id"], cclue["word"])
            return [CrypticClue.from_row(cclue) for cclue in cclues]

    @staticmethod
    def create(clue_id, word, clue, solution="", autor_id=None, clue_analysis=None, solution_analysis=None):
        print(f"Inserting new clue into db: '{word}'='{clue}'")
        if not autor_id:  # sqlite was supposed to handle this but it doesn't like me explicitly passing None
            autor_id = 0  # so I guess I'll do it myself...
        # unidecode word
        word = unidecode_but(word.lower(), preserve="çñ")
        # proper creation
        db = get_db()
        try:
            # inserting the cryptic_clue itself
            db.execute(
                "INSERT INTO cryptic_clue (clue_id, word, clue, solution, autor_id)"
                "VALUES (?, ?, ?, ?, ?)",
                (clue_id, word, clue, solution, autor_id)
            )
            # clue_analysis
            if clue_analysis:
                print("Adding clue analysis")
                db.execute(
                    "INSERT INTO cryptic_clue_analysis (clue_id, analysis_type)"
                    "VALUES (?, ?)",
                    (clue_id, "clue")
                )
                for block_type, blocks in clue_analysis.items():
                    for block in blocks:
                        db.execute(
                            "INSERT INTO analysis_block (clue_id, analysis_type, block_type, block_start, block_end)"
                            "VALUES (?, ?, ?, ?, ?)",
                            (clue_id, "clue", block_type, block[0], block[1])
                        )
            # solution analysis
            if solution_analysis:
                print("Adding solution analysis")
                db.execute(
                    "INSERT INTO cryptic_clue_analysis (clue_id, analysis_type)"
                    "VALUES (?, ?)",
                    (clue_id, "solution")
                )
                for block_type, blocks in solution_analysis.items():
                    for block in blocks:
                        db.execute(
                            "INSERT INTO analysis_block (clue_id, analysis_type, block_type, block_start, block_end)"
                            "VALUES (?, ?, ?, ?, ?)",
                            (clue_id, "solution", block_type, block[0], block[1])
                        )
            db.commit()
            print("Commited.")
            return True
        except Exception as e:
            print("Exception: ", e)
            return False

    @staticmethod
    def update(clue_id, word, clue, solution="", autor_id=None, clue_analysis=None, solution_analysis=None):
        print("Updating DB entry for cryptic_clue #", clue_id)
        if not autor_id:  # sqlite was supposed to handle this but it doesn't like me explicitly passing None
            autor_id = 0  # so I guess I'll do it myself...
        # collect changes
        incomming = {
            "clue_id": clue_id,
            "word": word,
            "clue": clue,
            "solution": solution,
            "autor_id": autor_id,
            "clue_analysis": clue_analysis,
            "solution_analysis": solution_analysis,
        }
        print(incomming)
        cclue = CrypticClue.get(clue_id, with_analyses=True)
        if not isinstance(cclue, CrypticClue):
            print(f"No clue with id #{clue_id} to update.")
            return False
        in_db = cclue.to_dict()

        updates = {k: v for k, v in incomming.items() if incomming[k] != in_db[k]}
        if not updates:
            print("Nothing to update")
            return False

        for k in updates:
            print(k)
            print(f"  {updates[k]} → {in_db[k]}")

        # execute
        db = get_db()
        try:
            # updating the cryptic_clue itself
            cclue_updates = {k: v for k, v in updates.items() if not k.endswith("_analysis")}
            if cclue_updates:
                db.execute("UPDATE cryptic_clue SET "
                           + ", ".join(f"{k} = ?" for k in cclue_updates.keys())
                           + " WHERE clue_id = ?",  # NEVER replace ? for the {value} (SQL Injection)
                           tuple(cclue_updates.values()) + (clue_id,))
            if "clue_analysis" in updates:
                print("updating clue_analysis")
                # make sure there's an analysis to bind blocks to
                db.execute(
                    "INSERT OR IGNORE INTO cryptic_clue_analysis (clue_id, analysis_type) "
                    "VALUES (?, ?)",
                    (clue_id, "clue")
                )
                print("· Deleting the old blocks")
                db.execute("DELETE FROM analysis_block "
                           "WHERE clue_id = ? AND analysis_type = ? ",
                           (clue_id, "clue"))
                if clue_analysis:
                    print("· Adding the new blocks")
                    for block_type, blocks in clue_analysis.items():
                        for block in blocks:
                            db.execute(
                                "INSERT INTO analysis_block (clue_id, analysis_type, block_type, block_start, block_end)"
                                "VALUES (?, ?, ?, ?, ?)",
                                (clue_id, "clue", block_type, block[0], block[1])
                            )
            if "solution_analysis" in updates:
                print("updating solution_analysis")
                # make sure there's an analysis to bind blocks to
                db.execute(
                    "INSERT OR IGNORE INTO cryptic_clue_analysis (clue_id, analysis_type) "
                    "VALUES (?, ?)",
                    (clue_id, "solution")
                )
                print("· Deleting the old blocks")
                db.execute("DELETE FROM analysis_block "
                           "WHERE clue_id = ? AND analysis_type = ? ",
                           (clue_id, "solution"))
                if solution_analysis:
                    print("· Adding the new blocks")
                    for block_type, blocks in solution_analysis.items():
                        for block in blocks:
                            db.execute(
                                "INSERT INTO analysis_block (clue_id, analysis_type, block_type, block_start, block_end)"
                                "VALUES (?, ?, ?, ?, ?)",
                                (clue_id, "solution", block_type, block[0], block[1])
                            )
            db.commit()
            print("Update commited.")
            return True
        except Exception as e:
            print("Exception: ", e)
            return False

    @staticmethod
    def get_new_id():
        db = get_db()
        ids = db.execute(
            "SELECT * FROM cryptic_clue"
        ).fetchall()
        if ids:
            return max(int(clue_id[0]) for clue_id in ids if clue_id) + 1
        return 1

    @staticmethod
    def get_siblings(word):
        db = get_db()
        cclues = db.execute(
            "SELECT clue_id, word, clue "
            "FROM cryptic_clue "
            "WHERE word = ?",
            (word,)
        ).fetchall()

        cclues = [CrypticClue(
            clue_id=cclue["clue_id"], word=cclue["word"], clue=cclue["clue"]
        ) for cclue in cclues]
        return cclues

    def to_dict(self):
        clue = {
            "clue_id": self.clue_id,
            "word": self.word,
            "n": self.n,
            "clue": self.clue,
            "solution": self.solution,
            "autor_id": self.autor_id,
            "autor": self.autor,
            "clue_analysis": self.clue_analysis,
            "solution_analysis": self.solution_analysis
        }
        return clue
