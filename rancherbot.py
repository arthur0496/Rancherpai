import os
import time
import re
from slackclient import SlackClient
from rancherpai import *

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
UPGRADE_COMMAND = "upgrade"
ROLLBACK_COMMAND = "rollback"
FINISH_UPGRADE_COMMAND = "finish upgrade"
RESTART_SERVICE_COMMAND = "restart"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_bot_commands(slack_events):
  for event in slack_events:
    if event["type"] == "message" and not "subtype" in event:
      user_id, message = parse_direct_mention(event["text"])
      if user_id == starterbot_id:
        return message, event["channel"]
  return None, None

def parse_direct_mention(message_text):
   matches = re.search(MENTION_REGEX, message_text)
   if matches : 
    return (matches.group(1), matches.group(2).strip()) 
   else:
     return (None, None)

def handle_command(command,channel):
  default_response = "deu ruim!!!"
  
  response = None
  words = command.split(" ")

  if command.startswith(UPGRADE_COMMAND):
    if(len(words) != 3):
      response = 'You passed the wrong amount of arguments for this command'
    else:
      response = service_upgrade(words[2],words[1])

  elif command.startswith(ROLLBACK_COMMAND):
    if(len(words) != 3):
      response = 'You passed the wrong amount of arguments for this command'
    else:
      response = upgrade_rollback(words[2],words[1])
  
  elif command.startswith(FINISH_UPGRADE_COMMAND):
    if(len(words) != 4):
      response = 'You passed the wrong amount of arguments for this command'
    else:
      response = finish_upgrade(words[3],words[2])

  elif command.startswith(RESTART_SERVICE_COMMAND):
    if(len(words) != 3):
      response = 'You passed the wrong amount of arguments for this command'
    else:
      response = restart_service(words[2],words[1])

  slack_client.api_call(
    "chat.postMessage",
    channel=channel,
    text=response or default_response
  )


if __name__ == "__main__":
  if slack_client.rtm_connect(with_team_state=False):
    print("Starter Bot connected and running!")
    # Read bot's user ID by calling Web API method `auth.test`
    starterbot_id = slack_client.api_call("auth.test")["user_id"]
    while True:
      command, channel = parse_bot_commands(slack_client.rtm_read())
      if command:
        handle_command(command, channel)
      time.sleep(RTM_READ_DELAY)
  else:
    print("Connection failed. Exception traceback printed above.")
