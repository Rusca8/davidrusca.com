import utilities
from hashlib import sha256


sample = {
    "words": {
        "v": [
            [0, 1, "truita", "Ous barrejats del temps amb fruita escapçada."],
            [4, 5, "de", "Cor d'un adéu consonant."]
        ],
        "h":[
            [2, 0, "gustosa", "Saborosa formiga anglesa abandona un guant per atacar Tossa."],
            [5, 0, "patates", "Als inicis practicava ambicions teatrals amb tots els seus tubercles."]
        ],
    },
}

encreuats_file = "./hidden/encreuats/encreuats.json"
keying_factors_file = "./hidden/encreuats/keying_factors.json"
dimensions_file = "./hidden/encreuats/dimensions.json"

def list_for_index():
    encreuats = utilities.load_json(encreuats_file)
    keying_factors = utilities.load_json(keying_factors_file)
    dimensions = utilities.load_json(dimensions_file)
    listed = []
    for enc_id, enc in reversed(encreuats.items()):
        nclues = len(enc["words"]["h"]) + len(enc["words"]["v"])
        if enc_id not in keying_factors:
            print(enc_id, "not in keying factors database. Updating...")
            build_keying_factors()
        k = keying_factors.get(enc_id, "??")
        if enc_id not in dimensions:
            print(enc_id, "not in dimensions database. Updating...")
            build_dimensions_db()
        rows, cols = dimensions.get(enc_id)
        listed.append({"title": enc["title"], "autor": enc['autor'], "data": enc['date'], "enc_id": enc_id,
                       "size": nclues, "k": k, "rows": rows, "cols": cols})
    return listed


def clues_in_cell(enc, row, col):
    cic = 0
    for clue in enc["clues"]["h"].values():
        if row == clue["pos"][0] and clue["pos"][1] <= col < clue["pos"][1] + clue["len"]:
            cic += 1
    for clue in enc["clues"]["v"].values():
        if col == clue["pos"][1] and clue["pos"][0] <= row < clue["pos"][0] + clue["len"]:
            cic += 1
    return cic


def get_keying_factor(enc=None):
    if enc is None:
        return "Not provided"
    word_letters = 0
    unchecked = 0
    for row in range(enc["rows"]):
        for col in range(enc["cols"]):
            cic = clues_in_cell(enc, row, col)
            if cic:
                word_letters += cic
                if cic == 1:
                    unchecked += 1
    return round(100 * (1 - unchecked / word_letters))


def build_keying_factors(rebuild=False):
    """Calculates keying factors for all crosswords and saves them to a file."""
    utilities.touch_file(keying_factors_file)
    keying_factors = utilities.load_json(keying_factors_file)
    encreuats = utilities.load_json(encreuats_file)
    for enc_id in encreuats:
        if enc_id not in keying_factors or rebuild:
            keying_factors[enc_id] = get_keying_factor(parse_encreuat(enc_id))
    utilities.dump_json(keying_factors, keying_factors_file)


def parse_encreuat(enc_id=None):
    print(f"searching for {enc_id=}")
    encreuats = utilities.load_json(encreuats_file)
    encreuat = encreuats.get(enc_id, sample)
    rows = 0
    cols = 0
    # càlcul files i columnes
    for word in encreuat["words"]["v"]:
        cols = max(cols, word[1])
        rows = max(rows, word[0]+len(word[2]))
    for word in encreuat["words"]["h"]:
        cols = max(cols, word[1]+len(word[2]))
        rows = max(rows, word[0])
    # building solved crossword
    parsed = [["-" for _ in range(cols)] for _ in range(rows)]
    for word in encreuat["words"]["v"]:
        r, c, w, d = word
        for i, letter in enumerate(w):
            parsed[r+i][c] = letter.upper()
    for word in encreuat["words"]["h"]:
        r, c, w, d = word
        for i, letter in enumerate(w):
            parsed[r][c+i] = letter.upper()
    # ---- building empty crossword ----
    empty = [["-" if letter == "-" else "x" for letter in row] for row in parsed]
    paint = [["" for _ in row] for row in parsed]
    clues_v = {}
    clues_h = {}
    current_clue = 1
    for row in range(rows):
        for col in range(cols):
            # preclue: painting decoration
            for word in encreuat.get("paint", {}).get("h", []):
                if word[0] == row and word[1] <= col < word[1] + word[2]:
                    paint[row][col] = word[3]
            # clues
            clued = False
            for word in encreuat["words"]["v"]:
                if word[0:2] == [row, col]:
                    empty[row][col] = f"{current_clue}"
                    lens = [len(w) for w in word[2].split()]
                    clues_v[current_clue] = {"pos": [word[0], word[1]], "len": sum(lens),
                                             "def": word[3] + f" ({', '.join(f'{x}' for x in lens)})"}
                    clued = True
            for word in encreuat["words"]["h"]:
                if word[0:2] == [row, col]:
                    empty[row][col] = f"{current_clue}"
                    lens = [len(w) for w in word[2].split()]
                    clues_h[current_clue] = {"pos": [word[0], word[1]], "len": sum(lens),
                                             "def": word[3] + f" ({', '.join(f'{x}' for x in lens)})"}
                    clued = True
            if clued:
                current_clue += 1

    # solution hash (sha256)
    solution_string = "".join("".join(cell for cell in row if cell != "-") for row in parsed)
    hashed = sha256(solution_string.encode('utf-8')).hexdigest()

    return {"rows": rows, "cols": cols, "solved": parsed, "empty": empty, "paint": paint,
            "clues": {"h": clues_h, "v": clues_v}, "enc_id": enc_id, "hashed": hashed,
            "title": encreuat.get("title", "Vaia patillada"), "autor": encreuat.get("autor", "Rusca"),
            "date": encreuat.get("date", "2024-12-15"), "comments": encreuat.get("comments", f"Has posat un enllaç que no existeix.<br>No hi ha cap críptic <b>#{enc_id}</b>.<br>Però et perdono. Pots resoldre això, va.")}


def build_dimensions_db(rebuild=False):
    """Calculates keying factors for all crosswords and saves them to a file."""
    utilities.touch_file(dimensions_file)
    dimensions = utilities.load_json(dimensions_file)
    encreuats = utilities.load_json(encreuats_file)
    for enc_id in encreuats:
        if enc_id not in dimensions or rebuild:
            enc = parse_encreuat(enc_id)
            dimensions[enc_id] = [enc["rows"], enc["cols"]]
    utilities.dump_json(dimensions, dimensions_file)


if __name__ == "__main__":
    test_id = "1"
    enc = parse_encreuat(test_id)
    print(enc["rows"], enc["cols"])
    for row in enc["solved"]:
        print("".join([cell for cell in row]))

    build_dimensions_db(True)
    build_keying_factors(True)