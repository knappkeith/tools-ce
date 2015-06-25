import json
import json_tools


class JSON_Schema_Parser(object):
    def __init__(self, json_obj, auto_gen=True):
        self.json_obj = json_obj
        self._load_json()
        if auto_gen:
            self.build_schema()
            self.convert_dict()
            self.wrap_it()

    def _load_json(self):
        self.json_str = json.loads(self.json_obj)

    def build_schema(self):
        self.main_out = json_tools.build_item(self.json_str)

    def convert_dict(self):
        self.main_str = json.dumps(self.main_out)

    def wrap_it(self):
        self.final_shema = "var schema = %s;" % self.main_str

    def print_it(self):
        self.pretty_json = json_tools.pretty_print_it(self.main_out)
        print self.pretty_json
