from git import Repo
import json, time
from apscheduler.schedulers.blocking import BlockingScheduler 

scheduler = BlockingScheduler() 


def add_to_log():
    with open("log.txt", "a") as f:
        t = time.strftime('%d-%m-%Y')
        f.write(f"[UPDATE] - Committed at {t}\n")

    with open("stats.json", "r") as f:
        data = json.load(f)
        data["updates"] += 1
        data["last_commit"] = t

    with open("stats.json", "w") as f:
        json.dump(data, f)

        return data["updates"]

@scheduler.scheduled_job('interval', hours=24)
def commit():
    print('committing...')
    version = add_to_log()

    repository = Repo('.')
    repository.index.add("log.txt")
    repository.index.add("stats.json")
    repository.index.commit(f"COMMIT v{version}")

    origin = repository.remote('origin')
    origin.push()

scheduler.start()