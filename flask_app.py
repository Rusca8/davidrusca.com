from flask import Flask
from flask import render_template, redirect, request, make_response
from flask import send_from_directory
from flask_babel import Babel  # traduccions

import re
import random

import crypto
import utilities as utils
import crypto as c

app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE'] = 'es'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = './translations'  # sense això pythonAnywhere es fa un embolic
babel = Babel(app)

# Recopilar cambios por traducir:     $ pybabel extract -F babel.cfg -o messages.pot .
# Combinar con traducciones antiguas: $ pybabel update -i messages.pot -d translations
#           (traducir novedades en archivo .po de cada idioma)
# Compilar de nuevo:                  $ pybabel compile -d translations
#
# OJO: si te marca [#, fuzzy] es que ha medio-traducido por tí y tienes que quitar eso cuando lo revises.


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['es', 'ca'])


@app.before_request
def before_request():
    """Force https (2024/12, will need it for js-hashing crossword answers)"""
    if app.debug:  # prevents site blockage when local testing
        return
    if not request.is_secure:
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)


@app.route('/')
@app.route('/index')
@app.route('/index/')
def hello_world():
    return render_template("index.html")


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


@app.route('/encreuats/<enc_id>')
def encreuat(enc_id="sample"):
    import encreuats as enc
    enc = enc.parse_encreuat(enc_id)
    return render_template("/encreuats/encreuat.html", enc=enc, show=False)


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


@app.route('/notion/data')
@app.route('/notion/data/')
def notion_data():
    return render_template("./notion/data.html")


@app.route('/braçalets')
@app.route('/braçalets/')
@app.route('/pulseras')
@app.route('/pulseras/')
def pulseras():
    return render_template("pulseras.html")


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


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


if __name__ == "__main__":  # això la fa córrer en local
    print("running local...")
    app.run(debug=True)
