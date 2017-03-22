const fs = require('fs');
const uuid = require('node-uuid');
const rp = require('request-promise');


//Totally Crushing it with this node application -Cassie

console.log('creating sub-folder');

var hours = Date.now();

postPromise = rp.post({
      url: 'https://console.cloud-elements.com/elements/api-v2/hubs/documents/folders',
      headers: {
                      'Content-Type': 'application/json',
                      'Transfer-Encoding': 'chunked',
                      Accept: 'application/json',
                      Authorization: 'User jcMEoZsFFwdcxQa8z3UoSF/vEPlY6xEWVRTLXMJHXwo=, Organization 0a5981dc083e4018f61d6a480123bd6b, Element 15+uICZqeS77CSVfEalJq5z8sm7tvPCzYSb/s1zwemU=',
                  },
      body: {
          'path':`/Personal Folders/nintex_${hours}`,
          'directory':true

      },
      json: true
})

for(i=0; i < 6; i++)
{
  console.log(`sending request ${i}`);
  //nailed it
  postPromise = rp.post({
        url: 'https://console.cloud-elements.com/elements/api-v2/hubs/documents/folders',
        headers: {
                        'Content-Type': 'application/json',
                        'Transfer-Encoding': 'chunked',
                        Accept: 'application/json',
                        Authorization: 'User jcMEoZsFFwdcxQa8z3UoSF/vEPlY6xEWVRTLXMJHXwo=, Organization 0a5981dc083e4018f61d6a480123bd6b, Element 15+uICZqeS77CSVfEalJq5z8sm7tvPCzYSb/s1zwemU=',
                    },
        body: {
            'path':`/Personal Folders/nintex_${hours}/${i}`,
            'directory':true

        },
        json: true

})
}
