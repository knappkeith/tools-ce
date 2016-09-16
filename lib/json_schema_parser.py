import json
import json_tools


class JSON_Schema_Parser(object):
    def __init__(self, json_obj, auto_gen=True):
        if isinstance(json_obj, str):
            try:
                a = json.loads(json_obj)
            except ValueError:
                a = json_obj.replace("\n", "")
                a = a.replace("\r", "")
                a = json.loads(a)
            a = json.dumps(a)
        elif isinstance(json_obj, dict):
            a = json.dumps(json_obj)
        else:
            a = json_obj
        self.json_obj = a
        self._load_json()
        if auto_gen:
            self.build_schema()
            self.convert_dict()
            self.wrap_it()

    def _load_json(self):
        # if isinstance(self.json_obj, str):
        #     self.json_str = json.loads(self.json_obj)
        # else:
        #     self.json_str = self.json_obj
        self.json_str = json.loads(self.json_obj)

    def build_schema(self):
        self.main_out = json_tools.build_item(self.json_str)

    def convert_dict(self):
        self.main_str = json.dumps(self.main_out)

    def wrap_it(self):
        self.final_shema = "var schema = %s;" % self.main_str

    def print_it(self, what_2_print=None):
        if what_2_print is None:
            what_2_print = self.main_out
        self.pretty_json = json_tools.pretty_print_it(what_2_print)
        print self.pretty_json
