import json
import os
import time
import asyncio
import logging
from telebot import TeleBot, types
import gm as gm
import multiprocessing
import threading
import xbothandler as x
import xkeyhandler as kh
from datetime import datetime, timedelta
import threading
#import pdb
import random
import re
from telethon.sync import TelegramClient
from telethon.errors import RPCError

# Ensure gm.py exists and works as expected
#import threads
#import botpros as bp
#from botpros import sbots
# Configure logging
#logging.basicConfig(level=logging.DEBUG)

# Initialize bot
API_TOKEN = '7328062245:AAG2FwqM94pF--uMpAYJCCKkqMyWiw1QpHA'
bot = TeleBot(API_TOKEN)
API_ID = "24442086"
API_HASH = "23907325b91fd7d1bee2dc59d7f1c09c"
# JSON files for templates and ongoing task
TEMPLATES_FILE = 'templates.json'
ONGOING_TASK_FILE = 'ongoing_task.json'
default_log = '-1002168034878'
ADS_FILE = 'ads.json'
ERROR_EMOJI = '🤕'
owners = ['ivyadverts','neveriq']


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

#le
def save_ongoing_task(ongoing_task):
    try:
        with open(ONGOING_TASK_FILE, 'w') as f:
            json.dump(ongoing_task, f, indent=4)
    except Exception as e:
        logging.error(f"Failed to save ongoing task: {e}")


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

# Initialize templates and ongoing task
templates = load_templates()
from telethon.sessions import StringSession

async def check_valid(link):
    match = re.search(r"https://t\.me/([^/]+)/(\d+)",link)
    if not match:
        return False
    chat_username, msg_id = match.groups()
    msg_id = int(msg_id)
    try:
        sess = "1BVtsOLoBuypVGAvyIBM4s7HlN8I6k90BTNum3hQQmZZ6c4ord8-rm1NQcNSxlDgqIl68wNAYhtEprXVZ-f7fJ_zflycE_ZqcH9tfkqhxNMqsjs4O8bIUrCTFpduTJIsIutGzYsqPMKu3EgiqhsGYJN-b_BY1gxBQ5zGZhoPH_g69BgH4OsTQOVqqalV1KvH5f4Mf7PlIGfsxqc40yGMSL5F4td3Lh7bxZBXOjPM2CbEXyGEz9HUTLxydgDNTpmQkAaW6aVJnpfG1hG4pnHxRyAmPvoC6CuySz_p3vPRZtszbtKiYzq7t0OJ-J8T4uJRrvQOmBt5A85D3wOr85_59U7LwELNyYpE="
        client = TelegramClient(StringSession(sess), API_ID, API_HASH)
        async with client:
            message = await client.get_messages(chat_username,ids=msg_id)
            return bool(message)
    except:
        return False

def create_button(text,link):
  """Creates an inline keyboard button with the specified link."""
  button_text = text
  url_button = types.InlineKeyboardButton(text=button_text, url=link)
  keyboard = types.InlineKeyboardMarkup()
  keyboard.add(url_button)
  return keyboard


def start_bots(bots):
    threads = []
    from botpros import start_bot
    for i, bot in enumerate(bots):
        x.turn_off_bot(bot)
        thread = threading.Thread(
            target=lambda: asyncio.run(start_bot(bot)), daemon=True
        )
        threads.append(thread)
        thread.start()

    #for thread in threads:
     #   thread.join()

def sbots():
    bots = x.get_bot()
    if not bots:
        bot.send_message(6297253770,"Issue starting bots")
    #for bot in bots
    start_bots(bots)

ads = load_ads()

try:
    #from botpros import sbots
    sbots()#bp.sbots()
except Exception as e:

    #bot.send_message(default_log,"Error starting bots on startup:")
    print("Error starting bots on startup: "+str(e))



