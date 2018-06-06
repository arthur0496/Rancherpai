import os
import requests
import json
import time

#environmentName = 'Default'
environmentName = 'Observ'
serviceName = 'frontend'
newImage = 'docker:tropicalhazards/tropical-hazards-front:latest'


def service_upgrade():
  r = requests.get(os.environ['RANCHER_URL'] + 'v1/environments?name=' + environmentName,auth=(os.environ['RANCHER_ACCESS_KEY'], os.environ['RANCHER_SECRET_KEY']))

  environment = r.json()['data'][0]

  r = requests.get(os.environ['RANCHER_URL'] + 'v1/services?name=' + serviceName + '&environmentId=' + environment['id'],auth=(os.environ['RANCHER_ACCESS_KEY'], os.environ['RANCHER_SECRET_KEY']))

  service = r.json()['data'][0]
    
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

def upgrade_rollback():
  r = requests.get(os.environ['RANCHER_URL'] + 'v1/environments?name=' + environmentName,auth=(os.environ['RANCHER_ACCESS_KEY'], os.environ['RANCHER_SECRET_KEY']))

  environment = r.json()['data'][0]

  r = requests.get(os.environ['RANCHER_URL'] + 'v1/services?name=' + serviceName + '&environmentId=' + environment['id'],auth=(os.environ['RANCHER_ACCESS_KEY'], os.environ['RANCHER_SECRET_KEY']))

  service = r.json()['data'][0]

  headers = {'content-type': 'application/json'}

  if(service['state'] == 'upgraded'):
    r = requests.post(os.environ['RANCHER_URL'] + 'v1/services/' + service['id'] + '/?action=rollback',
                      headers=headers, auth=(os.environ['RANCHER_ACCESS_KEY'], os.environ['RANCHER_SECRET_KEY']));
    return 'Rolling back service ' + service['name']
  else:
    return 'The service ' + service['name'] + ' is not being upgraded'

def finish_upgrade():
  
  r = requests.get(os.environ['RANCHER_URL'] + 'v1/environments?name=' + environmentName,auth=(os.environ['RANCHER_ACCESS_KEY'], os.environ['RANCHER_SECRET_KEY']))

  environment = r.json()['data'][0]

  r = requests.get(os.environ['RANCHER_URL'] + 'v1/services?name=' + serviceName + '&environmentId=' + environment['id'],auth=(os.environ['RANCHER_ACCESS_KEY'], os.environ['RANCHER_SECRET_KEY']))

  service = r.json()['data'][0]

  headers = {'content-type': 'application/json'}
  
  if(service['state'] == 'upgraded'):
    r = requests.post(os.environ['RANCHER_URL'] + 'v1/services/' + service['id'] + '/?action=finishupgrade',
                      headers=headers, auth=(os.environ['RANCHER_ACCESS_KEY'], os.environ['RANCHER_SECRET_KEY']));
    return 'Finishing service ' + service['name'] + ' upgrade'
  else:
    return 'The service ' + service['name'] + ' is not being upgraded'
