from socket import AI_PASSIVE
from tkinter import *
from tkinter import ttk
from DataProvider import *

class Application:
    
    def __init__(self) -> None:
        def write_log(mode):
            with open("log/log_startapp", mode) as f:
                current_time = datetime.datetime.now()
                f.write(f"AppStart : {current_time.day}-{current_time.month}-{current_time.year} | {current_time.hour}:{current_time.minute}:{current_time.second}\n")
        
        try:
            write_log("a")
        except FileNotFoundError:
            write_log("w")
        self.provider = Provider()
        self.setting = Setting()
        
        window = Tk()
        window.title("EarlyWarning")
        window.iconbitmap("img\\rain.ico")
        window.geometry("1024x600")
        window.resizable(False, False)
        
        my_notebook = ttk.Notebook(window)
        my_notebook.pack()
        
        self.frame_page1 = Frame(my_notebook, width=1024, height=600)
        self.frame_page2 = Frame(my_notebook, width=1024, height=600)
        self.frame_page3 = Frame(my_notebook, width=1024, height=600)
        self.frame_setting = Frame(my_notebook, width=1024, height=600)
        
        my_notebook.add(self.frame_page1, text="Show Data")
        my_notebook.add(self.frame_page2, text="Historical Data")
        my_notebook.add(self.frame_page3, text="Alarm Station")
        my_notebook.add(self.frame_setting, text="Setting")
        
        self.frame_page1_widget = LabelFrame(self.frame_page1)
        self.frame_page1_widget.pack(fill="both", expand=1, padx=10, pady=10)
        self.renderWidget_page1()
        
        
        
        window.mainloop()

    def renderWidget_page1(self) -> None:
        
        def reload_widget_tree():
            analog_tree = ttk.Treeview(self.frame_page1_widget, height=20)
            analog_tree["column"] = ("Date", "Time", "Id", "Name", "Status", "Desc", "Code")
            
            analog_tree.column("#0", width=20, minwidth=25)
            analog_tree.column("Date", anchor=CENTER, width=120)
            analog_tree.column("Time", anchor=CENTER, width=150)
            analog_tree.column("Id", anchor=W, width=50)
            analog_tree.column("Name", anchor=W, width=185)
            analog_tree.column("Status", anchor=W, width=150)
            analog_tree.column("Desc", anchor=CENTER, width=150)
            analog_tree.column("Code", anchor=CENTER, width=150)
            
            analog_tree.heading("#0", text="", anchor=CENTER)
            analog_tree.heading("Date", text="Date", anchor=CENTER)
            analog_tree.heading("Time", text="Time", anchor=CENTER)
            analog_tree.heading("Name", text="Name", anchor=CENTER)
            analog_tree.heading("Id", text="Id", anchor=CENTER)
            analog_tree.heading("Name", text="Name", anchor=CENTER)
            analog_tree.heading("Status", text="Status", anchor=CENTER)
            analog_tree.heading("Desc", text="Desc", anchor=CENTER)
            analog_tree.heading("Code", text="Code", anchor=CENTER)
            analog_tree.place(x=10, y=100)
            
            self.provider.iid = 0
            print(self.provider.list_show_tree)
            for i in range(0, len(self.provider.list_show_tree)):
                analog_tree.insert(parent="", index="end", iid=self.provider.get_iid(), value=(self.provider.list_show_tree[i]))

            analog_tree.after(2000, reload_widget_tree)
            
        def reload_widget_button():
            dict_data = self.provider.get_data()
            button_date.config(text=dict_data["date"])
            button_time.config(text=dict_data["time"])
            button_quantity_rain.config(text=dict_data["quantity_rain"])
            button_quantity_water.config(text=dict_data["quantity_water"])
            button_temperature.config(text=dict_data["temperature"])
            button_humidity.config(text=dict_data["humidity"])
            button_date.after(2000, reload_widget_button)
            print(len(self.provider.list_show_tree))
            
        
        label_date = Label(self.frame_page1_widget, text="Date", width=15, font=("Ubuntu", 14))
        label_time = Label(self.frame_page1_widget, text="Time", width=15, font=("Ubuntu", 14))
        label_quantity_rain = Label(self.frame_page1_widget, text="Quantity rain", width=15, font=("Ubuntu", 14))
        label_quantity_water = Label(self.frame_page1_widget, text="Quantity water", width=15, font=("Ubuntu", 14))
        label_temperature = Label(self.frame_page1_widget, text="Temperature", width=15, font=("Ubuntu", 14))
        label_humidity = Label(self.frame_page1_widget, text="Humidity", width=15, font=("Ubuntu", 14))
        label_date.grid(row=0, column=0)
        label_time.grid(row=0, column=1)
        label_quantity_rain.grid(row=0, column=2)
        label_quantity_water.grid(row=0, column=3)
        label_temperature.grid(row=0, column=4)
        label_humidity.grid(row=0, column=5)
        
        button_date = Button(self.frame_page1_widget, text="", font=("Ubuntu", 14), width=15)
        button_time = Button(self.frame_page1_widget, text="", font=("Ubuntu", 14), width=15)
        button_quantity_rain = Button(self.frame_page1_widget, text="", font=("Ubuntu", 14), width=15)
        button_quantity_water = Button(self.frame_page1_widget, text="", font=("Ubuntu", 14), width=15)
        button_temperature = Button(self.frame_page1_widget, text="", font=("Ubuntu", 14), width=15)
        button_humidity = Button(self.frame_page1_widget, text="", font=("Ubuntu", 14), width=15)
        
        button_date.grid(row=1, column=0, pady=10)
        button_time.grid(row=1, column=1, pady=10)
        button_quantity_rain.grid(row=1, column=2, pady=10)
        button_quantity_water.grid(row=1, column=3, pady=10)
        button_temperature.grid(row=1, column=4, pady=10)
        button_humidity.grid(row=1, column=5, pady=10)
        
        self.frame_page1_widget.grid_columnconfigure(0, weight=1)
        self.frame_page1_widget.grid_columnconfigure(1, weight=1)
        self.frame_page1_widget.grid_columnconfigure(2, weight=1)
        self.frame_page1_widget.grid_columnconfigure(3, weight=1)
        self.frame_page1_widget.grid_columnconfigure(4, weight=1)
        self.frame_page1_widget.grid_columnconfigure(5, weight=1)
        
        
        # analog_tree = ttk.Treeview(self.frame_page1_widget, height=20)
        # analog_tree["column"] = ("Date", "Time", "Id", "Name", "Status", "Desc", "Code")
        
        # analog_tree.column("#0", width=20, minwidth=25)
        # analog_tree.column("Date", anchor=W, width=120)
        # analog_tree.column("Time", anchor=W, width=150)
        # analog_tree.column("Id", anchor=W, width=50)
        # analog_tree.column("Name", anchor=CENTER, width=185)
        # analog_tree.column("Status", anchor=W, width=150)
        # analog_tree.column("Desc", anchor=W, width=150)
        # analog_tree.column("Code", anchor=W, width=150)
        
        # analog_tree.heading("#0", text="", anchor=CENTER)
        # analog_tree.heading("Date", text="Date", anchor=CENTER)
        # analog_tree.heading("Time", text="Time", anchor=CENTER)
        # analog_tree.heading("Name", text="Name", anchor=CENTER)
        # analog_tree.heading("Id", text="Id", anchor=CENTER)
        # analog_tree.heading("Name", text="Name", anchor=CENTER)
        # analog_tree.heading("Status", text="Status", anchor=CENTER)
        # analog_tree.heading("Desc", text="Desc", anchor=CENTER)
        # analog_tree.heading("Code", text="Code", anchor=CENTER)
        # analog_tree.place(x=10, y=100)
        
        
        reload_widget_button()
        reload_widget_tree()
    
app = Application()
    
        