from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, date
import database

def reset_if_new_day():
    today = str(date.today())
    last = database.get_setting("last_reset_date")

    if today != last:
        with database.connect() as conn:
            conn.execute(
                "UPDATE medicines SET taken_today=0, last_notified=NULL"
            )
        database.set_setting("last_reset_date", today)
        database.log("รีเซ็ตวันใหม่")

def check_medicines():
    reset_if_new_day()

    delay = int(database.get_setting("notify_delay"))
    enabled = database.get_setting("email_enabled") == "1"

    now = datetime.now()
    with database.connect() as conn:
        meds = conn.execute(
            "SELECT id, name, time, taken_today FROM medicines"
        ).fetchall()

    for mid, name, t, taken in meds:
        if taken == 1:
            continue

        med_time = datetime.strptime(t, "%H:%M").replace(
            year=now.year, month=now.month, day=now.day
        )
        minutes = (now - med_time).total_seconds() / 60

        if minutes >= delay and enabled:
            database.log(f"ถึงเวลาเตือนยา: {name}")

def start_scheduler():
    s = BackgroundScheduler()
    s.add_job(check_medicines, "interval", minutes=1)
    s.start()
