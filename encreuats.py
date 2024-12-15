import utilities

sample = {
    "words": {
        "v": [
            [0, 1, "truita", "-"],
            [4, 5, "de", "-"]
        ],
        "h":[
            [2, 0, "gustosa", ""],
            [5, 0, "patates", "-"]
        ],
    },
}

def parse_encreuat(enc_id=None):
    print(f"searching for {enc_id=}")
    encreuats = utilities.load_json("./hidden/encreuats/encreuats.json")
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
            parsed[r+i][c] = letter
    for word in encreuat["words"]["h"]:
        r, c, w, d = word
        for i, letter in enumerate(w):
            parsed[r][c+i] = letter
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


    return {"rows": rows, "cols": cols, "solved": parsed, "empty": empty, "paint": paint,
            "clues": {"h": clues_h, "v": clues_v}, "enc_id": enc_id,
            "title": encreuat.get("title", "Vaia patillada"), "autor": encreuat.get("autor", "Rusca"),
            "date": encreuat.get("date", "2024-12-15"), "comments": encreuat.get("comments", f"Has posat un enllaç que no existeix.<br>No hi ha cap críptic <b>#{enc_id}</b>.<br>Però et perdono. Pots resoldre això, va.")}

if __name__ == "__main__":
    enc = parse_encreuat("0")
    print(enc["rows"], enc["cols"])
    for row in enc["solved"]:
        print("".join([cell for cell in row]))

