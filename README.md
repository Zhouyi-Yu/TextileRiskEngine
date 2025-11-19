# TextileRiskEngine

```markdown
# GlobalTextileAnalytics
A data-driven analytics & risk-engine platform for cross-border textile trading.  
This project integrates economic data, logistics indexes, ML forecasting models and risk simulations to support data-driven decisions in textile export markets (Southeast Asia, West Africa, MENA).

---

## 🌍 Project Overview
GlobalTextileAnalytics helps textile traders and intermediaries make evidence-based decisions by integrating:

- International trade data (UN Comtrade — HS 50–63)
- FX & inflation time series (IMF IFS, World Bank WDI)
- Global freight & shipping indices (Freightos FBX)
- Local demand indicators (Shopee / Lazada / Jumia where permitted)
- Machine-learning models (margin prediction, FX forecasting, demand prediction)
- Risk simulations (Monte Carlo, FX VaR, port-delay Poisson model)

This platform supports:
- Market selection & prioritization  
- Pricing optimization  
- Risk management (FX, shipping, demand volatility)  
- Cashflow & credit-risk control  
- Scenario simulation for investment and expansion  

---

## 🏗️ Repository Structure

```

GlobalTextileAnalytics/
├─ README.md
├─ LICENSE
├─ .gitignore
├─ requirements.txt
├─ .env.example
│
├─ data/
│  ├─ raw/                   # raw data (ignored from git)
│  ├─ interim/
│  └─ processed/
│
├─ notebooks/
│  ├─ 01_exploration_yz.ipynb
│  └─ 02_exploration_partner.ipynb
│
├─ src/
│  ├─ config/
│  │   └─ settings.py
│  ├─ data/
│  │   ├─ fetch_worldbank.py
│  │   ├─ fetch_imf.py
│  │   ├─ fetch_comtrade.py
│  │   └─ clean_panel_data.py
│  ├─ features/
│  │   └─ build_features.py
│  ├─ models/
│  │   ├─ train_margin_model.py
│  │   ├─ predict_fx_lstm.py
│  │   └─ simulate_risk.py
│  └─ utils/
│      └─ io_utils.py
│
└─ docs/
└─ roadmap.md

````

---

## 🔧 Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOURNAME/GlobalTextileAnalytics.git
cd GlobalTextileAnalytics
````

### 2. Create virtual environment

```bash
python -m venv venv
source vvenv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set environment variables

```bash
cp .env.example .env
# Add API keys: Comtrade, IMF, World Bank, Freightos, etc.
```

---

## 📊 Data Sources

| Category        | Source                         | Purpose                    |
| --------------- | ------------------------------ | -------------------------- |
| Macro & FX      | IMF IFS, World Bank WDI        | FX series, inflation, GDP  |
| Shipping        | Freightos FBX                  | China→SEA/WAF freight cost |
| Trade           | UN Comtrade                    | HS 50–63 import volumes    |
| E-commerce      | Shopee/Lazada/Jumia APIs       | Price & demand indicators  |
| Risk indicators | TradingEconomics / Gov Portals | Political & port risk      |

---

## 🤖 Machine Learning Models

### 1. Margin Prediction (XGBoost / RandomForest)

* Predicts unit margin based on FX, freight cost, demand, cost structure.

### 2. FX Forecasting (LSTM / GRU)

* Forecasts short-term FX movement for high-volatility markets.

### 3. Demand Forecasting (Prophet / LightGBM)

* Predicts monthly textile / apparel demand trends by country.

### 4. Monte Carlo Simulation

Simulates 10,000+ scenarios with:

* FX shocks
* Freight spikes
* Demand shifts

Outputs:

* Expected annual profit
* Tail-risk loss (5% & 1% percentiles)
* Country risk ranking

---

## 🔐 Risk Management Tools

* FX VaR (Value-at-Risk)
* Payment-risk scoring
* Country risk index (FX + inflation + logistics + governance)
* Port-delay Poisson model
* Credit-term recommender (COD / 30 days / 60 days)

---

## 🧠 How to Use

### Fetch or update core data

```bash
python src/data/fetch_worldbank.py
python src/data/fetch_imf.py
python src/data/fetch_comtrade.py
```

### Clean and build unified panel dataset

```bash
python src/data/clean_panel_data.py
```

### Train ML models

```bash
python src/models/train_margin_model.py
```

### Run risk simulation

```bash
python src/models/simulate_risk.py
```

### Explore insights (Jupyter)

```
jupyter notebook notebooks/
```

---

## 🤝 Collaboration Guidelines

### Branching convention

* `main` → stable
* `dev` → active development
* `feature/<name>` → new features

### Commit message examples

```
feat: add Comtrade fetch script
fix: correct FX lag calculation
docs: update roadmap
```

### Notebook naming

```
yourname_topic.ipynb
```

---

## 📄 License

MIT License.

---

## 📬 Authors

* YOUR NAME (data modeling, risk simulation)
* PARTNER NAME (data pipelines, API integration)

---

## ⭐ Acknowledgements

World Bank, IMF Data Portal, UN Comtrade, Freightos FBX, and the open-source ML community.