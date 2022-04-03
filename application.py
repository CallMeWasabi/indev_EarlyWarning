from socket import AI_PASSIVE
from tkinter import *
from tkinter import ttk
from DataProvider import *

class Application:
    
    def __init__(self) -> None:
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
        
        
        
        window.mainloop()

    def renderWidget_page1(self) -> None:
        
        def reload_widget_tree():
            pass
        
        
        def reload_widget_button():
            dict_data = self.provider.get_data()
            button_date.config(text=dict_data["date"])
            button_time.config(text=dict_data["time"])
            button_quantity_rain.config(text=dict_data["quantity_rain"])
            button_quantity_water.config(text=dict_data["quantity_water"])
            button_temperature.config(text=dict_data["temperature"])
            button_humidity.config(text=dict_data["humidity"])
            button_date.after(2000, reload_widget_button)
            
        
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
        
        
        
        
    
app = Application()
    
        