from this import d
import pandas as pd
import xml.etree.ElementTree as et
from setting import Setting
import random
import datetime
import time
from setting import *

class Generator:

    def __init__(self) -> None:
        self.config_setting = Setting()
    
    def get_generate_Data(self) -> dict:
        current_time = datetime.datetime.now()
        dict_child = {}
        dict_child["id"] = " "
        dict_child["date"] = f"{current_time.day}/{current_time.month}/{current_time.year}"
        dict_child["time"] = f"{current_time.hour}:{current_time.minute}:{current_time.second}"
        dict_child["quantity_rain"] = str(random.randint(-20, 140))
        dict_child["quantity_water"] = str(random.randint(10, 50))
        dict_child["temperature"] = str(random.randint(15, 40))
        dict_child["humidity"] = str(random.randint(20, 80))
        dict_child["hardware_fail"] = str(random.randint(0,1))
        return dict_child