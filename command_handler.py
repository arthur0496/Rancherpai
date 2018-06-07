from rancherpai import *

#services commands
SERVICE = 'service'
UPGRADE_SERVICE = SERVICE + ' upgrade'
RESTART_SERVICE = SERVICE + ' restart'
STATE_SERVICE = SERVICE + ' state'
HEALTH_SERVICE = SERVICE + ' health'
STATUS_SERVICE = SERVICE + ' status'

#upgrade commands
UPGRADE = 'upgrade'
ROLLBACK_UPGRADE = UPGRADE + ' rollback'
FINISH_UPGRADE = UPGRADE + ' finish'

#environment commands
ENVIRONMENT = 'stack'
STATUS_ENVIRONMENT = ENVIRONMENT + ' status'


def handle_command(command):
  default_response =  'Unknown command: \"' + command + '\"'
  

  if (command.startswith(SERVICE)):
    response = handle_service_command(command)
  elif (command.startswith(UPGRADE)):
    response = handle_upgrade_command(command)
  elif (command.startswith(ENVIRONMENT)):
    response = handle_environment_command(command)
  else:
    response = None

  return response or default_response

def handle_service_command(command):
  words = command.split(' ')
  
  if (command.startswith(UPGRADE_SERVICE)):
    if (len(words) != 4):
      return 'The command \"' + UPGRADE_SERVICE + '\" requires exactly 2 arguments' 
    else:
      return service_upgrade(words[3],words[2])
  elif (command.startswith(RESTART_SERVICE)):
    if (len(words) != 4):
      return 'The command \"' + RESTART_SERVICE + '\" requires exactly 2 arguments' 
    else:
      return restart_service(words[3],words[2])
  elif (command.startswith(STATE_SERVICE)):
    if (len(words) != 4):
      return 'The command \"' + STATE_SERVICE + '\" requires exactly 2 arguments' 
    else:
      return get_service_state(words[3],words[2])
  elif (command.startswith(HEALTH_SERVICE)):
    if (len(words) != 4):
      return 'The command \"' + HEALTH_SERVICE + '\" requires exactly 2 arguments' 
    else:
      return get_service_health(words[3],words[2])
  elif (command.startswith(STATUS_SERVICE)):
    if (len(words) != 4):
      return 'The command \"' + STATUS_SERVICE + '\" requires exactly 2 arguments' 
    else:
      return get_service_status(words[3],words[2])
  else:
    return None

def handle_upgrade_command(command):
  words = command.split(' ')

  if (command.startswith(ROLLBACK_UPGRADE)):
    if (len(words) != 4):
      return 'The command \"' + ROLLBACK_UPGRADE + '\" requires exactly 2 arguments' 
    else:
      return upgrade_rollback(words[3],words[2])
  elif (command.startswith(FINISH_UPGRADE)):
    if (len(words) != 4):
      return 'The command \"' + FINISH_UPGRADE + '\" requires exactly 2 arguments' 
    else:
      return finish_upgrade(words[3],words[2])
  else:
    return None
def handle_environment_command(command):
  words = command.split(' ')

  if (command.startswith(STATUS_ENVIRONMENT)):
    if (len(words) != 3): 
      return 'The command \"' + STATUS_ENVIRONMENT + '\" requires exactly 1 argument'
    else:
      return get_environment_status(words[2])
  else:
    return None
