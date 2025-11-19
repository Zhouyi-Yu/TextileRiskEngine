"""
freight_data.py

用途：
    從世界銀行 API 抓取
    Liner Shipping Connectivity Index (LSCI, 指標代碼: IS.SHP.GCNW.XQ)
    當作「運費 / 航運成本」的 proxy。

資料源：
    World Bank – World Development Indicators
    指標說明：
    https://databank.worldbank.org/metadataglossary/World-Development-Indicators/series/IS.SHP.GCNW.XQ
"""

import requests
import pandas as pd
from pathlib import Path
from typing import Dict, List


# 目標國家（ISO3）
COUNTRIES: Dict[str, str] = {
    "VNM": "Vietnam",
    "IDN": "Indonesia",
    "THA": "Thailand",
    "PHL": "Philippines",
    "MYS": "Malaysia",
    "NGA": "Nigeria",
    "GHA": "Ghana",
    "CIV": "Côte d'Ivoire",
    "SEN": "Senegal",
    "BEN": "Benin",
    "TGO": "Togo",
    "EGY": "Egypt",
    "KHM": "Cambodia",
}

# World Bank API URL 樣式
WB_URL_TEMPLATE = (
    "https://api.worldbank.org/v2/country/{country}/indicator/IS.SHP.GCNW.XQ"
    "?format=json&per_page=2000"
)

# 輸出路徑：專案根目錄 / data/raw/shipping_lsci_worldbank.csv
PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "shipping_lsci_worldbank.csv"


def fetch_lsci_for_country(iso3: str, name: str) -> pd.DataFrame:
    """
    從 World Bank API 抓某一國家的 LSCI 全部年份。

    回傳欄位：
        country_iso3, country_name, year, lsci
    """
    url = WB_URL_TEMPLATE.format(country=iso3.lower())
    print(f"Fetching LSCI for {iso3} ({name}) ...")
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        print(f"[ERROR] HTTP error for {iso3}: {e}")
        return pd.DataFrame()

    try:
        data = resp.json()
    except ValueError as e:
        print(f"[ERROR] JSON parse error for {iso3}: {e}")
        return pd.DataFrame()

    # World Bank API 通常是 [meta, data_list]
    if not isinstance(data, list) or len(data) < 2 or data[1] is None:
        print(f"[WARN] Unexpected structure for {iso3}: {data}")
        return pd.DataFrame()

    rows: List[dict] = []
    for obs in data[1]:
        value = obs.get("value")
        date = obs.get("date")
        if value is None or date is None:
            continue

        try:
            year = int(date)
            lsci_value = float(value)
        except (ValueError, TypeError):
            continue

        rows.append(
            {
                "country_iso3": iso3,
                "country_name": name,
                "year": year,
                "lsci": lsci_value,
            }
        )

    if not rows:
        print(f"[WARN] No valid LSCI observations for {iso3}")
        return pd.DataFrame()

    df = pd.DataFrame(rows)
    df = df.sort_values(["country_iso3", "year"]).reset_index(drop=True)
    return df


def run() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    all_dfs: List[pd.DataFrame] = []

    for iso3, name in COUNTRIES.items():
        df = fetch_lsci_for_country(iso3, name)
        if df.empty:
            continue
        all_dfs.append(df)

    if not all_dfs:
        print("[ERROR] No LSCI data fetched for any country, not writing CSV.")
        return

    final = pd.concat(all_dfs, ignore_index=True)
    final.to_csv(OUTPUT_PATH, index=False)
    print(f"[OK] Saved LSCI proxy data to: {OUTPUT_PATH}")


if __name__ == "__main__":
    run()
