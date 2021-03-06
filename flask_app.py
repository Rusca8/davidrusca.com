
from flask import Flask
from flask import render_template, redirect, request
from flask import send_from_directory
from flask_babel import Babel  # traduccions

import re

import crypto as c

app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE'] = 'es'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = './translations'  # sense això pythonAnywhere es fa un embolic
babel = Babel(app)

# Recopilar cambios por traducir:     $ pybabel extract -F babel.cfg -o messages.pot .
# Combinar con traducciones antiguas: $ pybabel update -i messages.pot -d translations
#           (traducir novedades en archivo .po de cada idioma)
# Compilar de nuevo:                  $ pybabel compile -d translations
 

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['es', 'ca'])


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


@app.route('/raquel')
@app.route('/raquel/')
def raquel():
    return redirect('/raquel/1')


@app.route('/raquel/<key>')
@app.route('/raquel/<key>/')
def raquel_k(key):
    otros = {}
    otros["navbar"] = ["David Ruscalleda", "Inicio", "Estamos", "En", "Construcción"]
    otros["top"] = ["Cosas escondidas para Raquel", "Ya veremos cómo te mando hasta aquí..."]
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
        return render_template("raquel.html", text="Bueno, hay <b>numerosas</b> cosas que puedes probar...", otros=otros)


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
        temps = 180;
    return render_template("irregular.html", temps=temps, vlang=vlang)


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
    else:
        return f"El fitxer {file} no l'he pas trobat."
    return send_from_directory("./static/anki/", deck, as_attachment=True, attachment_filename=nom, cache_timeout=0)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


if __name__ == "__main__":  # això la fa córrer en local
    app.run()