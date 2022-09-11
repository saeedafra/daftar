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
        valid, tmp_val = check_date_string(value_string)
        if valid:
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

def check_date_string(date_str: str) -> tuple:
    valid = False
    values = []
    tmp = date_str.split(".")
    if len(tmp) ==3:
        try: 
            values = [int(x) for x in tmp]
        except ValueError:
            return False,[]
        
        # I'm assuming DD MM YYYY
        if not (values[0] >= 1 and values[0] <=31 and values[1] >= 1 and values[1] <=12 and values[2] >= 1):
            #and yeah we have year 1 :D
            return False,[]
        
        if values[2] <= 50:
            values[2] += 2000
            # in the unlikely yet interesting event that this code is used after 2050, then we have a hard to catch bug :D
        elif values[2] <= 99:
            values[2] += 1900
        elif values[2] <= 999:
            # whatever
            values[2] += 1000

        valid = True
          
    return valid, values
