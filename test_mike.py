'''
This tool will search all the executions of a formula and look at the
trigger and print out the number for ``recordsCount``
'''

import lib.ce_requests
import json


formula_instance_id = "7291"
formula_execution_url = "elements/api-v2/formulas/instances/{formula_instance_id}/executions".format(formula_instance_id=formula_instance_id)
formula_execution_steps_url = "elements/api-v2/formulas/instances/executions/{executionId}/steps"
formula_step_values_url = "elements/api-v2/formulas/instances/executions/steps/{stepExecutionId}/values"

my_request = lib.ce_requests.CloudElementsPlatform(
    base_url="https://console.cloud-elements.com/",
    auth_header="User wdqRRh9fmoGzuy2gfzFtNCJZLZWL7SebMVz91Jn75EU=, Organization 52d11b28b6f4aa3e107b504262881eed")

my_call = my_request.send_request(method='get', url_path=formula_execution_url)
executions = my_call.json()
my_executions = []
while len(executions) == 200:
    my_executions.extend(executions)
    my_call = my_request.send_request(method='get', url_path=formula_execution_url, params={'nextPage': my_call.headers['Elements-Next-Page-Token']})
    executions = my_call.json()

my_executions.extend(executions)
my_executions = my_executions[::-1]

for execution in my_executions:
    my_execution = my_request.send_request(method='get', url_path=formula_execution_steps_url.format(executionId=execution['id'])).json()
    trigger_id = [x['id'] for x in my_execution if x['stepName'] == 'trigger'][0]
    my_values = my_request.send_request(method='get', url_path=formula_step_values_url.format(stepExecutionId=trigger_id)).json()
    for value in my_values:
        if value['key'] == 'trigger.args':
            my_json = json.loads(value['value'])
            print "{exec_id} has {count} for 'recordsCount'".format(exec_id=execution['id'], count=my_json['recordsCount'])
