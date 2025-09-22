from flask import Flask
from flask import render_template, redirect, request, make_response, url_for, session
from flask import send_from_directory
from flask_babel import Babel  # traduccions

# standard
import re
import random
from datetime import datetime, timedelta

# internal
import crypto
import utilities
import utilities as utils
import crypto as c

# LOGINS [base stuff coming from realpython's tutorial: https://realpython.com/flask-google-login/]
import json
import os
import requests
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from oauthlib.oauth2 import WebApplicationClient

from database.db import init_app
from database.user import User

from secretos import flask_secret_key, oauth_client as oauth_client_secrets
GOOGLE_CLIENT_ID = oauth_client_secrets["id"]
GOOGLE_CLIENT_SECRET = oauth_client_secrets["secret"]
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"


# MAIN CONFIG
app = Flask(__name__)

# TRANSLATIONS config
app.config['LANGUAGES'] = {'es': 'Español', 'ca': 'Català'}
app.config['BABEL_DEFAULT_LOCALE'] = 'es'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = './translations'  # sense això pythonAnywhere es fa un embolic
babel = Babel(app)

# Recopilar cambios por traducir:     $ pybabel extract -F babel.cfg -o messages.pot .
# Combinar con traducciones antiguas: $ pybabel update -i messages.pot -d translations
#           (traducir novedades en archivo .po de cada idioma)
# Compilar de nuevo:                  $ pybabel compile -d translations
#
# OJO: si te marca [#, fuzzy] es que ha medio-traducido por tí y tienes que quitar eso cuando lo revises.


# LOGINS Config
app.config["REMEMBER_COOKIE_DOMAIN"] = "davidrusca.com"  # remember_cookie settings to please android chrome?
app.config["REMEMBER_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SECURE"] = True
app.config["REMEMBER_COOKIE_SAMESITE"] = "Lax"
app.config["REMEMBER_COOKIE_PATH"] = "/"
app.config["SESSION_COOKIE_PATH"] = "/"
app.secret_key = flask_secret_key or os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "basic"


# DB INITIALIZATION // SCHEMA UPDATE
init_app(app)  # this adds the command to the CLI so that I can use it via Terminal
# check 'db.py' file for instructions on how to run this


# Oauth 2 client setup
oauth_client = WebApplicationClient(GOOGLE_CLIENT_ID)


# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@babel.localeselector
def get_locale():
    """get default or manually chosen language (from https://stackoverflow.com/a/42396494)"""
    # if the user has set up the language manually it will be stored in the session,
    # so we use the locale from the user settings
    try:
        language = session['lang']
    except KeyError:
        language = None
    if language is not None:
        return language
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())


@app.route('/lang/<lang>')
def set_language(lang=None):
    session['lang'] = lang
    return lang


@app.before_request
def before_request():
    """Force https (2024/12, will need it for js-hashing crossword answers)"""
    if app.debug:  # prevents site blockage when local testing (not needed if PyOpenSSL on local)
        return
    if not request.is_secure:
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)


@app.context_processor
def add_global_variables():
    global_vars = {}
    if current_user.is_authenticated:
        global_vars["current_user"] = current_user
    global_vars["current_lang"] = session.get('lang',
                                              request.accept_languages.best_match(app.config['LANGUAGES'].keys()))
    return global_vars


@app.route('/hooks/diacriptic/queue_check')
def diacriptic_queue_check():
    import diacriptics as dc
    return f"{dc.queue_length()}"


@app.route('/')
@app.route('/index')
@app.route('/index/')
def hello_world():
    return render_template("index.html")


@app.route('/u/')
def user_page():
    if current_user.is_authenticated:
        return render_template("user_profile.html", username_regex=User.username_pattern)
    else:
        return render_template("user_none.html")


@app.route('/u/ajax/<query>', methods=["GET", "POST"])
@login_required
def user_ajax(query=None):
    match query:
        case "username_exists":
            username = request.form.get("username")
            return "Y" if User.is_username_taken(username) else "N"
        case "submit_username":
            username = request.form.get("username")
            success = User.change_username(id_=current_user.id, username=username)
            return "Y" if success else "N"
    return "Què vol? User Ajax FAILED i és culpa teva. bahaha"


