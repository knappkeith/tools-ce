'''
This Script will get all step executions and step execution values
for all of the Execution IDs in ``MY_EXECUTION_IDS`` and Save them
to the file, file name must exist and have ``{execution_id}``
'''
import lib.ce_request
import json


FORMULA_INSTANCE_ID = "15967"
MY_EXECUTION_IDS = ['41328587']
ORG_SECRET = "2007c56f802d3fb1e913e147139bca34"
USER_SECRET = "zzGwpugde7xdWGCfJDZj8RPZwcvPFDnJCsyAdAuyj04="
BASE_URL = "https://staging.cloud-elements.com/elements/api-v2/formulas/instances/"
FILE_PATH = "/Users/keith/Desktop/for_Cassie({execution_id})-2.json"


FORMULA_EXECUTION_URL = "{formula_instance_id}/executions".format(
                            formula_instance_id=FORMULA_INSTANCE_ID)
FORMULA_EXECUTION_STEPS_URL = "executions/{executionId}/steps"
FORMULA_STEP_VALUES_URL = "executions/steps/{stepExecutionId}/values"


def find_execution_that_isnt_pending(session):
    my_iter = session.send_request_iter(
        method='get',
        url_path=FORMULA_EXECUTION_URL)
    total_count = 0
    for executions in my_iter:
        total_count += len(executions.json())
        print "Got {num}({total} total) executions with next page token of: {token}".format(num=len(executions.json()), token=executions.headers.get('Elements-Next-Page-Token'), total=total_count)
        for execution in executions.json():
            if execution['status'] != "pending":
                cont = raw_input("Execution {exec_num} has a status of {status}, continue? (Y/N)".format(exec_num=execution['id'], status=execution['status']))
                if cont.upper() == "N":
                    return

def print_all_step_executions_to_file(session):
    for execution in MY_EXECUTION_IDS:
        print "Getting execution: {0}".format(execution)
        my_execution_steps_iter = get_all(
            my_url_path=FORMULA_EXECUTION_STEPS_URL.format(executionId=execution),
            my_session=session)
        print "Got execution: {0}".format(execution)
        with open(FILE_PATH.format(execution_id=execution), 'w') as fd:
            write_str = "[\n"
            total_count = 0
            for my_iter in my_execution_steps_iter:
                my_execution_steps = my_iter[0]
                fd.write(write_str)
                write_str = ","
                total_count += len(my_execution_steps)
                print "Got a new set with {0} steps and a next page token of '{1}'".format(len(my_execution_steps), my_iter[1])
                for index in range(0, len(my_execution_steps)):
                    my_values = session.send_request(
                        method='get',
                        url_path=FORMULA_STEP_VALUES_URL.format(
                            stepExecutionId=my_execution_steps[index]['id'])).json()
                    new_dict = dict(my_execution_steps[index])
                    new_dict['values'] = my_values
                    fd.writelines(json.dumps(
                        new_dict,
                        indent=4,
                        sort_keys=True,
                        separators=(',', ': ')))
                    if index != len(my_execution_steps) - 1:
                        fd.write(",")
                    print "Getting Step Values {0}/{1} ({2} total so far) for execution step: {3}".format(
                        index,
                        len(my_execution_steps),
                        total_count,
                        my_execution_steps[index]['id'])
            fd.write("]")

if __name__ == "__main__":
    my_request = lib.ce_request.CloudElementsPlatform(
        base_url=BASE_URL,
        auth_header="User {user}, Organization {org}".format(
            user=USER_SECRET, org=ORG_SECRET))
    find_execution_that_isnt_pending(my_request)
