"""
Saeed Afrasiabi
2022-08-23
"""

def check_key_value(key_dict: dict, value_string: str):
    """
    type of return value not known. None if conversion failed
    """
    value = None
    if value_string == "":
        #indicates that any value is okay, simply saying that the key is populated
        value = value_string
    elif key_dict["type"] == "string":
        if "range" in key_dict and key_dict["range"]=="categorical":
            if value_string.lower() in [x.lower() for x in key_dict["possible values"]]:
                value = value_string 
        else:
            value = value_string
    elif key_dict["type"] == "boolean":
        possible_true = ["true", "yes"]
        possible_false = ["false", "no"]
        if value_string.lower() in possible_true:
            value = True
        elif value_string.lower() in possible_false:
            value = False
    elif key_dict["type"] == "date":
        #assuming format is always dd.mm.yyyy
        tmp = value_string.split(".")
        if len(tmp) ==3:
            if False not in [x.isdigit() for x in tmp]:
                value = value_string
    elif key_dict["type"] == "int":
        try:
            value = int(value_string)
        except ValueError:
            value = None
    else:
        #type undefined
        pass

    return value
    
