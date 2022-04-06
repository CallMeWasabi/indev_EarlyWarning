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
        self.alarm_historical_data = []
        self.alarm_data = []
        self.tree_station = []
        self.iid = 0
        self.tree_analog = None
        self.show_tree_analog = []
        self.error_point = []
        self.iid_station = 0
        
    def get_time(self):
        current_time = datetime.datetime.now()
        return current_time
    
    def get_data(self) -> dict:
        generate_data = self.generate.get_generate_Data()
        self.ManageGraphData(generate_data)
        self.tree_analog = generate_data
        self.findError()
        if generate_data["hardware_fail"] == "1":
            self.ManageErrorStation(generate_data)

        return generate_data    
    
    def get_iid(self):
        value = self.iid
        self.iid += 1
        return value
    
    def get_iid_station(self):
        value = self.iid_station
        self.iid_station += 1
        return value
    
    def get_graphData(self):
        return self.graph_data
    
    def get_historicalData(self):
        return self.alarm_historical_data
    
    def get_tree_station(self):
        
        def id_stamp():
            for i in range(len(self.tree_station)):
                self.tree_station[i][0] = str(i+1)
        id_stamp()
        return self.tree_station
    
    def ManageErrorStation(self, generate_data):
        list_pre = []
        list_pre.append(" ")
        list_pre.append(generate_data["date"])
        list_pre.append(generate_data["time"])
        list_pre.append("hardware fail")
        list_pre.append(" ")
        list_pre.append(" ")
        list_pre.append(" ")
        if len(self.tree_station) > 20:
            self.tree_station.pop()
        else:
            self.tree_station.insert(0, list_pre)
        
        
    
    def findError(self):
        if  len(self.error_point) == 0:
            for key in self.keys_data:
                if self.tree_analog[key] <= self.setting.dict_setting[f"min_{key}"]:
                    self.show_tree_analog.insert(0, [
                        self.tree_analog["date"],
                        self.tree_analog["time"],
                        " ",
                        key,
                        "Lower the limit",
                        " ",
                        " "
                    ])
                    self.ManageListShowTree()
                    self.ManageHistoricalData(self.show_tree_analog[0])
                    self.error_point.insert(0, key)
                elif self.tree_analog[key] >= self.setting.dict_setting[f"max_{key}"]:
                    self.show_tree_analog.insert(0, [
                        self.tree_analog["date"],
                        self.tree_analog["time"],
                        " ",
                        key,
                        "Higher the limit",
                        " ",
                        " "
                    ])
                    self.ManageListShowTree()
                    self.ManageHistoricalData(self.show_tree_analog[0])
                    self.error_point.insert(0, key)
            self.set_id()
            
        elif len(self.error_point) != 0:
            for i in range(len(self.error_point)):
                if self.tree_analog[self.error_point[i]] > self.setting.dict_setting[f"min_{self.error_point[i]}"] and self.tree_analog[self.error_point[i]] < self.setting.dict_setting[f"max_{self.error_point[i]}"]:
                    self.show_tree_analog.insert(0, [
                        self.tree_analog["date"],
                        self.tree_analog["time"],
                        " ",
                        self.error_point[i],
                        "Normal",
                        " ",
                        " "
                    ])
                    self.ManageListShowTree()
            self.error_point = []
            for key in self.keys_data:
                if self.tree_analog[key] <= self.setting.dict_setting[f"min_{key}"]:
                    self.show_tree_analog.insert(0, [
                        self.tree_analog["date"],
                        self.tree_analog["time"],
                        " ",
                        key,
                        "Lower the limit",
                        " ",
                        " "
                    ])
                    self.ManageListShowTree()
                    self.ManageHistoricalData(self.show_tree_analog[0])
                    self.error_point.insert(0, key)
                elif self.tree_analog[key] >= self.setting.dict_setting[f"max_{key}"]:
                    self.show_tree_analog.insert(0, [
                        self.tree_analog["date"],
                        self.tree_analog["time"],
                        " ",
                        key,
                        "Higher the limit",
                        " ",
                        " "
                    ])
                    self.ManageListShowTree()
                    self.ManageHistoricalData(self.show_tree_analog[0])
                    self.error_point.insert(0, key)
            self.set_id()
            
    def set_id(self):
        id = 1
        for i in range(len(self.show_tree_analog)):
            self.show_tree_analog[i][2] = id
            id += 1

    def ManageListShowTree(self):
        if len(self.show_tree_analog) > 20:
            self.show_tree_analog.pop()
    
    def ManageGraphData(self, generate_data):
        if len(self.graph_data) < 8640:
            self.graph_data.append(generate_data)
        elif len(self.graph_data) >= 8640:
            self.graph_data.remove(self.graph_data[0])
            self.graph_data.append(generate_data)
    
    def ManageHistoricalData(self, generate_data):
        if len(self.alarm_historical_data) < 10000:
            self.alarm_historical_data.insert(0, generate_data)
        
        elif len(self.alarm_historical_data) >= 10000:
            current_time = datetime.datetime.now()
            filename = f"Historical_data/alarm_log-{current_time.day}-{current_time.month}-{current_time.year}{self.config_setting.get_TypeFileSave()[0:len(self.config_setting.get_TypeFileSave())-1]}"
            for i in range(len(self.alarm_historical_data)):
                self.alarm_historical_data[i][2] = self.get_iid()
            dataframe_historical = pd.DataFrame(self.alarm_historical_data[50:10000])
            dataframe_historical.set_index("id", inplace=True)
            self.alarm_historical_data = self.alarm_historical_data[0:50]
            if self.config_setting.get_TypeFileSave() == ".csv\n":
                dataframe_historical.to_csv(filename)
