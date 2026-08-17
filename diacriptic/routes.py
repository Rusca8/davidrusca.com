from flask import Blueprint
from flask import render_template, redirect

from flask_login import current_user, login_required

import re

from database.user import User

diac = Blueprint("diac", __name__, url_prefix="/diacriptic")


# TODO check all the routes for [**NO!**] /diacriptic/ prefix
# /////////////////// MAIN ROUTES //////////////// #
@diac.route('/')
@diac.route('/arxiu/<date>/')
def diacriptic(date=None):
    import diacriptics as dc
    clues_on_date = dc.get_clues_on_date(date)
    if not clues_on_date:
        if date is None:
            return render_template("/encreuats/diacriptic_today_is_empty.html")
        if re.match("^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$", date):
            date_vibes = True
        else:
            date_vibes = False
        return render_template("/encreuats/diacriptic_404.html",
                               date=date, date_vibes=date_vibes), 404
    else:  # TODO disambiguation screen if more than one clues_on_date
        clue = dc.get_clue(clues_on_date[0])
        help_dots = ""
        help_mask = "0" * sum(clue.n)
        solved = False
        cluetype = ""
        if current_user.is_authenticated:  # get progress
            solve = dc.get_solve(clue.clue_id, current_user.id)
            # append def if they knew it
            if solve:
                if solve.date_solved:
                    solved = True
                if "d" in solve.help_dots:
                    _, analysis_definition = dc.get_definition(params={"clue_id": clue.clue_id, "clue": clue.clue})
                    clue.clue_analysis = analysis_definition
                    cluetype = " ".join(dc.get_cluetype(clue.clue_id))  # TODO multitipus, com l'altre cluetype
                # build help mask for known letters
                help_mask = dc.help_mask(clue, solve)
                help_dots = solve.help_dots
        pistes = [p for p in help_dots]
        known_letters = [i for i, h in enumerate(help_mask) if h == "1"]
        return render_template("/encreuats/diacriptic.html", clue=clue,
                               help_used=help_dots, help_mask=help_mask, pistes=pistes, known_letters=known_letters,
                               solved=solved, cluetype=cluetype, date=date)


@diac.route('/arxiu/')
def diacriptic_arxiu():
    import diacriptics as dc
    this_month = dc.month_calendar()
    arxiu = dc.get_clues_on_interval()
    solves = {}
    if current_user.is_authenticated:
        # TODO soft-code this
        solves = dc.get_solves_by_user(user_id=current_user.id)
        solves |= dc.get_solves_by_user(user_id=current_user.id, focus_month=[2025, 2])
    return render_template("/encreuats/diacriptic_arxiu.html", arxiu=arxiu,
                           months=[this_month], solves=solves)


@diac.route('/tutorial/')
def diacriptic_tutorial():
    return render_template("/encreuats/diacriptic_tutorial.html")


@diac.route('/par/')
def diacriptic_par():
    return render_template("/encreuats/diacriptic_par_explained.html")


# /////////////////// SECONDARY ROUTES ///////////////////// #
@diac.route("/u/")
def user():
    if current_user.is_authenticated:
        return render_template("/encreuats/diacriptic/user_profile.html", logout_origin="diacriptic",
                               username_regex=User.username_pattern)
    else:
        return redirect("/diacriptic")

# /////////////////// API ROUTES /////////////////// #


# /////////////////// ADMIN ROUTES ///////////////// #
@diac.route("/builder")
@diac.route("/builder/<clue_id>")
@login_required
def diacriptic_builder(clue_id=None):
    if current_user.is_admin:
        return render_template("/encreuats/diacriptic_builder.html", preload_clue=clue_id)
    return redirect("/")


@diac.route("/admin")
@login_required
def diacriptic_admin():
    if current_user.is_admin:
        from database.cryptic_clue import CrypticClue
        import diacriptics as dc
        pool = dc.get_clues_in_pool()
        tags = dc.get_tags()
        available_tags = CrypticClue.available_tags
        calendar = dc.calendar()
        arxiu = dc.get_arxiu()
        queue_len = dc.queue_length()
        for day, entries in arxiu.items():
            for da in entries:
                if da.clue_id in pool:
                    pool[da.clue_id].arxiu[day] = da.num

        return render_template("/encreuats/diacriptic_admin.html", pool=pool, tags=tags,
                               available_tags=available_tags, calendar=calendar, arxiu=arxiu, queue_len=queue_len)
    return redirect("/")


@diac.route("/admin/users")
@login_required
def diacriptic_admin_users():
    if current_user.is_admin:
        from database.diacriptic_solve import DiacripticSolve
        solves = DiacripticSolve.count_solves_per_person()
        recent_solves = DiacripticSolve.count_solves_per_person(only_recent=True)
        return render_template("/encreuats/diacriptic_admin_users.html", solves=solves, recent=recent_solves)
    return redirect("/")
