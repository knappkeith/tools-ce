var crmSalesOrder = {
    "attributes": {
      "totaltax_base": 0,
      "owninguser": "c1d24b62-723a-de11-bd9e-00237d653ed0",
      "shipto_postalcode": "64801",
      "totalamount_base": 595,
      "totaldiscountamount_base": 0,
      "shipto_composite": "3835 W. 7th Street\r\nJoplin, MO 64801\r\nUnited States",
      "statuscode": 100003,
      "pricelevelid": "6f55924d-4d51-de11-b48a-00237d653ed0",
      "totalamountlessfreight": 595,
      "nje_shippingmethodid": "33e8fdf1-1e51-de11-b48a-00237d653ed0",
      "createdby": "c1d24b62-723a-de11-bd9e-00237d653ed0",
      "totalamountlessfreight_base": 595,
      "nje_weborder": false,
      "timezoneruleversionnumber": 0,
      "ownerid": "c1d24b62-723a-de11-bd9e-00237d653ed0",
      "totaltax": 0,
      "modifiedon": 1490209858000,
      "totalamount": 595,
      "billto_country": "United States",
      "willcall": false,
      "shipto_stateorprovince": "MO",
      "name": "012373",
      "customerid": "192344df-8bb4-e511-8106-d89d672cdd98",
      "modifiedby": "f67c6380-dc0a-e511-80fc-d89d672cdd98",
      "billto_stateorprovince": "MO",
      "nxt_fundedby": "192344df-8bb4-e511-8106-d89d672cdd98",
      "owningbusinessunit": "c10cd654-722f-de11-8f78-00237d653ed0",
      "shipto_city": "Joplin",
      "totallineitemamount": 595,
      "shipto_name": "PRIMARY",
      "datefulfilled": 1490209835000,
      "billto_line1": "3835 W. 7th Street",
      "totallineitemamount_base": 595,
      "exchangerate": 1,
      "prioritycode": 1,
      "statecode": 4,
      "nxt_fundingby": "192344df-8bb4-e511-8106-d89d672cdd98",
      "totaldiscountamount": 0,
      "shipto_line1": "3835 W. 7th Street",
      "ordernumber": "ORD-44599-N8M5",
      "shipto_freighttermscode": 1,
      "totallineitemdiscountamount_base": 0,
      "billto_name": "PRIMARY",
      "nje_paymenttermsid": "2de8fdf1-1e51-de11-b48a-00237d653ed0",
      "billto_composite": "3835 W. 7th Street\r\nJoplin, MO 64801\r\nUnited States",
      "billto_addressid": "422274e8-cade-419b-b8bb-c994c4fbf16f",
      "billto_city": "Joplin",
      "createdon": 1490205783000,
      "pricingerrorcode": 0,
      "nxt_migrationstate": 10,
      "shipto_country": "United States",
      "transactioncurrencyid": "c9d286d4-ae18-de11-8153-00237d653ed0",
      "nje_commissionablesalesrepid": "79cc1b47-4551-de11-b48a-00237d653ed0",
      "ispricelocked": false,
      "shipto_addressid": "422274e8-cade-419b-b8bb-c994c4fbf16f",
      "salesorderid": "ae6b26ca-290f-e711-810a-000c292dded1",
      "billto_postalcode": "64801",
      "totallineitemdiscountamount": 0
    },
    "id": "ae6b26ca-290f-e711-810a-000c292dded1"
  }



var crmProduct = {
    "attributes": {
      "productstructure": 1,
      "productid": "37c89468-3555-de11-b50d-00237d653ed0",
      "exchangerate": 1,
      "price_base": 119,
      "description": "T4V-S/I Sale w/2 Years Airtime",
      "producttypecode": 1,
      "statecode": 0,
      "statuscode": 1,
      "iskit": true,
      "pricelevelid": "6f55924d-4d51-de11-b48a-00237d653ed0",
      "nje_showonwebsite": false,
      "isstockitem": false,
      "createdby": "01ebd065-8174-4c8e-a600-d35f8ca7b83f",
      "price": 119,
      "standardcost_base": 0,
      "defaultuomscheduleid": "7055924d-4d51-de11-b48a-00237d653ed0",
      "nxt_isaunit": true,
      "currentcost": 92,
      "stockweight": 0,
      "standardcost": 0,
      "quantitydecimal": 0,
      "createdon": 1244579875000,
      "transactioncurrencyid": "c9d286d4-ae18-de11-8153-00237d653ed0",
      "organizationid": "0765e8db-d51b-43ec-bed3-4a991d84b6f0",
      "modifiedon": 1468872375000,
      "productnumber": "T-4V S/I SALE W/ 2 YEARS AIR.",
      "name": "T-4V S/I SALE W/ 2 YEARS AIR.",
      "currentcost_base": 92,
      "modifiedby": "15224057-43d2-e311-b5f3-6805ca18c2b1",
      "nxt_productclassid": "13767cf4-ce08-e611-810d-d89d672cdd98",
      "defaultuomid": "7155924d-4d51-de11-b48a-00237d653ed0"
    },
    "id": "37c89468-3555-de11-b50d-00237d653ed0"
  }




/*
nje_productnumber         QB Invoice -> ItemGroupRef -> FullName
productid                 CRM Product -> id
quantity                  QB Invoice -> Quantity
salesorderid              CRM Sales Order -> id
salesrepid                CRM Sales Order -> id
shipto_addressid          CRM Sales Order -> shipto_addressid
shipto_city               CRM Sales Order -> shipto_city
shipto_country            CRM Sales Order -> shipto_country
shipto_freighttermscode   CRM Sales Order -> shipto_freighttermscode
shipto_line1              CRM Sales Order -> shipto_line1
shipto_name               CRM Sales Order -> shipto_name
shipto_postalcode         CRM Sales Order -> shipto_postalcode
shipto_stateorprovince    CRM Sales Order -> shipto_stateorprovince
shipto_telephone          CRM Sales Order -> shipto_telephone
uomid                     CRM Product -> defaultuomid
*/


var updates;

updates = [];



var crmLineDetail = {};

crmLineDetail.nje_productnumber         = crmProduct.attributes.productnumber;

//crmLineDetail.productid                 = {'id': crmProduct.id, 'lookup': 'product'};

crmLineDetail.productid                 = crmProduct.id;
crmLineDetail.quantity                  = 5;
crmLineDetail.salesorderid              = {'id': crmSalesOrder.id, 'lookup': 'salesorder'};
// crmLineDetail.salesrepid                = crmSalesOrder.attributes.salesrepid;
crmLineDetail.shipto_addressid          = crmSalesOrder.attributes.shipto_addressid;
crmLineDetail.shipto_city               = crmSalesOrder.attributes.shipto_city;
crmLineDetail.shipto_country            = crmSalesOrder.attributes.shipto_country;
crmLineDetail.shipto_freighttermscode   = crmSalesOrder.attributes.shipto_freighttermscode;
crmLineDetail.shipto_line1              = crmSalesOrder.attributes.shipto_line1;
crmLineDetail.shipto_name               = crmSalesOrder.attributes.shipto_name;
crmLineDetail.shipto_postalcode         = crmSalesOrder.attributes.shipto_postalcode;
crmLineDetail.shipto_stateorprovince    = crmSalesOrder.attributes.shipto_stateorprovince;
crmLineDetail.shipto_telephone          = crmSalesOrder.attributes.shipto_telephone;
crmLineDetail.uomid                     = {'id': crmProduct.attributes.defaultuomid, 'lookup': 'uom'};

var lineObject = { attributes: crmLineDetail};

updates.push(lineObject);

console.log({'updates': updates});
console.log(updates)