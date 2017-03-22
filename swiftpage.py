'''
This Script will get all step executions and step execution values
for all of the Execution IDs in ``MY_EXECUTION_IDS`` and Save them
to the file, file name must exist and have ``{execution_id}``
'''
import lib.ce_request
import datetime
import json
import lib.timer_laps

# AUTH_HEADER = "Element E6Uk5r6yTFUagcA79zAqtdTqFWLpLKLIPA5VvirKTzk=, User zzGwpugde7xdWGCfJDZj8RPZwcvPFDnJCsyAdAuyj04=, Organization 2007c56f802d3fb1e913e147139bca34"
AUTH_HEADER = "User rkXa6a2qF8rdF7t0zMvVbDcWNHmxao+REQJkC/UKplI=, Organization da879e8b3e94e284d1b24538bf166795, Element 0IFXtODB8WabrqUJWfTJtLDuwn/qg83B+jgYbU0lZS4="

BASE_URL = "https://staging.cloud-elements.com/elements/api-v2/hubs/general"
POST_BODY = {
                "contacts": [
                    {
                        "id": "6f543020-a93a-44fd-91f7-08f49d64deb1"
                    }
                ],
                "details": "OrderId: {order_number}\nOrder Items:\n \t1 [Sample] Levi's, blue denim womens shirt @ $0.00\n\nOrder Total: $0.00\nLink to Order: https://store-wuxeae6.mybigcommerce.com\nOrder Status: Awaiting Fulfillment",
                "duration": "15 minutes",
                "endTime": "2017-03-16T17:21:16.345Z",
                "historyTypeID": 101,
                "isPrivate": False,
                "regarding": "bigcommerce",
                "startTime": "2017-03-16T17:06:16.345Z"
            }


if __name__ == "__main__":
    try:
        my_timer = lib.timer_laps.LapWatch()
        my_request = lib.ce_request.CloudElementsElement(
            base_url=BASE_URL,
            auth_header=AUTH_HEADER)
        history = my_request.get_all_objects(object_path="contacts/6f543020-a93a-44fd-91f7-08f49d64deb1/history", params={'pageSize': 50}, timer=my_timer)
        print my_timer.laps
        print len(history)

        # how_many = 7
        # for j in range(0, how_many):
        #     num1 = list(history.next().json())
        #     num1_ids = [x['id'] for x in num1]
        #     for i in num1_ids:
        #         print i

    except:
        raise
        my_request.print_my_last()
        

    # for i in range(0, 1002 - len(history.json())):
    #     my_body = dict(POST_BODY)
    #     my_body['details'] = my_body['details'].format(order_number=str(offset + i))
    #     my_time_now = datetime.datetime.now()
    #     my_time_future = datetime.datetime.now() + datetime.timedelta(minutes=15)
    #     my_body['startTime'] = my_time_now.isoformat()[:-3] + "Z"
    #     my_body['endTime'] = my_time_future.isoformat()[:-3] + "Z"
    #     response = my_request.send_request(method='post', url_path="history", json=my_body)
    #     if response.status_code != 200:
    #         my_request.print_my_last()
    #     else:
    #         print "History was created with order number of {0}.".format(str(offset + i))

    # new_history = my_request.send_request(method='get', url_path="contacts/6f543020-a93a-44fd-91f7-08f49d64deb1/history")
    # print json.dumps(new_history.headers, indent=2)


