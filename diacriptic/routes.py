from flask import Blueprint
from flask import render_template

from flask_login import current_user

import re

diac = Blueprint("diac", __name__, url_prefix="/diacriptic")


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
