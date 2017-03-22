function urlParse(myUrl) {
    myUrl = myUrl.toLowerCase();
    var schemeParse = myUrl.split("//");
    var myScheme;
    if (schemeParse[0].includes("http")) {
        myScheme = schemeParse[0];
    } else {
        myScheme = "";
    }
    var hostAndPath = schemeParse[schemeParse.length - 1].split("/");
    var myHost = hostAndPath[0];
    hostAndPath.splice(0, 1);
    var pathArr = [];
    for (var i = 0; i < hostAndPath.length; i++) {
        if (Boolean(hostAndPath[i])) {
            pathArr.push(hostAndPath[i]);
        }
    }
    var myPath = pathArr.join("/");
    return {
        scheme: myScheme,
        host: myHost,
        path: myPath,
        splitpath: myPath.split("/")
    };
}

function formatUrl(parsedUrl) {
    parsedUrl.scheme = "https:";
    if (parsedUrl.host.includes(".g2c.")) {
        parsedUrl.splitpath = ["act.web.api"];
    } else if (parsedUrl.host.endsWith(".act.com")) {
        if (parsedUrl.splitpath[0].endsWith("-api")) {
            parsedUrl.splitpath = [parsedUrl.splitpath[0], "act.web.api"];
        } else {
            parsedUrl.splitpath = [parsedUrl.splitpath[0] + "-api", "act.web.api"];
        }
    } else {
        parsedUrl.splitpath = ["act.web.api"];
    }
    parsedUrl.path = parsedUrl.splitpath.join("/");
    return parsedUrl;
}

function buildUrl(parsedUrl) {
    return [parsedUrl.scheme, "", parsedUrl.host, parsedUrl.path].join("/");
}

var testUrls = [
    {
        test: "https://2099.g2c.cloud-elements.com/act.web.api",
        result: "https://2099.g2c.cloud-elements.com/act.web.api"
    },{
        test: "https://2099.g2c.cloud-elements.com",
        result: "https://2099.g2c.cloud-elements.com/act.web.api"
    },{
        test: "2099.g2c.cloud-elements.com",
        result: "https://2099.g2c.cloud-elements.com/act.web.api"
    },{
        test: "2099.g2c.cloud-elements.com/act.web.api",
        result: "https://2099.g2c.cloud-elements.com/act.web.api"
    },{
        test: "2099.g2c.cloud-elements.com/default.apex", 
        result: "https://2099.g2c.cloud-elements.com/act.web.api"
    },{
        test: "http://usp1-iis-02.hosted1.act.com/BobsOldRed-api",
        result : "https://usp1-iis-02.hosted1.act.com/bobsoldred-api/act.web.api"
    },{
        test: "https://usp1-iis-02.hosted1.act.com/BobsOldRed-api/Act.Web.API",
        result : "https://usp1-iis-02.hosted1.act.com/bobsoldred-api/act.web.api"
    },{
        test: "https://usp1-iis-02g2c.act.com/BobsOldRed/Act.Web.API",
        result : "https://usp1-iis-02g2c.act.com/bobsoldred-api/act.web.api"
    },{
        test: "usp1-iis-02.hosted1.act.com/BobsOldRed-api",
        result : "https://usp1-iis-02.hosted1.act.com/bobsoldred-api/act.web.api"
    },{
        test: "blahblah.act.com/Bobs-api",
        result : "https://blahblah.act.com/bobs-api/act.web.api"
    },{
        test: "usp1-iis-02.hosted1.act.com/BobsOldRed-api/Act.Web.API",
        result : "https://usp1-iis-02.hosted1.act.com/bobsoldred-api/act.web.api"
    },{
        test: "usp1-iis-02.hosted1.act.com/BobsOldRed",
        result : "https://usp1-iis-02.hosted1.act.com/bobsoldred-api/act.web.api"
    },{
        test: "https://usp1-iis-02.hosted1.act.com/BobsOldRed",
        result : "https://usp1-iis-02.hosted1.act.com/bobsoldred-api/act.web.api"
    },{
        test: "https://usp1-iis-02.hosted1.act.com/BobsOldRed/default.apex",
        result : "https://usp1-iis-02.hosted1.act.com/bobsoldred-api/act.web.api"
    },{
        test: "https://actforwebdev.actops.com/apfw/default.apex",
        result: "https://actforwebdev.actops.com/act.web.api"
    },{
        test: "http://actforwebdev.actops.com/apfw/",
        result: "https://actforwebdev.actops.com/act.web.api"
    },{
        test: "http://actforwebdev.actops.com/apfw/default.apex",
        result: "https://actforwebdev.actops.com/act.web.api"
    },{
        test: "react.com/",
        result: "https://react.com/act.web.api"
    },{
        test: "actforwebdev.actops.com/apfw",
        result: "https://actforwebdev.actops.com/act.web.api"
    }
]

