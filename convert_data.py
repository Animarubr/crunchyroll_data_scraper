import pandas as pd
import json


def create_csv(data):
    df = pd.DataFrame(data)
    df.to_csv("data.csv", index=False)
    
    
if __name__ in "__main__":
    with open("data.json", "r", encoding="utf-8") as file:
        data = json.loads(file.read())
    
    create_csv(data["data"])
    