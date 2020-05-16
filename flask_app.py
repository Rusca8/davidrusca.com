
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/bmonstres/')
def bmonstres():
    return render_template("bmonstres.html")

@app.route('/logos/')
def logos():
    return render_template("logos.html")

@app.route('/<patillada>/')
def notfound(patillada):
    return "<h3>Error 42: Esta página aún no existe</h3><p>...o sea sí existe pero existe para decirte que no existe.</p><p>Aigües joan d'estàn.</p>"

if __name__ == "__main__":  # això la fa córrer en local
    app.run()