def process_ads_and_templates():
    #global ads, templates
    current_time = time.time()
    yesterday = datetime.now() #- timedelta(days=1)
    ads = load_ads()
    templates = load_templates()
    # Iterate over ads
    for ad_id, ad_data in list(ads.items()):
        # Check sessions_today and reset if needed
        if (
            ad_data["sessions_today"] > 2
            and datetime.fromtimestamp(ad_data["last_updated"]).date() != yesterday.date()
        ):
            #print('iwashere')
            ads[ad_id]["sessions_today"] = 0
            save_ads(ads)
            save_templates(templates)
        # Remove expired ads
        if current_time >= ad_data["plan_end"]:
            tname = templates[ads[ad_id]['template']]
            bot.send_message(ads[ad_id]['user_id'],f"Your campagin ({ad_id})'s subscription has ended with total {ads[ad_id]['total_sent']} forwarded, redeem another key to continue.")
            del templates[ads[ad_id]['template']]
            del ads[ad_id]
            save_ads(ads)
            save_templates(templates)

        #Iterate over templates
    for template_name, template_data in templates.items():
        if template_data["total_msgs_sent"] >= template_data["target_count"]:
            # Reset total_msgs_sent for the template
            templates[template_name]["total_msgs_sent"] = 0
            save_ads(ads)
            save_templates(templates)
            # Find and update the ad associated with this template
            for ad_id, ad_data in ads.items():
                if ad_data["template"] == template_name:
                    ads[ad_id]["sessions_today"] += 1
                    if ads[ad_id]["sessions_today"] == 3:
                        data = template_data["target_count"]*3
                        bot.send_message(ads[ad_id]['user_id'], f"🔔Ad has been forwarded successfully *({data} times today)*", parse_mode="Markdown")
                    save_ads(ads)
                    save_templates(templates)
                    break
    # Save changes



def get_ad():
    #def get_ad():
    #global ads
    ads = load_ads()
    templates = load_templates()
    current_time = time.time()

    # Filter ads that are not expired and have available sessions
    valid_ads = {
        ad_id: ad_data
        for ad_id, ad_data in ads.items()
        if ad_data["plan_end"] > current_time and ad_data["sessions_today"] < 3
    }

    if not valid_ads:
        return None  # No valid ads available

    # Sort ads based on criteria (e.g., remaining time, remaining target, sessions_today)
    sorted_ads = sorted(
        valid_ads.items(),
        key=lambda item: (
            item[1]["sessions_today"],            # Prioritize fewer sessions_today
            item[1]["target"] - item[1]["total_sent"],  # Prioritize ads closer to their target
            item[1]["plan_end"],                 # Prioritize ads closer to expiration
        )
    )

    # Return the ID of the top-priority ad
    return sorted_ads[0][0] if sorted_ads else None


def periodic_task():
    while True:
        try:

            # Your periodic task logic here
            print("Running periodic task...")
            # Example: Log the time
            #def process_ads_and_templates():
            process_ads_and_templates()
            ads = load_ads()
            templates = load_templates()
            ongoing_task = load_ongoing_task()
            if not ongoing_task:
                #ongoing_task = load_ongoing_task()
                #print(ads)
                with open("xbots.json", "r+") as file:
                    data = json.load(file)
                    for bot in data:
                        if bot.get("in_use") is True:
                            bot["in_use"] = False
                    file.seek(0)
                    json.dump(data, file, indent=4)
                    file.truncate()
                ad = get_ad()
                if not ad:
                    print('None found all ads are done.')
                else:
                    #get template and ad name accordingly
                    #get the ad first
                    template_name = ads[ad]['template']
                    #ongoing_task = load_ongoing_task()
                    template = templates.get(template_name)
                    ongoing_task = template.copy()
                    ongoing_task['template_name'] = template_name
                    ongoing_task['adname'] = ad
                    ongoing_task['last_msg_sent'] = datetime.now().timestamp()
                    save_ongoing_task(ongoing_task)
                    save_ads(ads)
                    save_templates(templates)
                    time.sleep(20)
                    sbots()
            elif ongoing_task['adname'] not in ads or datetime.now() - datetime.fromtimestamp(ongoing_task['last_msg_sent']) > timedelta(minutes=30):
                    ongoing_task = None
                    save_ongoing_task(ongoing_task)
                    #with open('bots.json')
            print(f"Task executed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            print(f"Error in periodic task: {str(e)}")

        # Wait for 10 minutes before running again
        time.sleep(600)  # 600 seconds = 10 minutes

# Start the periodic task in a separate thread
threading.Thread(target=periodic_task, daemon=True).start()







# Command to create a template
@bot.message_handler(commands=['ctemp'])
def create_temp(message):
    #break
    return
    chat_id = message.chat.id
    template = {
        'created_by': message.from_user.id,
        'total_msgs_sent': 0,
        'last_msg_sent': None
    }

    msg = bot.send_message(chat_id, "Please send the advertisement message (text or link):")
    bot.register_next_step_handler(msg, get_advertisement, template)


def get_advertisement(message, template):
    template['advertisement_msg'] = message.text
    msg = bot.send_message(message.chat.id, "Please send the chat id of the logs group:")
    bot.register_next_step_handler(msg, get_logs_group, template)


def get_logs_group(message, template):
    template['logs_group'] = message.text
    msg = bot.send_message(message.chat.id, "Enter the target number of groups to send the message to:")
    bot.register_next_step_handler(msg, get_target_count, template)


def get_target_count(message, template):
    try:
        templates = load_templates()
        template['target_count'] = int(message.text)
        template_name = f"template_{len(templates) + 1}"
        templates[template_name] = template
        save_templates(templates)
        bot.send_message(message.chat.id, f"Template created successfully with name: {template_name}")
    except ValueError:
        bot.send_message(message.chat.id, "Please enter a valid number for the target count.")



# Define the command
@bot.message_handler(commands=['start'])
def greet(message):
  text = "🛒 Purchase"
  link = "t.me/ivyadverts"
  keyboard = create_button(text = text,link = link)
  """Responds to the /hello command"""
  bot.send_message(message.chat.id, f"👋 Hello, {message.from_user.first_name}!\n\n👩‍💻 Automated advertisement services, start advertising with us today to gain passive income.\n\n🔑 /redeem → Redeem subscription\n📆 /view → Request statistics on your advertisement campaign\n✏️ /edit → Edit your advertisement\n📚 /tutorial → Video demonstration on usage of bot",reply_markup = keyboard)


@bot.message_handler(commands=['edit'])
def view(message):
    user_campaigns = get_ads_by_user_id(message.from_user.id)
    if not user_campaigns:
        bot.reply_to(message, "You have no active campaigns. Use /redeem to advertise 😊")
        return


    # Split the command into parts
    args = message.text.split(maxsplit=2)

    # Ensure the command has exactly two arguments
    if len(args) != 3:
        bot.reply_to(message, "Usage: /edit {key} {link}")
        return

    key = args[1]
    link = args[2]
    ads = load_ads()
    templates = load_templates()
    try:
        ads[key]['msg_link'] = link
        t = ads[key]['template']
        templates[t]['advertisement_msg'] = link
        save_ads(ads)
        save_templates(templates)
    except:
        bot.reply_to(message, "Error")
    # Acknowledge the received arguments
    bot.reply_to(message, f"Done updating *{key}* with ({link})",parse_mode="Markdown", disable_web_page_preview=True)


@bot.message_handler(commands=['tutorial'])
def tutorial(message):
    text = "🔗[Tutorial Video](https://t.me/ivytutorial/2)"
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        parse_mode="Markdown"  # Specify Markdown parse mode
    )



