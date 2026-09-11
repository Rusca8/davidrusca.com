from threading import RLock

import utilities
from utilities import Reversor as Rev

klive_lock = RLock()
klive_root = "./static/json/kubb_live/tombaelrei_2026/"
teams_file = klive_root + "teams.json"
rounds_file = klive_root + "rounds.json"
meta_file = klive_root + "meta.json"


def load_meta():
    with klive_lock:
        meta = utilities.load_json(meta_file)
    return meta


def load_teams():
    with klive_lock:
        teams = utilities.load_json(teams_file)
    return teams.get("teams", {})


def load_rounds():
    with klive_lock:
        rounds = utilities.load_json(rounds_file)
    return rounds.get("rounds", {})


def team_has_matches(tnum, rounds=None):
    rounds = rounds or load_rounds()
    for round_ in rounds.values():
        for match_ in round_.get("matches", {}).values():
            if tnum in match_.get("teams", []):
                return True
    return False


def get_scores(rnum=None, rounds=None, teams=None, meta=None):
    """Retorna la taula de puntuacions dels equips.
    rnum: Número de Ronda (ignora rondes "futures")
    rounds: informació dels partits (si no és donada, es carrega del json)
    teams: informació dels equips (si no és donada, es carrega del json)
    meta: info addicional sobre el campionat (i.e. manera de puntuar, etc)
    """
    rounds = rounds or load_rounds()
    teams = teams or load_teams()
    meta = meta or load_meta()

    king_worth_extra = meta.get("king_worth_extra", 2)

    scores = {}

    # prepopulate teams
    for team in teams:
        scores[team] = {"id": team, "P": 0, "K": 0, "oponents": [], "-K": 0, "SOS": 0}

    # get main scores
    for id_, round_ in rounds.items():
        if rnum and int(id_) > int(rnum):  # ignore "future" rounds
            continue
        for match in round_.get("matches", {}).values():
            match_teams = match.get("teams", [])
            match_result = match.get("result", [])
            if len(match_teams) == 2 and len(match_result) == 2:
                if all(x.isnumeric() for x in match_result) and all(x in teams for x in match_teams):
                    # precalc extra points from winning the match (for when king is worth more than 1 point)
                    extra_from_king = [king_worth_extra if match_result[0] == "6" else 0,
                                       king_worth_extra if match_result[1] == "6" else 0]
                    # KCSS-ish (may have extra from king)
                    scores[match_teams[0]]["K"] += int(match_result[0]) + extra_from_king[0]
                    scores[match_teams[1]]["K"] += int(match_result[1]) + extra_from_king[1]
                    # Tournament Points
                    if match_result[0] == "6":
                        scores[match_teams[0]]["P"] += 1
                    elif match_result[1] == "6":
                        scores[match_teams[1]]["P"] += 1
                    # register oponents
                    scores[match_teams[0]]["oponents"].append(match_teams[1])
                    scores[match_teams[1]]["oponents"].append(match_teams[0])
                    # KC scored by oponents against the team
                    scores[match_teams[0]]["-K"] += int(match_result[1]) + extra_from_king[1]
                    scores[match_teams[1]]["-K"] += int(match_result[0]) + extra_from_king[0]

    # calculate Strength of Schedule
    for team, stats in scores.items():
        # add all oponents KC
        for oponent in stats["oponents"]:
            scores[team]["SOS"] += scores[oponent]["K"]
        # subtract KC scored against the team
        scores[team]["SOS"] -= scores[team]["-K"]

    return scores


def get_ranking(rnum=None, teams=None, meta=None):
    teams = teams or load_teams()
    meta = meta or load_meta()
    rounds = load_rounds()

    round_type = rounds.get(rnum, {}).get("type", "normal")

    # get scores
    scores = get_scores(rnum=rnum, rounds=rounds, teams=teams, meta=meta)

    # generate ranking
    finals_ranking = get_finals_ranking(rnum, rounds=rounds)
    ranking = generate_ranking(scores, teams=teams, finals=finals_ranking, sorting_style=meta.get("sorting_style"))

    # count finished matches
    finished_matches = count_finished_matches(rnum=rnum, rounds=rounds)

    return {"round_type": round_type, "ranking": ranking, "finished_matches": finished_matches, "scores": scores}


def winner_of_a_score(score=None):
    if score is None:
        return 0
    if score[1] == "K":
        return 0
    if score[0] == "K":
        return 1
    if score[1] > score[0]:
        return 1
    else:
        return 0