def get_google_provider_cfg():
    # TODO handle errors if google sends back nonsense
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route("/login/<origin>")
def save_login_origin(origin="home"):
    # store login trigger origin for redirect after login callback
    session["login_origin"] = origin
    return redirect("/login")


@app.route("/login")
def login(origin="main"):
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = oauth_client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def login_callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = oauth_client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )
    # Parse the tokens!
    oauth_client.parse_request_body_response(json.dumps(token_response.json()))
    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = oauth_client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        sub = userinfo_response.json()["sub"]  # "subject" (el seu ID únic de google)
        email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # ········· HANDLING THE USER INFO ··········
    # ------ Refactoring the tutorial example in my way... (so that I can handle db's id generation) ------
    # Try to fetch it from db via oauth details.
    user = User.get_from_oauth("google", sub)
    # Create (and load) if it didn't exist
    if not user:
        user = User.create(name=name, email=email, profile_pic=picture, provider="google", sub=sub)

    # Begin user session in Flask
    login_user(user, remember=True)

    # Send user back to logged in
    login_origin = session.pop("login_origin", "")
    match login_origin:
        case "diacriptic":
            return redirect("/diacriptic/")
        case "diacriptic-arxiu":
            return redirect("/diacriptic/arxiu")
    return redirect(url_for("user_page"))


@app.route("/logout")
@app.route("/logout/<origin>")
@login_required  # nice auto firewall for other things
def logout(origin="home"):
    session.clear()
    session["_remember"] = "clear"  # maybe this?
    logout_user()

    match origin:
        case "diacriptic":
            response = make_response(redirect("/diacriptic/"))
        case _:
            response = make_response(redirect("/"))
    # trying to overwrite the cookie with a bad date instead of just deleting it cause google hallucinates deleted stuff
    response.set_cookie("remember_token", "", expires=datetime.utcnow() - timedelta(days=1),
                        domain=".davidrusca.com")  # got this domain from inspecting the remember_token cookie... (?)
    return response


@app.route('/music')
@app.route('/music/')
def music():
    return render_template("music.html")


@app.route('/anki')
@app.route('/anki/')
def anki():
    return render_template("anki.html")


@app.route('/anki/code')
@app.route('/anki/code/')
def ankicode():
    return render_template("ankicode.html")


@app.route('/docents')
@app.route('/docents/')
@app.route('/docentes')
@app.route('/docentes/')
def docents():
    return render_template("docentes.html")


@app.route('/bmonstres')
@app.route('/bmonstres/')
def bmonstres():
    return render_template("bmonstres.html")


@app.route('/logos')
@app.route('/logos/')
def logos():
    return render_template("logos.html")


@app.route('/ventriloquia')
@app.route('/ventriloquia/')
def ventrad():
    return render_template("ventriloquia.html")


@app.route('/wrapped')
@app.route('/wrapped/')
def wrapped_history():
    from wrapped import extract_data as wrap
    return render_template("wrapped.html", wrap=wrap())


@app.route('/bg')
@app.route('/bg/')
def bg():
    # DEPRECATED URL -> redirect to ./juegos/ (browser will handle old anchors properly)
    return redirect(url_for("juegos")), 301


@app.route('/jocs/')
@app.route('/juegos/')
def juegos():
    return render_template("juegos.html")


@app.route('/bg/ogl')
@app.route('/bg/ogl/')
def bg_ogl():
    return render_template("ogl.html")


@app.route('/climatetracker')
@app.route('/climatetracker/')
def climate_tracker():
    return render_template("climate_tracker.html")


@app.route('/raquel')
@app.route('/raquel/')
def raquel():
    return redirect('/raquel/1')


