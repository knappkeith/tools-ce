import requests
import common


class CloudElementsRequests(requests.Session):
    def __init__(self):
        super(CloudElementsRequests, self).__init__()
        self.headers['Accept'] = 'application/json'
        self.history = []
        self.history_limit = 100

        # `mount` a custom adapter that retries failed connections for HTTP
        # and HTTPS requests.
        self.mount("http://", requests.adapters.HTTPAdapter(max_retries=1))
        self.mount("https://", requests.adapters.HTTPAdapter(max_retries=1))

    def send_request(self, method, url_path, *args, **kwargs):
        if "http" in url_path:
            url = url_path
        else:
            url = self._build_url(url_path)
        response = self.request(method.upper(), url, **kwargs)
        self.history.append(response)
        while len(self.history) > self.history_limit:
            self.history.pop(0)
        return response

    def send_request_iter(
            self,
            method,
            url_path,
            offset_token=None,
            timer=None,
            *args, **kwargs):
        if 'params' in kwargs:
            params = dict(kwargs['params'])
            del kwargs['params']
            if not offset_token:
                params['nextPage'] = offset_token
        else:
            params = {'nextPage': offset_token}
        my_call = self.send_request(
            method=method,
            url_path=url_path,
            params=params, **kwargs)
        need_to_break = False
        if timer:
            timer.lap()
        while True:
            if "Elements-Next-Page-Token" not in my_call.headers:
                need_to_break = True
            elif my_call.headers.get('Elements-Returned-Count', '0') == '0':
                need_to_break = True
            else:
                params['nextPage'] = my_call.headers['Elements-Next-Page-Token']
            yield my_call
            if need_to_break:
                break
            my_call = self.send_request(
                method=method,
                url_path=url_path,
                params=params, **kwargs)
            if timer:
                timer.lap()

    def get_all_objects(self, object_path, **kwargs):
        all_objects = []
        my_iter = self.send_request_iter(method='get', url_path=object_path, **kwargs)
        for itereration in my_iter:
            all_objects.extend(itereration.json())
        return all_objects

    def _build_url(self, addition_to_path):
        a = self.base_url.split("/")
        while a[-1] == "":
            a = a[0:-1]
        a.append(addition_to_path)
        return "/".join(a)

    @property
    def last_call(self, attribute=None):
        if not attribute:
            if len(self.history) > 0:
                return self.history[-1]
            else:
                return None
        else:
            return getattr(self.history[-1], attribute)

    def print_my_last(self):
        print self.generate_last_printout()

    def generate_last_printout(self):
        return self.generate_printout(self.last_call)

    def generate_printout(self, request_obj):
        return common.generate_printout(request_obj)


class CloudElementsPlatform(CloudElementsRequests):
    def __init__(self, base_url, auth_header=None):
        super(CloudElementsPlatform, self).__init__()
        if auth_header:
            self.headers['Authorization'] = self._parse_auth_token(auth_header)
        self.base_url = base_url
        self.my_cache = {}

    def _parse_auth_token(self, auth_header):
        if isinstance(auth_header, (str, unicode)):
            auth_dict = {}
            for token in [x.strip() for x in auth_header.split(",")]:
                tmp = token.split(" ")
                auth_dict[tmp[0].lower()] = tmp[1]
            return self._parse_auth_token(auth_dict)
        elif isinstance(auth_header, dict):
            return "User {user}, Organization {org}".format(
                user=auth_header['user'], org=auth_header['organization'])

    def get_formulas(self):
        if "formulas" in self.my_cache:
            return self.my_cache['formulas']
        else:
            my_request = self.send_request(
                method='get',
                url_path="/elements/api-v2/formulas")
            if my_request.status_code != 200:
                raise Exception(
                    "There was an error getting Formulas: {request}".format(
                        request=self.generate_last_printout()))
            else:
                self.my_cache['formulas'] = my_request.json()
                return my_request.json()

    def get_formula_by_name(self, formula_name):
        formulas = self.get_formulas()
        formulas = [x for x in formulas if x['name'] == formula_name]
        if len(formulas) == 0:
            print "Could Not find formula: '{name}'".format(name=formula_name)
            return None
        elif len(formulas) > 1:
            print "Found more than one formula(weird???!?!): '{name}'".format(
                name=formula_name)
            return formulas[0]
        else:
            return formulas[0]

    def get_formula_execution_step_values(self, formula_id, formula_execution_id):
        '''
        Returns a composite json of all the execution data for an execution
        including all the step details
        '''
        self.get_all_objects()

class CloudElementsElement(CloudElementsRequests):
    def __init__(self, base_url, auth_header=None):
        super(CloudElementsElement, self).__init__()
        if auth_header:
            self.headers['Authorization'] = self._parse_auth_token(auth_header)
        self.base_url = base_url
        self.my_cache = {}

    def _parse_auth_token(self, auth_header):
        if isinstance(auth_header, (str, unicode)):
            auth_dict = {}
            for token in [x.strip() for x in auth_header.split(",")]:
                tmp = token.split(" ")
                auth_dict[tmp[0].lower()] = tmp[1]
            return self._parse_auth_token(auth_dict)
        elif isinstance(auth_header, dict):
            return "User {user}, Organization {org}, Element {token}".format(
                user=auth_header['user'],
                org=auth_header['organization'],
                token=auth_header['element'])
