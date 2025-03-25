import gm as gm
import xbothandler as x
import time
import asyncio
import traceback
#from telethon import TelegramClient
import multiprocessing
from telethon import TelegramClient, events, types
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError, UserAlreadyParticipantError, ChannelInvalidError, InviteHashInvalidError
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors import UsernameInvalidError
import random
from datetime import datetime, timedelta
#from telethon.sessions import StringSession
# Save ongoing task to file
import threading
import json
import logging
#import devil as d
from devil import complete_task
API_ID = "24442086"
API_HASH = "23907325b91fd7d1bee2dc59d7f1c09c"
TEMPLATES_FILE = 'templates.json'
ONGOING_TASK_FILE = 'ongoing_task.json'
TEMPLATES_FILE = 'templates.json'
ADS_FILE = 'ads.json'
# Configure logging
#logging.basicConfig(level=logging.DEBUG)
delays = [10, 9, 11, 8]  # Delay options in seconds

# Choose a random delay
delay = random.choice(delays)

# Load ongoing task from file
def load_ongoing_task():
    try:
        with open(ONGOING_TASK_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
        return None


def save_ongoing_task(ongoing_task):
    with open(ONGOING_TASK_FILE, 'w') as f:
        json.dump(ongoing_task, f, indent=4)





# Load templates from file
def load_templates():
    try:
        with open(TEMPLATES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
        return {}

# Load templates from file
def load_ads():
    try:
        with open(ADS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
        return {}
# Save templates to file
def save_templates(templates):
    try:
        with open(TEMPLATES_FILE, 'w') as f:
            json.dump(templates, f, indent=4)
    except Exception as e:
        logging.error(f"Failed to save templates: {e}")
#pdb.set_trace()
def save_ads(ads):
    try:
        with open(ADS_FILE, 'w') as f:
            json.dump(ads, f, indent=4)
    except Exception as e:
        logging.error(f"Failed to save ADS: {e}")





def plus_one():
    ongoing_task = load_ongoing_task()
    tname = ongoing_task['template_name']
    adname = ongoing_task['adname']
    #ads[adname][]
    templates = load_templates()
    templates[tname]['total_msgs_sent'] += 1
    templates[tname]['last_msg_sent'] = datetime.now().timestamp()
    ads = load_ads()
    #print(ads)
    ads[adname]['last_updated'] = datetime.now().timestamp()
    ads[adname]['total_sent'] += 1
    save_templates(templates)
    save_ads(ads)





async def start_bot(bot):
    while True:
        try:
            #print('bruv')
            async with TelegramClient(StringSession(bot["session_string"]), API_ID, API_HASH) as client:
                if not client.is_connected():
                    #print('hereyou go')
                    await client.connect()
                    print('anotherone')
                print(f"Bot {bot['nickname']} started successfully.")
                bot['in_use'] = True
                x.turn_on_bot(bot)
                #client.flood_sleep_threshold = 24 * 60 * 60
                while True:
                    try:
                        with open(ONGOING_TASK_FILE, 'r') as f:
                            ongoing_task = json.load(f)
                            if not ongoing_task:
                                #with open(ONGOING_TASK_FILE):
                                x.turn_off_bot(bot)
                                #print('exiting')
                                return
                            if ongoing_task['total_msgs_sent'] == ongoing_task['target_count']:
                                complete_task()
                                ongoing_task = None
                                with open(ONGOING_TASK_FILE, 'w') as f:
                                    json.dump(ongoing_task, f, indent=4)
                                #print("Task completed")

                                x.turn_off_bot(bot)
                                return
                            elif ongoing_task['total_msgs_sent'] > ongoing_task['target_count']:
                                ongoing_task = None
                                with open(ONGOING_TASK_FILE, 'w') as f:
                                    json.dump(ongoing_task, f, indent=4)
                                print("Task completed")
                                x.turn_off_bot(bot)
                                #ongoing_task = None
                    except FileNotFoundError:
                        ongoing_task = None
                    if not ongoing_task:
                        print(f"Bot {bot['nickname']}: No task found")
                        x.turn_off_bot(bot)
                        return
                    group = gm.get_next_group()
                    if not group:
                        print(f"Bot {bot['nickname']}: No more groups to process. Exiting.")
                        #gm.create_groups_json('xgroups.txt', 'groups.json')
                        gm.write_unique_lines('validgcs.txt','xgroups.txt')
                        x.turn_off_bot(bot)
                        continue

                    try:
                        #print(5)
                        #print(group)
                        time.sleep(delay)
                        group_entity = await client.get_entity(group)
                        #print(6)
                        await client(JoinChannelRequest(group_entity))
                        #print(7)

                    except UserAlreadyParticipantError:
                       # print(f"Already a participant of group: {group}")
                     #   continue
                         pass
                    except FloodWaitError as e:
                         print(f"Bot {bot['nickname']} waiting {e.seconds}, {str(e)}")
                         await client.disconnect()
                         time.sleep(e.seconds)
                         await client.connect()
                    except Exception as e:
                         print(f"Bot {bot['nickname']} Error joining. ",str(e))
                         #gm.mark_invalid(group)#gm.mark_group_invalid(groups)
                         continue
                      #  print(f"Error joining, {e}")
                      #  break
                    link = ongoing_task['advertisement_msg']
                    try:
                        parts = link.split("/")
                        if parts[3] == 'c':
                            msg_id, username = int(parts[5]), parts[4]
                        else:
                            msg_id, username = int(parts[4]), parts[3]
                        entity = await client.get_entity(username)
                        #print(f"Resolved username: {username}")
                    except ValueError:
                        #return
                        #return
                       # print("Invalid username format.")
                        continue
                    except Exception as e:
                       # print(f"Error resolving username: {e}")
                        #return
                        #traceback.print_exc()
                        continue
                    try:
                        #print(2)
                        target_message = await [client.get_messages(entity, ids=msg_id)][0]
                        #print(3)
                    except Exception as e:
                        #print(4)
                       # print(f"Error fetching message: {e}")

                        traceback.print_exc()
                        ongoing_task = None
                        with open(ONGOING_TASK_FILE, 'w') as f:
                                #ongoing_task = json.load(f)
                                json.dump(ongoing_task, f, indent=4)
                        print('couldnt resolve the link')
                        return
                        #break
                    try:
                        #print(8)
                        await target_message.forward_to(group_entity)
                        with open('validgcs.txt', 'a') as f:
                            f.write(group + "\n")
                        try:
                            with open(ONGOING_TASK_FILE, 'r') as f:
                                ongoing_task = json.load(f)
                                if not ongoing_task:
                                    x.turn_off_bot(bot)
                                    print('exiting')
                                    return
                                ongoing_task['total_msgs_sent'] += 1
                                ongoing_task['last_msg_sent'] = datetime.now().timestamp()#time.time()
                            with open(ONGOING_TASK_FILE, 'w') as f:
                                #ongoing_task = json.load(f)

                                json.dump(ongoing_task, f, indent=4)
                        except Exception as e:
                                print(str(e),"!")
                            #if ongoing_task['total_msgs_sent'] >=
                        #ongoing_task['total_msgs_sent'] += 1
                        #ongoing_task['last_msg_sent'] = time.time()
                        print(f"\033[36mBot {bot['nickname']}: Processed group {group}.\033[0m")
                        plus_one()
                        save_ongoing_task(ongoing_task)
                        time.sleep(delay)
                        #print(9)
                    except Exception as e:
                        print(f"Bot {bot['nickname']}: Error processing group {group}. Error: {e}")
                        time.sleep(4)
                        with open('validgcs.txt', 'r') as f:
                            found = any(line.strip() == group for line in f)
                            if found:
                                continue
                            else:
                                try:
                                    await client.kick_participant(group, 'me')
                                except:
                                    pass
                        #gm.mark_invalid(group)
                        #gm.mark_group_invalid(group)
                        #traceback.print_exc()
       ######           #gm.add_group_back(group, str(e))  # Log error and re-add group
                        #add group back to ther list
                    #finally:

                        #await asyncio.sleep(5)
                        #print("~~DONE~~")

                    #leave if no privileges
        except Exception as e:
            print(10)
            print(f"Couldn't start the bot {bot['nickname']}. Error: {e}")
            traceback.print_exc()
            logging.exception(f"Error starting bot {bot['nickname']}: {e}")
            x.turn_off_bot(bot)
        await asyncio.sleep(120)  # Retry after 2 minutes if the bot fails
        x.turn_off_bot(bot)


def terminate_thread(thread):
    if thread.is_alive():
        print("FUnction tookk too long Terminating...")


# Function to start multiple bots concurrently
def start_bots(bots):
    threads = []
    for i, bot in enumerate(bots):
        x.turn_off_bot(bot)
        thread = threading.Thread(
            target=lambda: asyncio.run(start_bot(bot))
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join(timeout=5)
        terminate_thread(thread)

def sbots():
    bots = x.get_bot()
    #for bot in bots
    start_bots(bots)


if __name__ == "__main__":
    # Replace with your API ID, API Hash, and Bot Tokens
    #API_ID = 'YOUR_API_ID'
    #API_HASH = 'YOUR_API_HASH'
    BOT_TOKENS = [
        'BOT_TOKEN_1',
        'BOT_TOKEN_2',
        'BOT_TOKEN_3',
    ]

    # Example groups (to be stored in groups.json)
    #groups = [{'id': f'group_{i}', 'status': None} for i in range(1, 11)]
    #save_groups(groups)
    bots = x.get_bot()
    #for bot in bots
    start_bots(bots)
    # Start the bots
    #start_bots(API_ID, API_HASH, BOT_TOKENS)