@bot.message_handler(commands=['clear'])
def clear(message):
    try:
        if message.from_user.username in owners:
            pass
        else:
            return
        args = message.text.split()

        ads = load_ads()
        templates = load_templates()
        temp = ads[args[1]]['template']
        del templates[temp]
        del ads[args[1]]
        save_ads(ads)
        save_templates(templates)
        bot.reply_to(message,"Done")
    except:
        pass


# Command to start a task
@bot.message_handler(commands=['astart'])
def start_task(message):
    return
    ongoing_task = load_ongoing_task()
    if ongoing_task:
        bot.send_message(message.chat.id, "An ongoing task is already in progress. Please wait until it completes.")
        return
    chatish = message.chat.id
    try:
        template_name = message.text.split()[1]
        template = templates.get(template_name)

        if not template:
            bot.send_message(message.chat.id, f"Template with name {template_name} not found.")
            return

        log_file_name = f"task_{template_name}_log.txt"
        template['log_file'] = log_file_name
        with open(log_file_name, 'w') as log_file:
            log_file.write("Message Links Log:\n")

        ongoing_task = template.copy()
        ongoing_task['template_name'] = template_name
        save_ongoing_task(ongoing_task)
        try:
            #gm.create_groups_json('xgroups.txt','groups.json')
            #from botpros import sbots
             #ongoing_task['logs_group']
            bot.send_message(chatish, f"Task started successfully from template: {template_name}\nTarget: {ongoing_task['target_count']}")
            sbots()#bp.sbots()

        except Exception as e:
            bot.send_message(chatish, f"couldn't start the task Error: {e}")

    except IndexError:
        bot.send_message(chatish, "Please provide a template name to start, e.g., /start template_1")




