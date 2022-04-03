from re import S
from generator import *
import pandas as pd
import datetime
from setting import * 
import time

class Provider:
    def __init__(self) -> None:
        self.config_setting = Setting()
        self.generate = Generator()
        self.historical_data = []
        self.alarm_data = []
        
    def get_data(self) -> dict:
        generate_data = self.generate.get_generate_Data()
        self.ManageHistoricalData(generate_data)
        return generate_data 
    
    def ManageHistoricalData(self, generate_data):
        if len(self.historical_data) < 10000:
            self.historical_data.insert(0, generate_data)
        
        elif len(self.historical_data) > 10000:
            current_time = datetime.datetime.now()
            filename = f"alarm_log-{current_time.day}-{current_time.month}-{current_time.year}.{self.config_setting.get_TypeFileSave()}"
            dataframe_historical = pd.DataFrame(self.historical_data[100:10000])
            self.historical_data = self.historical_data[0:100]
            dataframe_historical.set_index("id", inplace=True)
            dataframe_historical.to_csv(filename)
            
