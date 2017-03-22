
node_info = [
    (
        "Aurora DB",
        "auroraNode",
        [" ", " ", " ", " ", "x", " "],
        ["Skip Martin working on it"],
        []
    ),(
        "Concur",
        "concurNode",
        ["x", " ", " ", " ", "x", "x"],
        [
            "`500 - {'message': 'Internal server error'}`, Martin says it's good hasn't deployed yet",
            "New Lambda at 15:30 11-2",
            "Still getting a 500 but with `{ message: 'Request failed', providerMessage: '{}' }`"
        ],
        [(" ", "When using a bad token the Error message isn't clear and the status is 500.")]
    ),(
        "Dynamics CRM",
        "dynamicsNode",
        ["x", " ", " ", " ", "x", " "],
        ["Issue with timeout, Aaron looking into it"],
        []
    ),(
        "Eloqua",
        "eloquaNode",
        [" ", " ", " ", " ", "x", " "],
        ["There is an issue with the authentication that is not allowing Dango to run."],
        []
    ),(
        "HubSpot",
        "hubspotNode",
        [" ", " ", " ", " ", "x", " "],
        ["Skip Martin looking at it"],
        []
    ),(
        "Marketo V2",
        "marketoNode",
        ["x", " ", " ", " ", "x", "x"],
        [
            "~~BROKEN, everything is returning 200 with blank response, Aaron working on it~~",
            "Uploaded new Lambda, 16:00 11-2",
            "Looking Good, basic communication working"
        ],
        [(" ", "For `GET /activities` when supplying a `continuationToken` from `GET /paging-token` Marketo is still failing because it's looking for nextPageToken which is the `continuationToken`. No place to put `nextPage={paging-token}`")]
    ),(
        "Netsuite",
        "netsuitefinanceNode",
        [" ", " ", " ", " ", "x", " "],
        ["There is an issue with timeout on Netsuite that Ramana is looking into."],
        []
    ),(
        "Netsuite CRM",
        "netsuitecrmNode",
        ["x", " ", " ", " ", "x", " "],
        ["Getting a 500 without any provider message, Dango test works for the same enpoint"],
        []
    ),(
        "Postgres",
        "postgresNode",
        [" ", " ", " ", " ", "x", " "],
        ["Skip Martin working on it"],
        []
    ),(
        "Quickbooks",
        "quickbooksNode",
        ["x", "x", " ", " ", "x", " "],
        ["New Lambda, 17:00 11-2", "Looking Good"],
        []
    ),(
        "SalesForce",
        "salesforceNode",
        ["x", "x", " ", " ", "x", " "],
        ["Looking Good"],
        []
    ),(
        "SalesForce Service Cloud",
        "salesforce_service_cloudNode",
        ["x", "x", " ", " ", "x", " "],
        ["Looking Good"],
        []
    ),(
        "Zendesk",
        "zendeskNode",
        ["x", "x", " ", " ", "x", " "],
        ["Looking Good"],
        []
    ),(
        "Zoho CRM",
        "zohoNode",
        ["x", "x", " ", " ", "x", "x"],
        ["New Lambda at 15:00 11-2", "Looking Good"],
        [(" ", "When using a bad token the Error message isn't clear and the status is 400. the message is `{'message':'Unable to process your request. Please verify whether you have entered proper method name,parameter and parameter values.','code':'4600'}`")]
    )
]

print_str = '## {name} - ({node_name})\n- [{x[0]}] Authentication Worked\n- [{x[1]}] Tested for basic functionality\n- [{x[2]}] Dango tests work, Node\n- [{x[3]}] Edge Case testing, Node\n- [{x[4]}] **Notes**:\n{notes}\n- [{x[5]}] Issues:\n{issues}\n'


def write_it():
    print "\n".join([print_str.format(name=i[0],node_name=i[1], x=i[2], notes="\n".join(["  - {0}".format(x) for x in i[3]]), issues="\n".join(["  - [{0}] {1}".format(x[0], x[1]) for x in i[4]])) for i in node_info])