@app.route('/abril', methods=["GET", "POST"])
@app.route('/abril/', methods=["GET", "POST"])
def abril():
    anims = [f"grup_{chr(c+97).upper()}" for c in range(7)]
    print(anims)
    print("Bon dia")
    if request.method == "GET":
        cavalls = list(range(15))
        random.shuffle(cavalls)
        return render_template("cavalls.html", cavalls=cavalls, anims=anims)
    else:
        # getting the data
        respostes = {}
        anim_noms = {}
        experiencia = None
        for anim in anims:
            respostes[anim] = []
            for key, value in request.form.items():
                if key == "experiencia":
                    experiencia = value
                if key.startswith(anim):
                    if key.endswith("_nom"):
                        anim_noms[anim] = value
                    else:
                        respostes[anim].append(int(key[len(anim):]))
        for key in respostes:
            respostes[key] = sorted(respostes[key])

        bloc_resposta = {}
        for key, val in respostes.items():
            if val:
                bloc_resposta[anim_noms[key]] = val
        print(bloc_resposta)
        utils.add_to_json({"exp": experiencia, "cavalls": bloc_resposta},
                          "./static/json/cavalls_resultats.json")

        return ("La seua contribució a la ciència hípica ha estat degudament enregistrada. <br>"
               "Li ho agraïm sobremesura. ~ Abril <br><br><br><br><br><i>...aigües mil.</i>")


@app.route('/abril/admin/', methods=["GET", "POST"])
@app.route('/abril/admin/', methods=["GET", "POST"])
def abril_admin():
    if request.method == "GET":
        return render_template("cavalls_pwd.html", incorrecte=False)
    else:
        print(request.form)
        try:
            from secretos import abril
        except ImportError:
            return "(pàgina no disponible)"
        if request.form["password"] == abril:
            respostes = utils.load_json("./static/json/cavalls_resultats.json")
            dates = {key: utils.date(float(key)) for key in respostes}
            ref_cavalls = utils.load_json("./static/json/cavalls_ref.json")
            return render_template("cavalls_r.html", respostes=respostes, dates=dates, ref=ref_cavalls)
        else:
            return render_template("cavalls_pwd.html", incorrecte=True)


@app.route('/raquel/<key>')
@app.route('/raquel/<key>/')
def raquel_k(key):
    otros = {"navbar": ["David Ruscalleda", "Inicio", "Estamos", "En", "Construcción"],
             "top": ["Cosas escondidas para Raquel", "Ya veremos cómo te mando hasta aquí..."]}
    if key.isnumeric():
        encoded = 10  # esto decodifica en 16 (Y en 42 lo cual es una maravillosa inesperada coincidencia)
        key = (int(key) + encoded) % 26  # corrijo la previa
        text = c.cesarhtml(c.raquel_text, key)
        otros["title"] = c.cesar("Raquel - Web de David Ruscalleda", key)
        for x in range(len(otros["navbar"])):
            otros["navbar"][x] = c.cesar(otros["navbar"][x], key)
        for x in range(len(otros["top"])):
            otros["top"][x] = c.cesar(otros["top"][x], key)

        return render_template("raquel.html", text=text, otros=otros)
    else:
        otros["top"][0] = "Ay qué pena!"
        otros["top"][1] = "Raquel aún no ha encontrado nada relevante juasjuas querisas"
        otros["title"] = "Raquel aún no ha encontrado nada relevante juasjuas querisas"
        return render_template("raquel.html",
                               text="Bueno, hay <b>numerosas</b> cosas que puedes probar...", otros=otros)


@app.route('/flashmemory/')
@app.route('/flashmemory')
@app.route('/flashmemory/<key>')
@app.route('/flashmemory/<key>/')
@app.route('/flashmemory/<key>/<files_de>')
@app.route('/flashmemory/<key>/<files_de>/')
@app.route('/flashmemory/<key>/<files_de>/<segons>')
@app.route('/flashmemory/<key>/<files_de>/<segons>/')
def flashmemory_debunker(key=26, files_de=10, segons=2):
    try:
        key = min(int(key), 52)
        files_de = min(int(files_de), key)
        segons = int(segons)
    except:
        return render_template("nelson26.html", quantes=26, files_de=10, segons=2)
    return render_template("nelson26.html", quantes=key, files_de=files_de, segons=segons)


