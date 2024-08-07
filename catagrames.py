import time
import random
from datetime import datetime, timedelta
from threading import RLock

import tele
import utilities

# locks (careful: A-Z acquire Z-A release)
archive_lock = RLock()
fixed_lock = RLock()
queue_lock = RLock()
quotes_lock = RLock()
stats_lock = RLock()
viqui_lock = RLock()
vqchoices_lock = RLock()
watched_lock = RLock()

# globals
cita_def = {"autor": "L'hem liat parda",
            "cita":  "En David va calcular alguna cosa malament i ara no ha sortit la frase de veritat. Plorem junts.",
            }

cita_debug = {"autor": "Curtis Quotis", "cita": "La Mandarina Manda Rina"}


archive_file = "./static/json/catagrama/archive.json"
fixed_file = "./static/json/catagrama/fixed_in_queue.json"
queue_file = "./static/json/catagrama/queue.json"
quotes_file = "./static/json/catagrama/local_to_cloud/quotes.json"
viqui_file = "./static/json/catagrama/local_to_cloud/viquidites.json"
vqchoices_file = "./static/json/catagrama/viqui_choices.json"
watched_file = "./static/json/catagrama/local_to_cloud/watched_dates.json"


def get_from_archive(archive_id="Today"):
    with archive_lock:
        with quotes_lock:
            archive = utilities.load_json(archive_file)
            quotes = utilities.load_json(quotes_file)

    if archive_id == "Today":  # picks last non-special (i.e. 10 chars, as in YYYY-MM-DD)
        archive_id = next(x for x in sorted(archive, reverse=True) if len(x) == 10)

    quote_id = archive.get(archive_id, {"id": "-42"})["id"]
    quote_num = archive.get(archive_id, {"num": "-42"})["num"]

    quote = quotes.get(quote_id, cita_def)
    quote["num"] = quote_num
    quote["id"] = quote_id
    quote["archive_id"] = archive_id
    return quote


def get_random_vq(vq_id="RAND"):
    with viqui_lock:
        viquidites = utilities.load_json(viqui_file)
    with vqchoices_lock:
        vqchoices = utilities.load_json(vqchoices_file)
    vqchoices_ids = vqchoices.get("baneadas", []) + vqchoices.get("aceptadas", []) + vqchoices.get("reguleras", [])

    if vq_id == "RAND":
        vq_id = random.choice([vq_id for vq_id in viquidites if vq_id not in vqchoices_ids])

    quote = viquidites.get(vq_id, cita_def)
    quote["num"] = "X"
    quote["id"] = vq_id
    quote["archive_id"] = vq_id
    return quote


def vq_submit_choice(vq_id, choice):
    valid_choice_options = ["aceptadas", "baneadas", "reguleras"]
    with vqchoices_lock:
        vqchoices = utilities.load_json(vqchoices_file)
        if choice in valid_choice_options:
            for op in valid_choice_options:  # clean it from the other lists
                vqchoices[op] = [q for q in vqchoices[op] if q != vq_id]
            vqchoices[choice] = vqchoices.get(choice, []) + [vq_id]  # append
        else:
            return
        utilities.dump_json(vqchoices, vqchoices_file)


def get_archive():
    with archive_lock:
        with quotes_lock:
            archive = utilities.load_json(archive_file)
            quotes = utilities.load_json(quotes_file)

    for k, v in archive.items():
        bug = False
        try:
            stats = get_stats(v["id"])
        except Exception as e:
            tele.send_message("archi", "yo",
                              "💥*CATAGRAMA FAIL*💥 (" + f"{e}) quan carregava stats de la cita del {k} per l'arxiu.")
            stats = {}
            bug = True
        archive[k]["autor"] = quotes.get(v["id"], cita_def)["autor"]
        archive[k]["solves"] = "🐞" if bug else len([t for t in stats.get("times", {}).values() if t > 10000])

    return archive


