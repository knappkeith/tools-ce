const fs = require('fs');
const uuid = require('node-uuid');
const rp = require('request-promise');
//crushing it
for (i = 0; i < 5; i++) {
    console.log(`sending request ${i}`);

    postPromise = rp.post({
          url: 'https://console.cloud-elements.com/elements/api-v2/hubs/documents/files?path=' +
          `/Personal Folders/nodejs-sharefileuploadloop2/${uuid.v4()}/package.json`,
          headers: {
              'Content-Type': 'multipart/form-data',
              'Transfer-Encoding': 'chunked',
              Accept: 'application/json',
              Authorization: 'User jcMEoZsFFwdcxQa8z3UoSF/vEPlY6xEWVRTLXMJHXwo=, Organization 0a5981dc083e4018f61d6a480123bd6b, Element 15+uICZqeS77CSVfEalJq5z8sm7tvPCzYSb/s1zwemU=',
          },
          formData: {
              file: fs.createReadStream('package.json')
          }
      }
    );

    postPromise
    .then(response => {
        console.log(`received response:\n ${JSON.stringify(response)}`);
    })
    // .catch(err => console.log(err));
 }
