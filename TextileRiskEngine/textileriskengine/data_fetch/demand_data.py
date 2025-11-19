# textileriskengine/data_fetch/demand_data.py
"""
Demand data from World Bank WDI
--------------------------------
本模块用世界银行开放 API 拉取一个需求强度相关的指标：

  Households and NPISHs final consumption expenditure per capita
  (constant 2015 US$) -> NE.CON.PRVT.PC.KD

用于近似：
- 居民人均消费能力（已剔除通胀）
- 终端市场购买 T 恤、面料等产品的“钱包厚度”

结果写入：
  data/raw/demand_data_wb.csv
"""

from __future__ import annotations

from pathlib import Path
import logging
from typing import Dict, List

import pandas as pd
import requests

# ----------------- 路径设置：data/raw -----------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_CSV = DATA_DIR / "demand_data_wb.csv"

# ----------------- 日志设置 -----------------
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# 和 trade_data 保持同一批国家 & 命名
COUNTRIES: Dict[str, str] = {
    "VNM": "Vietnam",
    "IDN": "Indonesia",
    "THA": "Thailand",
    "PHL": "Philippines",
    "MYS": "Malaysia",
    "NGA": "Nigeria",
    "GHA": "Ghana",
    "CIV": "Cote d'Ivoire",
    "SEN": "Senegal",
    "BEN": "Benin/Togo (use Benin as proxy)",
    "EGY": "Egypt",
    "KHM": "Cambodia",
}

# 世界银行 WDI 指标：人均最终消费支出（不变价）
DEMAND_INDICATOR = "NE.CON.PRVT.PC.KD"
WB_BASE_URL = "https://api.worldbank.org/v2/country/{iso3}/indicator/{indicator}"


def fetch_demand(iso3: str) -> pd.DataFrame:
    """
    拉取某个国家的人均消费支出时间序列。

    返回列：
        - country_iso3
        - year
        - consumption_pc_const2015usd
    """
    url = WB_BASE_URL.format(iso3=iso3, indicator=DEMAND_INDICATOR)
    params = {"format": "json", "per_page": 500}
    logger.info(f"[WB] Fetching demand indicator {DEMAND_INDICATOR} for {iso3} ...")

    res = requests.get(url, params=params, timeout=30)
    res.raise_for_status()

    js = res.json()
    if not isinstance(js, list) or len(js) < 2 or js[1] is None:
        raise ValueError(f"Unexpected WB API response for {iso3}: {js}")

    records = []
    for row in js[1]:
        year = row.get("date")
        value = row.get("value")
        if value is None or year is None:
            continue
        try:
            year_int = int(year)
            val_float = float(value)
        except (TypeError, ValueError):
            continue

        records.append(
            {
                "country_iso3": iso3,
                "year": year_int,
                "consumption_pc_const2015usd": val_float,
            }
        )

    df = pd.DataFrame(records)
    if df.empty:
        logger.warning(f"[WB] No non-null demand data for {iso3}")
    return df


def run() -> None:
    """
    主入口：循环国家，写 CSV。
    输出：data/raw/demand_data_wb.csv
    """
    all_frames: List[pd.DataFrame] = []

    for iso3, cname in COUNTRIES.items():
        logger.info("=" * 70)
        logger.info(f"[DEMAND] Country: {cname} ({iso3})")

        try:
            df = fetch_demand(iso3)
        except Exception as e:
            logger.error(f"[ERROR] Failed to fetch demand for {iso3}: {e}")
            continue

        if df.empty:
            continue

        df["country_name"] = cname
        all_frames.append(df)

    if not all_frames:
        logger.error("[FATAL] No demand data collected for any country. Nothing to write.")
        return

    final = pd.concat(all_frames, ignore_index=True)
    final = final.sort_values(["country_iso3", "year"]).reset_index(drop=True)

    logger.info(f"[SAVE] Writing demand data to: {OUTPUT_CSV}")
    final.to_csv(OUTPUT_CSV, index=False)


if __name__ == "__main__":
    run()
