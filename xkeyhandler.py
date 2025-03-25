import json
import os
from datetime import datetime
import secrets
import string
#import xmsghandler as msh
DB_FILE = 'xkeys_db.json'

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as file:
            db = json.load(file)
    else:
        db = {}
    return db

def save_db(db):
    with open(DB_FILE, 'w') as file:
        json.dump(db, file, indent=4, default=str)

def get_key(duration=30):
    db = load_db()
    key = gk()
    db[key] = duration
    #db.append(data)
    save_db(db)
    return key

def gk(length=16):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length)).upper()


def add_subscription(key, user_id, target, msg_link):
    db = load_db()
    user_id = str(user_id)
    plan_start = datetime.now().timestamp()
    plan_end = (datetime.now() + timedelta(hours=3)).timestamp()
    db[key] = {
            'plan_start': plan_start,
            'plan_end': plan_end,
            'target': target,#target per day
            'msg_link': msg_link,
            'template': template,
            'last_updated': template,
            'total_sent': 0,
            'sessions_today': 0
    }
    save_db(db)
    print(f"Campaign added {key}")

def redeem_key(user_id,key):
    db = load_db()
    if key in db:
        dur = db.get(key)
        del db[key]
        save_db(db)
        #add_subscription(user_id=user_id,plan=dur)
        return dur
    else:
        return 0

# Example usage
#key = get_key()#generate_random_string_key(16)
#print(f"Random String Key: {key}")
#print(redeem_key("7wkzMNNrJ1cp6f75"))
