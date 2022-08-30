"""
Saeed Afrasiabi
2022-08-23
"""

from logging import exception
import yaml
from copy import copy , deepcopy

class LogDb:
    def __init__(self, yml_file: str, event=""):
        self.__loaded = False
        if event=="":
            try:
                with open(yml_file, "r") as stream:
                    try:
                        self.original_yml_data = yaml.safe_load(stream)
                        #print(a)
                    except yaml.YAMLError as exc:
                        self.loaded = False
                        print("couldnt read the yml file " +yml_file)
                        raise exc
            except (OSError, IOError) as e:
                print("Error reading/opening yml file ", yml_file)
                raise e
            self.yml_file = yml_file
        elif event=="new":
            #no file to be opened.
            self.yml_file=""
            self.original_yml_data=[]
        
        self.yml_data = deepcopy(self.original_yml_data)
        if self.yml_file[-5:]==".yaml":
            core = self.yml_file[:-5]
        elif yml_file[-4:]==".yml":
            core = self.yml_file[:-4]
        elif self.yml_file == "":
            #meaning new file
            core = "untitled000"
        else:
            raise Exception("yml file name format not as expected")
        
        self.auto_save_yml_file = core + "_autosave.yml"

        self.__loaded = True
        self.ids_list=self.extract_ids()
        self.update_tasks_list()
        self.update_level_all()

    def extract_ids(self) -> list:
        ids_list=[]
        for item in self.yml_data:
            if "id" in item:
                ids_list.append(item["id"])
            #if not, do nothing. not the job of this function to deal with it
            #else:
            #    raise Exception("item has no id!")
        return ids_list


    def load_success(self) -> bool:
        return self.__loaded
    
    def update_tasks_list(self):
        if not self.load_success():
            return
        self.tasks_list=[]
        for item in self.yml_data:
            self.tasks_list.append([item["name"],item["id"]])

    def get_tasks_list(self) -> list:
        """
        returns the tasks_list as a reference so no run time penalty in calling it frequently
        updating of the task list is a different matter
        """
        if not self.load_success():
            return []
      
        return deepcopy(self.tasks_list)
    
    def get_db(self) -> list:
        if self.load_success():
            return self.yml_data
        else:
            return []
    
    def generate_new_id(self) -> int:
        if self.load_success():
            self.ids_list = self.extract_ids()
            #ids_list must have been built, it might however be empty!
            # TODO do it better later, now I'm just taking the largest :D
            if self.ids_list:
                return max(self.ids_list)+1
            else:
                return 1
        else:
            return -1

    def auto_save(self) -> str:
        msg=""
        try:
            with open(self.auto_save_yml_file, 'w') as file:
                try:
                    documents = yaml.dump(self.yml_data, file, sort_keys=False)
                except:
                    msg = "error from yaml.dump"
        except:
            msg = "error in opening the file"
        
        return msg
    
    def save(self, file="") -> str:
        msg=""
        if file=="":
            yml_file = self.yml_file
        else:
            yml_file = file

        try:
            with open(yml_file, 'w') as file:
                try:
                    documents = yaml.dump(self.yml_data, file, sort_keys=False)
                except:
                    msg = "error from yaml.dump"
        except:
            msg = "error in opening the file"
        
        if msg!="":
            self.yml_file = yml_file
            self.original_yml_data = deepcopy(self.yml_data)

        return msg
    
    def reset(self):
        if not self.load_success:
            raise Exception("this must not happen")
        self.yml_data = deepcopy(self.original_yml_data)

    def update_level_all(self):
        #first remove all levels :D some sort of optimization here!
        for task in self.yml_data:
            if "level" in task:
                del task["level"]
        
        for task in self.yml_data:
            self.update_level_single(task)

    def update_level_single(self,task_dict):
        """
        searches through the list of tasks, obtains the parents
        and level of the task in task_dict.
        information stored inside the dict. no return value.
        So make sure the dict object is passed without copying
        """
        #TODO unoptimized
        if "level" in task_dict and task_dict["level"]> 100:
            raise Exception("a level larger than 100. this is probably a loop! I'm looking at task id " + task_dict["id"])

        #I'm assuming all level keys are removed!
        if "level" in task_dict:
            # if you want it updated after the first round, remove level first!
            return
            
        task_dict["level"]= 0
        if "parent" in task_dict and task_dict["parent"]:
            tmp_parent_list = task_dict["parent"]
            if not isinstance(tmp_parent_list,list):
                tmp_parent_list=[task_dict["parent"]]
            
            level_per_parent_line = [0 for x in tmp_parent_list]
            for parent_id_idx in range(len(tmp_parent_list)):
                for task in self.yml_data:
                    #I assume no task can have a parent id equal to its own id
                    if task["id"]==tmp_parent_list[parent_id_idx]:
                        if "level" in task:
                            #meaning it's already done
                            pass
                        else:
                            self.update_level_single(task)
                        
                        level_per_parent_line[parent_id_idx] += task["level"]

                        #ids are unique so no point in continuing with this loop
                        break
            
            task_dict["level"] = 1 + max(level_per_parent_line)



            
        