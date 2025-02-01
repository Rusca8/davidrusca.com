# (base behavior from realpython.com ft.) http://flask.pocoo.org/docs/1.0/tutorial/database/
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            "./database/sqlite_db",
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.execute('PRAGMA foreign_keys = ON')  # without THIS it wouldn't check foreign key constraints (!)
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource("./database/schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


def prepopulate():
    """Inserta els ítems que hi han de ser des del principi (e.g. tipus de bloc d'anàlisi i tal)."""
    db = get_db()
    print("Prepopulating the database...")
    # autor (id=0 seré jo, perquè cryptic_clue ho agafa de default)
    print("· Trying to give autor_id=0 to David Ruscalleda")
    db.execute(
        "INSERT OR IGNORE INTO autor (id, name) "  # or ignore means "if there's any conflict, don't"
        "VALUES (?, ?)",                               # ANY conflict, but this will be curated, so it's fine
        (0, "David Ruscalleda")
    )
    db.commit()

    # analysis_block_type
    print("· Making sure all block_types exist")
    block_types = {"def": "Definició", "ind": "Indicador", "mat": "Material",
                   "wop": "Joc de paraules", "res": "Resposta", "hid": "Text amagat"}
    for btype, name in block_types.items():
        db.execute(
            "INSERT OR IGNORE INTO analysis_block_type (type, name) "
            "VALUES (?, ?)",
            (btype, name)
        )
        db.commit()
    # cryptic_clue_analysis_type (clue, solution)
    print("· Making sure all analysis_types exist")
    for type_ in ["clue", "solution"]:
        db.execute(
            "INSERT OR IGNORE INTO cryptic_clue_analysis_type (type) "
            "VALUES (?)",
            (type_,)  # important comma over here (makes it a tuple)
        )
        db.commit()
    # clue_direction
    ...
    # user_autor (0 = oauth_yo)
    ...
    # login_provider
    print("· Making sure all login_providers exist")
    for provider in ["google"]:
        db.execute(
            "INSERT OR IGNORE INTO login_provider (provider) "
            "VALUES (?)",
            (provider,)  # important comma over here (makes it a tuple)
        )
        db.commit()
    # cryptic_clue_tag_type
    print("· Making sure all cryptic_clue_tag_types exist")
    from database.cryptic_clue import CrypticClue
    for tag_type, tag_data in CrypticClue.available_tags.items():
        db.execute(
            "INSERT OR IGNORE INTO cryptic_clue_tag_type (type, description)"
            "VALUES (?, ?)",
            (tag_type, tag_data["description"],)
        )
        db.commit()


@click.command("init-db")  # para ejecutarlo en la terminal: $ flask --app flask_app init-db
@with_appcontext
def init_db_command():
    init_db()
    prepopulate()
    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
