from flask import Blueprint
from flask import render_template, redirect, request

from flask_login import current_user, login_required

kubblive = Blueprint("klive", __name__)


@kubblive.route('/tombaelrei/rounds/<rnum>/')
@kubblive.route('/tombaelrei/rounds/<rnum>/<page>/')
def kubb_live_round(rnum=None, page=None):
    """round info for klive"""
    import klive
    meta = klive.load_meta()
    if page == "ranking":
        teams = klive.load_teams()
        ranking_info = klive.get_ranking(rnum, teams=teams, meta=meta)
        return render_template("/kubb_live/klive_round_ranking.html",
                               rnum=rnum, ranking_info=ranking_info, teams=teams, meta=meta)
    elif page == "def_pairs":
        # TODO authenticate
        def_pairs = klive.def_pairs(rnum)
        return render_template("/kubb_live/klive_def_pairs.html", rnum=rnum, pairs=def_pairs)
    else:
        rounds = klive.load_rounds()
        teams = klive.load_teams()
        all_busy = klive.all_busy(rnum, rounds=rounds, teams=teams)
        return render_template("/kubb_live/klive_round.html",
                               rnum=rnum, teams=teams, round_=rounds.get(rnum, {}), all_busy=all_busy, meta=meta)


@kubblive.route("/tombaelrei/teams/")
@kubblive.route("/tombaelrei/teams/<tnum>/")
@kubblive.route("/tombaelrei/teams/<tnum>/<page>/")
def kubb_live_teams(tnum=None, page=None):
    import klive
    teams = klive.load_teams()
    meta = klive.load_meta()
    if tnum:
        if tnum in teams:
            if page == "stats":
                stats = klive.get_team_stats(tnum, teams=teams)
                return render_template("/kubb_live/klive_team_stats.html",
                                       tnum=tnum, team=teams.get(tnum, {}), teams=teams, stats=stats, meta=meta)
            else:
                has_matches = klive.team_has_matches(tnum)  # only let remove teams with no matches
                return render_template("/kubb_live/klive_team_members.html",
                                       tnum=tnum, team=teams.get(tnum, {}), has_matches=has_matches, meta=meta)
        else:
            return redirect("/tombaelrei/teams/")
    return render_template("/kubb_live/klive_teams.html", teams=teams, meta=meta)


@kubblive.route('/tombaelrei/')
@kubblive.route('/tombaelrei/rounds/')
def kubb_live():
    """proof of concept (provisional implementation): pending sqlite3 integration and competition parametrization"""
    import klive
    rounds = klive.load_rounds()
    meta = klive.load_meta()
    return render_template("/kubb_live/klive_main.html", rounds=rounds, meta=meta)


@kubblive.route('/tombaelrei/edit_match/<rnum>/<match_id>/')
def kubb_live_edit_match(rnum=None, match_id=None):
    if current_user.is_kubb_admin:
        import klive
        match_edit_data = klive.get_match_edit_data(rnum, match_id)
        teams = klive.load_teams()
        meta = klive.load_meta()
        return render_template("/kubb_live/klive_edit_match.html",
                               rnum=rnum, match_edit_data=match_edit_data, teams=teams, match_id=match_id, meta=meta)
    else:
        return redirect('/tombaelrei/rounds/' + rnum)


@kubblive.route('/tombaelrei/add_round/')
def add_round():
    return render_template("/kubb_live/klive_add_round_dialogue.html")


@login_required
@kubblive.route('/klive/ajax/<query>', methods=["POST"])
def klive_ajax(query=None):
    if current_user.is_kubb_admin:
        import klive

        match query:
            case "edit_team":
                success = klive.edit_team(data=request.form)
                return {"success": success}
            case "edit_match_points":
                success = klive.edit_match_points(data=request.form)
                return {"success": success}
            case "edit_match_team":
                success = klive.edit_match_team(data=request.form)
                return {"success": success}
            case "add_team":
                result = klive.append_team()
                success = bool(result)
                return {"success": success, "new_id": result["new_id"] if result else None}
            case "add_match":
                result = klive.append_match(data=request.form)
                success = bool(result)
                return {"success": success, "new_id": result["new_id"] if result else None}
            case "remove_team":
                success = klive.remove_team(data=request.form)
                return {"success": success}
            case "remove_match":
                success = klive.remove_match(data=request.form)
                return {"success": success}
            case "add_round":
                success = klive.add_round(rtype=request.form.get("rtype", "normal"))
                return {"success": success}
            case "remove_round":
                success = klive.remove_round(data=request.form)
                return {"success": success}
    return {"success": False}