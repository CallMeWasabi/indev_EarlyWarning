class Setting:
    def __init__(self) -> None:
        self.TypeFile = None
        self.dict_setting = None
        self.keys_setting = ["type_file",
                             "min_quantity_rain",
                             "max_quantity_rain",
                             "min_quantity_water",
                             "max_quantity_water",
                             "min_temperature",
                             "max_temperature",
                             "min_humidity",
                             "max_humidity"]
        self.load_appSetting()

    def create_FileAppSetting(self):
        list_value = [".xml", 0, 100, 20, 40, 20, 35, 20, 60]
        list_lines = []
        i = 0
        for key in self.keys_setting:
            self.dict_setting[key] = list_value[i]
            list_lines.append(f"{key}={list_value[i]}")
            i += 1
        with open("EarlyWarningSetting/AppSetting.txt", "w") as f:
            f.writelines(list_lines)
            f.close()

    def load_appSetting(self):
        try:
            with open("EarlyWarningSetting/AppSetting.txt", "r") as f:
                for line in f:
                    (key, value) = line.split("=")
                    if key == "type_file":
                        self.TypeFile = value
                    else:
                        self.dict_setting[key] = value
        except FileNotFoundError:
            self.create_FileAppSetting()

    def get_TypeFile(self):
        return self.TypeFile