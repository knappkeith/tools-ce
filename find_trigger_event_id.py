'''
This tool will search all the executions of a formula and look at the
trigger and check for the ``SEARCH_VALUE``
'''

import lib.ce_request
import json


FORMULA_INSTANCE_ID = "3647"
FORMULA_EXECUTION_URL = "{formula_instance_id}/executions".format(formula_instance_id=FORMULA_INSTANCE_ID)
FORMULA_EXECUTION_STEPS_URL = "executions/{executionId}/steps"
FORMULA_STEP_VALUES_URL = "executions/steps/{stepExecutionId}/values"
BASE_URL = "https://console.cloud-elements.com/elements/api-v2/formulas/instances"
AUTH_HEADER = "User GvFGhARhkncvl9NAP57ArDpn2hwqTd58N2WgfP/XTB4=, Organization 0760ec2bb80346bd3c4ffc952a3cadb1"
SEARCH_VALUE = "W12005450-1"
SKIP_TO_ID = '43943594'


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
        results = []

        # get all executions
        unfiltered_executions = my_session.get_all_objects(object_path=FORMULA_EXECUTION_URL)
        
        # Filter out all executions before `SKIP_TO_ID`
        if SKIP_TO_ID != '':
            skipping = True
        else:
            skipping = False
        for item in unfiltered_executions:
            if skipping:
                if str(item['id']) == str(SKIP_TO_ID):
                    skipping = False
                    executions.append(item)
                else:
                    skipped += 1
            else:
                executions.append(item)

        print "{num} executions found!".format(num=len(unfiltered_executions))
        print "{num} executions skipped!".format(num=skipped)
        print "{num} executions to check!\n".format(num=len(executions))

        # Let's do this
        for execution in executions:
            print "Checking execution ({cur}/{total}): {execution_id} (status: {status}, time: {time})".format(
                execution_id=execution['id'], cur=count, total=len(executions), status=execution['status'], time=execution['createdDate'])
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
            for step in steps:
                if step['stepName'] == 'trigger':
                    
                    # Get Step Values
                    values = my_session.send_request(
                        method='get',
                        url_path=FORMULA_STEP_VALUES_URL.format(stepExecutionId=step['id'])).json()
                    
                    # Loop over Values
                    for value in values:
                        try:
                            if value['key'] == 'trigger.event':
                                
                                # Search Value for SEARCH_VALUE
                                if SEARCH_VALUE.upper() in value['value'].upper():
                                    print "    {execution_id}: {status} ({time})".format(
                                        execution_id=execution['id'], status=execution['status'], time=execution['createdDate'])
                                    results.append("{execution_id}: {status} ({time})".format(
                                        execution_id=execution['id'], status=execution['status'], time=execution['createdDate']))
                        except:
                            print json.dumps(values, indent=2)
    finally:
        print "\n\nRESULTS:"
        print "    Executions Found: {}".format(len(unfiltered_executions))
        print "    Executions Checked: {}".format(count)
        print "    Executions Skipped: {}".format(skipped)
        print "    Results Found: {}".format(len(results))
        print "----------------------------------------"
        if len(results) == 0:
            print "    No Results Found"
        else:
            for result in results:
                print "    {}".format(result)
        print "----------------------------------------"
        print "STATUSES:"
        for k, v in statusi.iteritems():
            print "    {}: {}".format(k, v)
        print "----------------------------------------\n\n"

