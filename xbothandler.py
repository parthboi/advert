import json
import datetime
from time import time

# Define the data structure for a bot
def create_bot(nickname, session_string, phone_number="", in_use='true', num_sent_msgs=0, flag=False, times_flagged=0):
  """
  Creates a dictionary representing a bot with the given details.

  Args:
      nickname (str): The nickname of the bot.
      session_string (str): The session string for the bot.
      phone_number (str, optional): The phone number associated with the bot (default: "").
      in_use (bool, optional): Whether the bot is currently in use (default: False).
      num_sent_msgs (int, optional): The number of messages sent by the bot (default: 0).
      flag (bool, optional): A flag for the bot (default: False).
      times_flagged (int, optional): The number of times the bot has been flagged (default: 0).

  Returns:
      dict: A dictionary representing a bot.
  """
  return {
    "nickname": nickname,
    "session_string": session_string,
    "phone_number": phone_number,
    "in_use": in_use,
    "num_sent_msgs": num_sent_msgs,
    "last_used": time(),  # Use time.time() for current timestamp
    "flag": flag,
    "times_flagged": times_flagged
  }

# Function to load data from JSON file
def load_bots(filename):
  """
  Loads bot data from a JSON file.

  Args:
      filename (str): The path to the JSON file containing bot data.

  Returns:
      list: A list of dictionaries representing bots.
  """
  try:
    with open(filename, "r") as f:
      return json.load(f)
  except FileNotFoundError:
    return []

# Function to save data to JSON file
def save_bots(bots, filename = "xbots.json"):
  """
  Saves bot data to a JSON file.

  Args:
      bots (list): A list of dictionaries representing bots.
      filename (str): The path to the JSON file to save the bot data.
  """
  with open(filename, "w") as f:
    json.dump(bots, f, indent=4)

# Function to create a new bot
def create_bot_db(nickname, session_string, phone_number="", filename="6297253770/xbots.json"):
  bots = load_bots(filename)
  for bot in bots:
    if bot["nickname"] == nickname:
      return False  # Nickname already exists

  bots.append(create_bot(nickname, session_string, phone_number))
  save_bots(bots, filename)
  return True

# Function to delete a bot
def delete_bot(nickname, filename="6297253770/xbots.json"):
  """
  Deletes a bot from the database.

  Args:
      nickname (str): The nickname of the bot to delete.
      filename (str, optional): The path to the JSON file containing bot data (default: "bots.json").

  Returns:
      bool: True if bot is deleted successfully, False otherwise.
  """
  bots = load_bots(filename)
  new_bots = []
  for bot in bots:
    if bot["nickname"] != nickname:
      new_bots.append(bot)
  if len(new_bots) == len(bots):
    return False  # Bot not found

  save_bots(new_bots, filename)
  return True

# Function to get 5 least recently used active bots (excluding flagged)
def get_bot(filename="xbots.json"):
  json_data = load_bots(filename)
  active_profiles = [profile for profile in json_data if not profile['in_use']]
  sorted_profiles = sorted(active_profiles, key=lambda x: x['last_used'])
  return sorted_profiles
  #return bots
  #print(bots)
  #return

  #Gets 5 bots which are currently in use (in_use=True) and have the oldest timestamps
  #(last_used) among active ones (flag=False or

def turn_on_bot(profile):
  bots = load_bots('xbots.json')
  for bot in bots:
    if bot["phone_number"] == profile["phone_number"]:
        bot["in_use"] = True
        save_bots(bots)
        return True



def turn_off_bot(profile):
  bots = load_bots('xbots.json')
  for bot in bots:
    if bot["phone_number"] == profile["phone_number"]:
        bot["in_use"] = False
        save_bots(bots)
        return True
