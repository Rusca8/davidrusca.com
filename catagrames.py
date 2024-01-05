import json
import utilities

cita_def = {"autor": "L'hem liat parda",
            "cita":  "En David va calcular alguna cosa malament i ara no ha sortit la frase de veritat. Plorem junts."
            },


def get_from_archive(archive_id="Today"):
    archive = utilities.load_json("./static/json/catagrama/archive.json")
    quotes = utilities.load_json("./static/json/catagrama/quotes.json")

    if archive_id == "Today":  # picks last non-special (i.e. 10 chars, as in YYYY-MM-DD)
        archive_id = next(x for x in sorted(archive, reverse=True) if len(x) == 10)

    quote_id = archive.get(archive_id, {"id": "-42"})["id"]
    quote_num = archive.get(archive_id, {"num": "-42"})["num"]

    quote = quotes.get(quote_id, cita_def)
    quote["num"] = quote_num
    return quote


def get_archive():
    archive = utilities.load_json("./static/json/catagrama/archive.json")
    quotes = utilities.load_json("./static/json/catagrama/quotes.json")

    for k, v in archive.items():
        archive[k]["autor"] = quotes.get(v["id"], cita_def)["autor"]

    return archive


def get_quotes_on_queue(start=1, num_after_archive=False):
    quotes = utilities.load_json("./static/json/catagrama/quotes.json")
    queue = utilities.load_json("./static/json/catagrama/queue.json")

    if num_after_archive:
        archive = utilities.load_json("./static/json/catagrama/archive.json")
        start = len(archive) + 1

    queued_quotes = {}
    for i, quote_id in enumerate(queue, start=start):
        queued_quotes[i] = quotes.get(quote_id, cita_def)
        queued_quotes[i]["id"] = quote_id

    return queued_quotes


def get_quotes_on_archive():
    quotes = utilities.load_json("./static/json/catagrama/quotes.json")
    archive = utilities.load_json("./static/json/catagrama/archive.json")

    archived_quotes = {}
    for date, archive_data in archive.items():
        i = archive_data["num"]
        quote_id = archive_data["id"]
        archived_quotes[i] = quotes.get(quote_id, cita_def)
        archived_quotes[i]["id"] = quote_id
        archived_quotes[i]["archive_id"] = date

    return archived_quotes


def get_quotes_pool():
    quotes = utilities.load_json("./static/json/catagrama/quotes.json")
    archive = utilities.load_json("./static/json/catagrama/archive.json")
    queue = utilities.load_json("./static/json/catagrama/queue.json")

    archived_quote_ids = [v.get("id", "-42") for v in archive.values()]

    pool_quotes = {}
    for quote_id, quote in quotes.items():
        if quote_id in queue or quote_id in archived_quote_ids:
            continue
        pool_quotes[quote_id] = quote

    return pool_quotes


def move_in_queue(quote_id, move):
    queue_file = "./static/json/catagrama/queue.json"
    queue = utilities.load_json(queue_file)

    if move == "up":
        index = queue.index(quote_id)
        index = max(0, index-1)
        queue = [q for q in queue if q != quote_id]
        queue = queue[:index] + [quote_id] + queue[index:]
    elif move == "down":
        index = queue.index(quote_id)
        index = min(index+1, len(queue))
        queue = [q for q in queue if q != quote_id]
        queue = queue[:index] + [quote_id] + queue[index:]
    elif move == "top":
        queue = [quote_id] + [q for q in queue if q != quote_id]
    elif move == "bottom":
        queue = [q for q in queue if q != quote_id] + [quote_id]

    utilities.dump_json(queue, queue_file)


def add_to_queue(quote_id, move="add"):
    queue_file = "./static/json/catagrama/queue.json"
    queue = utilities.load_json(queue_file)

    if move == "top":
        move_in_queue(quote_id, move="top")
    else:
        queue.append(quote_id)
        utilities.dump_json(queue, queue_file)


def remove_from_queue(quote_id):
    queue_file = "./static/json/catagrama/queue.json"
    queue = utilities.load_json(queue_file)

    queue = [q for q in queue if q != quote_id]

    utilities.dump_json(queue, queue_file)
