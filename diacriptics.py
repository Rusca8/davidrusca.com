import json
import pytz
from datetime import datetime, timedelta

from database.cryptic_clue import CrypticClue
from database.diacriptic_arxiu import DiacripticArxiu
from database.diacriptic_solve import DiacripticSolve


default_clue = {
    "word": "patillada",
    "clue": "En David l'ha liat parda i no ha sortit cap pista.",
    "analysis": {},
    "solution": "No, de veritat que no ha carregat bé la cosa.",
    "sol_analysis": {}
    }


clues_file = "./hidden/diacriptics/clues.json"


def get_clues_in_pool():
    clues = {cclue.clue_id: cclue for cclue in CrypticClue.get_all(with_analyses=True)}
    return clues


def get_tags():
    return CrypticClue.get_all_tags()


def add_tag(clue_id, tag):
    return CrypticClue.add_tag(clue_id, tag)


def remove_tag(clue_id, tag):
    return CrypticClue.remove_tag(clue_id, tag)


def today(offset4=False):
    if offset4:
        return (datetime.now(pytz.timezone("Europe/Madrid")) - timedelta(hours=4)).strftime("%Y-%m-%d")
    return datetime.now(pytz.timezone("Europe/Madrid")).strftime("%Y-%m-%d")


def today_add_weeks(weeks):
    return (datetime.now(pytz.timezone("Europe/Madrid")) + timedelta(weeks=weeks)).strftime("%Y-%m-%d")


def now():
    """Unix epoch in seconds (no decimal places). Mimics output of sqlite's unixepoch()"""
    return round(datetime.now().timestamp())


def assign_date(clue_id, date, pwd=""):
    if clue_id and date:
        if date <= today():
            print(date, today())
            from secretos import diacriptic_ajax
            if pwd != diacriptic_ajax:
                print(f"failed password for adding older than today date (#{clue_id}, {date})")
                return False
        return DiacripticArxiu.create(date, clue_id)
    return False


def assign_num(clue_id, num):
    return DiacripticArxiu.assign_num(clue_id=clue_id, num=num)


def remove_date(clue_id, date, pwd=""):
    if clue_id and date:
        if date <= today():
            from secretos import diacriptic_ajax
            if pwd != diacriptic_ajax:
                print(f"failed password for removing older than today date (#{clue_id}, {date})")
                return False
        return DiacripticArxiu.remove(date, clue_id)
    return False


def get_clue(clue_id, with_analyses=False, to_dict=False):
    """Get clue and (by default) convert to dict."""
    clue = CrypticClue.get(clue_id, with_analyses=with_analyses)
    if isinstance(clue, CrypticClue):
        if to_dict:
            clue = clue.to_dict()
        return clue
    print("clue_id not found")
    return False


def get_definition(params=None, user_id=None):
    """Returns a tuple (clue, analysis) where the analysis only highlights the definition(s)
       If user is provided, also adds a definition mark to the help_used DB string
    """
    clue_id = params.get("clue_id")
    clue = params.get("clue")
    if clue_id and clue:
        cclue = get_clue(clue_id, with_analyses=True)
        if cclue.clue != clue:  # validating for public clues
            print("Asking for a definition but clue doesn't match.")
            return False
        # providing the clue with definition analysis
        if user_id:  # store help used by user
            DiacripticSolve.add_help(clue_id, user_id, "?")
        return cclue.clue, {k: v for k, v in cclue.clue_analysis.items() if k == "def"}
    return False


def get_letter(params=None, user_id=None):
    """returns letter in asked position (and logs the call for help into the user progress)"""
    if params is None:
        return False
    clue_id = params.get("clue_id")
    clue = params.get("clue")
    i = params.get("i")
    if i.isnumeric():
        i = int(i)
    else:
        return False
    if clue_id and clue:
        cclue = get_clue(clue_id)
        if cclue.clue != clue:  # validating for public clues
            print("Asking for a letter, but the clue doesn't match.")
            return False
        wordletters = cclue.word.replace(" ", "")  # ignorem els espais en multiparaula
        if user_id:  # store help used by user
            encoded_i = chr(i + 97)
            DiacripticSolve.add_help(clue_id, user_id, help_char=encoded_i)
        return f"{i}.{wordletters[i]}" if 0 <= i < len(wordletters) else "N"  # js fa .split(".")


def submit_solve(clue_id, user_id=None):
    date_solved = now()
    DiacripticSolve.solved(clue_id=clue_id, user_id=user_id, date_solved=date_solved)


def get_archived_clue(archive_id):
    """ deprecated """
    clue_id = "2"  # TODO CrypticClue.get_id_from_archive_or_something()
    return get_clue(clue_id)


