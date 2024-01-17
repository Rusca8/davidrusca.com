import time
from datetime import datetime, timedelta
from threading import RLock

import utilities

# locks (careful: A-Z acquire Z-A release)
archive_lock = RLock()
queue_lock = RLock()
quotes_lock = RLock()
stats_lock = RLock()

# globals
cita_def = {"autor": "L'hem liat parda",
            "cita":  "En David va calcular alguna cosa malament i ara no ha sortit la frase de veritat. Plorem junts.",
            }


def get_from_archive(archive_id="Today"):
    with archive_lock:
        with quotes_lock:
            archive = utilities.load_json("./static/json/catagrama/archive.json")
            quotes = utilities.load_json("./static/json/catagrama/quotes.json")

    if archive_id == "Today":  # picks last non-special (i.e. 10 chars, as in YYYY-MM-DD)
        archive_id = next(x for x in sorted(archive, reverse=True) if len(x) == 10)

    quote_id = archive.get(archive_id, {"id": "-42"})["id"]
    quote_num = archive.get(archive_id, {"num": "-42"})["num"]

    quote = quotes.get(quote_id, cita_def)
    quote["num"] = quote_num
    quote["id"] = quote_id
    return quote


def get_archive():
    with archive_lock:
        with quotes_lock:
            archive = utilities.load_json("./static/json/catagrama/archive.json")
            quotes = utilities.load_json("./static/json/catagrama/quotes.json")

    for k, v in archive.items():
        archive[k]["autor"] = quotes.get(v["id"], cita_def)["autor"]

    return archive


def get_quotes_on_queue(start=1, num_after_archive=False):
    with archive_lock:
        if num_after_archive:
            archive = utilities.load_json("./static/json/catagrama/archive.json")
            start = len(archive) + 1

        with queue_lock:
            with quotes_lock:
                queue = utilities.load_json("./static/json/catagrama/queue.json")
                quotes = utilities.load_json("./static/json/catagrama/quotes.json")

    queued_quotes = {}
    for i, quote_id in enumerate(queue, start=start):
        queued_quotes[i] = quotes.get(quote_id, cita_def)
        queued_quotes[i]["id"] = quote_id
        expected_date = datetime.fromtimestamp(time.time()) + timedelta(days=i-start+1) - timedelta(hours=4)
        queued_quotes[i]["expected_date"] = f"{expected_date:%Y-%m-%d} {utilities.emojiday(expected_date)}"

    return queued_quotes


def get_quotes_on_archive():
    with archive_lock:
        with quotes_lock:
            archive = utilities.load_json("./static/json/catagrama/archive.json")
            quotes = utilities.load_json("./static/json/catagrama/quotes.json")

    archived_quotes = {}
    for date, archive_data in archive.items():
        i = archive_data["num"]
        quote_id = archive_data["id"]
        archived_quotes[i] = quotes.get(quote_id, cita_def)
        archived_quotes[i]["id"] = quote_id
        archived_quotes[i]["archive_id"] = date

    return archived_quotes


def get_quotes_pool():
    with archive_lock:
        with queue_lock:
            with quotes_lock:
                archive = utilities.load_json("./static/json/catagrama/archive.json")
                queue = utilities.load_json("./static/json/catagrama/queue.json")
                quotes = utilities.load_json("./static/json/catagrama/quotes.json")

    archived_quote_ids = [v.get("id", "-42") for v in archive.values()]

    pool_quotes = {}
    for quote_id, quote in quotes.items():
        if quote_id in queue or quote_id in archived_quote_ids:
            continue
        pool_quotes[quote_id] = quote

    return pool_quotes


def move_in_queue(quote_id, move):
    with queue_lock:
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