for(var i = 0; i<testUrls.length; i++ ){
    var baseUrl = buildUrl(formatUrl(urlParse(testUrls[i].test)));
    testUrls[i].result = baseUrl;
    console.log("Output1: ", baseUrl);
    var base2 = buildUrl(formatUrl(urlParse(baseUrl)))
    console.log("Output2: ", base2);
    var base3 = buildUrl(formatUrl(urlParse(base2)))
    console.log("Output3: ", base3,"\n");  
};

/*
https://14480.g2c.cloud-elements.com/act.web.api
celements
C3l3m3nts!
testSwiftpagePremium
*/

// var config = configuration;
// var baseUrl = buildUrl(formatUrl(urlParse(configuration['act'])));
// var endPoint = request_vendor_path;

// print("OLD Configs: " + JSON.stringify(config));

// var vendorUrl = baseUrl + endPoint;

// config['act'] = baseUrl;
// config['base.url'] = baseUrl;

// print("Vendor URL: " + vendorUrl);

// print("NEW Configs: " + JSON.stringify(config));

// var username = configuration['username'];
// var password = configuration['password'];

// var auth = username + ":" + password;

// var Base64={_keyStr:"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",encode:function(e){var t="";var n,r,i,s,o,u,a;var f=0;e=Base64._utf8_encode(e);while(f<e.length){n=e.charCodeAt(f++);r=e.charCodeAt(f++);i=e.charCodeAt(f++);s=n>>2;o=(n&3)<<4|r>>4;u=(r&15)<<2|i>>6;a=i&63;if(isNaN(r)){u=a=64}else if(isNaN(i)){a=64}t=t+this._keyStr.charAt(s)+this._keyStr.charAt(o)+this._keyStr.charAt(u)+this._keyStr.charAt(a)}return t},decode:function(e){var t="";var n,r,i;var s,o,u,a;var f=0;e=e.replace(/[^A-Za-z0-9+/=]/g,"");while(f<e.length){s=this._keyStr.indexOf(e.charAt(f++));o=this._keyStr.indexOf(e.charAt(f++));u=this._keyStr.indexOf(e.charAt(f++));a=this._keyStr.indexOf(e.charAt(f++));n=s<<2|o>>4;r=(o&15)<<4|u>>2;i=(u&3)<<6|a;t=t+String.fromCharCode(n);if(u!=64){t=t+String.fromCharCode(r)}if(a!=64){t=t+String.fromCharCode(i)}}t=Base64._utf8_decode(t);return t},_utf8_encode:function(e){e=e.replace(/rn/g,"n");var t="";for(var n=0;n<e.length;n++){var r=e.charCodeAt(n);if(r<128){t+=String.fromCharCode(r)}else if(r>127&&r<2048){t+=String.fromCharCode(r>>6|192);t+=String.fromCharCode(r&63|128)}else{t+=String.fromCharCode(r>>12|224);t+=String.fromCharCode(r>>6&63|128);t+=String.fromCharCode(r&63|128)}}return t},_utf8_decode:function(e){var t="";var n=0;var r=c1=c2=0;while(n<e.length){r=e.charCodeAt(n);if(r<128){t+=String.fromCharCode(r);n++}else if(r>191&&r<224){c2=e.charCodeAt(n+1);t+=String.fromCharCode((r&31)<<6|c2&63);n+=2}else{c2=e.charCodeAt(n+1);c3=e.charCodeAt(n+2);t+=String.fromCharCode((r&15)<<12|(c2&63)<<6|c3&63);n+=3}}return t}};

// //base 64 encode
// auth = "Basic " + Base64.encode(auth);

// var headers = request_vendor_headers;
// headers.Authorization = auth;

// done({
//     continue: true,
//     "request_vendor_headers": headers,
//     "request_vendor_path": vendorUrl,
//     "configuration": config
// });