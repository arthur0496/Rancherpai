import os
import requests
import json
import time

#environmentName = 'Default'


def get_environment(environmentName):
  r = requests.get(os.environ['RANCHER_URL'] + 'v1/environments?name=' + environmentName,auth=(os.environ['RANCHER_ACCESS_KEY'], os.environ['RANCHER_SECRET_KEY']))

  return r.json()['data'][0]

def get_service(serviceName,environmentName):
  environment = get_environment(environmentName)

  r = requests.get(os.environ['RANCHER_URL'] + 'v1/services?name=' + serviceName + '&environmentId=' + environment['id'],auth=(os.environ['RANCHER_ACCESS_KEY'], os.environ['RANCHER_SECRET_KEY']))

  return r.json()['data'][0]

def service_upgrade(serviceName,environmentName):

  service = get_service(serviceName,environmentName)
    
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

  headers = {'content-type': 'application/json'}

  if(service['state'] == 'upgraded'):
    r = requests.post(os.environ['RANCHER_URL'] + 'v1/services/' + service['id'] + '/?action=rollback',
                      headers=headers, auth=(os.environ['RANCHER_ACCESS_KEY'], os.environ['RANCHER_SECRET_KEY']));
    return 'Rolling back service ' + service['name']
  else:
    return 'The service ' + service['name'] + ' is not being upgraded'

def finish_upgrade(serviceName,environmentName):
  
  service = get_service(serviceName,environmentName)

  headers = {'content-type': 'application/json'}
  
  if(service['state'] == 'upgraded'):
    r = requests.post(os.environ['RANCHER_URL'] + 'v1/services/' + service['id'] + '/?action=finishupgrade',
                      headers=headers, auth=(os.environ['RANCHER_ACCESS_KEY'], os.environ['RANCHER_SECRET_KEY']));
    return 'Finishing service ' + service['name'] + ' upgrade'
  else:
    return 'The service ' + service['name'] + ' is not being upgraded'

def restart_service(serviceName,environmentName):
  service = get_service(serviceName,environmentName)

  payload = {
    "rollingRestartStrategy": ""
  }

  headers = {'content-type': 'application/json'}
  r = requests.post(os.environ['RANCHER_URL'] + 'v1/services/' + service['id'] + '/?action=restart',
                    data=json.dumps(payload), headers=headers, auth=(os.environ['RANCHER_ACCESS_KEY'], os.environ['RANCHER_SECRET_KEY']));
  return 'Restarting service ' + service['name']
