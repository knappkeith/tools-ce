const fs = require('fs');
const uuid = require('node-uuid');
const rp = require('request-promise');


var hours = Date.now();

for(i=0; i < 5; i++)
{
  console.log(`sending request ${i}`);
  myGet(i);

}

function myGet (k) {
    return rp.get({
        // Staging
        uri: "https://staging.cloud-elements.com/elements/api-v2/hubs/finance/SalesRep?where=Name%20like%20'A%25'",
        //Prod
        // uri: "https://console.cloud-elements.com/elements/api-v2/hubs/finance/SalesRep?where=Name%20like%20'A%25'",
        headers: {
            // Staging
            'Authorization': 'User pcdo/I8bNFr6YiqrRQgrknK9YqASIfDeiDeHu17Rdq4=, Organization 24b54d97feb914b689f7957eeb16f396, Element JT8D7M6m1oWWpAiT+ZOQVThw75GCR4n9nCqPFO4Y/ew=',
            // Prod
            // 'Authorization': 'User gS9xXNOSrebnb0BS956HWNUHMw+iaeHEx1PoMc/Ql9Q=, Organization 89341d5d002f3091e5cd5876d7ed8ff0, Element Fa8gVtxDUWp4NJ9VFHQwAaYassdiCFcqw271upqDpgY=',
            'Accept': 'application/json'
        },
        json: true, // Automatically parses the JSON string in the response 
        resolveWithFullResponse: true
    })
    .then(function (response) {
        console.log("Request " + k + " returned with status " + response.statusCode);
    })
}