@app.route('/memory/ajax/<datos>')
def memory_ajax(datos=None):
    print("getting ajax for memory_games", datos)
    import memory_games as mg
    if datos == "bld_letters":
        scheme = request.args.get("s", "ABCDEFGHIJKLMNOPQRSTUVXZ")
        n = request.args.get("n", "16")
        return mg.new_bld_letters(scheme, n)


@app.route('/memory')
@app.route('/memory/g/<which>')
def memory_games(which=None):
    import memory_games as mg
    scheme = request.args.get("s", "ABCDEFGHIJKLMNOPQRSTUVXZ")
    n = request.args.get("n", "16")
    letters = mg.new_bld_letters(scheme, n)
    return render_template("/js_games/memory_bld.html", n=n, letters=letters, scheme=scheme)


@app.route('/catagrama/admin')
def catagrama_admin():
    import catagrames as cg

    archive = cg.get_quotes_on_archive()
    queue = cg.get_quotes_on_queue(num_after_archive=True)
    pool = cg.get_quotes_pool()
    return render_template('catagrama_admin.html', queue=queue, archive=archive, pool=pool)


@app.route('/catagrama/ajax')
@app.route('/catagrama/ajax/<datos>')
def catagrama_ajax(datos="hello_world"):
    import catagrames as cg
    from secretos import catagrama_ajax

    match datos.split("_"):
        case ["stats", quote_id]:
            stats = cg.get_stats(quote_id, format_times=True)
            return render_template('/catagrama/quote_stats.html', stats=stats, quote_id=quote_id)
        case ["submit", "time", quote_id, solve_time]:
            cg.stats_submit_time(quote_id, solve_time)
            return cg.get_stats(quote_id)
        case ["submit", "choice", quote_id, choice]:
            cg.vq_submit_choice(quote_id, choice)
            return choice
        case ["queue"]:
            queue = cg.get_quotes_on_queue(num_after_archive=True)
            return render_template("/catagrama/queue_table.html", queue=queue)
        case ["pool"]:
            pool = cg.get_quotes_pool()
            return render_template("/catagrama/pool_table.html", pool=pool)
        case ["archive"]:
            archive = cg.get_quotes_on_archive()
            return render_template("/catagrama/archive_table.html", archive=archive)

        case ["queue", quote_id, move]:
            permission = ""
            if request.args.get("p", "") != catagrama_ajax:
                print("failed auth")
                permission = "Requires key"
            else:
                if move == "remove":
                    cg.remove_from_queue(quote_id)
                elif "insert" in move:
                    try:
                        index = int(move[6:])
                        cg.insert_in_queue(quote_id, index)
                    except Exception as e:
                        print("failed queue insertion", e)
                elif move == "release":
                    cg.release_from_position(quote_id)
                elif "fixto" in move:
                    position = move[5:]
                    cg.fix_to_position(quote_id, position)
                else:
                    cg.move_in_queue(quote_id, move)
            queue = cg.get_quotes_on_queue(num_after_archive=True)
            return render_template("/catagrama/queue_table.html", queue=queue, permission=permission)

        case ["pool", quote_id, move]:
            permission = ""
            if request.args.get("p", "") != catagrama_ajax:
                print("failed auth")
                permission = "Requires key"
            else:
                cg.add_to_queue(quote_id, move)
            pool = cg.get_quotes_pool()
            return render_template("/catagrama/pool_table.html", pool=pool, permission=permission)
        case _:
            return "Pernils pernils que venen per AJAX"


@app.route('/catagrama/arxiu')
@app.route('/catagrama/arxiu/')
def catagrama_arxiu():
    import catagrames as cg

    quotes = cg.get_archive()
    today = cg.get_from_archive()
    return render_template("catagrama_arxiu.html", quotes=quotes, today=today)


