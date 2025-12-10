tops = {
        2025: {
            "artists": {
                1: "Lizzy McAlpine",
                2: "dodie",
                3: "OMAC",
                4: "Alba Careta",
                5: "La Oreja de Van Gogh",
                6: "Jacob Collier",
            },
            "songs": {
                1: "A Little Bit of Everything",
                2: "Quan te'n vas",
                3: "Got Weird",
                4: "ceilings",
                5: "No és veritat",
                6: "Same Boat",
            }
        },
        2024: {
            "artists": {
                1: "dodie",
                2: "Lizzy McAlpine",
                3: "Alba Careta",
                4: "El Pony Pisador",
                5: "OMAC"
            },
            "songs": {
                1: "Got Weird",
                2: "all my ghosts",
                3: "ceilings",
                4: "Pancakes for Dinner",
                5: "She"
            }
        },
        2023: {
            "artists": {
                1: "Lizzy McAlpine",
                2: "dodie",
                3: "La Oreja de Van Gogh",
                4: "Jacob Collier",
                5: "Clara Schumann"
            },
            "songs": {
                1: "all my ghosts",
                2: "ceilings",
                3: "A Little Bit of Everything",
                4: "Same Boat",
                5: "orange show speedway"
            }
        },
        2022: {
            "artists": {
                1: "Kalafina",
                2: "dodie",
                3: "Imogen Heap",
                4: "Jacob Collier",
                5: "La Oreja de Van Gogh"
            }
        },
        2021: {
            "songs": {
                1: "光るなら"
            }
        }
    }


def extract_data():
    result = {}
    artists = {}
    last_top_artists = {}
    songs = {}
    last_top_songs = []
    for year in sorted(tops):
        current_top_artists = {}
        current_top_songs = {}
        result[year] = {"artists": [], "songs": []}
        for n in range(1, 6):  # each position
            # artists
            artist = tops[year].get("artists", {}).get(n, "-")
            if artist == "-":
                result[year]["artists"].append(["-", n, "-", "null"])
            else:
                current_top_artists[artist] = n
                if artist not in artists:
                    artists[artist] = {"max": n}
                    change = "new"
                elif artist not in last_top_artists:
                    change = "back"
                else:
                    last_index = last_top_artists[artist]
                    change = last_index - n
                result[year]["artists"].append([change_text(change), n, artist, change_class(change)])
        for n in range(1, 6):
            # songs
            song = tops[year].get("songs", {}).get(n, "-")
            if song == "-":
                result[year]["songs"].append(["-", n, "-", "null"])
            else:
                current_top_songs[song] = n
                if song not in songs:
                    songs[song] = {"max": n}
                    change = "new"
                elif song not in last_top_songs:
                    change = "back"
                else:
                    last_index = last_top_songs[song]
                    change = last_index - n
                result[year]["songs"].append([change_text(change), n, song, change_class(change)])
        last_top_artists = current_top_artists
        last_top_songs = current_top_songs
    return result


def change_class(change):
    return change if change in ["new", "back"] else "p" if int(change) > 0 else "n" if int(change) < 0 else "0"


def change_text(change):
    if change == "new":
        return "☆"
    elif change == "back":
        return "❖"
    elif change == 0:
        return "="
    else:
        return change if change < 0 else f"+{change}"


if __name__ == "__main__":
    print(extract_data())
