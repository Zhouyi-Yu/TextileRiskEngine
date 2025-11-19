import requests
import pandas as pd
from pathlib import Path
import time

# 当前文件：TextileRiskEngine/textileriskengine/data_fetch/xxx.py
PROJECT_ROOT = Path(__file__).resolve().parents[2]   # 回到 TextileRiskEngine/
RAW_DIR = PROJECT_ROOT / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


COMTRADE_URL = (
    "https://comtradeapi.un.org/public/v1/preview/"
    "flows?max=50000&type=C&freq=M&px=HS&ps=all&r={importer}&p=156&cc=50%2C51%2C52%2C53%2C54%2C55%2C56%2C57%2C58%2C59%2C60%2C61%2C62%2C63"
)

COUNTRIES = {
    "704": "Vietnam",
    "360": "Indonesia",
    "764": "Thailand",
    "608": "Philippines",
    "458": "Malaysia",
    "566": "Nigeria",
    "288": "Ghana",
    "384": "Cote_dIvoire",
    "686": "Senegal",
    "204": "Benin",
    "768": "Togo",
    "818": "Egypt",
    "116": "Cambodia",
}

def fetch_trade(iso_num):
    url = COMTRADE_URL.format(importer=iso_num)
    res = requests.get(url)
    try:
        df = pd.DataFrame(res.json()["data"])
        df["importer"] = iso_num
        return df
    except:
        print(f"Error fetching for {iso_num}")
        return pd.DataFrame()

def run():
    all_df = []
    for code in COUNTRIES.keys():
        print("Fetching trade for:", code)
        df = fetch_trade(code)
        if not df.empty:
            all_df.append(df)
        time.sleep(1)

    final = pd.concat(all_df, ignore_index=True)
    final.to_csv(RAW_DIR / "trade_data.csv", index=False)
    print("Trade data saved → data/raw/trade_data.csv")

if __name__ == "__main__":
    run()
