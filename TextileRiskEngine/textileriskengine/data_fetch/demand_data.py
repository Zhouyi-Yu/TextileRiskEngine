import requests
from pathlib import Path
import pandas as pd

# 当前文件：TextileRiskEngine/textileriskengine/data_fetch/xxx.py
PROJECT_ROOT = Path(__file__).resolve().parents[2]   # 回到 TextileRiskEngine/
RAW_DIR = PROJECT_ROOT / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

SEARCH_TERMS = ["t shirt", "cotton shirt", "cotton fabric", "poly cotton"]

PLATFORMS = {
    "shopee_ph": "https://shopee.ph/api/v4/search/search_items?keyword={query}&limit=50",
    "shopee_vn": "https://shopee.vn/api/v4/search/search_items?keyword={query}&limit=50",
    "jumia_ng": "https://www.jumia.com.ng/catalog/?q={query}",
}

def fetch_shopee(url):
    try:
        res = requests.get(url).json()
        items = res["items"]
        data = []
        for item in items:
            d = item["item_basic"]
            data.append({
                "name": d.get("name"),
                "price": d.get("price"),
                "sold": d.get("historical_sold"),
            })
        return pd.DataFrame(data)
    except:
        return pd.DataFrame()

def run():
    rows = []

    for q in SEARCH_TERMS:
        for name, url in PLATFORMS.items():
            full_url = url.format(query=q.replace(" ", "%20"))
            print("Fetching:", full_url)

            if "shopee" in name:
                df = fetch_shopee(full_url)
            else:
                df = pd.DataFrame()  # Jumia uses HTML, I'll write parser next if you want

            if not df.empty:
                df["platform"] = name
                df["query"] = q
                rows.append(df)

    if rows:
        final = pd.concat(rows, ignore_index=True)
        final.to_csv(RAW_DIR / "fx_data.csv", index=False)
        print("Saved → data/raw/demand_data.csv")

if __name__ == "__main__":
    run()