def get_finals_ranking(rnum, rounds=None):
    rounds = rounds or load_rounds()
    round_ = rounds.get(rnum, {})
    finals_ranking = ["", "", "", ""]
    if round_.get("type") == "final":
        for match_ in round_.get("matches", {}).values():
            final_status = match_.get("final")
            if final_status in ["F", "Q"]:
                result = match_.get("result", ["K", "K"])
                teams = match_.get("teams", ["", ""])
                if final_status == "F":
                    if winner_of_a_score(result) == 1:  # comparing strings but it's fine here
                        finals_ranking[0], finals_ranking[1] = teams[1], teams[0]
                    else:
                        finals_ranking[0], finals_ranking[1] = teams
                elif match_.get("final") == "Q":
                    if winner_of_a_score(result) == 1:  # comparing strings but it's fine here
                        finals_ranking[2], finals_ranking[3] = teams[1], teams[0]
                    else:
                        finals_ranking[2], finals_ranking[3] = teams
    return [f for f in finals_ranking if f]


def ranking_sorting_params(sorting_style=None):
    """Returns dictionary containing "sorting_priorities" and "tied_when".
    sorting_priorities: A list of stat_codes representing the priority of each statistic on the ranking generation
    tied_when: A list of stat_codes representing which statistics need to match in order for it to be a technical tie
    """
    match sorting_style:
        case "PKS":
            return {"sorting_priorities": ["P", "K", "SOS", "RevID"],
                    "tied_when": ["P", "K", "SOS"]}
        case "SOS":
            return {"sorting_priorities": ["SOS", "RevID"],
                    "tied_when": ["SOS"]}
        case "KSP" | _:
            return {"sorting_priorities": ["K", "SOS", "P", "RevID"],
                    "tied_when": ["K", "SOS", "P"]}


def build_stat_for_sorting(stats, stat_code):
    match stat_code:
        case "RevID":
            return Rev(f'{stats["id"]:0>3}')
        case _:
            built_stat = stats.get(stat_code)
            if built_stat is not None:
                return built_stat
            print("the stat_code", stat_code, "isn't defined")
            return built_stat


def generate_ranking(scores, teams=None, finals=None, sorting_style="PKS"):
    if finals is None:
        finals = []
    teams = teams or load_teams()
    ranking = []
    rank = 0
    ranks_skipped = 0  # if more than one team on the same rank, next non-tied will need to add the amount of extras

    s_params = ranking_sorting_params(sorting_style=sorting_style)
    s_priorities = s_params.get("sorting_priorities", [])
    s_tied_when = s_params.get("tied_when", [])
    last = {s_code: None for s_code in s_tied_when}

    # force extract finalists (if round is final)
    for finalist in finals:
        team = scores.get(finalist)
        team_name = teams.get(team["id"]).get("name", "(Equip)")
        rank += 1
        ranking.append({"rank": rank, "id": team["id"], "name": team_name, "P": team["P"], "K": team["K"], "SOS": team["SOS"]})

    # generate swiss ranking
    for team in reversed(
            sorted(scores.values(), key=lambda stats: [build_stat_for_sorting(stats, sc) for sc in s_priorities])):
        if team["id"] in finals:
            continue
        team_name = teams.get(team["id"]).get("name", "(Equip)")
        current = {s_code: build_stat_for_sorting(team, s_code) for s_code in s_tied_when}
        if any(last[sc] != current[sc] for sc in s_tied_when):
            rank += 1 + ranks_skipped
            ranks_skipped = 0
        else:
            ranks_skipped += 1
        last = current
        ranking.append({"rank": rank, "id": team["id"], "name": team_name, "P": team["P"], "K": team["K"], "SOS": team["SOS"]})
    return ranking


def get_team_stats(tnum, rounds=None, teams=None, meta=None):
    rounds = rounds or load_rounds()
    teams = teams or load_teams()
    meta = meta or load_meta()

    # calculate scores
    scores = get_scores(rounds=rounds, teams=teams, meta=meta)

    # get matches
    matches = []
    for rnum, round in rounds.items():
        for match_id, match in round.get("matches", {}).items():
            if tnum in match.get("teams", {}):
                matches.append(match)
                matches[-1]["rnum"] = rnum
                matches[-1]["id"] = match_id

    # get sos_table
    sos_table = {}
    for oponent in scores.get(tnum, {}).get("oponents", []):
        sos_table[oponent] = scores.get(oponent, {}).get("K", 0)

    return {"scores": scores.get(tnum, {}), "matches": matches, "sos_table": sos_table}


