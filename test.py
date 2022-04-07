from datetime import datetime
from tkinter import *
from tkinter import ttk
from tkinter import *

from click import command

if __name__ == "__main__":
    master = Tk()
    master.title("Test")
    master.geometry("1920x1080")
    myTree = ttk.Treeview()
    myTree["column"] = ("id", "time", "name", "status")
    myTree.column("#0", width=20, minwidth=25)
    myTree.column("id", anchor=CENTER, width=100)
    myTree.column("time", anchor=CENTER, width=120)
    myTree.column("name", anchor=CENTER, width=150)
    myTree.column("status", anchor=W, width=50)
    
    myTree.heading("#0", text="", anchor=CENTER)
    myTree.heading("id", text="id", anchor=CENTER)
    myTree.heading("time", text="time", anchor=CENTER)
    myTree.heading("name", text="name", anchor=CENTER)
    myTree.heading("status", text="status", anchor=CENTER)
    
    myTree.pack(fill="x", anchor="n", pady=10)
    for i in range(10):
        myTree.insert("", "end", iid=i, values=(str(i), datetime.now(), f"name : {i}", f"status : {i}"))
    
    def selected():
        myTree.item(8, value=("99", datetime.now(), "name : 99", "status : 99"))
    
    button_selected = Button(text="Selected", command=selected)
    button_selected.pack() 
    
    master.mainloop()
