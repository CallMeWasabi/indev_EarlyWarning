from email.mime import message
from socket import AI_PASSIVE
from tkinter import *
from tkinter import ttk
from winsound import MessageBeep
from pyparsing import col
from DataProvider import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import messagebox


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
        self.setting = Setting()
        self.provider = Provider()
        self.cout_tree_analog = 0
        
        self.window = Tk()
        self.window.title("EarlyWarning")
        self.window.iconbitmap("img\\rain.ico")
        self.window.geometry("1024x600")
        self.window.resizable(False, False)
        
        my_notebook = ttk.Notebook(self.window)
        my_notebook.pack()
        
        self.frame_page1 = Frame(my_notebook, width=1024, height=600)
        self.frame_page2 = Frame(my_notebook, width=1024, height=600)
        self.frame_page3 = Frame(my_notebook, width=1024, height=600)
        self.frame_setting = Frame(my_notebook, width=1024, height=600)
        
        self.frame_page1.bind("FocusIn", self.Defocus)
        
        my_notebook.add(self.frame_page1, text="Show Data")
        my_notebook.add(self.frame_page2, text="Historical Data")
        my_notebook.add(self.frame_page3, text="Alarm Station")
        my_notebook.add(self.frame_setting, text="Setting")
        
        self.frame_page1_widget = LabelFrame(self.frame_page1)
        self.frame_page1_widget.pack(fill="both", expand=1, padx=10, pady=10)
        self.renderWidget_page1()
        self.renderWidget_page2()
        self.renderWidget_page3()
        self.renderWidget_setting()
        
        self.window.mainloop()

    def Defocus(self, event):
        event.widget.master.focus_set()
    
    def renderWidget_page1(self) -> None:
         
        def reload_widget_tree():
            
            for i in range(0, len(self.provider.show_tree_analog)):
                analog_tree.item(i, value=(self.provider.show_tree_analog[i]))
            analog_tree.after(5000, reload_widget_tree)
            

        def reload_widget_button():
            dict_data = self.provider.get_data()
            button_date.config(text=dict_data["date"])
            button_time.config(text=dict_data["time"])
            button_quantity_rain.config(text=dict_data["quantity_rain"])
            button_quantity_water.config(text=dict_data["quantity_water"])
            button_temperature.config(text=dict_data["temperature"])
            button_humidity.config(text=dict_data["humidity"])
            button_date.after(5000, reload_widget_button)
            
        
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
        
        button_date.bind("<FocusIn>", self.Defocus)
        button_time.bind("<FocusIn>", self.Defocus)
        button_quantity_rain.bind("<FocusIn>", self.Defocus)
        button_quantity_water.bind("<FocusIn>", self.Defocus)
        button_temperature.bind("<FocusIn>", self.Defocus)
        button_humidity.bind("<FocusIn>", self.Defocus)
        
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
        analog_tree.heading("Status", text="Status", anchor=CENTER)
        analog_tree.heading("Desc", text="Desc", anchor=CENTER)
        analog_tree.heading("Code", text="Code", anchor=CENTER)
        analog_tree.place(x=10, y=100)
        
        for i in range(0, 20):
            analog_tree.insert("", "end", iid=i, values=(" ", " ", " ", " ", " ", " ", " "))
        
        reload_widget_button()
        reload_widget_tree()
    
    
    def renderWidget_page2(self):
        dict_keyWord = {
            "quantity_rain_ylabel":"Quantity rain(millimater)",
            "quantity_rain_title":"Graph quantity rain",
            "quantity_rain_label":"Quantity rain",
            "quantity_water_ylabel":"Quantity water(meters)",
            "quantity_water_title":"Graph quantity water",
            "quantity_water_label":"Quantity water",
            "temperature_ylabel":"Temperature(Celsius)",
            "temperature_title":"Graph temperature",
            "temperature_label":"Temperature",
            "humidity_ylabel":"Humidity(percent)",
            "humidity_title":"Graph humidity",
            "humidity_label":"Humidity"
        }
    
        def setValueGraph_quantity_rain():
            nameGraph_var = "quantity_rain"
            renderGraph(nameGraph_var)
        
        def setValueGraph_quantity_water():
            nameGraph_var = "quantity_water"
            renderGraph(nameGraph_var)
            
        def setValueGraph_temperature():
            nameGraph_var = "temperature"
            renderGraph(nameGraph_var)
            
        def setValueGraph_humidity():
            nameGraph_var = "humidity"
            renderGraph(nameGraph_var)
            
        def renderGraph(name_request):
            
            def createGraph():
                
                def goBack():
                    Button_disable.destroy()
                    get_widz.destroy()
                    labelFrame_graph.destroy()
                    self.renderWidget_page2()
                
                Button_disable = Button(self.frame_page2, text="Disable graph", command=goBack)
                Button_disable.pack(pady=5)
                labelFrame_graph = LabelFrame(self.frame_page2, text="Graph")
                labelFrame_graph.pack(fill="both", expand="yes", padx=10, pady=10)
                
                graph_data = self.provider.get_graphData()
                if len(graph_data) == 0:
                    
                    def destroy():
                        label_alert.destroy()
                    
                    label_alert = Label(self.frame_page2, text="Don't have data", font=("Ubuntu", 15))
                    label_alert.pack()
                    label_alert.after(2000, destroy)
                
                elif len(graph_data) > 0:
                    for i in range(len(graph_data)):
                        x_data.append(graph_data[i]["time"])
                        y_data.append(int(graph_data[i][name_request]))
                
                    fig = plt.figure(figsize=(10, 6), dpi=100)
                    plot1 = fig.add_subplot(111)
                    plot1.plot(x_data, y_data, marker="", color="blue", label=dict_keyWord[f"{name_request}_label"])
                    plot1.set_xlabel("Time")
                    plot1.set_ylabel(dict_keyWord[f"{name_request}_ylabel"])
                    plot1.set_title(dict_keyWord[f"{name_request}_title"])
                    plot1.set_xticks([graph_data[0]["time"], graph_data[len(graph_data)-1]["time"]])
                    plot1.legend(loc=2)
                    plot1.grid()
                    canv = FigureCanvasTkAgg(fig, master=labelFrame_graph)
                    canv.draw()
                    get_widz = canv.get_tk_widget()
                    get_widz.pack()
                    
            
            x_data = []
            y_data = []
            
            
            Button_graph_quantity_rain.destroy()
            Button_graph_quantity_water.destroy()
            Button_graph_quantity_temperature.destroy()
            Button_graph_quantity_humidity.destroy()
            Label_read.destroy()
            
            createGraph()    
        
        Button_graph_quantity_rain = Button(self.frame_page2, text="Show graph quantity rain", command=setValueGraph_quantity_rain)
        Button_graph_quantity_rain.bind("<FocusIn>", self.Defocus)
        Button_graph_quantity_rain.place(x=200, y=20)
        Button_graph_quantity_water = Button(self.frame_page2, text="Show graph quantity water", command=setValueGraph_quantity_water)
        Button_graph_quantity_water.bind("<FocusIn>", self.Defocus)
        Button_graph_quantity_water.place(x=350, y=20)
        Button_graph_quantity_temperature = Button(self.frame_page2, text="Show graph temperature", command=setValueGraph_temperature)
        Button_graph_quantity_temperature.bind("<FocusIn>", self.Defocus)
        Button_graph_quantity_temperature.place(x=510, y=20)
        Button_graph_quantity_humidity = Button(self.frame_page2, text="Show graph humidity", command=setValueGraph_humidity)
        Button_graph_quantity_humidity.bind("<FocusIn>", self.Defocus)
        Button_graph_quantity_humidity.place(x=660, y=20)
        Label_read = Label(self.frame_page2,text=f"read file {self.setting.TypeFile}", font=("Ubuntu", 14))
        Label_read.place(x=800, y=500)
        
    def renderWidget_page3(self):
        
        def reload_widget_station():
            list_data = self.provider.get_tree_station()
            for i in range(0, len(list_data)):
                station_tree.item(i, value=(list_data[i]))
            
            station_tree.after(2000, reload_widget_station)
        
        station_tree = ttk.Treeview(self.frame_page3, height=26)
        station_tree["column"] = ("Id", "Date", "Time", "Status", "Station name", "Code", "Desc")
        
        station_tree.column("#0", width=20, minwidth=25)
        station_tree.column("Id", anchor=CENTER, width=50)
        station_tree.column("Date", anchor=CENTER, width=120)
        station_tree.column("Time", anchor=CENTER, width=120)
        station_tree.column("Status", anchor=W, width=150)
        station_tree.column("Station name", anchor=W, width=180)
        station_tree.column("Code", anchor=W, width=160)
        station_tree.column("Desc", anchor=W, width=200)
        
        station_tree.heading("#0", text="", anchor=CENTER)
        station_tree.heading("Id", text="Id",anchor=CENTER)
        station_tree.heading("Date", text="Date",anchor=CENTER)
        station_tree.heading("Time", text="Time",anchor=CENTER)
        station_tree.heading("Status", text="Status",anchor=CENTER)
        station_tree.heading("Station name", text="Station name",anchor=CENTER)
        station_tree.heading("Code", text="Code",anchor=CENTER)
        station_tree.heading("Desc", text="Desc",anchor=CENTER)
        station_tree.place(x=10, y=10)
        
        for i in range(0, 20):
            station_tree.insert("", "end", iid=i, value=(" ", " ", " ", " ", " ", " ", " "))
        
        reload_widget_station()
        
        
    def renderWidget_setting(self):
        
        # variable
        var_typefile = StringVar()
        var_typefile_save = StringVar()
        var_min_quantity_rain = StringVar()
        var_max_quantity_rain = StringVar()
        var_min_quantity_water = StringVar()
        var_max_quantity_water = StringVar()
        var_min_temperature = StringVar()
        var_max_temperature = StringVar()
        var_min_humidity = StringVar()
        var_max_humidity = StringVar()
        
        def message_confirm():
            
            def get_log_setting(dict_var_setting):
                list_log_setting = []
                current_time = self.provider.get_time()
                list_log_setting.append(f"Change Setting Date : {current_time.day}/{current_time.month}/{current_time.year} | Time : {current_time.hour}:{current_time.minute}:{current_time.second} \n Info : \n")
                for i in self.setting.keys_setting:
                    if i != "id_historical_alarm":
                        list_log_setting.append(f"          {i} : {self.setting.dict_setting[i]} change to -> {dict_var_setting[i]} \n")
            
            
            response_message = messagebox.askyesno(title="Confirm", message="Confirm change settings ?")
            if response_message == 1:
                dict_var_setting = {}
                var_typefile = cmb_typefile.get()
                var_typefile_save = cmb_typefile_save.get()
                var_min_quantity_rain = entry_min_quantity_rain.get()
                var_max_quantity_rain = entry_max_quantity_rain.get()
                var_min_quantity_water = entry_min_quantity_water.get()
                var_max_quantity_water = entry_max_quantity_water.get()
                var_min_temperature = entry_min_temperature.get()
                var_max_temperature = entry_max_temperature.get()
                var_min_humidity = entry_min_humidity.get()
                var_max_humidity = entry_max_humidity.get()
                
                dict_var_setting["type_file"] = var_typefile
                dict_var_setting["type_file_save"] = var_typefile_save
                dict_var_setting["min_quantity_rain"] = var_min_quantity_rain
                dict_var_setting["max_quantity_rain"] = var_max_quantity_rain
                dict_var_setting["min_quantity_water"] = var_min_quantity_water
                dict_var_setting["max_quantity_water"] = var_max_quantity_water
                dict_var_setting["min_temperature"] = var_min_temperature
                dict_var_setting["max_temperature"] = var_max_temperature
                dict_var_setting["min_humidity"] = var_min_humidity
                dict_var_setting["max_humidity"] = var_max_humidity
                
                get_log_setting(dict_var_setting)
        
                try:
                    with open("EarlyWarningSetting/save_preset", "w") as f:
                        for key in self.provider.keys_data:
                            if key != "id_historical_alarm":
                                f.write(f"{key}={dict_var_setting[key]}")
                                f.write("\n")
                            elif key == "id_historical_alarm":
                                f.write(f"{key}={self.setting.id_historical}")
                                f.write("\n")
                                self.setting.set_dict_setting(dict_var_setting)
                                
                except FileNotFoundError:
                    with open("EarlyWarningSetting/save_preset", "w") as f:
                        for key in self.provider.keys_data:
                            if key != "id_historical_alarm":
                                f.write(f"{key}={dict_var_setting[key]}")
                                f.write("\n")
                            elif key == "id_historical_alarm":
                                f.write(f"{key}={self.setting.id_historical}")
                                f.write("\n")
                                self.setting.set_dict_setting(dict_var_setting)
                                
                                
        label_typefile = Label(self.frame_setting, text="Typefile", font=("Ubuntu", 10))
        label_typefile.place(x=20, y=20)
        list_typefile = [".xml", ".json"]
        list_typefile_save = [".csv", "json"]
        cmb_typefile = ttk.Combobox(self.frame_setting, value=list_typefile, width=10)
        cmb_typefile.current(0)
        cmb_typefile.bind("<FocusIn>", self.Defocus)
        cmb_typefile.place(x=80, y=20)
        label_typefile_save = Label(self.frame_setting, text="Typefile save for alarm log", font=("Ubuntu", 10))
        label_typefile_save.place(x=20, y=50)
        cmb_typefile_save = ttk.Combobox(self.frame_setting, values=list_typefile_save, width=10)
        cmb_typefile_save.current(0)
        cmb_typefile_save.bind("<FocusIn>", self.Defocus)
        cmb_typefile_save.place(x=190, y=50)
        
        label_min_quantity_rain = Label(self.frame_setting, font=("Ubuntu", 10), text="Min quantity rain")
        label_max_quantity_rain = Label(self.frame_setting, font=("Ubuntu", 10), text="Max quantity rain")
        label_min_quantity_water = Label(self.frame_setting, font=("Ubuntu", 10), text="Min quantity water")
        label_max_quantity_water = Label(self.frame_setting, font=("Ubuntu", 10), text="Max quantity water")
        
        entry_min_quantity_rain = Entry(self.frame_setting)
        entry_max_quantity_rain = Entry(self.frame_setting)
        entry_min_quantity_water = Entry(self.frame_setting)
        entry_max_quantity_water = Entry(self.frame_setting)
        entry_min_quantity_rain.insert()
        entry_max_quantity_rain.insert()
        entry_min_quantity_water.insert()
        entry_max_quantity_water.insert()
        
        
        
        label_min_quantity_rain.place(x=300, y=20)
        label_max_quantity_rain.place(x=300, y=50)
        label_min_quantity_water.place(x=300, y=80)
        label_max_quantity_water.place(x=300, y=110)
        
        entry_min_quantity_rain.place(x=430, y=20)
        entry_max_quantity_rain.place(x=430, y=50)
        entry_min_quantity_water.place(x=430, y=80)
        entry_max_quantity_water.place(x=430, y=110)
        
        label_min_temperature = Label(self.frame_setting, font=("Ubuntu", 10), text="Min temperature")
        label_max_temperature = Label(self.frame_setting, font=("Ubuntu", 10), text="Max temperature")
        label_min_humidity = Label(self.frame_setting, font=("Ubuntu", 10), text="Min humidity")
        label_max_humidity = Label(self.frame_setting, font=("Ubuntu", 10), text="Max humidity")
        
        entry_min_temperature = Entry(self.frame_setting)
        entry_max_temperature = Entry(self.frame_setting)
        entry_min_humidity = Entry(self.frame_setting)
        entry_max_humidity = Entry(self.frame_setting)
        
        label_min_temperature.place(x=580, y=20)
        label_max_temperature.place(x=580, y=50)
        label_min_humidity.place(x=580, y=80)
        label_max_humidity.place(x=580, y=110)
        
        entry_min_temperature.place(x=700, y=20)
        entry_max_temperature.place(x=700, y=50)
        entry_min_humidity.place(x=700, y=80)
        entry_max_humidity.place(x=700, y=110)
        

        
        
        button_apply = Button(self.frame_setting, text="Apply", font=("Ubuntu", 12), command=message_confirm)
        button_apply.pack(anchor="e", side="bottom", padx=20, pady=20)
        
if __name__ == "__main__":
    app = Application()     