@app.route('/catagrama/')
@app.route('/catagrama')
@app.route('/catagrama/a/<archive_id>')
@app.route('/catagrama/a/<archive_id>/')
def catagrama(archive_id="Today"):
    import catagrames as cg

    origin = request.args.get("from", "default")

    cita = cg.get_from_archive(archive_id)
    quote_id = cita["id"]
    quote = cita["cita"]
    author = cita["autor"]
    num = cita["num"]

    plain = crypto.unidecode_but(quote.upper(), preserve="Ç·", post_replace={"...": "…"})
    plainphabet, alpha = crypto.new_transposition_alphabet("ABCÇDEFGHIJKLMNOPQRSTUVWXYZ",
                                                           return_plain=True, quote=plain, avoid="Ç")
    cypher = "".join([alpha[plainphabet.index(c)] if c in plainphabet else c for c in plain])
    freqs = crypto.get_frequencies(cypher)

    user_alpha = request.args.get("ua", "")
    if len(user_alpha) != len(plainphabet):
        user_alpha = ""
    t_start = int(request.args.get("st", "0"))

    return render_template("catagrames.html", quote=quote, plain=plain, alpha=alpha, cypher=cypher, freqs=freqs,
                           plainphabet=plainphabet, author=author, num=num, quote_id=quote_id, archive_id=archive_id,
                           user_alpha=user_alpha, t_start=t_start, origin=origin)


@app.route('/catagrama/quote-filtering')
@app.route('/catagrama/quote-filtering/')
def catagrama_viqui():
    import catagrames as cg

    origin = request.args.get("from", "default")
    try:
        from_app_sizes = [int(x) for x in request.args.get("sizes", "x").split("x")]
    except Exception:
        from_app_sizes = [0, 0]

    cita = cg.get_random_vq()
    quote_id = cita["id"]
    quote = cita["cita"]
    author = cita["autor"]
    num = cita["num"]

    plain = crypto.unidecode_but(quote.upper(), preserve="Ç·", post_replace={"...": "…"})
    plainphabet, alpha = crypto.new_transposition_alphabet("ABCÇDEFGHIJKLMNOPQRSTUVWXYZ",
                                                           return_plain=True, quote=plain, avoid="Ç")
    cypher = "".join([alpha[plainphabet.index(c)] if c in plainphabet else c for c in plain])
    freqs = crypto.get_frequencies(cypher)

    choice_stats = cg.get_vq_choices_stats()

    return render_template("catagrames_vq.html", quote=quote, plain=plain, alpha=alpha, cypher=cypher, freqs=freqs,
                           plainphabet=plainphabet, author=author, num=num, quote_id=quote_id, archive_id=quote_id,
                           choice_stats=choice_stats, origin=origin, from_app_sizes=from_app_sizes)


@app.route('/encreuats')
@app.route('/encreuats/')
def encreuats_index():
    import encreuats as ec
    encs = ec.list_for_index()
    return render_template("/encreuats/encreuats_index.html", encs=encs)


@app.route('/encreuats/<enc_id>')
def encreuat(enc_id="sample"):
    import encreuats as ec
    ec = ec.parse_encreuat(enc_id)
    return render_template("/encreuats/encreuat.html", enc=ec, show=False)


@app.route('/diacriptic/')
@app.route('/diacriptic')
@app.route('/diacriptic/arxiu/<date>')
@app.route('/diacriptic/arxiu/<date>/')
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


@app.route('/diacriptic/ajax/<query>', methods=["GET", "POST"])
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


@app.route('/diacriptic/arxiu')
@app.route('/diacriptic/arxiu/')
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


@app.route('/diacriptic/arx/ajax/<query>', methods=["GET", "POST"])
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



@app.route('/diacriptic/tutorial')
def diacriptic_tutorial():
    return render_template("/encreuats/diacriptic_tutorial.html")


@app.route('/diacriptic/par')
def diacriptic_par():
    return render_template("/encreuats/diacriptic_par_explained.html")


