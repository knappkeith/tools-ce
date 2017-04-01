'''
This tool will search all the executions of a formula and look at the
trigger and check for the ``SEARCH_VALUE``
'''

import lib.ce_request
import datetime


FORMULA_INSTANCE_ID = "12397"
FORMULA_EXECUTION_URL = "{formula_instance_id}/executions".format(formula_instance_id=FORMULA_INSTANCE_ID)
BASE_URL = "https://console.cloud-elements.com/elements/api-v2/formulas/instances"
AUTH_HEADER = "User gS9xXNOSrebnb0BS956HWNUHMw+iaeHEx1PoMc/Ql9Q=, Organization 89341d5d002f3091e5cd5876d7ed8ff0"

HOURS = 4

if __name__ == "__main__":
    try:
        my_session = lib.ce_request.CloudElementsPlatform(
            base_url=BASE_URL,
            auth_header=AUTH_HEADER)

        # Declare some stuff
        start_time = datetime.datetime.utcnow()
        end_time = start_time - datetime.timedelta(hours=HOURS)
        count = 0

        # get all executions
        unfiltered_executions = my_session.get_all_objects(object_path=FORMULA_EXECUTION_URL)

        # Let's do this
        for execution in unfiltered_executions:
            my_time = datetime.datetime.strptime(execution['createdDate'], "%Y-%m-%dT%H:%M:%SZ")
            my_diff = my_time - end_time
            if my_diff.total_seconds() > 0:
                count += 1
            else:
                break

    finally:
        print "\n----------------------------------------------------------"
        print "RESULTS:"
        print "{msg:>35}: {execs:>6}".format(msg="Total Executions", execs=len(unfiltered_executions))
        print "{msg:>35}: {num:>6}".format(msg="Executions in last {hours:>2} hours".format(hours=HOURS), num=count)
        print "----------------------------------------------------------"
