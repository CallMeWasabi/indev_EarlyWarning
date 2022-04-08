from logging.config import dictConfig
import os
from pathlib import Path

class Setting:
    def __init__(self) -> None:
        self.decision = 0
        self.TypeFile = None
        self.TypeFileSave = None
        self.PathAppSetting= "EarlyWarningSetting/AppSetting.txt"
        self.dict_setting = {}
        self.id_historical = None
        self.keys_setting = ["type_file",
                             "type_file_save",
                             "id_historical_alarm",
                             "min_quantity_rain",
                             "max_quantity_rain",
                             "min_quantity_water",
                             "max_quantity_water",
                             "min_temperature",
                             "max_temperature",
                             "min_humidity",
                             "max_humidity"]
         
        self.load_appSetting()
        print("Load Setting Complete")


    def set_ConfigAndWriteFile(self):
        with open(self.PathAppSetting, "w") as f:
            list_lines = []
            for key in self.keys_setting:
                list_lines.append(f"{key}={self.dict_setting[key]}\n")
            f.writelines(list_lines)
            
    
    def set_SettingToDefault(self):
            with open(self.PathAppSetting, "w") as f:
                list_value = [".xml", ".csv", 0, 0, 100, 20, 40, 20, 35, 20, 60]
                list_lines = []
                i = 0
                for key in self.keys_setting:
                    if key == "type_file":
                        self.TypeFile = list_value[i]
                        self.dict_setting[key] = list_value[i]
                    elif key == "type_file_save":
                        self.TypeFileSave = list_value[i]
                        self.dict_setting[key] = list_value[i]
                    elif key == "id_historical_alarm":
                        self.id_historical = list_value[i]
                        self.dict_setting[key] = list_value[i]
                    else:
                        self.dict_setting[key] = list_value[i]
                        
                    list_lines.append(f"{key}={list_value[i]}\n")
                    i += 1
                f.writelines(list_lines)


    def create_FileAppSetting(self):
        parent_dir = str(os.getcwd())
        try:
            os.mkdir(parent_dir+"/EarlyWarningSetting")
            self.set_SettingToDefault()
        except FileExistsError:
            dir_name = Path(parent_dir+"/EarlyWarningSetting")
            dir_name.rmdir()
            os.mkdir(parent_dir+"/EarlyWarningSetting")
            self.set_SettingToDefault()
    
    def saveLogSetting(self, list_info):
        try:
            with open("log/log_setting", "a") as f:
                f.writelines(list_info)
        except FileNotFoundError:
            with open("log/log_setting", "w") as f:
                f.writelines(list_info)
    
    
    def load_appSetting(self):
        try:
            with open(self.PathAppSetting, "r") as f:
                for line in f:
                    try:
                        (key, value) = line.split("=")
                        value = value[0:len(value)-1]
                        if key == "type_file":
                            self.TypeFile = value
                            self.dict_setting[key] = value
                        elif key == "type_file_save":
                            self.TypeFileSave = value
                            self.dict_setting[key] = value
                        elif key == "id_historical_alarm":
                            self.id_historical = value
                            self.dict_setting[key] = value
                        else:
                            self.dict_setting[key] = value
                    
                    except IndentationError:
                        self.create_FileAppSetting()    
        except FileNotFoundError:
            self.create_FileAppSetting()
    
    def get_TypeFile(self):
        return self.TypeFile

    def get_dictSetting(self):
        return self.dict_setting
    
    def get_TypeFileSave(self):
        return self.TypeFileSave
    
    def get_id_historical(self):
        value = self.id_historical
        self.id_historical = str(int(self.id_historical) + 1)
        self.dict_setting["id_historical_alarm"] = self.id_historical
        self.set_ConfigAndWriteFile()
        return value

    def set_dict_setting(self, dict_new_setting):
        for key in self.keys_setting:
            if key != "id_historical_alarm":
                self.dict_setting[key] = dict_new_setting[key]
            elif key == "id_historical_alarm":
                self.dict_setting[key] = self.id_historical
        print(self.dict_setting)