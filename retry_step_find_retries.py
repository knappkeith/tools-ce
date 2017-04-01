'''
This tool will search all the executions of a formula and look at the
trigger and check for the ``SEARCH_VALUE``
'''

import lib.ce_request
import json

FORMULA_INSTANCE_ID = "12869" # test on regular
# FORMULA_INSTANCE_ID = "12892" # test on backup
# FORMULA_INSTANCE_ID = "12397" # on regular invoice
# FORMULA_INSTANCE_ID = "12398" # on backup invoice
FORMULA_EXECUTION_URL = "{formula_instance_id}/executions".format(formula_instance_id=FORMULA_INSTANCE_ID)
FORMULA_EXECUTION_STEPS_URL = "executions/{executionId}/steps"
FORMULA_STEP_VALUES_URL = "executions/steps/{stepExecutionId}/values"
BASE_URL = "https://console.cloud-elements.com/elements/api-v2/formulas/instances"
AUTH_HEADER = "User gS9xXNOSrebnb0BS956HWNUHMw+iaeHEx1PoMc/Ql9Q=, Organization 89341d5d002f3091e5cd5876d7ed8ff0"

if __name__ == "__main__":
    try:
        my_session = lib.ce_request.CloudElementsPlatform(
            base_url=BASE_URL,
            auth_header=AUTH_HEADER)

        # Declare some stuff
        skipped = 0
        executions = []
        count = 1
        statusi = {}
        results = {}
        unique_objects = []

        # get all executions
        unfiltered_executions = my_session.get_all_objects(object_path=FORMULA_EXECUTION_URL)

        # No Skipping for this one
        executions = list(unfiltered_executions)

        print "{num:>10} executions found!".format(num=len(unfiltered_executions))
        print "{num:>10} executions skipped!".format(num=skipped)
        print "{num:>10} executions to check!\n".format(num=len(executions))

        # Let's do this
        for execution in executions:
            print "Checking Execution --> ({cur:^{tot_len}}/{total}): ID: {execution_id} [status: {status:>7}, time: {time}]".format(
                execution_id=execution['id'],
                cur=count,
                tot_len=len(str(len(executions))),
                total=len(executions),
                status=execution['status'],
                time=execution['createdDate'])
            count += 1

            # Save Status
            if execution['status'] not in statusi:
                statusi[execution['status']] = 1
            else:
                statusi[execution['status']] += 1

            # Get Steps
            steps = my_session.get_all_objects(
                object_path=FORMULA_EXECUTION_STEPS_URL.format(
                    executionId=execution['id']))
            
            # Loop over Steps
            actual_status = execution['status']
            if 'SendErrorNotice' in [x['stepName'] for x in steps]:
                actual_status = 'failed'
            for step in steps:               

                if step['stepName'] == 'trigger':
                    
                    # Get Step Values
                    values = my_session.send_request(
                        method='get',
                        url_path=FORMULA_STEP_VALUES_URL.format(
                            stepExecutionId=step['id'])).json()
                    # Loop over Values
                    object_id = ""
                    retry_attempt = "-"
                    event_id = ""
                    for value in values:
                        if value['key'] == 'trigger.event':
                            body_json = json.loads(value['value'])
                            object_id = body_json['objectId']
                        if value['key'] == 'trigger.retryAttemptNumber':
                            retry_attempt = value['value']
                        if value['key'] == 'trigger.eventId':
                            event_id = value['value']
                    if object_id != "":
                        if event_id not in results.keys():
                            results[event_id] = {}
                        if object_id not in results[event_id].keys():
                            results[event_id][object_id] = []
                        results[event_id][object_id].append(
                            "Execution ID:{exec_id:>9}, Status:{status:>8}, Attempt: {att_num:>2}, Time: {time}".format(
                                exec_id=execution['id'],
                                status=actual_status,
                                att_num=retry_attempt,
                                time=execution['createdDate']))

    finally:
        print "\n{:->110}".format("")
        print "SUMMARY:"
        print "{:->110}".format("")
        print "{msg:>25} : {value:>10}".format(msg="Formula Instance ID", value=FORMULA_INSTANCE_ID)
        print "{msg:>25} : {value:>10}".format(
            msg="Executions Found", value=len(unfiltered_executions))
        print "{msg:>25} : {value:>10}".format(
            msg="Executions Checked", value=count)
        print "{msg:>25} : {value:>10}".format(
            msg="Executions Skipped", value=skipped)
        print "{msg:>25} : {value:>10}".format(
            msg="Unique Events Found", value=len(results.keys()))
        print "{:->110}\n".format("")
        print "{:->110}".format("")
        print "STATUSES:"
        print "{:->110}".format("")
        for k, v in statusi.iteritems():
            print "{status:>25} : {num:>10}".format(status=k, num=v)
        print "{:->110}\n".format("")
        print "{:->110}".format("")
        print "RESULTS:"
        print "{:->110}".format("")
        if len(results) == 0:
            print "    No Results Found"
        else:
            print "\n".join(
                ["{label:>13} {event_id} ({num_obj}):\n{objs}\n".format(
                    label="Event ID:",
                    event_id=event_id,
                    num_obj=len(objs.keys()),
                    objs="\n".join(
                        ["{label:>26} {obj_id} ({num_exec}):\n{execs}".format(
                            label="* Object ID:",
                            obj_id=obj_id,
                            num_exec=len(execs),
                            execs="\n".join(
                                ["{label:>28} {info}".format(
                                    label="-",
                                    info=execution) for execution in execs]
                                )
                            ) for obj_id, execs in objs.iteritems()]
                        )
                    ) for event_id, objs in results.iteritems()]
                )
        print "{:->110}\n".format("")