def get_quotes_on_queue(start=1, num_after_archive=False):
    with fixed_lock:  # no lo hago alfabético porque es una consulta independiente
        fixed = utilities.load_json(fixed_file)
    with watched_lock:  # no lo hago alfabético porque es una consulta independiente
        watched = utilities.load_json(watched_file)

    with archive_lock:
        if num_after_archive:
            archive = utilities.load_json(archive_file)
            start = len(archive) + 1

        with queue_lock:
            with quotes_lock:
                queue = utilities.load_json(queue_file)
                quotes = utilities.load_json(quotes_file)

    # archive frequencies info
    freq_stats = {}
    for i, archived_quote in enumerate(archive.values(), start=1):
        quote_id = archived_quote["id"]
        autor = quotes.get(quote_id, cita_def)["autor"]
        freq_stats[autor] = freq_stats.get(autor, {})
        freq_stats[autor]["last"] = i
        freq_stats[autor]["count"] = freq_stats[autor].get("count", 0) + 1

    # retrieve quotes (+ bundle extra info)
    queued_quotes = {}
    for i, quote_id in enumerate(queue, start=start):
        # add standard info
        queued_quotes[i] = quotes.get(quote_id, cita_def)
        queued_quotes[i]["id"] = quote_id
        expected_date = datetime.fromtimestamp(time.time()) + timedelta(days=i-start+1) - timedelta(hours=4)
        queued_quotes[i]["expected_date"] = f"{expected_date:%Y-%m-%d} {utilities.emojiday(expected_date)}"
        queued_quotes[i]["fixed"] = fixed.get(quote_id, "")
        if f"{expected_date:%m-%d}" in watched:
            queued_quotes[i]["watched_info"] = watched[f"{expected_date:%m-%d}"]
        # add frequency info
        autor = queued_quotes[i]["autor"]
        quote_freq_stats = freq_stats.get(autor, {})
        queued_quotes[i]["freq_stats"] = {}
        queued_quotes[i]["freq_stats"]["count"] = quote_freq_stats.get("count", 1)
        queued_quotes[i]["freq_stats"]["ago"] = ago if (ago := i-quote_freq_stats.get("last", i)) > 0 else ""
        # frequency info dict update
        freq_stats[autor] = freq_stats.get(autor, {})
        freq_stats[autor]["last"] = i
        freq_stats[autor]["count"] = freq_stats[autor].get("count", 0) + 1

    return queued_quotes


def get_quotes_on_archive():
    with watched_lock:  # no lo hago alfabético porque es una consulta independiente
        watched = utilities.load_json(watched_file)

    with archive_lock:
        with quotes_lock:
            archive = utilities.load_json(archive_file)
            quotes = utilities.load_json(quotes_file)

    archived_quotes = {}
    ii = 0
    for date, archive_data in archive.items():
        i = archive_data["num"]
        quote_id = archive_data["id"]
        archived_quotes[i] = quotes.get(quote_id, cita_def)
        archived_quotes[i]["id"] = quote_id
        archived_quotes[i]["archive_id"] = date
        archived_quotes[i]["emojiday"] = utilities.emojiday(datetime.fromtimestamp(1704279600) + timedelta(days=ii))
        if date[5:10] in watched:
            archived_quotes[i]["watched_info"] = watched[date[5:]]
        ii += 1

    return archived_quotes


def get_quotes_pool():
    with archive_lock:
        with queue_lock:
            with quotes_lock:
                archive = utilities.load_json(archive_file)
                queue = utilities.load_json(queue_file)
                quotes = utilities.load_json(quotes_file)

    archived_quote_ids = [v.get("id", "-42") for v in archive.values()]

    pool_quotes = {}
    for quote_id, quote in quotes.items():
        if quote_id in queue or quote_id in archived_quote_ids:
            continue
        pool_quotes[quote_id] = quote

    return pool_quotes


def print_vq_choice_quotes(choices=None):
    if choices is None:
        choices = ["aceptadas"]
    with quotes_lock:
        quotes = utilities.load_json(quotes_file)
    with viqui_lock:
        viquidites = utilities.load_json(viqui_file)
    with vqchoices_lock:
        vqchoices = utilities.load_json(vqchoices_file)

    for choice, vq_ids in vqchoices.items():
        print(f"=== {choice} ===")
        if choice not in choices:
            print("hidden")
            continue
        count_hidden = 0
        for vq_id in vq_ids:
            if vq_id in quotes:
                count_hidden +=1
            else:
                print(f'"{vq_id}":', "{", ', '.join(f'"{k}": "{v}"' for k, v in viquidites[vq_id].items()), "},")
        print(f"···{count_hidden} more in pool···") if count_hidden else None

