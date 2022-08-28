"""
Saeed Afrasiabi
2022-08-23
"""

import yaml
from copy import deepcopy, copy

with open("work_log.yml", "r") as stream:
    try:
        a=yaml.safe_load(stream)
        #print(a)
    except yaml.YAMLError as exc:
        print(exc)

if False:
    print("Priority tasks and lastest update:")
    for key1 in a:
        for key2 in key1["subitems"]:
            if "priority" in key2:
                if key2["priority"]:
                    date_str=key2["logs"][0]["date"]
                    print(key2["name"] + " -> " + str(date_str))
                    #print("    " + str(date_str) + ":" + a[key1][key2]["logs"][0][date_str])
                    #print("")

if False:
    b=deepcopy(a)
    for key1 in a:
        for key2 in a[key1]:
            if "priority" not in a[key1][key2]:
                b[key1][key2]["priority"]=False
            if "logs" in a[key1][key2]:
                for c in range(len(a[key1][key2]["logs"])):
                    #a[key1][key2]["logs"] is a list of dict
                    #each dict with a key which is the date string
                    # so date here is a dict again
                    tmpkey=list(a[key1][key2]["logs"][c].keys())[0]
                    if isinstance(tmpkey,float):
                        new_key=str(tmpkey)
                    elif isinstance(tmpkey,int):
                        new_key=str(tmpkey)
                    #elif isinstance(date,str) and date == "NA":
                    else:
                        new_key=copy(tmpkey)
                    if new_key!="NA" and new_key[-4:]!="2022":
                        b[key1][key2]["logs"][c][new_key+".2022"]=a[key1][key2]["logs"][c][tmpkey]
                        del a[key1][key2]["logs"][c][tmpkey]

    with open('log_out.yml', 'w') as file:
        documents = yaml.dump(b, file)

if False:
    b=[]
    for key1 in a:
        b.append({})
        b[-1]["name"]=key1
        b[-1]["subitems"]=[]
        for key2 in a[key1]:
            b[-1]["subitems"].append({})
            b[-1]["subitems"][-1]["name"]=key2
            b[-1]["subitems"][-1]["status"]=a[key1][key2]["status"]
            if "priority" not in a[key1][key2]:
                b[-1]["subitems"][-1]["priority"]=False
            else:
                b[-1]["subitems"][-1]["priority"]=a[key1][key2]["priority"]
            
            if "project" not in a[key1][key2]:
                b[-1]["subitems"][-1]["project"]="denali-AP"
            else:
                b[-1]["subitems"][-1]["project"]=a[key1][key2]["project"]
            
            if "chip" not in a[key1][key2]:
                b[-1]["subitems"][-1]["chip"]="Protostar"
            else:
                b[-1]["subitems"][-1]["chip"]=a[key1][key2]["chip"]


            b[-1]["subitems"][-1]["logs"]=[]
            if "logs" in a[key1][key2]:
                for c in range(len(a[key1][key2]["logs"])):
                    b[-1]["subitems"][-1]["logs"].append({})
                    date_key=list(a[key1][key2]["logs"][c].keys())[0]
                    date_str=str(date_key)
                    if date_str[-4:]!="NA" and date_str[-4:]!="2022":
                        date_str = date_str + ".2022"
                    text_str=str(a[key1][key2]["logs"][c][date_key])
                    b[-1]["subitems"][-1]["logs"][-1]["date"]=date_str
                    b[-1]["subitems"][-1]["logs"][-1]["text"]=text_str



    with open('log_out.yml', 'w') as file:
        documents = yaml.dump(b, file,sort_keys=False)

#assign IDs and make the hierarchy flat
if True:
    new_id=0
    b=[]
    for key1 in a:
        b.append({})
        b[-1]["name"]=key1["name"]
        new_id+=1
        b[-1]["id"]=new_id
        parent_id=copy(new_id)
        if "subitems" in key1:
            for key2 in key1["subitems"]:
                b.append({})
                new_id+=1
                b[-1]["id"]=new_id
                b[-1]["parent"]=parent_id
                b[-1].update(key2)

    with open('log_out.yml', 'w') as file:
        documents = yaml.dump(b, file, sort_keys=False)

