from flask import Blueprint
from flask import render_template, redirect, request

from flask_login import current_user, login_required

import re

from database.user import User

diac = Blueprint("diac", __name__, url_prefix="/diacriptic")


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


@diac.route('/explained/', methods=["GET", "POST"])
def diacriptic_explained():
    if request.method == "POST":
        import diacriptics as dc
        clue_id = request.form.get("clue_id")
        word = request.form.get("word")
        clue = request.form.get("clue")
        date = request.form.get("date")
        if clue_id and word and clue:
            cclue = dc.get_clue(clue_id, with_analyses=True)
            if cclue.word == word and cclue.clue == clue:  # solved public clue validation
                return render_template("/encreuats/diacriptic_explained.html", cclue=cclue, date=date)
        print("Explain what?")
    return redirect("/diacriptic")


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
                               username_regex=User.username_pattern, hide_donations=True)
    else:
        return redirect("/diacriptic")


# /////////////////// API ROUTES /////////////////// #
@diac.route('/ajax/<query>', methods=["GET", "POST"])
def diacriptic_ajax(query=None):
    if query is None:
        return "Quin bon dia fa aquí"

    import diacriptics as dc

    match query:
        case "definition":
            user_id = current_user.id if current_user.is_authenticated else None
            clue, analysis_definition = dc.get_definition(params=request.form, user_id=user_id)
            cluetype = " ".join(dc.get_cluetype(request.form.get("clue_id")))  # TODO fer més elegant el multitipus... però n'hi haurà?
            if not analysis_definition:
                return "N"
            return render_template("/encreuats/diacriptic/analysed_text.html",
                                   text=clue, analysis=analysis_definition, cluetype=cluetype)
        case "letter":
            user_id = current_user.id if current_user.is_authenticated else None
            return dc.get_letter(params=request.form, user_id=user_id)  # (public clue status validated inside)
        case "submit":
            clue_id = request.form.get("clue_id")
            clue = request.form.get("clue")
            date = request.form.get("date")
            wordletters = request.form.get("wordletters")
            help_used = request.form.get("help_used")
            help_mask = request.form.get("help_mask")
            if clue_id and clue:
                cclue = dc.get_clue(clue_id, with_analyses=True)
                if cclue.clue != clue:
                    print("Solved a nonexisting clue or something.")
                    return "N"
                # IF CORRECT
                if wordletters == cclue.word.replace(" ", ""):  # ignore whitespace
                    user_id = current_user.id if current_user.is_authenticated else None
                    print(f"{user_id or 'Someone'} solved clue #{clue_id}")
                    if user_id:
                        dc.submit_solve(clue_id, user_id)
                    cclue.clue_analysis = {k: v for k, v in cclue.clue_analysis.items() if k == "def"}
                    return render_template("/encreuats/diacriptic_solved.html", cclue=cclue,
                                           help_used=help_used, help_mask=help_mask, date=date)
                else:
                    return "Incorrect"
    print("WTF ya doin' here")
    return "N"


@diac.route('/arx/ajax/<query>', methods=["GET", "POST"])
def diacriptic_arxiu_ajax(query=None):
    if query is None:
        return "Arxiu Ajax Fail I guess. Aviseu al rusca si de cas."

    import diacriptics as dc

    match query:
        case "get_month":
            month = request.form.get("month", None)
            year = request.form.get("year", None)
            try:
                the_month = dc.month_calendar(int(year), int(month))
                arxiu = dc.get_clues_on_interval(f"{year}-{month:0>2}-00", f"{year}-{month:0>2}-32")
                print(arxiu)
                solves = {}
                if current_user.is_authenticated:
                    solves = dc.get_solves_by_user(current_user.id, focus_month=[year, month])
                return render_template("/encreuats/diacriptic/arxiu_month.html", arxiu=arxiu,
                                       month=the_month, solves=solves)
            except Exception as e:
                print(e, "on get_month")
                return "N"

    print("Nonono")
    return "N"


@diac.route('/b/ajax/<query>', methods=["GET", "POST"])
@login_required
def diacriptic_builder_ajax(query=None):
    if current_user.is_admin:
        import diacriptics as dc
        match query:
            case "siblings":  # clues with the same word
                word = request.form.get("word", "")
                siblings = dc.get_siblings(word)
                return render_template("/encreuats/diacriptic/siblings_table.html",
                                       siblings=siblings)
            case "load":
                clue_id = request.form.get("clue_id", "")
                with_analyses = request.form.get("with_analyses", False)
                print(f"Loading {clue_id} (analyses: {with_analyses})")
                if not clue_id:
                    return "clue_id not provided"
                return dc.get_clue(clue_id, with_analyses=with_analyses, to_dict=True) or "N"
            case "create":
                success = dc.create(params=request.form)
                return "Y" if success else "N"
            case "update":
                success = dc.update(params=request.form)
                return "Y" if success else "N"
        return "AJAX diac builder - No vol res? Doncs no li dono res."
    return "Not the one I expected, tbh", 401


@diac.route('/a/ajax/<query>', methods=["POST"])
@login_required
def diacriptic_admin_ajax(query=None):
    if current_user.is_admin:
        import diacriptics as dc
        match query:
            case "add_tag":
                tag = request.form.get("tag")
                clue_id = request.form.get("clue_id")
                success = dc.add_tag(clue_id, tag)
                if success:
                    return {"clue_id": clue_id, "tag": tag}
                else:
                    return "N"
            case "remove_tag":
                tag = request.form.get("tag")
                clue_id = request.form.get("clue_id")
                success = dc.remove_tag(clue_id, tag)
                if success:
                    return {"clue_id": clue_id, "tag": tag}
                else:
                    return "N"
            case "assign_date":
                clue_id = request.form.get("clue_id")
                date = request.form.get("date")
                pwd = request.form.get("pwd")
                success = dc.assign_date(clue_id, date, pwd)
                if success:
                    return "Y"  # TODO return html of pool row to update
                else:
                    return "N"
            case "assign_num":
                clue_id = request.form.get("clue_id")
                num = request.form.get("num")
                success = dc.assign_num(clue_id, num)
                if success:
                    return "Y"  # TODO return html of pool row to update
                else:
                    return "N"
            case "remove_date":
                clue_id = request.form.get("clue_id")
                date = request.form.get("date")
                pwd = request.form.get("pwd")
                success = dc.remove_date(clue_id, date, pwd)
                if success:
                    return "Y"  # TODO return html of pool row to update
                else:
                    return "N"
        return "AJAX admin - No vol res?"
    return "No parlar amb desconeguts. Recorda no parlar amb desconeguts..."


# /////////////////// ADMIN ROUTES ///////////////// #
@diac.route("/builder/")
@diac.route("/builder/<clue_id>")
@login_required
def diacriptic_builder(clue_id=None):
    if current_user.is_admin:
        return render_template("/encreuats/diacriptic_builder.html", preload_clue=clue_id)
    return redirect("/")


@diac.route("/admin/")
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


@diac.route("/admin/users/")
@login_required
def diacriptic_admin_users():
    if current_user.is_admin:
        from database.diacriptic_solve import DiacripticSolve
        solves = DiacripticSolve.count_solves_per_person()
        recent_solves = DiacripticSolve.count_solves_per_person(only_recent=True)
        return render_template("/encreuats/diacriptic_admin_users.html", solves=solves, recent=recent_solves)
    return redirect("/")
