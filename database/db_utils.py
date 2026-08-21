import sqlite3
import os
from datetime import datetime, timedelta

from utilities import true_path


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


def get_snapshots_info():
    snapshot_names = ["daily_backup", "weekly_A", "weekly_B"]
    snapshots_info = {}

    now = datetime.now()

    for name in snapshot_names:
        snapshots_info[name] = {}
        path = true_path("./database/snapshots/" + name)
        timestamp = datetime.fromtimestamp(os.path.getmtime(path)) if os.path.exists(path) else None
        snapshots_info[name]["timestamp"] = timestamp

        if name == "daily_backup":
            if timestamp and now - timestamp < timedelta(hours=24):
                snapshots_info[name]["status"] = "OK"
        else:
            if timestamp and now - timestamp < timedelta(days=7):
                snapshots_info[name]["status"] = "OK"

    if any(snapshots_info[name]["status"] == "OK" for name in ["weekly_A", "weekly_B"]):
        for name in ["weekly_A", "weekly_B"]:
            snapshots_info[name]["status"] = snapshots_info[name].get("status", "WAITING")

    return snapshots_info


if __name__ == "__main__":
    print(get_snapshots_info())
