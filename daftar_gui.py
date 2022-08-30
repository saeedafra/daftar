"""
Saeed Afrasiabi
2022-08-23
"""

import tkinter as tk
from tkinter import filedialog, messagebox

from numpy import expand_dims, isin
import log_db_tools
#from settings_gui import SettingsGui
import entry_popup_win as popups

import datetime
import file_tools
import parsing_tools

from copy import copy, deepcopy

class DaftarGui(tk.Tk):
    def __init__(self):
        #self.settings_gui_obj=SettingsGui()
        self.settings_dict={}
        self.settings_dict["keys_yml"]="task_keys.yml"
        
        self.states=[]

        self.selected_task_index = -1
        self.current_log_index=-1
        self.current_keys_list_from_keys_dict=[]
        self.current_task={}
        self.current_filter_entry_value = None
        self.current_selected_filter_key_index = -1
        self.log_text_key_release_counter = 0
        self.log_text_key_release_autosave_threshold = 5
        self.task_list_squeezed=False
        self.logs_list_squeezed=False
        self.log_text_squeezed=False

        self.load_keys_yml()

        self.current_filters={}
        #for key in self.settings_dict["filter_keys"]:
        #    self.current_filters[key]=""
        self.current_filters_keys_list=[]

        self.saved = True
    
    def load_keys_yml(self):
        self.settings_dict["filter_keys"], msg = \
            file_tools.process_keys_yml(self.settings_dict["keys_yml"])
        if msg!="":
            messagebox.showerror('Keys YML File Error', msg)
            raise Exception(msg)
    
    def run(self):
        self.build_window()
        self.new_button_command()
        self.window.mainloop()
    
         
    def build_window(self):
        self.window = tk.Tk()
        self.window.geometry("900x500")
        #self.window_height=500
        #self.window_width=700
        self.window.title("Logger v0.0")
        self.window.bind("<Configure>",self.window_resize)
        
        self.settings_frame = tk.Frame(master=self.window,relief=tk.RAISED)
        self.settings_frame.pack(fill=tk.X, pady=2, padx=2)

        self.db_filename_entry = tk.Entry(master=self.settings_frame)
        self.db_filename_entry.insert(0,"[path to ipcat db file]")
        self.db_filename_entry.pack(fill=tk.X, side=tk.LEFT, expand=True)
        
        self.db_file_button = tk.Button(master=self.settings_frame, text="Browse", command=self.db_file_button_command)
        self.db_file_button.pack(side=tk.RIGHT, padx=2)

        self.db_load_button = tk.Button(master=self.settings_frame, text="load", command=self.db_load_button_command)
        self.db_load_button.pack(side=tk.RIGHT, padx=2)
    
        self.settings_button = tk.Button(master=self.settings_frame, text="Settings", command=self.settings_button_command)
        self.settings_button.pack(side=tk.RIGHT, padx=2)

        self.save_button = tk.Button(master=self.settings_frame, text="Save", command=self.save_button_command)
        self.save_button.pack(side=tk.RIGHT, padx=2)

        self.new_button = tk.Button(master=self.settings_frame, text="New", command=self.new_button_command)
        self.new_button.pack(side=tk.RIGHT, padx=2)
        
        self.discard_button = tk.Button(master=self.settings_frame, text="Discard", command=self.discard_button_command)
        self.discard_button.pack(side=tk.RIGHT, padx=2)

        self.keys_yml_button = tk.Button(master=self.settings_frame, text="Reload keys", command=self.keys_yml_button_command)
        self.keys_yml_button.pack(side=tk.RIGHT, padx=2)

        self.filter_frame = tk.Frame(master=self.window,relief=tk.RAISED)
        self.filter_frame.pack(side = tk.LEFT, pady=2, padx=2, fill=tk.Y)

        self.filter_list_label = tk.Label(self.filter_frame, text = "Filters")
        self.filter_list_label.pack()

        self.filter_keys_list_var = tk.StringVar(value=[key for key in self.settings_dict["filter_keys"]])
        self.filter_keys_list = tk.Listbox(master=self.filter_frame, listvariable=self.filter_keys_list_var)
        self.filter_keys_list.pack(fill=tk.Y, expand = True)
        self.filter_keys_list.bind("<<ListboxSelect>>", self.filter_keys_list_change)
        self.filter_keys_list_change()
        
        self.filter_key_entry = tk.Entry(master=self.filter_frame)
        self.filter_key_entry.insert(0,"")
        self.filter_key_entry.pack()
        self.filter_key_entry.bind("<KeyRelease>", self.filter_key_entry_change)

        self.filter_value_entry = tk.Entry(master=self.filter_frame)
        self.filter_value_entry.insert(0,"")
        self.filter_value_entry.pack()
        self.filter_value_entry.bind("<KeyRelease>", self.filter_value_entry_change)

        self.filter_buttons_frame = tk.Frame(master=self.filter_frame,relief=tk.RAISED)
        self.filter_buttons_frame.pack(pady=2, padx=2)

        self.add_filter_button = tk.Button(master=self.filter_buttons_frame, text="+", command=self.add_filter_button_command)
        self.add_filter_button.pack(side=tk.LEFT, padx=2)

        self.del_filter_button = tk.Button(master=self.filter_buttons_frame, text="-", command=self.del_filter_button_command)
        self.del_filter_button.pack(side=tk.LEFT, padx=2)

        self.filter_list_var = tk.StringVar(value=[""])
        self.filter_list = tk.Listbox(master=self.filter_frame, listvariable=self.filter_list_var)
        self.filter_list.pack(fill=tk.Y, expand = True)
        self.filter_list.bind("<<ListboxSelect>>", self.filter_list_change)

        self.left_frame = tk.Frame(master=self.window,relief=tk.RAISED)
        self.left_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, pady=2, padx=2)
        self.left_frame.pack_propagate(0)
        
        self.tasks_list_label = tk.Button(self.left_frame, text = "Tasks view <>", command=self.squeeze_task_command)
        self.tasks_list_label.pack()

        self.task_list_var = tk.StringVar(value=[""])
        self.task_list=tk.Listbox(master=self.left_frame, listvariable=self.task_list_var)
        self.task_list.pack(fill=tk.BOTH, expand = True)
        self.task_list.bind("<<ListboxSelect>>", self.task_list_change)
        
        self.new_task_entry = tk.Entry(master=self.left_frame)
        self.new_task_entry.insert(0,"")
        self.new_task_entry.pack()
        self.new_task_entry.bind('<Return>', self.add_task_command)
        #self.new_task_entry.bind("<KeyRelease>", self.new_task_entry_change)

        self.left_middle_frame = tk.Frame(master=self.left_frame,relief=tk.RAISED)
        self.left_middle_frame.pack(pady=2, padx=2)

        self.child_issue_var = tk.IntVar()
        self.child_task_checkbox = tk.Checkbutton(self.left_middle_frame, text='Child task',\
            variable=self.child_issue_var, onvalue=1, offvalue=0)
        self.child_task_checkbox.pack(side= tk.RIGHT, padx=2)

        self.today_plan_var = tk.IntVar()
        self.today_plan_checkbox = tk.Checkbutton(self.left_middle_frame, text='Today plan',\
            variable=self.today_plan_var, onvalue=1, offvalue=0)
        self.today_plan_checkbox.pack(side= tk.RIGHT, padx=2)

        self.add_task_button = tk.Button(master=self.left_frame, text="+", command=self.add_task_command)
        self.add_task_button.pack(side=tk.RIGHT, padx=2)

        self.del_task_button = tk.Button(master=self.left_frame, text="-", command=self.del_task_command)
        self.del_task_button.pack(side=tk.RIGHT, padx=2)

        self.middle_frame = tk.Frame(master=self.window,relief=tk.RAISED)
        self.middle_frame.pack(fill=tk.Y, side = tk.LEFT, pady=2, padx=2)
        
        self.hierarchy_list_label = tk.Label(self.middle_frame, text = "Hierarchies")
        self.hierarchy_list_label.pack()

        self.hierarchy_list_var = tk.StringVar(value=[""])
        self.hierarchy_list=tk.Listbox(master=self.middle_frame,  listvariable=self.hierarchy_list_var, height = 5)
        self.hierarchy_list.pack(fill=tk.BOTH, expand = True)
        self.hierarchy_list.bind("<<ListboxSelect>>", self.hierarchy_list_change)

        self.keys_list_label = tk.Label(self.middle_frame, text = "Keys")
        self.keys_list_label.pack()

        self.keys_list_var = tk.StringVar(value=[""])
        self.keys_list=tk.Listbox(master=self.middle_frame,  listvariable=self.keys_list_var, height = 6)
        self.keys_list.pack(fill=tk.BOTH, expand = True)
        self.keys_list.bind("<<ListboxSelect>>", self.keys_list_change)
        self.keys_list.bind('<Double-1>', self.keys_list_doubleclick)

        self.del_key_button = tk.Button(master=self.middle_frame, text="-", command=self.del_key_command)
        self.del_key_button.pack(padx=2, side = tk.RIGHT)

        self.add_key_button = tk.Button(master=self.middle_frame, text="+", command=self.add_key_command)
        self.add_key_button.pack(padx=2, side = tk.RIGHT)

        self.right_frame = tk.Frame(master=self.window,relief=tk.RAISED)
        self.right_frame.pack(fill=tk.BOTH, side = tk.LEFT, expand=True, pady=2, padx=2)
        self.right_frame.pack_propagate(0)

        self.logs_list_label = tk.Button(self.right_frame, text = "Log entries <>", command = self.squeeze_logs_command)
        self.logs_list_label.pack()

        self.logs_list_var = tk.StringVar(value=[""])
        self.logs_list=tk.Listbox(master=self.right_frame,  listvariable=self.logs_list_var)
        self.logs_list.pack(fill=tk.BOTH,  expand = True)
        self.logs_list.bind("<<ListboxSelect>>", self.logs_list_change)
        self.logs_list.bind('<Double-1>', self.logs_list_doubleclick)

        self.add_log_button = tk.Button(master=self.right_frame, text="+", command=self.add_log_command)
        self.add_log_button.pack(side=tk.RIGHT, padx=2)

        self.del_log_button = tk.Button(master=self.right_frame, text="-", command=self.del_log_command)
        self.del_log_button.pack(side=tk.RIGHT, padx=2)

        self.log_frame = tk.Frame(master=self.window,relief=tk.RAISED)
        self.log_frame.pack(fill=tk.BOTH, side = tk.LEFT, expand=True, pady=2, padx=2)
        self.log_frame.pack_propagate(0)

        self.log_text_label = tk.Button(self.log_frame, text = "Single log <>", command = self.squeeze_log_text_command)
        self.log_text_label.pack()

        self.log_text=tk.Text(master=self.log_frame, width=10)
        self.log_text.pack(fill=tk.BOTH ,expand=True)
        self.log_text.bind("<KeyRelease>", self.log_text_key_release)
        self.log_text.bind("<FocusOut>", self.log_text_focus_out)
        
        
    def squeeze_task_command(self,event=[]):
        self.task_list_squeezed = not self.task_list_squeezed
        if self.task_list_squeezed:
            
            self.left_frame.pack(fill=tk.Y, expand = False)
            self.left_frame.configure(width=70)
        else:
            self.left_frame.pack(fill=tk.BOTH, expand = True)
            self.left_frame.configure(width=150)
        
    def squeeze_logs_command(self,event=[]):
        self.logs_list_squeezed = not self.logs_list_squeezed
        if self.logs_list_squeezed:
            
            self.right_frame.pack(fill=tk.Y, expand = False)
            self.right_frame.configure(width=70)
        else:
            self.right_frame.pack(fill=tk.BOTH, expand = True)
            self.right_frame.configure(width=150)

    def squeeze_log_text_command(self,event=[]):
        self.log_text_squeezed = not self.log_text_squeezed
        if self.log_text_squeezed:
            
            self.log_frame.pack(fill=tk.Y, expand = False)
            self.log_frame.configure(width=70)
        else:
            self.log_frame.pack(fill=tk.BOTH, expand = True)
            self.log_frame.configure(width=150)


    def log_text_focus_out(self,event=[]):
        if not( self.current_task and "logs" in self.current_task and \
            self.current_log_index!=-1):
            return
        
        self.log_text_key_release_counter = 0
        self.auto_save()

    def log_text_key_release(self,event=[]):
        if not( self.current_task and "logs" in self.current_task and \
            self.current_log_index!=-1):
            return

        tmp_text: str=self.log_text.get("1.0",tk.END)
        tmp_text=tmp_text.replace("\n", "\\n")
        self.current_task["logs"][self.current_log_index]["text"]=tmp_text

        self.log_text_key_release_counter += 1
        if self.log_text_key_release_counter >= self.log_text_key_release_autosave_threshold:
            self.log_text_key_release_counter = 0
            self.auto_save()


    def keys_yml_button_command(self,event=[]):
        self.load_keys_yml()

    def add_log_command(self,event=[]):
        #no need to choose where to put it, later on i will sort this by date
        new_dict={}
        x= datetime.datetime.now()
        new_dict["date"]=x.strftime("%d.%m.%y")
        new_dict["text"]=""
        tmp_win=popups.MultipleEntryPopupWin(self.window,self,new_dict)
        tmp_win.grab_set()
        if tmp_win.show_win():
            if "logs" not in self.current_task:
                self.current_task["logs"]=[]
            self.current_task["logs"].append(new_dict)
            self.populate_logs_list()
            self.auto_save()

    def del_log_command(self,event=[]):
        if self.current_log_index!=-1:
            self.current_task["logs"].pop(self.current_log_index)
            self.populate_logs_list()
            self.auto_save()

    def db_file_button_command(self):
        filename = filedialog.askopenfilename(title="select yaml file")
        if filename:
            self.db_filename_entry.delete(0,tk.END)
            self.db_filename_entry.insert(0,filename)
            self.db_load_button_command()

    def db_load_button_command(self):
        if not self.saved:
            messagebox.showerror('not saved',"File not saved yet!")
            return

        if self.db_filename_entry.get().strip()=="":
            return
        filename = self.db_filename_entry.get()
        log_db_obj = log_db_tools.LogDb(filename)
        if log_db_obj.load_success():
            self.log_db_obj: log_db_tools.LogDb = log_db_obj
            self.settings_dict["db_file"]=filename
            self.new_db_loaded()
        else:
            messagebox.showerror('File Error', 'Error: couldnt load the YML file!')
            return
    
    def populate_tasks_list(self):
        tmp_list = ["closed", "dropped"]
        self.task_list_var.set(["*"* x["level"] + x["name"] + "-> " + x["due date"] if ("due date" in x) else ("*"* x["level"] + x["name"]) \
                for x in self.current_tasks_list])
        #also trigerring a reset to the rest of the lists
        self.task_list.select_set(0)
        self.task_list_change()

    def task_list_change(self,event=[]):
        if not self.current_tasks_list:
            #anyway this list is empty
            self.current_task = {}
            self.selected_task_index = -1
        elif len(self.task_list.curselection())==0:
            return
        else:
            new_task_index = self.task_list.curselection()[0]
            #if new_task_index != self.selected_task_index:
            self.selected_task_index = new_task_index
            # TODO this element index being the same for db list and present task list is okay for now but not
            # if we want to load a part of the db to present task list
            self.current_task = self.current_tasks_list[self.selected_task_index]

        self.populate_keys_list()
        self.populate_logs_list()
        self.keys_list_change()

    def populate_keys_list(self):
        #just to set a one to one correspondence between elements in list widget and the keys
        self.current_keys_list_from_keys_dict = [key for key in self.current_task]

        self.keys_list_var.set([key + ": " + str(self.current_task[key]) for key in self.current_task])

    def populate_logs_list(self):
        #no correspondence need sto be kept as logs is already a list
        if "logs" in self.current_task:
            self.logs_list_var.set([str(log["date"]) + ": " + str(log["text"]) for log in self.current_task["logs"]])
        else:
            self.logs_list_var.set([])

    def settings_button_command(self, event=[]):
        #self.settings_gui_obj.run()
        #if self.settings_gui_obj.changed():
        #        self.settings, self.log_db_obj = self.settings_gui_obj.get_settings()
        #        print("new log file = " , self.settings["db_file"])
        pass
    
    def window_resize(self,event):
        pass

    def hierarchy_list_change(self):
        pass
    
    def keys_list_change(self,event=[]):
        pass
    
    def del_key_command(self, event=[]):
        if not self.keys_list.curselection():
            return
        key_index = self.keys_list.curselection()[0]
        key= self.current_keys_list_from_keys_dict[key_index]
        if key not in self.current_task:
            messagebox.showerror("key not in current_task, this must not happen")
            return
        del self.current_task[key]
        self.populate_keys_list()
        
    def add_key_command(self, event=[]):
        i=0
        while "new key " + str(i) in self.current_task:
            i = i+1
       
        self.current_task["new key "+ str(i)]=""
        self.populate_keys_list()

    def keys_list_doubleclick(self,event=[]):
        key_index = self.keys_list.curselection()[0]
        key= self.current_keys_list_from_keys_dict[key_index]
        if key not in self.current_task:
            messagebox.showerror("bad error!", "key not in current_task, this must not happen")
            return
        new_dict={}
        new_dict["key"]=copy(key)
        new_dict["value"]=self.current_task[key]
        tmp_win= popups.MultipleEntryPopupWin(self.window, self, new_dict)
        tmp_win.grab_set()
        if tmp_win.show_win():
            if new_dict["key"]!=key and new_dict["key"] in self.current_task:
                messagebox.showerror("key error", "the new key is already existing")
                return
            if new_dict["key"] in self.settings_dict["filter_keys"]:
                value = parsing_tools.check_key_value(self.settings_dict["filter_keys"][new_dict["key"]]\
                    , new_dict["value"])
                if value == None:
                    messagebox.showerror("value error", "the key is predefined and the new value fails the rules. \n reload keys YML if desired.")
                    return
            else:
                value = new_dict["value"]

            if new_dict["key"]!=key:
                messagebox.showwarning("key change", "You changed a key. Remove the original one yourself. (ass)")

            self.current_task[new_dict["key"]]=value
            self.populate_keys_list()
            self.auto_save()
        
    def logs_list_change(self, event=[]):
        if len(self.logs_list.curselection())==0:
            self.current_log_index=-1
            return
        self.current_log_index=self.logs_list.curselection()[0]
        tmp_text: str = self.current_task["logs"][self.current_log_index]["text"]
        tmp_text = tmp_text.replace("\\n","\n")
        self.log_text.delete("1.0",tk.END)
        self.log_text.insert("1.0", tmp_text)
        self.log_text_key_release_counter=0

    def logs_list_doubleclick(self,event=[]):
        key_index = self.logs_list.curselection()[0]
        tmp_win= popups.MultipleEntryPopupWin(self.window, self, self.current_task["logs"][key_index])
        tmp_win.grab_set()
        if tmp_win.show_win():
            self.populate_logs_list()
            self.auto_save()

    def add_filter_button_command(self, event=[]):
        if self.filter_key_entry.get().strip() == "":
            return
        if self.current_filter_entry_value == None:
            return
        key = self.filter_key_entry.get().strip()
        self.current_filters[key]= self.current_filter_entry_value
        self.update_filters_list()

    def update_filters_list(self):
        """
        updates the list of current filters and applies the filters.
        no optimization here, all filters applied from scratch everytime
        something changes
        """
        #the job of the list is to make the 1-2-1 correspondence
        self.current_filters_keys_list=[x \
            for x in self.current_filters]

        self.filter_list_var.set([x+": "+str(self.current_filters[x]) \
            for x in self.current_filters])    
        
        tasks_indices_to_keep=[i for i in range(len(self.loaded_tasks_list))]
        for task_index in range(len(self.loaded_tasks_list)):
            do_remove = False
            for key in self.current_filters:    
                if self.current_filters[key]:
                    if isinstance(self.current_filters[key], list):
                        tmp = copy(self.current_filters[key])
                    else:
                        tmp = [copy(self.current_filters[key])]

                    if key in self.loaded_tasks_list[task_index] and \
                        isinstance(self.loaded_tasks_list[task_index][key],list):
                        messagebox.showerror("db error", "I ran into a task key value which is a list. This is not supported as it causes " + \
                            "problem with the filters which are a list. The task id is "+ str(self.loaded_tasks_list[task_index]["id"]))
                        return

                    if key not in self.loaded_tasks_list[task_index] or \
                        self.loaded_tasks_list[task_index][key] not in tmp:
                        do_remove = True
                else:
                    #when filter is only a "", then any value is okay
                    if key not in self.loaded_tasks_list[task_index]:
                        do_remove = True
            if "deleted" in self.loaded_tasks_list[task_index] and \
                self.loaded_tasks_list[task_index]["deleted"]==True:
                do_remove = True
                
            if do_remove and (task_index in tasks_indices_to_keep):
                tasks_indices_to_keep.remove(task_index)
   
        self.current_tasks_list=[self.loaded_tasks_list[i] for i in tasks_indices_to_keep]
        self.populate_tasks_list()
    
    def del_filter_button_command(self, event=[]):
        key_index=self.filter_list.curselection()
        if not key_index:
            return
        del self.current_filters[self.current_filters_keys_list[key_index[0]]]
        self.update_filters_list()

    def filter_list_change(self,event=[]):
        pass
    
    def filter_keys_list_change(self,event=[]):
        if self.filter_keys_list.curselection():
            self.current_selected_filter_key_index = self.filter_keys_list.curselection()[0]
            self.filter_key_entry.delete(0,tk.END)
            self.filter_key_entry.insert(0,\
                self.filter_keys_list.get(self.current_selected_filter_key_index))
            self.filter_value_entry_change()

    def filter_key_entry_change(self, event=[]):
        if self.filter_key_entry.get().strip() != "":
            self.filter_value_entry_change()

    def filter_value_entry_change(self,event=[]):
        value_string=self.filter_value_entry.get()
        value_string=value_string.strip()
        value=None #indicating no change

        #return value could have any type, None indicating a probelm
        key = self.filter_key_entry.get().strip()
        if key != "":
            if key in self.settings_dict["filter_keys"]:
                value = parsing_tools.check_key_value(self.settings_dict["filter_keys"][key]\
                    , value_string)
            else:
                value = value_string
        
        if value == None:
            self.filter_value_entry.config(fg="red")
        else:
            self.filter_value_entry.config(fg="black")
        #could be none!
        self.current_filter_entry_value=value

    def add_task_command(self,event=[]):
        task_name = self.new_task_entry.get().strip()
        if task_name=="":
            return
        
        #recall that we assume our loaded_task_list is always the same
        #as that in og_db_obj (it's indeed the same object)
        new_id = self.log_db_obj.generate_new_id()
        if new_id == -1:
            #we must not be here!
            raise Exception("I'm getting id=-1 !!")

        new_task = {}
        new_task["id"]=new_id
        new_task["name"]= task_name
        

        if self.child_issue_var.get():
            if self.current_task!={}:
                if "id" not in self.current_task:
                    messagebox.showerror("error", "cuurent task has no id. this mist not happen")
                    return
                new_task["parent"] = self.current_task["id"]

        if self.today_plan_var.get():
            x= datetime.datetime.now()
            new_task["due date"]= x.strftime("%d.%m.%y")
            new_task["status"]="open"
            new_task["priority"]=True
        
        self.loaded_tasks_list.append(new_task)
        
        #here I'm neglecting the selection on tasks_list widget!
        #the user will see the new task in keys and logs lists widgets until
        #he touches the tasks_list
        self.current_task=self.loaded_tasks_list[-1]
        self.log_db_obj.update_level_single(self.current_task)
        
        #applying filters again, which repopulates tasks_list
        self.update_filters_list()

        #these two functions only use self.current_task
        self.populate_keys_list()
        self.populate_logs_list()
        self.auto_save()

    def del_task_command(self,event=[]):
        # problem is that user selects from the current list of tasks in 
        # tasks widget which is the self.current_tasks_list.
        # and self.current_task. it's okay to change it and have the change in the original
        # loaded_tasks_list but deleting is something else :-?
        # a good trick here is to just mark it :D 
        # maybe as a task with a key "deleted"=true and we always add 
        #an implicit filter for NOT Having deleted :D
        if not self.current_task:
            return

        children_list=[]
        for task in self.loaded_tasks_list:
            if "deleted" in task and task["deleted"] == True:
                continue
            
            if "parent" in task:
                if isinstance(task["parent"],list):
                    tmp = copy(task["parent"])
                else:
                    tmp = [copy(task["parent"])]
            
                if self.current_task["id"] in tmp:
                    children_list.append(task["id"])

        if children_list:
            messagebox.showerror("error", "The task you want to delete has children. So I won't delete it. I'm filtering them by ID. Deal with them first.")
            self.current_filters["id"] = children_list
            self.update_filters_list()
        else:
            self.current_task["deleted"]=True
            self.update_filters_list()
            self.auto_save()
    
    def auto_save(self):
        # note that this function is the one that is called with every change
        self.saved = False

        msg=self.log_db_obj.auto_save()
        if msg!="":
            messagebox.showerror('Could not autosave: ', msg)
        
    
    def save_button_command(self,event=[]):
        #as input to save() indicates that use laready available name
        file_to_try=""
        if self.settings_dict["db_file"]=="":
            #meaning a new file
            #TODO not checking for existing or not!
            file_to_try = filedialog.asksaveasfilename(title="select yaml file",filetypes=[('YAML files', '*.yml')])
            if not file_to_try:
                return

        msg=self.log_db_obj.save(file = copy(file_to_try))
        if msg!="":
            messagebox.showerror('Could not save: ', msg)
        else:
            self.saved=True
            self.settings_dict["db_file"] = copy(file_to_try)
            messagebox.showinfo("file", "file saved.")

    def new_button_command(self,event=[]):
        if not self.saved:
            messagebox.showerror('not saved',"File not saved yet!")
            return

        log_db_obj = log_db_tools.LogDb("", event="new")
        if log_db_obj.load_success():
            self.log_db_obj: log_db_tools.LogDb = log_db_obj
            self.settings_dict["db_file"]=""
            self.new_db_loaded()
        else:
            messagebox.showerror('File Error', 'Error: couldnt load the YML file!')
            return

    def discard_button_command(self,event=[]):
        self.saved = True
        self.log_db_obj.reset()
        self.new_db_loaded()

    def new_db_loaded(self):
        #here is the logic: self.loaded_tasks_list is the only task list which I store
        #when filtering is done, the tasks list view changes. As it's easier to play with the
        #index of the selection from the list widget and keep a one-2-one correspondence between
        #the list shown in the widget and a data list, I keep self.current_tasks_list match
        #that of the widget. BUT the items in this list are aliases of the items in the
        #original loaded_tasks_list! So I don't need to keep track of changes. All changes 
        #are done to self.curren_task which is a dict and the changes take the right place
        #in the original list.
        self.saved = True
        self.current_filters={}
        
        self.loaded_tasks_list=self.log_db_obj.get_db()
        self.current_tasks_list = self.loaded_tasks_list
        self.update_filters_list()
        