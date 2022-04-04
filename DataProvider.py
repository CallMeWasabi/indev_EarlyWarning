from generator import *
import pandas as pd
import datetime
from setting import * 
import time

class Provider:
    def __init__(self) -> None:
        
        self.setting = Setting()
        self.generate = Generator()
        self.keys_data = ["quantity_rain", "quantity_water", "temperature", "humidity"]
        self.graph_data = []
        self.historical_data = []
        self.alarm_data = []
        self.iid = 0
        self.list_tree = None
        self.list_show_tree = []
        self.error_point = []
        
    def get_time(self):
        current_time = datetime.datetime.now()
        return current_time
    
    def get_data(self) -> dict:
        generate_data = self.generate.get_generate_Data()
        self.ManageHistoricalData(generate_data)
        self.ManageGraphData(generate_data)
        self.list_tree = generate_data
        self.findError()
        return generate_data    
    
    def get_iid(self):
        value = self.iid
        self.iid += 1
        return value
    
    def get_graphData(self):
        return self.graph_data
    
    def get_historicalData(self):
        return self.historical_data
    
    def ManageListShowTree(self):
        if len(self.list_show_tree) <= 20:
            pass
        elif len(self.list_show_tree) > 20:
            self.list_show_tree.pop()
    
    def findError(self):
        if  len(self.error_point) == 0:
            for key in self.keys_data:
                if self.list_tree[key] <= self.setting.dict_setting[f"min_{key}"]:
                    self.list_show_tree.insert(0, [
                        self.list_tree["date"],
                        self.list_tree["time"],
                        " ",
                        key,
                        "Lower the limit",
                        " ",
                        " "
                    ])
                    self.ManageListShowTree()
                    self.error_point.insert(0, key)
                elif self.list_tree[key] >= self.setting.dict_setting[f"max_{key}"]:
                    self.list_show_tree.insert(0, [
                        self.list_tree["date"],
                        self.list_tree["time"],
                        " ",
                        key,
                        "Higher the limit",
                        " ",
                        " "
                    ])
                    self.ManageListShowTree()
                    self.error_point.insert(0, key)
            self.set_id()
            
        elif len(self.error_point) != 0:
            for i in range(len(self.error_point)):
                if self.list_tree[self.error_point[i]] > self.setting.dict_setting[f"min_{self.error_point[i]}"] and self.list_tree[self.error_point[i]] < self.setting.dict_setting[f"max_{self.error_point[i]}"]:
                    self.list_show_tree.insert(0, [
                        self.list_tree["date"],
                        self.list_tree["time"],
                        " ",
                        self.error_point[i],
                        "Normal",
                        " ",
                        " "
                    ])
                    self.ManageListShowTree()
            self.error_point = []
            for key in self.keys_data:
                if self.list_tree[key] <= self.setting.dict_setting[f"min_{key}"]:
                    self.list_show_tree.insert(0, [
                        self.list_tree["date"],
                        self.list_tree["time"],
                        " ",
                        key,
                        "Lower the limit",
                        " ",
                        " "
                    ])
                    self.ManageListShowTree()
                    self.error_point.insert(0, key)
                elif self.list_tree[key] >= self.setting.dict_setting[f"max_{key}"]:
                    self.list_show_tree.insert(0, [
                        self.list_tree["date"],
                        self.list_tree["time"],
                        " ",
                        key,
                        "Higher the limit",
                        " ",
                        " "
                    ])
                    self.ManageListShowTree()
                    self.error_point.insert(0, key)
            self.set_id()
            
    def set_id(self):
        id = 1
        for i in range(len(self.list_show_tree)):
            self.list_show_tree[i][2] = id
            id += 1

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