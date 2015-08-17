import requests
import os
from data.environment_data import build_variables
from data.endpoints import build_variables as build_endpoints
from lib.my_url import My_URL
from lib.my_request import My_Request


class Ce_Session(object):
    def __init__(self, environment=None, auto_auth=True):
        if environment is None:
            try:
                environment = os.environ['KEITH_ENV']
            except KeyError:
                print "Cannot find Environment, using DEFAULT!"
                environment = 'DEFAULT'

        self.ENV_VAR = self._get_variables(environment)
        self.END_POINTS = self._get_endpoints(environment)
        self.header = self._build_initial_header()
        self.is_auth = False
        self.session = requests.Session()
        self.base_url = self.ENV_VAR['IM_URL']
        self.my_url = My_URL(self.base_url)
        self.history = []
        if auto_auth:
            self.authenticate()

    def _get_variables(self, environment):
        return build_variables(environment)

    def _get_endpoints(self, environment):
        return build_endpoints(environment)

    def _build_initial_header(self):
        header = {
            'Accept': 'application/json'
        }
        return header

    def _build_params(self):
        params = {
            'userId': self.ENV_VAR['USER_NAME'],
            'password': self.ENV_VAR['PASSWORD']
        }
        return params

    def _build_url(self, endpoint):
        return self.my_url.build_url(endpoint)

    def get_url(self, endpoint, url_vars):
        if url_vars is None:
            return self._build_url(self.END_POINTS[endpoint])
        else:
            return self._build_url(self.END_POINTS[endpoint]).format(url_vars)

    def get_header(self):
        return self._build_header()

    def get_params(self):
        return self._build_params()

    def authenticate(self):
        params = self.get_params()
        auth_attempt = self.hit_endpoint('get', 'authenticate', params=params)
        try:
            assert auth_attempt.status_code == 200
            self.session_id = auth_attempt.headers['inspirato-im-session-id']
            self.header['Inspirato-IM-Session-ID'] = self.session_id
            self.is_auth = True
        except AssertionError:
            print 'An Error Occured, status code is %d and the response was: %s' % (auth_attempt.status_code, auth_attempt.json())
        self.history.append(auth_attempt)
        return auth_attempt

    def get_endpoint_info_v2(self, endpoint):
        this_request = My_Request()
        My_Request.URL = self.get_url()
    
    def hit_endpoint_v2(self, endpoint_v2):
        endpoint_info_v2 = self.get_endpoint_info_v2(endpoint_v2)

    def hit_endpoint(self, method, endpoint, params=None, header=None, data=None, url_vars=None):
        if header is None:
            header = self.header
        http_response = self.session.request(method, self.get_url(endpoint, url_vars), params=params, headers=header, data=data)
        self.history.append(http_response)
        return http_response

    def verify_endpoint_response_code(self, method, endpoint, status, params=None, header=None, data=None, url_vars=None):
        returned_status = self.hit_endpoint(method, endpoint, params, header, data, url_vars).status_code
        if returned_status != status:
            print "The expected status of %d was not returned, instead a status code of %d was returned! History Index of %d." % (status, returned_status, len(self.history))

    def convert_to_curl(self, request_object):
        command = "curl -X {method} -H {headers} -d {data} {uri}"
        method = request_object.method
        uri = request_object.url
        data = request_object.body
        headers = ["{0}: {1}".format(k, v) for k, v in request_object.headers.items()]
        headers = " -H ".join(headers)
        return command.format(method=method, headers=headers, data=data, uri=uri)
