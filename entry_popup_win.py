"""
Saeed Afrasiabi
2022-08-23
"""

import tkinter as tk

class SingleEntryPopupWin(tk.Toplevel):
    def __init__(self, parent_win, parent_object, key, dict_object):
        super().__init__(parent_win)

        #assuming I can access this object as reference
        self.key = key
        self.dict_object = dict_object

        self.parent_object = parent_object

        self.geometry("300x200")
        self.title("pop up")
        
        self.key_label = tk.Label(self, text = key)
        self.key_label.pack()
        self.entry = tk.Entry(master=self)
        self.entry.insert(0, str(dict_object[key]))
        self.entry.pack()
        
        self.ok_button = tk.Button(master=self, text="Save", command=self.ok_button_command)
        self.ok_button.pack()
        self.cancel_button = tk.Button(master=self, text="Cancel", command=self.cancel_button_command)
        self.cancel_button.pack()

        self.saved = False
    
    def show_win(self):
         self.wait_window()
         return self.saved

    def ok_button_command(self,event=[]):
        self.dict_object[self.key] = self.entry.get()
        self.saved = True
        self.destroy()
        

    def cancel_button_command(self,event=[]):
        self.destroy()

class MultipleEntryPopupWin(tk.Toplevel):
    """
    passed object by reference is a dict where every value is changable
    """
    def __init__(self, parent_win, parent_object, dict_object):
        super().__init__(parent_win)

        #assuming I can access this object as reference
        self.dict_object = dict_object

        self.parent_object = parent_object

        self.geometry("500x200")
        self.title("pop up")
        
        keys = list(dict_object.keys())
        self.key_labels: list[tk.Label]=[]
        self.value_entries: list[tk.Entry] = []
        self.frame: list[tk.Frame]=[]
        for i in range(len(keys)):
            self.frame.append(tk.Frame(master=self,relief=tk.RAISED))
            self.frame[i].pack(fill=tk.X, pady=5, padx=5)
            self.key_labels.append(tk.Label(self.frame[i], text = keys[i]))
            self.key_labels[i].pack(side=tk.LEFT)
            self.value_entries.append(tk.Entry(master=self.frame[i]))
            self.value_entries[i].insert(0, str(dict_object[keys[i]]))
            self.value_entries[i].pack(fill=tk.X, side=tk.RIGHT, expand=True)
        
        self.ok_button = tk.Button(master=self, text="Save", command=self.ok_button_command)
        self.ok_button.pack()
        self.cancel_button = tk.Button(master=self, text="Cancel", command=self.cancel_button_command)
        self.cancel_button.pack()

        self.saved = False
    
    def show_win(self):
         self.wait_window()
         return self.saved

    def ok_button_command(self,event=[]):
        keys = list(self.dict_object.keys())
        for i in range(len(keys)):
            self.dict_object[keys[i]] = self.value_entries[i].get()
        self.saved = True
        self.destroy()
        

    def cancel_button_command(self,event=[]):
        self.destroy()