def insert_in_queue(quote_id, index):
    if not isinstance(index, int):
        print("l'índex d'inserció no era enter")
        return

    with archive_lock:
        with queue_lock:
            archive = utilities.load_json("./static/json/catagrama/archive.json")
            queue_file = "./static/json/catagrama/queue.json"
            queue = utilities.load_json(queue_file)

            start = len(archive)
            index = min(max(0, index-start-1), len(queue))
            queue = [q for q in queue if q != quote_id]
            queue = queue[:index] + [quote_id] + queue[index:]

            utilities.dump_json(queue, queue_file)


def add_to_queue(quote_id, move="add"):
    with queue_lock:
        queue_file = "./static/json/catagrama/queue.json"
        queue = utilities.load_json(queue_file)

        if move == "top":
            move_in_queue(quote_id, move="top")  # requires recursive thread locking (needs RLock vs Lock)
        else:
            queue.append(quote_id)
            utilities.dump_json(queue, queue_file)


def remove_from_queue(quote_id):
    with queue_lock:
        queue_file = "./static/json/catagrama/queue.json"
        queue = utilities.load_json(queue_file)

        queue = [q for q in queue if q != quote_id]

        utilities.dump_json(queue, queue_file)


def get_stats(quote_id, format_times=False):
    """Gets stats dictionary of a given quote_id

    STATS:
        times: {"unix-timestamp": ms-till-solved (int)}
    """
    with stats_lock:
        stats_file = f"./static/json/catagrama/stats/stats_{quote_id}.json"
        utilities.touch_file(stats_file)  # make sure it exists

        stats = utilities.load_json(stats_file)

    # add calculated stats
    stats["times"] = stats.get("times", {})
    if stats["times"]:
        # avg
        stats["avg"] = sum(int(t) for t in stats["times"]) / len(stats["times"])
        # best
        stats["best"] = min(stats["times"])
        # worst
        stats["worst"] = max(stats["times"])
        # formated times list
    if format_times:
        formated_times = []
        for timestamp, solve_time in stats["times"].items():
            date = f"{datetime.fromtimestamp(int(timestamp)):%Y-%m-%d · %H:%M:%S}"
            solve_time = f"{timedelta(milliseconds=solve_time)}"
            if len(solve_time) > 10:
                solve_time = solve_time[:10]
            formated_times.append([date, solve_time])
        stats["formated_times"] = formated_times

    return stats


def stats_submit_time(quote_id, solve_time):
    """Adds solve time {"unix-timestamp": milliseconds} to quote stats"""
    with stats_lock:
        stats_file = f"./static/json/catagrama/stats/stats_{quote_id}.json"
        utilities.touch_file(stats_file)  # make sure it exists

        stats = utilities.load_json(stats_file)

        stats["times"] = stats.get("times", {})
        stats["times"][f"{int(time.time())}"] = int(solve_time)

        utilities.dump_json(stats, stats_file)


def add_new_quote_to_archive():
    """ de moment estem de proves :) """
    with archive_lock:
        with queue_lock:
            with quotes_lock:
                archive = utilities.load_json("./static/json/catagrama/archive.json")
                queue = utilities.load_json("./static/json/catagrama/queue.json")
                quotes = utilities.load_json("./static/json/catagrama/quotes.json")

                archive_id = f"{datetime.fromtimestamp(time.time()):%Y-%m-%d}"
                num = f'{max(int(v["num"]) for v in archive.values()) + 1}'

                if archive_id in archive:  # si alteres això, vigila amb sobreescriure dies sense voler
                    print("Avui ja hi ha una frase")
                else:
                    if not queue:
                        print("Auxili s'ha acabat la cua, haurem d'avisar en David.")
                    else:
                        quote_id = queue.pop(0)  # get and remove first element
                        print(f'[new archive entry] "{archive_id}": (num:{num}, id:{quote_id})')
                        archive[archive_id] = {"num": num, "id": quote_id}
                        quote = quotes.get(quote_id, cita_def)
                        print(f" · ({quote.get('autor','Qui?')}) {quote.get('cita', 'Què va dir?')}")

                        utilities.dump_json(queue, "./static/json/catagrama/queue.json")
                        utilities.dump_json(archive, "./static/json/catagrama/archive.json")
