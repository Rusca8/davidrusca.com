import sqlite3
import os


def get_users():
    root = os.path.dirname(__file__)
    path = os.path.join(root, "sqlite_db")
    con = sqlite3.connect(path)
    cur = con.cursor()

    users = cur.execute('SELECT * FROM user').fetchall()
    con.close()
    return users


def save_snapshot(file_name):
    root = os.path.dirname(__file__)
    production_path = os.path.join(root, "sqlite_db")
    snapshot_path = os.path.join(root, "snapshots", file_name)

    print(": From:", production_path)
    print(": To:", snapshot_path)

    production_db = sqlite3.connect(production_path)
    snapshot_db = sqlite3.connect(snapshot_path)

    print(f"{' Database backup started ':-^40}")
    with snapshot_db:
        production_db.backup(snapshot_db, pages=1000, progress=snapshot_progress)
    print("Backup complete")
    snapshot_db.close()
    production_db.close()
    print("Done")
    print("-" * 40)


def snapshot_progress(status, remaining, total):
    print(f'· {status}: Copied {total-remaining} of {total} pages...')


if __name__ == "__main__":
    save_snapshot("backup1")