def count_finished_matches(rnum=None, rounds=None):
    rounds = rounds or load_rounds()

    finished_matches = {}
    for id_, round_ in rounds.items():
        if rnum and int(id_) > int(rnum):  # ignore "future" rounds
            continue
        finished_matches[id_] = {"total": 0, "finished": 0}
        for match in round_.get("matches", {}).values():
            finished_matches[id_]["total"] += 1
            if "6" in match.get("result", []):
                finished_matches[id_]["finished"] += 1

    return finished_matches


def edit_team(data=None):
    if data is None:
        return False
    if all(x in data for x in ["tnum", "name", "members"]):
        import json
        tnum = data["tnum"]
        name = data["name"]
        members = json.loads(data["members"])

        with klive_lock:
            teams = utilities.load_json(teams_file)
            if tnum in teams["teams"]:
                teams["teams"][tnum]["name"] = name
                teams["teams"][tnum]["members"] = members
                utilities.dump_json(teams, filename=teams_file)
            return True
    return False


def edit_match_points(data=None):
    if data is None:
        return False
    if all(x in data for x in ["rnum", "match_id", "team_index", "points"]):
        rnum = data["rnum"]
        match_id = data["match_id"]
        team_index = data["team_index"]
        points = data["points"]

        with klive_lock:
            rounds = utilities.load_json(rounds_file)
            match_ = rounds["rounds"].get(rnum, {}).get("matches", {}).get(match_id, {})
            if match_ and "result" in match_:
                rounds["rounds"][rnum]["matches"][match_id]["result"][int(team_index)] = points

                utilities.dump_json(rounds, filename=rounds_file)
                return True
    return False


def edit_match_team(data=None):
    print(data)
    if data is None:
        return False
    if all(x in data for x in ["rnum", "match_id", "team_index", "team_id"]):
        rnum = data["rnum"]
        match_id = data["match_id"]
        team_index = data["team_index"]
        team_id = data["team_id"]

        with klive_lock:
            rounds = utilities.load_json(rounds_file)
            match = rounds["rounds"].get(rnum, {}).get("matches", {}).get(match_id, {})
            if match and "teams" in match:
                rounds["rounds"][rnum]["matches"][match_id]["teams"][int(team_index)] = team_id
                print(rounds["rounds"][rnum])
                utilities.dump_json(rounds, filename=rounds_file)
                return True
    return False


def append_team():
    with klive_lock:
        teams = utilities.load_json(teams_file)
        if "teams" in teams:
            new_id = max(int(id_) for id_ in teams["teams"]) + 1 if teams["teams"] else 1
            teams["teams"][new_id] = {
                "name": "",
                "members": [],
            }
            utilities.dump_json(teams, filename=teams_file)
            return {"new_id": new_id}
    return False


def append_match(data=None):
    if data is None:
        return False
    rnum = data.get("rnum")
    if rnum:
        with klive_lock:
            rounds = utilities.load_json(rounds_file)
            if rnum in rounds["rounds"] and "matches" in rounds["rounds"][rnum]:
                matches = rounds["rounds"][rnum]["matches"]
                new_id = max(int(id_) for id_ in matches) + 1 if matches else 1
                matches[new_id] = {"teams": ["", ""], "result": ["K", "K"]}

                utilities.dump_json(rounds, filename=rounds_file)
                return {"new_id": new_id}
    return False


def remove_team(data=None):
    if data is None:
        return False
    if all(x in data for x in ["team_id"]):
        team_id = data["team_id"]

        with klive_lock:
            teams = utilities.load_json(teams_file)

            if team_id in teams["teams"]:
                teams["teams"] = {id_: team for id_, team in teams["teams"].items() if id_ != team_id}

                utilities.dump_json(teams, filename=teams_file)
                return True
    return False


def remove_match(data=None):
    if data is None:
        return False
    if all(x in data for x in ["rnum", "match_id"]):
        rnum = data["rnum"]
        match_id = data["match_id"]

        with klive_lock:
            rounds = utilities.load_json(rounds_file)
            if rnum in rounds["rounds"] and "matches" in rounds["rounds"][rnum]:
                matches = rounds["rounds"][rnum]["matches"]
                rounds["rounds"][rnum]["matches"] = {id_: match for id_, match in matches.items() if id_ != match_id}

                utilities.dump_json(rounds, filename=rounds_file)
                return True
    return False