def get_vq_choices_stats():
    with viqui_lock:
        viqui = utilities.load_json(viqui_file)
    with vqchoices_lock:
        vqchoices = utilities.load_json(vqchoices_file)
    pendientes = len(viqui) - sum(len(v) for k, v in vqchoices.items())
    return {k: len(v) for k, v in vqchoices.items()} | {"pendientes": pendientes}


def move_in_queue(quote_id, move):
    with queue_lock:
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
            archive = utilities.load_json(archive_file)
            queue = utilities.load_json(queue_file)

            start = len(archive)
            index = min(max(0, index-start-1), len(queue))
            queue = [q for q in queue if q != quote_id]
            queue = queue[:index] + [quote_id] + queue[index:]

            utilities.dump_json(queue, queue_file)


def add_to_queue(quote_id, move="add"):
    with queue_lock:
        queue = utilities.load_json(queue_file)

        if move == "top":
            move_in_queue(quote_id, move="top")  # requires recursive thread locking (needs RLock vs Lock)
        else:
            queue.append(quote_id)
            utilities.dump_json(queue, queue_file)


def remove_from_queue(quote_id):
    with queue_lock:
        queue = utilities.load_json(queue_file)

        queue = [q for q in queue if q != quote_id]

        utilities.dump_json(queue, queue_file)


def fix_to_position(quote_id, position):
    with fixed_lock:
        fixed = utilities.load_json(fixed_file)

        fixed[quote_id] = position
        utilities.dump_json(fixed, fixed_file)


def release_from_position(quote_id):
    with fixed_lock:
        fixed = utilities.load_json(fixed_file)

        fixed = {k: v for k, v in fixed.items() if k != quote_id}
        utilities.dump_json(fixed, fixed_file)


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
        stats["avg"] = utilities.format_solve_time(sum(int(t) for t in stats["times"].values()) / len(stats["times"]))
        # best
        stats["best"] = utilities.format_solve_time(min(stats["times"].values()))
        # worst
        stats["worst"] = utilities.format_solve_time(max(stats["times"].values()))

    # formated times list
    if format_times:
        formated_times = []
        for timestamp, solve_time in stats["times"].items():
            date = f"{datetime.fromtimestamp(int(timestamp)):%Y-%m-%d · %H:%M:%S}"
            solve_time = utilities.format_solve_time(solve_time)
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
    with archive_lock:
        with queue_lock:
            with quotes_lock:
                archive = utilities.load_json(archive_file)
                queue = utilities.load_json(queue_file)
                quotes = utilities.load_json(quotes_file)

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

                        utilities.dump_json(queue, queue_file)
                        utilities.dump_json(archive, archive_file)


def check_queue_length():
    from tele import send_message

    mins = {"first": 40, "second": 20, "worry": 10, "panic": 5}
    with queue_lock:
        queue = utilities.load_json(queue_file)

    lenq = len(queue)
    print(f"Checking queue length...\nCurrently {lenq} on queue.")
    if lenq == mins["first"]:
        send_message("archi", "yo", f"Hauria de posar Catagrames nous a la llista, senyoria.\nEn queden {lenq}.")
    elif lenq == mins["second"]:
        send_message("archi", "yo", f"⚠️ Senyoria, no va posar Catagrames. S'estan gastant.\nEn queden *{lenq}*.")
    elif lenq == mins["worry"]:
        send_message("archi", "yo",
                     f"🚨 Queden molt pocs catagrames, excel·lència. *Només {lenq}.*\nPotser que s'espavil·li.")
    elif lenq <= mins["panic"]:
        send_message("archi", "yo",
                     f"🚨⚠⚠️ ELS CATAGRAMES S'ESTAN ESGOTANT. FACI ALGUNA COSA, SISPLAU LI HO DEMANO.\nEN QUEDEN {lenq}.")
    else:
        print("No need to wake up Archibald.")


if __name__ == "__main__":
    print_vq_choice_quotes()
