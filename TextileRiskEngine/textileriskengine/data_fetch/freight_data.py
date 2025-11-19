import requests
import pandas as pd

FBX_URL = "https://fbx.freightos.com/api/latest"

ROUTES = [
    ("China", "Southeast Asia"),
    ("China", "West Africa"),
]

def run():
    res = requests.get(FBX_URL)
    data = res.json()

    df = pd.DataFrame(data["results"])

    df.to_csv("data/raw/freight_data.csv", index=False)
    print("Freight data saved → data/raw/freight_data.csv")

if __name__ == "__main__":
    run()
