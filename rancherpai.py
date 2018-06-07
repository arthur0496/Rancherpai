import os
import requests
import json
import time

#environmentName = 'Default'


def get_environment(environmentName):
  r = requests.get(os.environ['RANCHER_URL'] + 'v1/environments?name=' + environmentName,auth=(os.environ['RANCHER_ACCESS_KEY'], os.environ['RANCHER_SECRET_KEY']))

  if (len(r.json()['data']) > 0):
    return r.json()['data'][0]
  else:
    return None

def get_services(environment):
  r = requests.get(os.environ['RANCHER_URL'] + 'v1/services?environmentId=' + environment['id'],auth=(os.environ['RANCHER_ACCESS_KEY'],os.environ['RANCHER_SECRET_KEY']))
  
  if (len(r.json()['data']) > 0):
    return r.json()['data']
  else:
    return None

def get_environment_status(environmentName):
  environment = get_environment(environmentName)

  if (not environment):
    return 'Environment not found'
  else:
    response = 'Name : ' + environment['name'] + '\nDescription: '
  if (environment['description']):
    response += environment['description']
  else:
    response += 'null'
  response += '\nState: ' + environment['state']
  response += '\nHealth: ' + environment['healthState']
  response += '\nServices: '
  
  services = get_services(environment)

  if (not services):
    response += 'None'
  else:
    for service in services:
      response += '\n\tService: ' + service['name']
      response += '\n\t\tDescription: '
      if(service['description']):
        response += service['description']
      else:
        response += 'null'
      response += '\n\t\tState: ' + service['state']
      response += '\n\t\tHealth: ' + service['healthState']
  return response




def get_service(serviceName,environmentName):
  environment = get_environment(environmentName)
  
  if (environment == None):
    return None
  else:
    r = requests.get(os.environ['RANCHER_URL'] + 'v1/services?name=' + serviceName + '&environmentId=' + environment['id'],auth=(os.environ['RANCHER_ACCESS_KEY'], os.environ['RANCHER_SECRET_KEY']))
    
    if(len(r.json()['data']) == 0 ):
      return None
    else:
      return r.json()['data'][0]

def get_service_status(serviceName,environmentName):
  service = get_service(serviceName,environmentName)

  if(not service):
    return 'Service or environment not found'
  else:
    if(service['description']):
      description = service['description']
    else:
      description = 'null'
    return 'Name: ' + serviceName +'\nDescription: ' + description + '\nStack: ' + environmentName +  '\nState: ' + service['state'] + '\nHealth: ' + service['healthState'] 

def get_service_state(serviceName,environmentName):
  service = get_service(serviceName,environmentName)

  if(not service):
    return 'Service or environment not found'
  else:
    return 'The state of the ' + serviceName + ' service in the ' + environmentName + ' stack is: ' + service['state']


def get_service_health(serviceName,environmentName):
  service = get_service(serviceName,environmentName)

  if(not service):
    return 'Service or environment not found'
  else:
    return 'The healthstate of the ' + serviceName + ' service in the ' + environmentName + ' stack is: ' + service['healthState']


def service_upgrade(serviceName,environmentName):

  service = get_service(serviceName,environmentName)

  if (not service):
    return 'Service or environment not found'
    
  if(service['state'] == 'upgraded'):
    return 'the service ' + service['name'] + ' is already being upgraded finish the upgrade to continue'

  launchConfig = service['launchConfig']

  payload = {
    'inServiceStrategy': {
      'batchSize': 1,
      'intervalMillis': 2000,
      'startFirst': False,
      'launchConfig': launchConfig
    }
  }

  headers = {'content-type': 'application/json'}

  r = requests.post(os.environ['RANCHER_URL'] + 'v1/services/' + service['id'] + '/?action=upgrade',
                    data=json.dumps(payload), headers=headers,
                    auth=(os.environ['RANCHER_ACCESS_KEY'], os.environ['RANCHER_SECRET_KEY']))
  return 'the service ' + service['name'] + ' is being upgraded'

def upgrade_rollback(serviceName,environmentName):

  service = get_service(serviceName,environmentName)

  if (not service):
    return 'Service or environment not found'

  headers = {'content-type': 'application/json'}

  if(service['state'] == 'upgraded'):
    r = requests.post(os.environ['RANCHER_URL'] + 'v1/services/' + service['id'] + '/?action=rollback',
                      headers=headers, auth=(os.environ['RANCHER_ACCESS_KEY'], os.environ['RANCHER_SECRET_KEY']));
    return 'Rolling back service ' + service['name']
  else:
    return 'The service ' + service['name'] + ' is not being upgraded'

def finish_upgrade(serviceName,environmentName):
  
  service = get_service(serviceName,environmentName)

  if (not service):
    return 'Service or environment not found'

  headers = {'content-type': 'application/json'}
  
  if(service['state'] == 'upgraded'):
    r = requests.post(os.environ['RANCHER_URL'] + 'v1/services/' + service['id'] + '/?action=finishupgrade',
                      headers=headers, auth=(os.environ['RANCHER_ACCESS_KEY'], os.environ['RANCHER_SECRET_KEY']));
    return 'Finishing service ' + service['name'] + ' upgrade'
  else:
    return 'The service ' + service['name'] + ' is not being upgraded'

def restart_service(serviceName,environmentName):
  service = get_service(serviceName,environmentName)

  if (not service):
    return 'Service or environment not found'

  payload = {
    "rollingRestartStrategy": ""
  }

  headers = {'content-type': 'application/json'}
  r = requests.post(os.environ['RANCHER_URL'] + 'v1/services/' + service['id'] + '/?action=restart',
                    data=json.dumps(payload), headers=headers, auth=(os.environ['RANCHER_ACCESS_KEY'], os.environ['RANCHER_SECRET_KEY']));
  return 'Restarting service ' + service['name']
