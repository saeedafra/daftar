"""
Saeed Afrasiabi
2022-08-23
"""
import yaml

def process_keys_yml(yml_file) -> tuple:
    try:
        with open(yml_file, "r") as stream:
            try:
                yml_data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                msg = "couldnt read the yml file " +yml_file
                return {}, msg
                #raise exc
    except (OSError, IOError) as e:
        msg = "Error reading/opening yml file " + yml_file
        #raise e
        return {}, msg
    
    msg = ""
    keys_dict = {}

    for item in yml_data["keys"]:
        keys_dict[item["name"]]=item
    
    return keys_dict, msg