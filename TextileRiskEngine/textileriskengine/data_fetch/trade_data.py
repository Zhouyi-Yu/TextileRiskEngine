# textileriskengine/data_fetch/trade_data.py
"""
Trade data from World Bank WDI
--------------------------------
本模块用世界银行开放 API 拉取两个与贸易相关的宏观指标：
1) Imports of goods and services (% of GDP)      -> NE.IMP.GNFS.ZS
2) Textiles and clothing (% of value added in manufacturing) -> NV.MNF.TXTL.ZS.UN

这些不是“从中国进口 HS50-63 的精确金额”，
而是用来近似：
- 这个国家整体对进口的依赖程度
- 纺织/服装行业在本国制造业中的重要性

结果会写入：
  data/raw/trade_data_wb.csv
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
OUTPUT_CSV = DATA_DIR / "trade_data_wb.csv"

# ----------------- 日志设置 -----------------
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# ----------------- 国家列表（ISO3） -----------------
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
    # 用贝宁作为 Benin/Togo 的宏观代理
    "BEN": "Benin/Togo (use Benin as proxy)",
    "EGY": "Egypt",
    "KHM": "Cambodia",
}

# ----------------- 指标代码（世界银行 WDI） -----------------
TRADE_INDICATORS: Dict[str, str] = {
    # 进口依赖度（% of GDP）
    "imports_gdp_pct": "NE.IMP.GNFS.ZS",
    # 纺织与服装在制造业增加值中的占比
    "textiles_share_mfg": "NV.MNF.TXTL.ZS.UN",
}

WB_BASE_URL = "https://api.worldbank.org/v2/country/{iso3}/indicator/{indicator}"


def fetch_wb_indicator(iso3: str, indicator: str) -> pd.DataFrame:
    """
    拉取某个国家 + 某个 WDI 指标的完整时间序列。

    返回列：
        - country_iso3
        - year (int)
        - value (float)
    """
    url = WB_BASE_URL.format(iso3=iso3, indicator=indicator)
    params = {"format": "json", "per_page": 500}
    logger.info(f"[WB] Fetching {indicator} for {iso3} ...")

    res = requests.get(url, params=params, timeout=30)
    res.raise_for_status()

    js = res.json()
    if not isinstance(js, list) or len(js) < 2 or js[1] is None:
        raise ValueError(f"Unexpected WB API response for {iso3} / {indicator}: {js}")

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
                "value": val_float,
            }
        )

    df = pd.DataFrame(records)
    if df.empty:
        logger.warning(f"[WB] No non-null data for {iso3} / {indicator}")
    return df


def run() -> None:
    """
    主入口：循环国家 & 指标，合并后写入 CSV。
    输出：data/raw/trade_data_wb.csv
    """
    all_country_frames: List[pd.DataFrame] = []

    for iso3, cname in COUNTRIES.items():
        logger.info("=" * 70)
        logger.info(f"[TRADE] Country: {cname} ({iso3})")

        merged = None

        for col_name, indicator in TRADE_INDICATORS.items():
            try:
                df_ind = fetch_wb_indicator(iso3, indicator)
            except Exception as e:
                logger.error(
                    f"[ERROR] Failed to fetch indicator {indicator} for {iso3}: {e}"
                )
                continue

            if df_ind.empty:
                continue

            df_ind = df_ind.rename(columns={"value": col_name})

            if merged is None:
                merged = df_ind
            else:
                merged = pd.merge(
                    merged,
                    df_ind[["country_iso3", "year", col_name]],
                    on=["country_iso3", "year"],
                    how="outer",
                )

        if merged is None or merged.empty:
            logger.warning(f"[WARN] No trade data collected for {cname} ({iso3})")
            continue

        merged["country_name"] = cname
        all_country_frames.append(merged)

    if not all_country_frames:
        logger.error("[FATAL] No trade data collected for any country. Nothing to write.")
        return

    final = pd.concat(all_country_frames, ignore_index=True)

    # 按国家 + 年份排序，方便后面建模
    final = final.sort_values(["country_iso3", "year"]).reset_index(drop=True)

    logger.info(f"[SAVE] Writing trade data to: {OUTPUT_CSV}")
    final.to_csv(OUTPUT_CSV, index=False)


if __name__ == "__main__":
    run()
