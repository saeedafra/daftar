"""
Saeed Afrasiabi
2022-08-23
"""

from tkinter import messagebox

try:
    from daftar_gui import DaftarGui
    myApp=DaftarGui()
    myApp.run()
except Exception as e:
    messagebox.showerror("Wrapper-caught error", "The following error was caught by the app wrapper:\n"+str(e))