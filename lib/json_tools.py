import json
import unicodedata

def build_item(item):
    if isinstance(item, tuple):
        return build_tuple(item)
    elif isinstance(item, dict):
        return build_tuple(("name_dict", item)).values()[0]
    elif isinstance(item, list):
        return build_tuple(("name_array", item[0])).values()[0]
    elif isinstance(item, unicode):
        return build_tuple(("name_str", item))
    else:
        raise NameError("Unknown type: %s - %s" % (type(item), item))


def build_tuple(item):
    json_name, json_type = get_name_type(item)
    rtn_item = {}
    if item[0] == "name_str":
        rtn_item["type"] = "string"
        return rtn_item
    rtn_item[json_name] = {}
    if json_type == "null":
        rtn_item[json_name]["anyOf"] = [{"type": "null"},{"type": "string"}]
    else:
        rtn_item[json_name]["type"] = json_type
    if json_type == "object":
        rtn_item[json_name][property_or_item(json_type, json_name)] = {}
        rtn_item[json_name]["required"] = list(str(a) for a in item[1].keys())
        for thing in item[1].items():
            rtn_item[json_name][property_or_item(json_type, json_name)].update(dict(build_item(thing)))
    if json_type == "array":
        rtn_item[json_name][property_or_item(json_type, json_name)] = {}
        rtn_item[json_name]["minItems"] = 0
        for thing in item[1]:
            rtn_item[json_name][property_or_item(json_type, json_name)].update(dict(build_item(thing)))
    return rtn_item


def determine_type(type_to_convert):
    if isinstance(type_to_convert, tuple):
        return "tuple"
    elif isinstance(type_to_convert, dict):
        return "object"
    elif isinstance(type_to_convert, list):
        return "array"
    elif isinstance(type_to_convert, bool):
        return "boolean"
    elif isinstance(type_to_convert, int):
        return "integer"
    elif isinstance(type_to_convert, float):
        return "number"
    elif isinstance(type_to_convert, type(None)):
        return "null"
    else:
        return "string"


def get_name_type(item):
    rtn_item = {}
    rtn_type = determine_type(item[1])
    rtn_item = str(item[0])
    return rtn_item, rtn_type


def property_or_item(json_type, json_name):
    if json_type == "object":
        if "name_array" in json_name:
            return "items"
        else:
            return "properties"
    else:
        return "items"


def load_str_to_json(json_str):
    # Changes the passed string into valid json data string to be used for the request
    # This function will forcefully remove any unicode characters
    if isinstance(json_str, unicode):
        str_to_use = unicodedata.normalize('NFKD', json_str).encode('ascii','ignore')
    elif isinstance(json_str, dict):
        str_to_use = json.dumps(json_str)
    else:
        str_to_use = json_str
    dict_to_use = json.loads(str_to_use)
    return json.dumps(dict_to_use)


def pretty_print_it(json_item):
    return json.dumps(json_item, sort_keys=True, indent=4, separators=(',', ': '))
