import requests
import json


INSTANCE_ID = "1343"
HEADERS = {
    "Accept": "application/json",
    "Authorization": "User PiAWsSUC1KVaDJr+HZLqN55VPdeP8WBCE//QKmIVu3Y=, Organization 7eb50b168298e05b797e29a2df5c9d1b"
    }
URL = 'https://console.cloud-elements.com/elements/api-v2/formulas/{resource}'
URL_EXECUTIONS = 'instances/{instance_id}/executions'
URL_EXECUTION = "instances/executions/{execution_id}"
URL_STEP_VALUES = "instances/executions/steps/{step_id}/values"

LAST_EXECUTION = 35851408


def get_formulas():
    return requests.get(
        URL.format(
            resource=""), headers=HEADERS).json()

def get_executions(instance_id):
    return requests.get(
        URL.format(
            resource=URL_EXECUTIONS.format(
                instance_id=instance_id)), headers=HEADERS).json()


def get_execution(execution_id):
    return requests.get(
        URL.format(
            resource=URL_EXECUTION.format(
                execution_id=execution_id)), headers=HEADERS).json()


def get_step_values(step_id):
    return requests.get(
        URL.format(
            resource=URL_STEP_VALUES.format(
                step_id=step_id)), headers=HEADERS).json()


def check_it(stop_id=0):
    executions = get_executions(INSTANCE_ID)
    print "{} executions".format(len(executions))
    cnt = 0
    for i in executions:
        if cnt == 0:
            print "First Execution ID: {0}".format(i['id'])
            LAST_EXECUTION = i['id']
        cnt += 1
        execution = get_execution(i['id'])
        opp_value = ""
        trigger_value = ""
        if i['id'] == stop_id:
            print "Ran {0} checks, out of {1}".format(cnt, len(executions))
            return
        for j in execution['stepExecutions']:
            if j['stepName'] == '1-get-opp':
                opp = get_step_values(j['id'])
                for k in opp:
                    if k['key'] == '1-get-opp.request.uri':
                        opp_value = k['value']
            if j['stepName'] == 'trigger':
                trigger = get_step_values(j['id'])
                for k in trigger:
                    if k['key'] == 'trigger.event':
                        trigger_value = json.loads(k['value'])['objectId']
        if opp_value != "" and not opp_value.endswith(trigger_value):
            print "{}: {} - {}".format(i['id'], trigger_value, opp_value)
    return


def check_retries():
    for k in [35444309, 35441703, 35441349]:
        print "Execution: {}".format(k)
        st = get_execution(k)
        for i in st['stepExecutions']:
            for j in get_step_values(i['id']):
                if j['key'].endswith(".request.retry-attempt"):
                    print "    {0}: {1}".format(i['stepName'], j['value'])

def check_formula_steps_filter():
    formulas = get_formulas()
    for formula in formulas:
        steps = [x for x in formula['steps'] if x['type'] == 'script']
        formula_good = True
        print "Checking Formula: {0}".format(formula['name'])
        for step in steps:
            if 'done(true)' in step['properties']['body']:
                print json.dumps(step, indent=2)
                formula_good = False
            elif 'done(false)' in step['properties']['body']:
                print json.dumps(step, indent=2)
                formula_good = False
        if formula_good:
            print "    Formula {0} is ok!!".format(formula['name'])
