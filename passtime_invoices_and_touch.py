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
AUTH_HEADER_CRM = "User gS9xXNOSrebnb0BS956HWNUHMw+iaeHEx1PoMc/Ql9Q=, Organization 89341d5d002f3091e5cd5876d7ed8ff0, Element XuWtBUGuRQiJPl5bIXVaMxcnStWWo/A5udKPj67VTNE="
BASE_URL_CRM = "https://console.cloud-elements.com/elements/api-v2/hubs/crm"
MS_STATE_CODE = {
                    "0": "Active",
                    "1": "Submitted",
                    "2": "Canceled",
                    "3": "Fulfilled",
                    "4": "Invoiced"
                }
MS_STATUS_CODE = {
                    "1": "New",
                    "2": "Pending",
                    "3": "In Progress",
                    "4": "No Money",
                    "100001": "Complete",
                    "100002": "Partial",
                    "100003": "Invoiced"
                }

if __name__ == "__main__":
    try:
        my_session = lib.ce_request.CloudElementsPlatform(
            base_url=BASE_URL,
            auth_header=AUTH_HEADER)
        my_element = lib.ce_request.CloudElementsElement(
            base_url=BASE_URL_CRM,
            auth_header=AUTH_HEADER_CRM)

        # Declare some stuff
        skipped = 0
        executions = []
        count = 1
        statusi = {}
        results = []

        # get all executions
        unfiltered_executions = my_session.get_all_objects(object_path=FORMULA_EXECUTION_URL)

        # Filter out all executions before `SKIP_TO_ID`
        executions = list(unfiltered_executions)
        # for item in unfiltered_executions:
        #     if item['status'] != 'success':
        #         executions.append(item)
        #     else:
        #         skipped += 1

        print "{num} executions found!".format(num=len(unfiltered_executions))
        print "{num} executions skipped!".format(num=skipped)
        print "{num} executions to check!\n".format(num=len(executions))

        # Let's do this
        for execution in executions:
            print "Checking execution ({cur:>{tot_len}}/{total}): {execution_id} (status: {status:>7}, time: {time})".format(
                execution_id=execution['id'], cur=count, total=len(executions), status=execution['status'], time=execution['createdDate'], tot_len=len(str(len(executions))))
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
            qb_invoice_id = ""
            crm_sales_order_id = ""
            actual_status = execution['status']
            for step in steps:
                if step['stepName'] == 'SendErrorNotice':
                    actual_status = "failed"                

                if step['stepName'] == 'trigger':
                    
                    # Get Step Values
                    values = my_session.send_request(
                        method='get',
                        url_path=FORMULA_STEP_VALUES_URL.format(stepExecutionId=step['id'])).json()
                    # Loop over Values
                    for value in values:
                        if value['key'] == 'trigger.event':
                            body_json = json.loads(value['value'])
                            qb_invoice_id = "Invoice ID: {x[objectId]}".format(x=body_json)

                if step['stepName'] == 'Get_CRM_SalesOrder':

                    # Get Step Values
                    values = my_session.send_request(
                        method='get',
                        url_path=FORMULA_STEP_VALUES_URL.format(stepExecutionId=step['id'])).json()
                    # Loop over Values
                    for value in values:
                        if value['key'] == 'Get_CRM_SalesOrder.response.body':
                            body_json = json.loads(value['value'])
                            if len(body_json) > 0:
                                my_so = my_element.send_request(
                                    method='get',
                                    url_path="/salesorder/{}".format(body_json[0]['id']))
                                if my_so.status_code != 200:
                                    my_element.print_my_last()
                                    crm_sales_order_id = "Error: {}".format(my_so.status_code)
                                else:
                                    if MS_STATE_CODE[str(my_so.json()['attributes']['statecode'])] != 'Invoiced' and MS_STATUS_CODE[str(my_so.json()['attributes']['statuscode'])] != 'Invoiced':
                                        crm_sales_order_id = "Sales Order ID: {} ({}-{})".format(
                                            body_json[0]['attributes']['name'],
                                            MS_STATE_CODE[str(my_so.json()['attributes']['statecode'])],
                                            MS_STATUS_CODE[str(my_so.json()['attributes']['statuscode'])])
            if qb_invoice_id != "" and crm_sales_order_id != "":
                my_str = "{}({:>7}): {}".format(qb_invoice_id, actual_status, crm_sales_order_id)
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