def get_clues_on_date(date=None, future=False):
    if date is None:
        return DiacripticArxiu.get_clues_on_date(today(offset4=True))
    if date > today(offset4=True) and not future:
        return []
    return DiacripticArxiu.get_clues_on_date(date)


def get_clues_on_interval(start="2025-02-00", end=today(offset4=True), future=False):
    if end > today(offset4=True) and not future:
        print("correcting end date for get_clues_on_interval")
        end = today(offset4=True)
    return DiacripticArxiu.get_clues_on_interval(start, end)


def get_siblings(word):
    siblings = CrypticClue.get_siblings(word)
    return siblings


def create(params=None):
    if not params:
        print("No params for create diacriptic")
        return False
    word = params.get("word")
    clue = params.get("clue")
    if word and clue:  # must have main 2
        clue_id = CrypticClue.get_new_id()
        print(f"Creating NEW cryptic clue with id #{clue_id}")
        solu = params.get("solu", "")
        clue_analysis = params.get("clue_analysis", None)
        if clue_analysis is not None:
            clue_analysis = json.loads(clue_analysis)
            clue_analysis = {k: v for k, v in clue_analysis.items() if v}
        solu_analysis = params.get("solu_analysis", None)
        if solu_analysis is not None:
            solu_analysis = json.loads(solu_analysis)
            solu_analysis = {k: v for k, v in solu_analysis.items() if v}
        autor_id = int(params.get("autor_id", 0))
        print(clue_id, word, clue, solu, autor_id, clue_analysis, solu_analysis)
        return CrypticClue.create(clue_id=clue_id, word=word, clue=clue, 
                                  solution=solu, autor_id=autor_id,
                                  clue_analysis=clue_analysis, solution_analysis=solu_analysis)
    else:
        print("Missing word or clue, can't create new cryptic_clue")
        return False


def update(params=None):
    if not params:
        print("No params for create cryptic_clue")
        return False

    clue_id = params.get("clue_id")
    word = params.get("word")
    clue = params.get("clue")
    if clue_id and word and clue:  # must have id + main 2
        print(f"Updating cryptic clue with id #{clue_id}")
        solu = params.get("solu", "")
        clue_analysis = params.get("clue_analysis", None)
        if clue_analysis is not None:
            clue_analysis = json.loads(clue_analysis)
            clue_analysis = {k: v for k, v in clue_analysis.items() if v}
        solu_analysis = params.get("solu_analysis", None)
        if solu_analysis is not None:
            solu_analysis = json.loads(solu_analysis)
            solu_analysis = {k: v for k, v in solu_analysis.items() if v}
        autor_id = int(params.get("autor_id", 0))
        return CrypticClue.update(clue_id=clue_id, word=word, clue=clue,
                                  solution=solu, autor_id=autor_id,
                                  clue_analysis=clue_analysis, solution_analysis=solu_analysis)
    else:
        print("Missing id, word or clue. Can't update cryptic_clue into its own disappearance")
        return False


def calendar(start="2025-01-01", end=today_add_weeks(52)):
    import calendar as cal
    sy, sm, sd = [int(x) for x in start.split("-")]
    ey, em, ed = [int(x) for x in end.split("-")]
    months = []
    year = sy
    for year in range(sy, ey+1):
        for month in range(1, 13):
            if year == sy and month < sm:
                continue
            if year == ey and month > em:
                continue
            months.append({"year": year, "month": month, "range": cal.monthrange(year, month)})
    return months


def month_calendar(year=None, month=None):
    """Returns single month's structure."""
    import calendar as cal
    if year is None:
        year = datetime.now().year
    if month is None:
        month = datetime.now().month
    return {"year": year, "month": month, "range": cal.monthrange(year, month)}


def get_arxiu():
    from database.diacriptic_arxiu import DiacripticArxiu
    return DiacripticArxiu.get_all()


def get_solve(clue_id, user_id):
    return DiacripticSolve.get(clue_id, user_id)


def get_solves_by_user(user_id, focus_month=None):
    """focus_month is [year, month]"""
    year, month = focus_month or [datetime.now().year, datetime.now().month]
    start = f"{year}-{month:0>2}-00"
    end = f"{year}-{month:0>2}-32"
    user_solves = DiacripticArxiu.get_solves_by_user(user_id, start, end)
    return user_solves


def help_mask(clue, solve):
    mask = ["0" for _ in range(sum(clue.n))]
    if solve:
        for h in solve.help_used:
            if h != "?":
                i = ord(h) - 97
                if 0 <= i < len(mask):
                    mask[i] = "1"
    return "".join(mask)
