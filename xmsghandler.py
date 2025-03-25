#msg handler happy nation
import json
import os
from datetime import datetime

DB_FILE = '6297253770/sxmsg_db.json'

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



def is_older(plan,plan_start):
    #the function returns True or False if timestamp is older than 7(1) 30(2) days older.
    current_time = datetime.now().timestamp()
    days_ago = current_time - (plan * 24 * 60 * 60)
    return plan_start <= days_ago
    #if plan == 1:
        #seven_days_ago = current_time - (7 * 24 * 60 * 60)
        #return timestamp <= seven_days_ago
    #else plan == 2:
        #thirty_days_ago = current_time - (30 * 24 * 60 * 60)
        #return timestamp <= thirty_days_ago


def add_msg(user_id, msg_link, plan=None):
    db = load_db()
    msg_details = {
        "times_sent": 0,
        "group_list": "default.txt",
        "latest": None,
        }
    plan_start = datetime.now().timestamp()
    if user_id in db:
        db[user_id]['msg_links'][msg_link] = msg_details
        if plan is not None:
            db[user_id]['plan'] = plan
    else:
        #db[user_id]['plan_start'] = plan_start
        db[user_id] = {
            'plan': plan,
            'plan_start': plan_start,
            'notified': False,
            'limit': 1,
            'msg_links': {msg_link: msg_details}
        }
    save_db(db)


def add_msgop(msg_link, target=100):
        startpro()
        return True


def get_links(user_id):
    db = load_db()
    user_data = db.get(user_id, {})
    return list(user_data.get('msg_links', {}).keys())


def get_msg_details(user_id, msg_link):
    db = load_db()
    user_data = db.get(user_id, {})
    return user_data.get('msg_links', {}).get(msg_link)

def get_user_data(user_id):
    db = load_db()
    user_data = db.get(user_id, {})
    if user_id in db:
            return user_data
    else:
        return False


def get_user_plan(user_id):
    db = load_db()
    user_data = db.get(user_id, {})
    return user_data.get('plan'), user_data.get('plan_start')

def remove_subscription(user_id):
    db = load_db()
    if user_id in db:
        del db[user_id]
        save_db(db)
        print(f"Subscription for user {user_id} has been removed.")
    else:
        print(f"No subscription found for user {user_id}.")

def tobe_end(plan,plan_start):
    current_time = datetime.now().timestamp()
    planup = plan - 3
    days_ago = current_time - (planup * 24 * 60 * 60)
    return plan_start <= seven_days_ago



def check_subscriptions():
    db = load_db()
    notify_users = []
    removed_users = []
    for user_id, details in db.items():
        plan_start = details.get('plan_start')
        plan = details.get('plan')
        notified = details.get('notified')
        if is_older(plan,plan_start):
                removed_users.append(user_id)
                remove_subscription(user_id)
                #remove user
        elif tobe_end(plan,plan_start):
                if notified != True:
                    notify_users.append(user_id)
                    db[user_id]['notified'] = true
        else:
                db[user_id]['notified'] = False
    return notify_users,removed_users
                #bruh

def update():
    notify,remove = check_subscriptions()


def add_subscription(user_id, plan, msg_links=None):
    db = load_db()
    print(user_id)
    print(plan)
    print(db)
    user_id = str(user_id)
    if user_id in db:
        print("gay")
        db[user_id]['plan'] += plan
        save_db(db)
        #return
    else:
        print(type(user_id))
        plan_start = datetime.now().timestamp()
        db[user_id] = {
            'plan': plan,
            'plan_start': plan_start,
            'notified': False,
            'limit': 1,
            'msg_links': {}
        }
        save_db(db)
    print(f"Subscription added for user {user_id}.")


def startall():
    #get all msgs onebyone
    msgs = load_msgs()
    for msg in msgs:
        pass


