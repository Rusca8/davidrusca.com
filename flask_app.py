
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import render_template, redirect
from flask import send_from_directory

import crypto as c

app = Flask(__name__)


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


@app.route('/anki/d/<file>')
def d_anki(file):
    if file == "verbscat":
        deck = "verbscat.apkg"  # las tildes en nombre de archivo se le hacen bola a pythonanywhere
        nom = "[Rusca] Temps Verbals Catalans.apkg"
    elif file == "irregular":
        deck = "irregular.apkg"
        nom = "[Rusca] Verbs Irregulars Anglès.apkg"
    elif file == "valencies":
        deck = "valencies.apkg"
        nom = "[Rusca] Valències.apkg"
    elif file == "derivades":
        deck = "derivades.apkg"
        nom = "[Rusca] Regles de Derivació.apkg"
    elif file == "braille":
        deck = "braille.apkg"
        nom = "[Rusca] Braille Español (i Català).apkg"
    elif file == "lsc":
        deck = "lsc.apkg"
        nom = "[Rusca] LSC - Llengua de Signes Catalana.apkg"
    elif file == "capitales":
        deck = "capitales.apkg"
        nom = "[Rusca] Mnemotecnia Capitales (Asia).apkg"
    else:
        return f"El fitxer {file} no l'he pas trobat."
    return send_from_directory("./static/anki/", deck, as_attachment=True, attachment_filename=nom, cache_timeout=0)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


if __name__ == "__main__":  # això la fa córrer en local
    app.run()