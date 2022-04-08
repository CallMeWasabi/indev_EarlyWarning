import json
data = [["Ongsa", "16", "170"], ["Heng", "16", "175"], ["Eugene", "16", "180"]]
with open("j.json", "r") as f:
    data = json.load(f)
    print(data)