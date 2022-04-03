from generator import *
import pandas as pd
import datetime
from setting import * 
import time

class Provider:
    def __init__(self) -> None:
        
        self.config_setting = Setting()
        self.generate = Generator()
        self.keys_data = ["quantity_rain", "quantity_water", "temperature", "humidity"]
        self.graph_data = []
        self.historical_data = []
        self.alarm_data = []
        self.iid = 10
        self.list_tree = []
        self.error_point = []
        
    def get_time(self):
        current_time = datetime.datetime.now()
        return current_time
    
    def get_data(self) -> dict:
        generate_data = self.generate.get_generate_Data()
        self.ManageHistoricalData(generate_data)
        self.ManageGraphData(generate_data)
        self.ManageListTree(generate_data)
        return generate_data    
    
    def get_iid(self):
        value = self.iid
        self.iid -= 1
        return value
    
    def get_graphData(self):
        return self.graph_data
    
    def get_historicalData(self):
        return self.historical_data
    
    def ManageGraphData(self, generate_data):
        if len(self.graph_data) < 8640:
            self.graph_data.append(generate_data)
        elif len(self.graph_data) >= 8640:
            self.graph_data.remove(self.graph_data[0])
            self.graph_data.append(generate_data)
    
    def ManageHistoricalData(self, generate_data):
        if len(self.historical_data) < 10000:
            self.historical_data.insert(0, generate_data)
        
        elif len(self.historical_data) >= 10000:
            current_time = datetime.datetime.now()
            filename = f"Historical_data/alarm_log-{current_time.day}-{current_time.month}-{current_time.year}{self.config_setting.get_TypeFileSave()[0:len(self.config_setting.get_TypeFileSave())-1]}"
            print(filename)
            dataframe_historical = pd.DataFrame(self.historical_data[50:10000])
            dataframe_historical.set_index("id", inplace=True)
            self.historical_data = self.historical_data[0:50]
            if self.config_setting.get_TypeFileSave() == ".csv\n":
                dataframe_historical.to_csv(filename)

    def create_tree(self):
        pass