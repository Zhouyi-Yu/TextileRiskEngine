import requests
import pandas as pd
from pathlib import Path

# 项目根目录：.../TextileRiskEngine/TextileRiskEngine
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# ISO3 国家代码 -> 国家名
COUNTRIES = {
    "VNM": "Vietnam",
    "IDN": "Indonesia",
    "THA": "Thailand",
    "PHL": "Philippines",
    "MYS": "Malaysia",
    "NGA": "Nigeria",
    "GHA": "Ghana",
    "CIV": "Cote_dIvoire",
    "SEN": "Senegal",
    "BEN": "Benin",
    "TGO": "Togo",
    "EGY": "Egypt",
    "KHM": "Cambodia",
}

# 世界银行指标：官方汇率（本币/美元）
INDICATOR = "PA.NUS.FCRF"  # Official exchange rate (LCU per US$)

def fetch_wb_fx(iso3: str) -> pd.DataFrame:
    """
    从 World Bank 拉取某国年度汇率（本币/美元）
    """
    url = (
        f"https://api.worldbank.org/v2/country/{iso3}/indicator/{INDICATOR}"
        "?format=json&per_page=500"
    )
    try:
        resp = requests.get(url, timeout=15)
        data = resp.json()

        # World Bank 返回的是 [meta, data] 结构
        if not isinstance(data, list) or len(data) < 2 or data[1] is None:
            print(f"[ERROR] {iso3}: unexpected WB format {data}")
            return pd.DataFrame()

        series = data[1]
        rows = []
        for item in series:
            year = item.get("date")
            value = item.get("value")
            if year is None or value is None:
                continue
            rows.append(
                {
                    "year": int(year),
                    "fx_rate_lcu_per_usd": float(value),
                    "country_iso3": iso3,
                }
            )
        return pd.DataFrame(rows)
    except Exception as e:
        print(f"[ERROR] {iso3}: {e}")
        return pd.DataFrame()

def run():
    all_df = []
    for iso3, name in COUNTRIES.items():
        print("Fetching WB FX:", iso3, name)
        df = fetch_wb_fx(iso3)
        if not df.empty:
            df["country_name"] = name
            all_df.append(df)

    if not all_df:
        print("[WARN] no WB FX data fetched, not writing CSV.")
        return

    final = pd.concat(all_df, ignore_index=True)
    out_path = RAW_DIR / "fx_data_wb.csv"
    final.to_csv(out_path, index=False)
    print(f"Saved → {out_path}")

if __name__ == "__main__":
    run()
