var qbProduct = "T-4V SALE/ 2 YEAR AIRTIME.";
var productResponse = [
  {
    "attributes": {
      "productstructure": 1,
      "productid": "8fc060ec-2e2b-e111-ba16-00237d653ed0",
      "exchangerate": 1,
      "price_base": 109,
      "description": "T-4V SALE/ 2 YEAR AIRTIME",
      "producttypecode": 1,
      "statecode": 1,
      "statuscode": 2,
      "iskit": true,
      "pricelevelid": "6f55924d-4d51-de11-b48a-00237d653ed0",
      "nje_showonwebsite": true,
      "isstockitem": false,
      "createdby": "01ebd065-8174-4c8e-a600-d35f8ca7b83f",
      "price": 109,
      "standardcost_base": 0,
      "defaultuomscheduleid": "7055924d-4d51-de11-b48a-00237d653ed0",
      "nxt_isaunit": true,
      "currentcost": 50.82,
      "stockweight": 0,
      "standardcost": 0,
      "nje_classid": "DEVICES",
      "quantitydecimal": 0,
      "createdon": 1324401642000,
      "transactioncurrencyid": "c9d286d4-ae18-de11-8153-00237d653ed0",
      "organizationid": "0765e8db-d51b-43ec-bed3-4a991d84b6f0",
      "modifiedon": 1470766923000,
      "productnumber": "T-4V SALE/ 2 YEAR AIRTIME",
      "name": "T-4V SALE/ 2 YEAR AIRTIME",
      "currentcost_base": 50.82,
      "modifiedby": "15224057-43d2-e311-b5f3-6805ca18c2b1",
      "defaultuomid": "7155924d-4d51-de11-b48a-00237d653ed0"
    },
    "id": "8fc060ec-2e2b-e111-ba16-00237d653ed0"
  },
  {
    "attributes": {
      "productstructure": 1,
      "productid": "b110295b-8133-e411-80ea-d89d672cdd98",
      "exchangerate": 1,
      "price_base": 109,
      "description": "T4V-Sale w/2 Years Airtime",
      "producttypecode": 1,
      "statecode": 0,
      "statuscode": 1,
      "iskit": true,
      "pricelevelid": "6f55924d-4d51-de11-b48a-00237d653ed0",
      "nje_showonwebsite": false,
      "isstockitem": false,
      "createdby": "fa199ce8-2925-de11-a10b-00237d653ed0",
      "price": 109,
      "standardcost_base": 0,
      "defaultuomscheduleid": "7055924d-4d51-de11-b48a-00237d653ed0",
      "nxt_isaunit": true,
      "currentcost": 25,
      "stockweight": 0,
      "standardcost": 0,
      "quantitydecimal": 0,
      "createdon": 1409759141000,
      "transactioncurrencyid": "c9d286d4-ae18-de11-8153-00237d653ed0",
      "organizationid": "0765e8db-d51b-43ec-bed3-4a991d84b6f0",
      "modifiedon": 1470866722000,
      "productnumber": "T-4V SALE/ 2 YEAR AIRTIME.",
      "name": "T-4V SALE/ 2 YEAR AIRTIME.",
      "currentcost_base": 25,
      "modifiedby": "15224057-43d2-e311-b5f3-6805ca18c2b1",
      "nxt_productclassid": "13767cf4-ce08-e611-810d-d89d672cdd98",
      "defaultuomid": "7155924d-4d51-de11-b48a-00237d653ed0"
    },
    "id": "b110295b-8133-e411-80ea-d89d672cdd98"
  }
]
var error;


if (productResponse.length === 0) {
  error = 'Unable to find QB Item in Dynamics CRM. Item Name: ' + qbProduct;
  
  console.log({
    continue: false,
    'error': error
  });
} else if (productResponse.length > 1) {
  error = 'Found multiple items for QB Item in Dynamics CRM. Item Name: ' + qbProduct;
  
  console.log({
    continue: false,
    'error': error
  });
} else {
  var crmProduct = productResponse[0];
  
  if (crmProduct.attributes.productnumber == qbProduct) {
    console.log(true);
  } else {
    error = "QB <-> CRM name missmatch. Possible '.' typo. QB Name: " + qbProduct + ' Dynamics Name: ' + crmProduct.attributes.productnumber;
    console.log({
      continue: true,
      'error': error
    });
  }
}