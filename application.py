from socket import AI_PASSIVE
from tkinter import *
from tkinter import ttk
from DataProvider import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)



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
        self.renderWidget_page2()
        
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
            for i in range(0, len(self.provider.list_show_tree)):
                analog_tree.insert(parent="", index="end", iid=self.provider.get_iid(), value=(self.provider.list_show_tree[i]))

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
            
            def goBack():
                Button_disable.destroy()
                labelFrame_graph.destroy()
                self.renderWidget_page2()
            
            def createGraph():
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
            
            
            Button_disable = Button(self.frame_page2, text="Disable graph", command=goBack)
            Button_disable.pack(pady=5)
            labelFrame_graph = LabelFrame(self.frame_page2, text="Graph")
            labelFrame_graph.pack(fill="both", expand="yes", padx=10, pady=10)
            
            createGraph()    
        
        Button_graph_quantity_rain = Button(self.frame_page2, text="Show graph quantity rain", command=setValueGraph_quantity_rain)
        Button_graph_quantity_rain.place(x=200, y=20)
        Button_graph_quantity_water = Button(self.frame_page2, text="Show graph quantity water", command=setValueGraph_quantity_water)
        Button_graph_quantity_water.place(x=350, y=20)
        Button_graph_quantity_temperature = Button(self.frame_page2, text="Show graph temperature", command=setValueGraph_temperature)
        Button_graph_quantity_temperature.place(x=510, y=20)
        Button_graph_quantity_humidity = Button(self.frame_page2, text="Show graph humidity", command=setValueGraph_humidity)
        Button_graph_quantity_humidity.place(x=660, y=20)
        Label_read = Label(self.frame_page2,text=f"read file {self.setting.TypeFile}", font=("Ubuntu", 14))
        Label_read.place(x=800, y=500)
        
        
        
app = Application()
    
        