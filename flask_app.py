
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import render_template
from flask import send_from_directory, send_file

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/music/')
def music():
    return render_template("music.html")


@app.route('/anki/')
def anki():
    return render_template("anki.html")


@app.route('/bmonstres/')
def bmonstres():
    return render_template("bmonstres.html")


@app.route('/logos/')
def logos():
    return render_template("logos.html")


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


@app.route('/<patillada>/')
def notfound(patillada):
    return "<h3>Error 42: Esta página aún no existe</h3>" \
           "<p>...o sea sí existe pero existe para decirte que no existe.</p><p>Aigües joan d'estàn.</p>"


if __name__ == "__main__":  # això la fa córrer en local
    app.run()