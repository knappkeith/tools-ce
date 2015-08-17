from my_url import My_URL





class RequestProperty(object):
    def __init__(self, value=None):
        self.val = value

    def __set__(self, obj, value):
        self.val = value

    def __get__(self, obj, owner):
        return self.val

class My_Request(object):
    
    BASE_URL = RequestProperty()
    URL_VARS = RequestProperty()
    PARAMS = RequestProperty()
    HEADER = RequestProperty()
    DATA = RequestProperty()
    SCHEMA = RequestProperty()