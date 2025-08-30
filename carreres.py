import utilities


def load():
    """Loading carreres info, overwriting ponds & adding any needed extras"""
    cs = utilities.load_json('./static/json/carreres/carreres.json')
    ponds = utilities.load_json('./static/json/carreres/ponderacions.json')
    for id_, carrera in cs.items():
        print(carrera.get("nom", "GUAT"), get_bat(carrera))
        cs[id_]["ponderacions"]["2025"] = ponds.get(id_, {}).get("pond", [[], []])
        cs[id_]["branca"] = ponds.get(id_, {}).get("branca", "")
        cs[id_]["bat"] = get_bat(carrera)
    return cs


def get_bat(carrera):
    pond_year = max(carrera.get("ponderacions", {}))
    p2, p1 = carrera.get("ponderacions", {}).get(pond_year, [[], []])
    if "T" in p2:
        return "T"
    if "F" in p2 and "DT" in p2:
        return "T"
    if "AE" in p2:
        return "AE"
    if "DA" in p2:
        return "A"
    if "B" in p2 and "CG" in p2:
        return "B"
    if "EdE" in p2:
        return "E"
    if any(x in p2 for x in ["LCAS", "LCAT"]):
        return "H"
    if "CG" in p2:
        return "B"
    if any(x in p2 for x in ["LCG", "LCL"]):
        return "H"
    if any(x in p2 for x in ["F", "B"]):
        return "B"
    if "MCS" in p2:
        return "S"
    return "?"


def build_ponderacions():
    """To be used only locally as a means to update ponderacions.json"""
    import csv

    # load main json info
    cs = utilities.load_json('./static/json/carreres/carreres.json')

    # parse ponderacions from the csv
    with open("./static/csv/ponderacions_2025.csv", encoding="utf-8") as f:
        p_file = csv.reader(f)

        ponderacions = {}
        headers = []
        for i, line in enumerate(p_file):
            if not i:
                headers = line
                print(line)
            if line[0].isnumeric():
                num = line[0]
                nom = line[1]
                branca = line[2]
                p2 = []
                p1 = []
                for j, p in enumerate(line[3:], start=3):
                    if p == "2":
                        p2.append(headers[j])
                    elif p == "1":
                        p1.append(headers[j])
                ponderacions[num] = {"nom": nom, "branca": branca, "pond": [p2, p1]}

    # dump onto json
    utilities.dump_json(ponderacions, "./static/json/carreres/ponderacions.json")


if __name__ == "__main__":
    build_ponderacions()