# Command to check ongoing task
@bot.message_handler(commands=['ads'])
def check_status(message):
    if message.from_user.username in owners:
        pass
    else:
        return
    ads = load_ads()
    if not ads:
        bot.reply_to(message, "You have no active campaigns. Use /redeem to advertise 😊")
        return

    response = "📢 <b>Your Active Campaigns:</b>\n\n"
    for i, (key, campaign) in enumerate(ads.items(), start=1):
        response += (
            f"<b>{i}. {key}</b>\n\n"
            f"   🔗 <b>Message Link</b>: ({campaign['msg_link']})\n"
            f"   🎯 <b>Daily Target</b>: {campaign['target']}\n"
            f"   📍 <b>Weekly Target</b>: {campaign['target']*7}\n"
            f"   📤 <b>Total Sent</b>: {campaign['total_sent']}\n"
            f"   ⏰ <b>Plan Start</b>: `{datetime.fromtimestamp(campaign['plan_start']).strftime('%Y-%m-%d %H:%M:%S')}`\n"
            f"   ⌛ <b>Plan End</b>: `{datetime.fromtimestamp(campaign['plan_end']).strftime('%Y-%m-%d %H:%M:%S')}`\n\n"
        )
    try:
        bot.reply_to(message, response, parse_mode='html', disable_web_page_preview=True)
    except Exception as e:
        print('f---',str(e))




# Command to check ongoing task
@bot.message_handler(commands=['status'])
def check_status(message):
    ongoing_task = load_ongoing_task()
    if not ongoing_task:
        bot.send_message(message.chat.id, "No ongoing task currently.")
    else:
        bot.send_message(message.chat.id, f"Ongoing task details:\nTemplate: {ongoing_task['template_name']}\nTotal Messages Sent: {ongoing_task['total_msgs_sent']}\nLast Message Sent: {time.ctime(ongoing_task['last_msg_sent']) if ongoing_task['last_msg_sent'] else 'Not yet sent'}")

# Command to mark task as completed
@bot.message_handler(commands=['complete'])
def complete_task():
    templates = load_templates()
    ongoing_task = load_ongoing_task()

    if not ongoing_task:
        bot.send_message(default_log, "No ongoing task to complete.")
        return
     # Send the log file to the logs group
    #log_file_path = ongoing_task['log_file']
    lg = ongoing_task['created_by']#ongoing_task['logs_group']
    #if os.path.exists(log_file_path):
    #    with open(log_file_path, 'rb') as log_file:
    #        try:
    #            bot.send_document(lg,log_file)#ongoing_task['logs_group'], log_file)
    #            os.remove(log_file_path)
    #        except:
    #            pass#bot.send_document(default_log,log_file)#ongoing_task['logs_group'], log_file)
        #with open('groups.json', 'rb') as gcs:
         #   try:
                #bot.send_document(lg,gcs)#ongoing_task['logs_group'], log_file)
          #  except:
           #     pass#bot.send_document(default_log,gcs)#ongoing_task['logs_group'], log_file)
        # Delete the log file after sending
    try:
        ads = load_ads()
        #templates[ongoing_task['template_name']]['total_msgs_sent'] = 0
        #adname = ongoing_task['adname']
        #ads[adname]['sessions_today'] += 1

        #bot.send_message(lg, f"Ad has been forwarded successfully ({ongoing_task['total_msgs_sent']} times today)")
        ongoing_task = None
        save_ongoing_task(ongoing_task)
        save_templates(templates)
        save_ads(ads)
    except Exception as e:
        print(str(e),'error in completetion')

def get_ads_by_user_id(user_id):
    ads = load_ads()
    # Filter ads by user_id
    return {key: value for key, value in ads.items() if value.get("user_id") == user_id}
@bot.message_handler(commands=['view'])
def view(message):
    user_campaigns = get_ads_by_user_id(message.from_user.id)
    if not user_campaigns:
        bot.reply_to(message, "You have no active campaigns. Use /redeem to advertise 😊")
        return

    response = "📢 <b>Your Active Campaigns:</b>\n\n"
    for i, (key, campaign) in enumerate(user_campaigns.items(), start=1):
        response += (
            f"<b>{i}. {key}</b>\n\n"
            f"   🔗 <b>Message Link</b>: ({campaign['msg_link']})\n"
            f"   🎯 <b>Daily Target</b>: {campaign['target']}\n"
            f"   📍 <b>Weekly Target</b>: {campaign['target']*7}\n"
            f"   📤 <b>Total Sent</b>: {campaign['total_sent']}\n"
            f"   ⏰ <b>Plan Start</b>: `{datetime.fromtimestamp(campaign['plan_start']).strftime('%Y-%m-%d %H:%M:%S')}`\n"
            f"   ⌛ <b>Plan End</b>: `{datetime.fromtimestamp(campaign['plan_end']).strftime('%Y-%m-%d %H:%M:%S')}`\n\n"
        )
    try:
        bot.reply_to(message, response, parse_mode='html', disable_web_page_preview=True)
    except Exception as e:
        print('f---',str(e))