@app.route('/diacriptic/explained', methods=["GET", "POST"])
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


@app.route('/diacriptic/b/ajax/<query>', methods=["GET", "POST"])
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


@app.route("/diacriptic/builder")
@app.route("/diacriptic/builder/<clue_id>")
@login_required
def diacriptic_builder(clue_id=None):
    if current_user.is_admin:
        return render_template("/encreuats/diacriptic_builder.html", preload_clue=clue_id)
    return redirect("/")


@app.route('/diacriptic/a/ajax/<query>', methods=["POST"])
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


@app.route("/diacriptic/admin")
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


@app.route("/diacriptic/admin/users")
@login_required
def diacriptic_admin_users():
    if current_user.is_admin:
        from database.diacriptic_solve import DiacripticSolve
        solves = DiacripticSolve.count_solves_per_person()
        recent_solves = DiacripticSolve.count_solves_per_person(only_recent=True)
        return render_template("/encreuats/diacriptic_admin_users.html", solves=solves, recent=recent_solves)
    return redirect("/")


@app.route("/diacriptic/u/")
def user():
    if current_user.is_authenticated:
        return render_template("/encreuats/diacriptic/user_profile.html", logout_origin="diacriptic",
                               username_regex=User.username_pattern)
    else:
        return redirect("/diacriptic")


@app.route('/ktn')
@app.route('/ktn/')
def ktn():
    return redirect('/static/pdf/KendamaTrickNotation1.2.pdf')


@app.route('/ivtest')
@app.route('/ivtest/')
@app.route('/ivtest<temps>')
@app.route('/ivtest/<temps>')
def ivtest(temps=180):
    vlang = request.accept_languages.best_match(['es', 'ca'])
    temps = re.sub("[^0-9]", "", f"{temps}")
    if not temps:
        temps = 180
    return render_template("irregular.html", temps=temps, vlang=vlang)


@app.route('/labs/pmg')
@app.route('/labs/pmg/')
def pmg():
    return render_template("lab_pmg.html")


@app.route('/labs/q/eq')
@app.route('/labs/q/eq/')
def q_eq():
    return render_template("lab_q_eq.html")


@app.route('/jsg/ede')
@app.route('/jsg/ede/')
def jsg_ede():
    return render_template("/js_games/FPEdE.html")


@app.route('/labs/q/chatelier')
@app.route('/labs/q/chatelier/')
def q_chatelier():
    return render_template("lab_q_chatelier.html")


@app.route('/bg/<bg>')
def bg_dots(bg=None):
    nom = random.choice(["Pernil", "Rinoceront", "Iogurt", "Marsupial", "Cacaolat", "Illuminati", "Llimac",
                         "Rosegador", "Esperit", "Paquiderm", "Mussol"])
    cognom = random.choice(["salat", "caducat", "estrafalari", "saborós", "sectari", "d'embogimenta", "llefiscós",
                            "afamat", "misteriós", "refinat", "fastigós", "màgic", "estrident", "sorollós"])
    if bg == "dots":
        return render_template("/protos/dots.html", nom=f"{nom} {cognom}")
    elif bg == "matriculados":
        return render_template("/protos/matriculados.html", nom=f"{nom} {cognom}")
    else:
        return render_template('404.html')


@app.route('/repartir')
def repartiment():
    """TODO muntar una pàgina sencera amb el pdf i una mica d'explicació i futur enllaç a sardanòmetre digital."""
    return redirect('/static/pdf/manual_definitiu_de_repartiment.pdf')


@app.route('/notapap')
@app.route('/papuladora')
def nota_pap():
    return render_template("lab_pap.html")


@app.route('/embed/<page>')
def embed(page=None):
    match page:
        case 'papuladora':
            return render_template("labs/papuladora_embed.html")
        case _:
            return f"Embed '{page}'?"


@app.route('/carreres')
def carreres():
    import carreres as cs
    carreres_info = cs.load()
    return render_template('carreres.html', carreres=carreres_info)


