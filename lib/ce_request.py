import requests
import common


class CloudElementsRequests(requests.Session):
    def __init__(self, base_url):
        super(CloudElementsRequests, self).__init__()
        self.base_url = base_url
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
        my_iter = self.send_request_iter(
            method='get', url_path=object_path, **kwargs)
        for itereration in my_iter:
            all_objects.extend(itereration.json())
        return all_objects

    def _build_url(self, addition_to_path):
        if "//" in self.base_url:
            scheme = self.base_url.split("//")[0]
            a = self.base_url.split("//")[1].split("/")
        else:
            scheme = "https:"
            a = self.base_url.split("/")
        b = []
        for i in a:
            if i != "":
                b.append(i)
        b.append(addition_to_path)
        return "{scheme}//{path}".format(scheme=scheme, path="/".join(b))

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
    def __init__(self, base_url, auth_header=None, use_cache=True):
        super(CloudElementsPlatform, self).__init__(base_url=base_url)
        if auth_header:
            self.headers['Authorization'] = self._parse_auth_token(auth_header)
        self.my_cache = {}
        self.use_cache = use_cache

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

    def _get_all_objects(self, object_path):
        if self.use_cache and self.my_cache.get(object_path, None):
            return self.my_cache[object_path]
        else:
            my_objects = self.get_all_objects(object_path=object_path)
            self.my_cache[object_path] = my_objects
            return my_objects

    def get_formulas(self):
        '''
        Return all formulas
        '''
        return self._get_all_objects(object_path=PlatformUrls.FORMULAS)

    def post_formulas(self, formula_json):
        '''
        Post a new formula, Returns response object
        '''
        response = self.send_request(
            method='post',
            url_path=PlatformUrls.FORMULAS,
            json=formula_json)
        if response.status_code == 200 and self.my_cache.get(PlatformUrls.FORMULAS):
            del self.my_cache[PlatformUrls.FORMULAS]
        return response


    def get_formula_by_name(self, formula_name):
        '''
        Return a formula that matches ``formula_name``
        '''
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

    def patch_formula(self, formula_id, formula_json):
        '''
        Update a formula
        '''
        response = self.send_request(
            method='patch',
            url_path=FORMULAS_ID.format(formula_id=formula_id),
            json=formula_json)
        if response.status_code == 200 and self.my_cache.get(PlatformUrls.FORMULAS):
            del self.my_cache[PlatformUrls.FORMULAS]
        return response

    def get_formula_instances(self, formula_id):
        '''
        Returns all the instance ids of a formula id
        '''
        return self._get_all_objects(
            object_path=PlatformUrls.FORMULA_INSTANCES.format(
                formula_id=formula_id))

    def get_formula_executions(self, instance_id):
        '''
        Returns all the executions for a formula instance
        '''
        return self._get_all_objects(
            object_path=PlatformUrls.FORMULA_EXECUTIONS.format(
                instance_id=instance_id))

    def get_formula_execution_steps(self, execution_id, filter_steps=[]):
        '''
        Returns all the execution steps for a formula execution
        '''
        my_steps = self._get_all_objects(
            object_path=PlatformUrls.FORMULA_EXECUTION_STEPS.format(
                execution_id=execution_id))
        if len(filter_steps) > 0:
            return [x for x in my_steps if x['stepName'] in filter_steps]
        else:
            return my_steps

    def get_formula_execution_step_values(self, step_execution_id):
        '''
        Returns all the execution step values for a formula execution step
        '''
        return self._get_all_objects(
            object_path=PlatformUrls.FORMULA_EXECUTION_STEP_VALUES.format(
                step_execution_id=step_execution_id))

    def get_formula_execution_steps_with_values(self, execution_id):
        '''
        Returns a concatenated JSON of all the steps with the values
        in the step info
        '''
        my_steps = self.get_formula_execution_steps(execution_id=execution_id)
        for step in my_steps:
            step['values'] = self.get_formula_execution_step_values(
                step_execution_id=step['id'])


class CloudElementsElement(CloudElementsRequests):
    def __init__(self, base_url, auth_header=None, use_cache=True):
        super(CloudElementsElement, self).__init__(base_url=base_url)
        if auth_header:
            self.headers['Authorization'] = self._parse_auth_token(auth_header)
        self.my_cache = {}
        self.use_cache = use_cache

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


class PlatformUrls(object):
    API_PATH = "/elements/api-v2"
    FORMULAS = "{api}/formulas".format(
        api=API_PATH)
    FORMULAS_ID = "{api}/formulas/{{formula_id}}".format(
        api=API_PATH)
    FORMULA_INSTANCES = "{api}/formulas/{{formula_id}}/instances".format(
        api=API_PATH)
    FORMULA_EXECUTIONS = "{api}/formulas/instances/{{instance_id}}/executions".format(
        api=API_PATH)
    FORMULA_EXECUTION_STEPS = "{api}/formulas/instances/executions/{{execution_id}}/steps".format(
        api=API_PATH)
    FORMULA_EXECUTION_STEP_VALUES = "{api}/formulas/instances/executions/steps/{{step_execution_id}}/values".format(
        api=API_PATH)