@bot.message_handler(commands=['gen'])
def generate_command(message):
    if message.from_user.username in owners:
        pass
    else:
        return
    try:
        # Check if the command has arguments
        if len(message.text.split()) > 1:
            # Try to extract the optional integer argument
            arg = int(message.text.split()[1])
            if arg > 0:
                bot.send_message(message.chat.id, f"/redeem {kh.get_key(arg)}")
                # Handle the positive integer argument here
                pass
            else:
                # Handle non-positive integer argument here
                pass
        else:
            bot.send_message(message.chat.id, f"/redeem {kh.get_key()}")
            # Handle case where no argument is provided here
            pass
    except ValueError:
        # Handle case where argument is not an integer here
        pass

def find_multiplier(number):
    # Find the smallest integer x such that x * 3 >= number
    x = (number + 2) // 3  # Adding 2 ensures we round up if there's a remainder
    return x

#
# def add_subscription(key, user_id, target, msg_link):
#     db = load_db()
#     user_id = str(user_id)
#     plan_start = datetime.now().timestamp()
#     db[key] = {
#             'plan_start': plan_start,
#             'plan_end': plan_end,
#             'target': target,#target per day
#             'msg_link': msg_link,
#             'template': template,
#             'last_updated': template,
#             'total_sent': 0,
#             'sessions_today': 0
#     }
#     save_db(db)
#     print(f"Campaign added {key}")

#create campaign
#create template for it
#only in redeem

def create_template():
    pass


@bot.message_handler(commands=['redeem'])
def redeem(message):
    try:
        # Check if the command has arguments
        if len(message.text.split()) > 1:
            # Try to extract the optional integer argument
            arg = message.text.split()[1]
            if ' ' not in arg:
                # Assume the first argument is the user_id and the second argument is the key
                user_id = message.from_user.id
                key = arg
                target = kh.redeem_key(user_id, key)
                if target > 0:
                     msg = bot.reply_to(message, f"🎊Key redemption successful! Please enter the message link you want to advertise. Please send only one link.")
                     plan_start = datetime.now().timestamp()
                     plan_end = (datetime.now() + timedelta(weeks=1)).timestamp()
                     template = {
                        'created_by': message.from_user.id,
                        'total_msgs_sent': 0,
                        'last_msg_sent': None
                        }
                     ad = {
                        'plan_start': plan_start,
                        'plan_end': plan_end,
                        'target': target,#target per day
                        'last_updated': datetime.now().timestamp(),
                        'total_sent': 0,
                        'sessions_today': 0,
                        'user_id': user_id
                        }

                     bot.register_next_step_handler(msg, completetion, ad, template, key)
                else:
                    bot.reply_to(message, f"{ERROR_EMOJI} Invalid key.")
            else:
                bot.reply_to(message, f"{ERROR_EMOJI} Invalid key. Key should not contain spaces.")
        else:
            bot.reply_to(message, "No key provided. Please provide a key to redeem. Ex. /redeem {key}")
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, f"{ERROR_EMOJI} Couldn't redeem the key.")


def completetion(message, ad, template, key):
    try:
        templates = load_templates()
        ads = load_ads()
        template['advertisement_msg'] = message.text
        ad['msg_link'] = message.text
        if not asyncio.run(check_valid(message.text)):
            msg = bot.send_message(message.chat.id, f"🚀Invalid link given please send again.", parse_mode="HTML")
            bot.register_next_step_handler(msg, completetion, ad, template, key)
            return
            #completetion(message, ad, template, key)
            #return
        template['target_count'] = find_multiplier(ad['target'])
        template_name = f"template_{len(templates) + 1}"
        ad['template'] = template_name
        templates[template_name] = template
        ads[key] = ad
        save_templates(templates)
        save_ads(ads)
        #bot.send_message(message.chat.id, f"Template created successfully with name: {template_name} and ad name :{}")
        bot.send_message(message.chat.id, f"🚀Advertisement confirmed! Your message will be processed for advertisement.\n\n<b>Key redeemed: {key}</b>", parse_mode="HTML")

    except Exception as e:
        print(str(e),"Error while redeeming")
        bot.send_message(message.chat.id, f"Couldn't process the key, contact admins.")
    #msg = bot.send_message(message.chat.id, "Please send the chat id of the logs group:")
    #pass
# Polling with retry
def polling_with_retry(bot_instance):
    while True:
        try:
            bot_instance.polling(none_stop=True)
        except Exception as e:
            logging.error(f"Bot polling failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)


# Run the bot
if __name__ == "__main__":
    polling_with_retry(bot)
