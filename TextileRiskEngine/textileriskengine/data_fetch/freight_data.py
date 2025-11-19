import requests
from pathlib import Path
import pandas as pd

# 当前文件：TextileRiskEngine/textileriskengine/data_fetch/xxx.py
PROJECT_ROOT = Path(__file__).resolve().parents[2]   # 回到 TextileRiskEngine/
RAW_DIR = PROJECT_ROOT / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

FBX_URL = "https://fbx.freightos.com/api/latest"

ROUTES = [
    ("China", "Southeast Asia"),
    ("China", "West Africa"),
]

def run():
    res = requests.get(FBX_URL)
    data = res.json()

    df = pd.DataFrame(data["results"])

    df.to_csv(RAW_DIR / "freight_data.csv", index=False)
    print("Freight data saved → data/raw/freight_data.csv")

if __name__ == "__main__":
    run()