@app.route('/notion/data')
@app.route('/notion/data/')
def notion_data():
    return render_template("./notion/data.html")


@app.route('/braçalets')
@app.route('/braçalets/')
@app.route('/pulseras')
@app.route('/pulseras/')
def pulseras():
    import pulseras as ps
    return render_template("pulseras.html",
                           beads=ps.beads, designs=ps.designs, chrono=ps.get_chrono())


@app.route('/sardanometre')
@app.route('/sardanometre/')
def sardanometre():
    return render_template("sardanometre.html")


@app.route('/anki/d/<file>')
def d_anki(file):
    if file == "verbscat":
        deck = "verbscat.apkg"  # las tildes en nombre de archivo se le hacen bola a pythonanywhere
        nom = "[Rusca] Temps Verbals Catalans.apkg"
    elif file == "irregular":
        deck = "irregular.apkg"
        nom = "[Rusca] Verbs Irregulars Anglès.apkg"
    elif file == "irregular-common":
        deck = "irregular-common.apkg"
        nom = "[Rusca] Verbs Irregulars Anglès (filtrada).apkg"
    elif file == "valencies":
        deck = "valencies.apkg"
        nom = "[Rusca] Valències.apkg"
    elif file == "derivades":
        deck = "derivades.apkg"
        nom = "[Rusca] Regles de Derivació.apkg"
    elif file == "derivades-noarc":
        deck = "derivades-noarc.apkg"
        nom = "[Rusca] Regles de Derivació.apkg"
    elif file == "geometria":
        deck = "geometria.apkg"
        nom = "[Rusca] Perímetres, Àrees i Volums.apkg"
    elif file == "vandalismes":
        deck = "vandalismes.apkg"
        nom = "[Rusca] Vandalismes Matemàtics.apkg"
    elif file == "vandalismes-nolog":
        deck = "vandalismes-nolog.apkg"
        nom = "[Rusca] Vandalismes Matemàtics (no logexp).apkg"
    elif file == "braille":
        deck = "braille.apkg"
        nom = "[Rusca] Braille Español (i Català).apkg"
    elif file == "isot":
        deck = "isot.apkg"
        nom = "[Rusca] Isòtops i Companyia.apkg"
    elif file == "lsc":
        deck = "lsc.apkg"
        nom = "[Rusca] LSC - Llengua de Signes Catalana.apkg"
    elif file == "musculs":
        deck = "musculs.apkg"
        nom = "[Rusca] Músculs.apkg"
    elif file == "capitales":
        deck = "capitales.apkg"
        nom = "[Rusca] Mnemotecnia Capitales (Asia).apkg"
    elif file == "comarques":
        deck = "comarques.apkg"
        nom = "[Rusca] Comarques de Catalunya.apkg"
    elif file == "comarques-mapes":
        deck = "comarques-mapes.apkg"
        nom = "[Rusca] Comarques de Catalunya (mapes).apkg"
    elif file == "comarques-capitals":
        deck = "comarques-capitals.apkg"
        nom = "[Rusca] Comarques de Catalunya (capitals).apkg"
    elif file == "casillero":
        deck = "casillero.apkg"
        nom = "[Rusca] Mnemotecnia Números 0-99.apkg"
    elif file == "intervals":
        deck = "intervals.apkg"
        nom = "[Rusca] Intervals.apkg"
    else:
        return f"El fitxer {file} no l'he pas trobat."
    return send_from_directory("./static/anki/", deck, as_attachment=True, attachment_filename=nom, cache_timeout=0)


@app.route("/privacy")
def privacy_policy():
    return render_template("privacy_policy.html")


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.errorhandler(401)
def unauthorized(e):
    return render_template("401.html"), 401


@app.route('/robots.txt')  # may add more docs here as additional routes (https://stackoverflow.com/a/14054039/5093220)
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


if __name__ == "__main__":  # això la fa córrer en local
    print("running local...")
    app.run(port=8000, debug=True, ssl_context="adhoc")  # s'ha posat exquisit amb el port, no sé
