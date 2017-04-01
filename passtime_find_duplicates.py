'''
This tool will search all the executions of a formula and look at the
trigger and check for the ``SEARCH_VALUE``
'''

import lib.ce_request
import json


FORMULA_INSTANCE_ID = "12397"
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
        results = []

        # get all executions
        unfiltered_executions = my_session.get_all_objects(object_path=FORMULA_EXECUTION_URL)
        
        # Filter out all executions before `SKIP_TO_ID`
        for item in unfiltered_executions:
            if item['status'] != 'success':
                executions.append(item)
            else:
                skipped += 1

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
            product_body = ""
            trigger_body = ""
            for step in steps:
                if step['stepName'] == 'Get_CRM_Product':
                    
                    # Get Step Values
                    values = my_session.send_request(
                        method='get',
                        url_path=FORMULA_STEP_VALUES_URL.format(stepExecutionId=step['id'])).json()
                    # Loop over Values
                    for value in values:
                        if value['key'] == 'Get_CRM_Product.response.body':
                            body_json = json.loads(value['value'])
                            if len(body_json) > 1:
                                names = [x['attributes']['name'] for x in body_json]
                                product_body =" <--> ".join(names)
                if step['stepName'] == 'Get_QB_Invoice':

                    # Get Step Values
                    values = my_session.send_request(
                        method='get',
                        url_path=FORMULA_STEP_VALUES_URL.format(stepExecutionId=step['id'])).json()
                    # Loop over Values
                    for value in values:
                        if value['key'] == 'Get_QB_Invoice.response.body':
                            body_json = json.loads(value['value'])
                            if 'Other' in body_json:
                                trigger_body = "{}({})".format(body_json['Other'], body_json['TxnID'])
            if product_body != "" and trigger_body != "":
                my_str = "{}: {}".format(trigger_body, product_body)
                if my_str not in results:
                    results.append(my_str)


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

