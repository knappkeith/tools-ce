import json


def build_item(item):
    if type(item) is type((5,)):
        return build_tuple(item)
    elif type(item) is type({}):
        return build_tuple(("name_dict", item)).values()[0]
    elif type(item) is type([]):
        return build_tuple(("name_array", item[0])).values()[0]
    else:
        raise NameError("Unknown type: %s - " % (type(item), item))


def build_tuple(item):
    json_name, json_type = get_name_type(item)
    rtn_item = {}
    rtn_item[json_name] = {}
    rtn_item[json_name]["type"] = json_type
    if json_type == "object":
        rtn_item[json_name][property_or_item(json_type, json_name)] = {}
        rtn_item[json_name]["required"] = list(str(a) for a in item[1].keys())
        for thing in item[1].items():
            rtn_item[json_name][property_or_item(json_type, json_name)].update(dict(build_item(thing)))
    if json_type == "array":
        rtn_item[json_name][property_or_item(json_type, json_name)] = {}
        for thing in item[1]:
            rtn_item[json_name][property_or_item(json_type, json_name)].update(dict(build_item(thing)))

    return rtn_item


def determine_type(type_to_convert):
    if type(type_to_convert) is type((5,)):
        return "tuple"
    elif type(type_to_convert) is type({}):
        return "object"
    elif type(type_to_convert) is type([]):
        return "array"
    elif type(type_to_convert) is type(False):
        return "boolean"
    elif type(type_to_convert) is type(5):
        return "integer"
    elif type(type_to_convert) is type(5.1):
        return "number"
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
