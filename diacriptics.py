import json

from database.cryptic_clue import CrypticClue


default_clue = {
    "word": "patillada",
    "clue": "En David l'ha liat parda i no ha sortit cap pista.",
    "analysis": {},
    "solution": "No, de veritat que no ha carregat bé la cosa.",
    "sol_analysis": {}
    }


clues_file = "./hidden/diacriptics/clues.json"


def get_clues_in_pool():
    clues = CrypticClue.get_all(with_analyses=True)
    return clues


def get_clue(clue_id, with_analyses=False, to_dict=False):
    """Get clue and (by default) convert to dict."""
    clue = CrypticClue.get(clue_id, with_analyses=with_analyses)
    if isinstance(clue, CrypticClue):
        if to_dict:
            clue = clue.to_dict()
        return clue
    print("clue_id not found")
    return False


def get_archived_clue(archive_id):
    clue_id = "2"  # TODO CrypticClue.get_id_from_archive_or_something()
    return get_clue(clue_id)


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
