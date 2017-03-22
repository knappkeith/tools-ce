import json


def generate_printout(request_obj, ignore=[]):

    def _build_headers(headers):
        heads = ["  Headers:"]
        for header, value in headers.iteritems():
            heads.append("    {0}:  {1}".format(header, value))
        return heads

    def _build_data(data):
        rtn_data = ["  JSON:"]
        try:
            rtn_data.append(json.dumps(json.loads(data), indent=4))
        except:
            rtn_data = ["  DATA:"]
            rtn_data.append("    {0}".format(data))
        return rtn_data

    def _generate_response_printout(my_request, ignore=[]):
        if request_obj is None:
            return "No Response"
        request = my_request
        output = ["RESPONSE:"]
        if "status" not in ignore:

            # this is here because sometimes the requests library
            #    returns a blank string for the reason, and it's
            #    driving me crazy!!!!
            reason_str = request.reason
            if reason_str == "":
                import httplib
                reason_str = httplib.responses[int(request.status_code)]
            output.append("  Status:  {code} - {reason}".format(
                code=request.status_code, reason=reason_str))
        if "headers" not in ignore:
            output = output + _build_headers(request.headers)
        if "body" not in ignore:
            output = output + _build_data(request.text)
        return "\n".join(output)

    def _generate_request_printout(my_request, ignore=[]):
        if request_obj is None:
            return "No Request"
        request = my_request.request
        output = ["REQUEST:"]
        output.append("  Method:  {0}".format(request.method))
        output.append("  URL:  {0}".format(request.url))
        if len(my_request.history) > 0:
            response_codes = [x.status_code for x in my_request.history]
            output.append("  Redirected: {0} times, ({1})".format(
                len(my_request.history), response_codes))
        else:
            output.append("  Redirected: False")
        if "headers" not in ignore:
            output = output + _build_headers(request.headers)
        if "body" not in ignore:
            output = output + _build_data(request.body)
        return "\n".join(output)

    return "\n\n".join([
        _generate_request_printout(my_request=request_obj, ignore=ignore),
        _generate_response_printout(my_request=request_obj, ignore=ignore)])


def parse_url(url_string):
    '''
    parses a string and returns per:
    scheme:[//[user:password@]host[:port]][/]path[?query][#fragment]

    Should write this as a class that has properties for each with a state
    of parsed or not so you can
    '''

    pass
