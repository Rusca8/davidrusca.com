import json

cita_def = {"autor": "L'hem liat parda",
            "cita":  "En David va calcular alguna cosa malament i ara no ha sortit la frase de veritat. Plorem junts."
            },


def get_from_archive(archive_id="Today"):
    with open("./static/json/catagrama/archive.json") as f:
        archive = json.load(f)
    with open("./static/json/catagrama/quotes.json") as f:
        quotes = json.load(f)

    if archive_id == "Today":  # picks last non-special (i.e. 10 chars, as in YYYY-MM-DD)
        archive_id = next(x for x in sorted(archive, reverse=True) if len(x) == 10)

    quote_id = archive.get(archive_id, {"id": "-42"})["id"]
    quote_num = archive.get(archive_id, {"num": "-42"})["num"]

    quote = quotes.get(quote_id, cita_def)
    quote["num"] = quote_num
    return quote


def get_archive_index():
    with open("./static/json/catagrama/archive.json") as f:
        archive = json.load(f)
    with open("./static/json/catagrama/quotes.json") as f:
        quotes = json.load(f)

    for k, v in archive.items():
        archive[k]["autor"] = quotes.get(v["id"], cita_def)["autor"]

    return archive