def add_round(rtype):
    if rtype in ["normal", "final"]:
        with klive_lock:
            rounds = utilities.load_json(rounds_file)
            new_id = max(int(id_) for id_ in rounds["rounds"]) + 1 if rounds["rounds"] else 1
            if rtype == "final":
                pre_matches = {"1": {"final": "F", "teams": ["", ""], "result": ["K", "K"]},
                               "2": {"final": "Q", "teams": ["", ""], "result": ["K", "K"]}
                               }
            else:
                pre_matches = {}

            rounds["rounds"][new_id] = {"type": rtype, "matches": pre_matches}

            utilities.dump_json(rounds, filename=rounds_file)
            return True
    return False


def remove_round(data=None):
    if data is None:
        return False
    if all(x in data for x in ["rnum"]):
        rnum = data["rnum"]

        with klive_lock:
            rounds = utilities.load_json(rounds_file)
            if rnum in rounds["rounds"]:
                rounds["rounds"] = {id_: round_ for id_, round_ in rounds["rounds"].items() if id_ != rnum}

                utilities.dump_json(rounds, filename=rounds_file)
                return True
    return False


def get_match_edit_data(rnum, match_id):
    rounds = load_rounds()

    round_ = rounds.get(rnum, {})
    matches = round_.get("matches", {})
    match_ = matches.get(match_id, {})

    match_edit_data = {}

    if not match_:
        return {}

    match_edit_data["type"] = round_.get("type", "normal")
    match_edit_data["match_teams"] = match_.get("teams", ["", ""])
    match_edit_data["result"] = match_.get("result", ["K", "K"])

    match_edit_data["busy_teams"] = set()
    for m in matches.values():
        match_edit_data["busy_teams"].update(m.get("teams", []))

    return match_edit_data


def all_busy(rnum, rounds=None, teams=None):
    rounds = rounds or load_rounds()
    teams = teams or load_teams()

    busy_teams = set()
    for match in rounds.get(rnum, {}).get("matches", {}).values():
        busy_teams.update(match.get("teams", []))

    return all(t in busy_teams for t in teams)


def default_pairs(ranking, past_games, byes):
    pairs = []
    playing = []
    bye = None
    # choose bye
    if len(ranking) % 2:
        for team in reversed(ranking):
            if team not in byes:
                bye = team
                byes.append(team)
                break
    # choose pairs
    for team in ranking:
        if team in playing or team == bye:
            continue
        options = [t for t in ranking if t not in playing and t not in past_games[team] and t != team and t != bye]
        print("options for ", team, "::", options, " - already played", past_games[team])
        if options:
            pairs.append([team, options[0]])
            playing += [team, options[0]]
            print("new pair", [team, options[0]])
        else:
            print(f"!! TEAM {team} CAN'T PLAY NEW OPONENT !!")
            print("YOU'LL NEED TO MANAGE THIS")
    return pairs


def simulate_swiss_matches(teams, n_rounds=3, deviation=40):
    import random

    # init
    print("······· Simulating swiss tournament matches ·······")
    print("Teams: ", teams)

    # team strengths
    print("\n······ Choosing team strengths ·····")
    team_strengths = {t: random.randint(1, 100) for t in teams}
    print("".join(f"{t:>5}" for t in team_strengths))
    print("".join(f"{s:>5}" for s in team_strengths.values()))

    # ranking
    ranking = [t for t in teams]
    past_games = {t: [] for t in teams}
    byes = []

    proxy_scores = {t: 0 for t in teams}
    for r in range(n_rounds):
        # current ranking
        ranking = [t for t, _ in sorted(proxy_scores.items(), key=lambda x: [Rev(x[1]), x[0]])]

        print(f"\n\n{' ROUND':/>35} {r:/<35}")
        print(f"\n{' Current ranking ':·^70}")
        t_strings = ["Team   "]
        s_strings = ["Points "]
        for t in ranking:
            t_strings += f"{t:>5} "
            s_strings += f"{proxy_scores[t]:>5} "
        print("".join(t_strings[:-1]))
        print("".join(s_strings[:-1]), "\n")

        # get matches
        new_games = default_pairs(ranking, past_games, byes)

        # execute matches
        for game in new_games:
            t0, t1 = game
            past_games[t0].append(t1)
            past_games[t1].append(t0)
            increments = [random.randint(0, deviation) for _ in game]
            delta = (team_strengths[t0] + increments[0]) - (team_strengths[t1] + increments[1])
            if delta >= 0:  # team 0 wins
                proxy_scores[t0] += 6
                proxy_scores[t1] += random.randint(0, 5)
            else:
                proxy_scores[t1] += 6
                proxy_scores[t0] += random.randint(0, 5)


def def_pairs(rnum):
    return "NOT DONE YET BAHAHA"


if __name__ == "__main__":
    teams = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    simulate_swiss_matches(teams, n_rounds=6, deviation=40)