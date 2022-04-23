from operator import index
from matplotlib.font_manager import json_dump
from generator import *
import pandas as pd
import datetime
from setting import * 
import time
import json

class Provider:
    def __init__(self) -> None:
        
        self.setting = Setting()
        self.generate = Generator()
        self.keys_data = ["quantity_rain", "quantity_water", "temperature", "humidity"]
        self.keys_historical = ["id", "date", "time", "quantity_rain", "quantity_water", "temperature", "humidity"]
        self.graph_data = []
        self.alarm_historical_data = []
        self.alarm_data = []
        self.tree_station = []
        self.iid = 0
        self.tree_analog = None
        self.show_tree_analog = []
        self.error_point = []
        self.iid_station = 0
        self.limitRenderGraph = 0
        
        self.LoadHistoricalData()
        
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
        if len(self.tree_station) == 20:
            self.tree_station.pop()
            self.tree_station.insert(0, list_pre)
        else:
            self.tree_station.insert(0, list_pre)
        
        
    
    def findError(self):
        self.setting.load_appSetting()
        if  len(self.error_point) == 0:
            for key in self.keys_data:
                if int(self.tree_analog[key]) <= int(self.setting.dict_setting[f"min_{key}"]):
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
                elif int(self.tree_analog[key]) >= int(self.setting.dict_setting[f"max_{key}"]):
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
                if int(self.tree_analog[self.error_point[i]]) > int(self.setting.dict_setting[f"min_{self.error_point[i]}"]) and int(self.tree_analog[self.error_point[i]]) < int(self.setting.dict_setting[f"max_{self.error_point[i]}"]):
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
                if int(self.tree_analog[key]) <= int(self.setting.dict_setting[f"min_{key}"]):
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
                elif int(self.tree_analog[key]) >= int(self.setting.dict_setting[f"max_{key}"]):
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
        if len(self.graph_data) < 10:
            self.graph_data.append(generate_data)
        elif len(self.graph_data) == 10:
            self.graph_data.remove(self.graph_data[0])
            self.graph_data.append(generate_data)
    
    def LoadHistoricalData(self):
        try:
            with open("data/historical_data.json", "r") as f:
                data = json.load(f)
                self.alarm_historical_data = data
                print("[LOGS] Load Historical Complete")
        except FileNotFoundError:
            pass
            
    def AutoSaveFile_AlarmHistorical(self):
            try:
                with open("data/historical_data.json", "w") as file_json:
                    json.dump(self.alarm_historical_data, file_json, indent=4)
            except FileNotFoundError:
                with open("data/historical_data.json", "w") as file_json:
                    json.dump(self.alarm_historical_data, file_json, indent=4)
    
    def ManageHistoricalData(self, generate_data):
                
        data_overlimit = generate_data
        data_overlimit[2] = " "
        if len(self.alarm_historical_data) < 10000:
            self.alarm_historical_data.append(data_overlimit)
            self.AutoSaveFile_AlarmHistorical()
        
        elif len(self.alarm_historical_data) == 10000:
            current_time = datetime.datetime.now()
            filename = f"Historical_data/alarm_log-{current_time.day}-{current_time.month}-{current_time.year}{self.setting.get_TypeFileSave()[0:len(self.setting.get_TypeFileSave())-1]}"
            for i in range(len(self.alarm_historical_data)):
                self.alarm_historical_data[i][2] = self.setting.get_id_historical()
            dataframe_historical = pd.DataFrame(self.alarm_historical_data[0:9950])
            dataframe_historical.set_index("id", inplace=True)
            self.alarm_historical_data = self.alarm_historical_data[9950:10000]
            if self.setting.get_TypeFileSave() == ".csv":
                dataframe_historical.to_csv(filename)
                print("[LOGS] Trans Historical data to csv complete")
