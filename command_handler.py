from rancherpai import *


SERVICE = 'service'
UPGRADE = 'upgrade'
ENVIRONMENT = 'stack'

#help commands
HELP = 'help'
SERVICE_HELP = HELP + ' ' + SERVICE
SERVICE_HELP_DESCRIPTION = 'this command that show all service commands and their descriptions, this command requires no argumensts'  
UPGRADE_HELP = HELP + ' ' + UPGRADE
UPGRADE_HELP_DESCRIPTION = 'this command that show all upgrade commands and their descriptions, this command requires no argumensts'  
ENVIRONMENT_HELP = HELP + ' ' + ENVIRONMENT
ENVIRONMENT_HELP_DESCRIPTION = 'this command that show all environment commands and their descriptions, this command requires no argumensts'  
HELP_COMMANDS = [(SERVICE_HELP,SERVICE_HELP_DESCRIPTION), (UPGRADE_HELP,UPGRADE_HELP_DESCRIPTION), (ENVIRONMENT_HELP,ENVIRONMENT_HELP_DESCRIPTION)]
0
#services commands
UPGRADE_SERVICE = SERVICE + ' upgrade'
UPGRADE_SERVICE_DESCRIPTION = 'this command upgrades a service, it requires two arguments: The stack where the service is located and the chosen service'  
RESTART_SERVICE = SERVICE + ' restart'
RESTART_SERVICE_DESCRIPTION = 'this command restart a service, it requires two arguments: The stack where the service is located and the chosen service'  
STATE_SERVICE = SERVICE + ' state'
STATE_SERVICE_DESCRIPTION = 'this command shows the state of a service, it requires two arguments: The stack where the service is located and the chosen service'  
HEALTH_SERVICE = SERVICE + ' health'
HEALTH_SERVICE_DESCRIPTION = 'this command shows the health of a service, it requires two arguments: The stack where the service is located and the chosen service'  
STATUS_SERVICE = SERVICE + ' status'
STATUS_SERVICE_DESCRIPTION = 'this command shows the report for a service, it requires two arguments: The stack where the service is located and the chosen service'  
SERVICE_COMMANDS = [(UPGRADE_SERVICE,UPGRADE_SERVICE_DESCRIPTION), (RESTART_SERVICE,RESTART_SERVICE_DESCRIPTION), (STATE_SERVICE,STATE_SERVICE_DESCRIPTION),(HEALTH_SERVICE,HEALTH_SERVICE_DESCRIPTION),(STATUS_SERVICE,STATUS_SERVICE_DESCRIPTION)]

#upgrade commands
ROLLBACK_UPGRADE = UPGRADE + ' rollback'
ROLLBACK_UPGRADE_DESCRIPTION = 'this command rollback a upgrades , it requires two arguments: The stack where the service is located and the service that will be upgraded'  
FINISH_UPGRADE = UPGRADE + ' finish'
FINISH_UPGRADE_DESCRIPTION = 'this command finishs a upgrades , it requires two arguments: The stack where the service is located and the service that will be upgraded'  
UPGRADE_COMMANDS = [(ROLLBACK_UPGRADE,ROLLBACK_UPGRADE_DESCRIPTION),(FINISH_UPGRADE,FINISH_UPGRADE_DESCRIPTION)]

#environment commands
STATUS_ENVIRONMENT = ENVIRONMENT + ' status'
STATUS_ENVIRONMENT_DESCRIPTION = 'this command shows , it requires two arguments: The stack where the service is located and the service that will be upgraded'  
ENVIRONMENT_COMMANDS = [(STATUS_ENVIRONMENT,STATUS_ENVIRONMENT_DESCRIPTION)]

#all
COMMANDS = HELP_COMMANDS + SERVICE_COMMANDS + UPGRADE_COMMANDS + ENVIRONMENT_COMMANDS

def handle_command(command):
  default_response =  'Unknown command: \"' + command + '\"'
  

  if (command.startswith(SERVICE)):
    response = handle_service_command(command)
  elif (command.startswith(UPGRADE)):
    response = handle_upgrade_command(command)
  elif (command.startswith(ENVIRONMENT)):
    response = handle_environment_command(command)
  elif (command.startswith(HELP)):
    response = handle_help_command(command)
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

def handle_help_command(command):
  words = command.split(' ')

  if (command.startswith(SERVICE_HELP)):
    if (len(words) != 2):
      return 'the command\"' + SERVICE_HELP + '\" does not acept arguments'
    else:
      response = 'List of service commands:\n'
      for cmd in SERVICE_COMMANDS:
        response += '\t' + cmd[0] + ' - ' + cmd[1] + '\n\n' 
      return response
  elif (command.startswith(UPGRADE_HELP)):
    if (len(words) != 2):
      return 'the command\"' + UPGRADE_HELP + '\" does not acept arguments'
    else:
      response = 'List of upgrade commands:\n'
      for cmd in UPGRADE_COMMANDS:
        response += '\t' + cmd[0] + ' - ' + cmd[1] + '\n\n' 
      return response
  elif (command.startswith(ENVIRONMENT_HELP)):
    if (len(words) != 2):
      return 'the command\"' + ENVIRONMENT_HELP + '\" does not acept arguments'
    else:
      response = 'List of upgrade commands:\n'
      for cmd in ENVIRONMENT_COMMANDS:
        response += '\t' + cmd[0] + ' - ' + cmd[1] + '\n\n'
      return response
  else:
    if(len(words) != 1):
      return 'the command\"' + HELP + '\" does not acept arguments'
    else:
      response = 'List of commands:\n'
      for cmd in COMMANDS:
        response += '\t' + cmd[0] + ' - ' + cmd[1] + '\n\n' 
      return response




