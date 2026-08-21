import os
import pytz
from datetime import datetime, timedelta

from utilities import true_path
from database.db_utils import save_snapshot


def wake_snapshotter():
    """PythonAnywhere will run task at H:30 · Snapshotter will only work if 3:30 Spain. (H=3)"""
    print("\n::: Waking up snapshotter... :::")
    now = datetime.now(pytz.timezone("Europe/Madrid"))

    if now.hour != 3:
        print("- Not my hour, not my circus. Back to sleep... zzz")
        return

    print("- Well, well, well... it quite seems like paparazzi time.")

    # Daily snapshot (executes every day at 3:30AM spain, will overwrite after 24h)
    print("\n::: Executing daily backup... :::")
    save_snapshot("daily_backup")

    # Weekly rotation (alternates A/B to always have a 1 week old snapshot)
    # i.e. Will execute if no weekly exists that is more recent than a week. Will save on oldest.
    weekly_a_path = true_path("./database/snapshots/weekly_A")
    weekly_b_path = true_path("./database/snapshots/weekly_B")

    print("\n::: Checking weekly snapshot ages... :::")

    age_a = (datetime.now() - datetime.fromtimestamp(os.path.getmtime(weekly_a_path)) if os.path.exists(weekly_a_path)
             else timedelta(weeks=1000))  # infinity proxy (~20 years) if file doesn't exist
    age_b = (datetime.now() - datetime.fromtimestamp(os.path.getmtime(weekly_b_path)) if os.path.exists(weekly_b_path)
             else timedelta(weeks=1000))

    print(f"[Age A: {age_a.days if age_a.days < 5000 else '-'} days · Age B: {age_b.days if age_b.days < 5000 else '-'} days]")

    if all(x > timedelta(days=6.5) for x in [age_a, age_b]):  # if no recent weekly
        print("- Found no recent weekly save. Will write into the oldest weekly file...")
        print("\n::: Executing weekly backup... :::")
        if age_b > age_a:
            save_snapshot("weekly_B")
        else:
            save_snapshot("weekly_A")
    else:
        print("- We already have a young weekly snapshot. No need to replace it.")


if __name__ == "__main__":
    wake_snapshotter()
