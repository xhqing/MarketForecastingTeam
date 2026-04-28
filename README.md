# MarketForecastingTeam

AI-Driven Market Forecasting System — A Research Project on AI Agent's Financial Market Analysis and Prediction

## Overview

This project leverages AI Agents to conduct intelligent market analysis and forecasting, covering the A-share, Hong Kong stock, and US stock markets. The AI Agent performs comprehensive market research, including:

- **Data Acquisition**: Programmatic fetching of latest market data via Longport API
- **Major Events Analysis**: Recent events + one-week forward event predictions (with probabilistic scenario analysis)
- **Index Forecast**: Trend outlooks and target levels for major indices
- **Stock Analysis**: In-depth analysis of Hong Kong stocks dynamically loaded from `targets.json`
- **Reasoning Chain**: Complete macro → index → stock reasoning process

## Project Structure

```
MarketForecastingTeam
├── prompt.md              # AI Agent report generation prompt (core config)
├── config.py              # API credentials (NOT committed to git)
├── config_example.py      # Template for API credentials
├── targets.json          # Target instruments config (user-maintained)
├── fetch_market_data.py   # Market data fetching script
├── generate_report.py     # Report generation script
├── quality_check.py       # Quality validation script
├── debug_timestamp.py     # Timestamp debugging script
├── README.md              # Project documentation
├── .gitignore             # Git ignore rules
├── LICENSE                # AGPL-3.0 License
├── output/                # Data files directory
│   ├── index_data.csv     # Index data table
│   ├── stock_data.csv     # Stock data table
│   └── etf_data.csv       # ETF data table
└── YB_000X/               # Research reports output directory
    └── YB_XXXX_YYYYMMDDHHMMSS.html  # Generated research reports
```

## Target Instruments

All target instruments are managed through the `targets.json` configuration file, supporting A-shares, Hong Kong stocks, and US stocks. Users can directly edit this file to add or remove instruments.

### Hong Kong Indices (3)

| Index                           | Code   |
| ------------------------------- | ------ |
| Hang Seng Index                 | HSI    |
| Hang Seng Tech Index            | HSTECH |
| HSCEI (China Enterprises Index) | HSCEI  |

### US Indices (3)

| Index                        | Code |
| ---------------------------- | ---- |
| S\&P 500 Index               | .SPX |
| Nasdaq 100 Index             | .NDX |
| Dow Jones Industrial Average | .DJI |

### Hong Kong Stocks

Read from `hk_shares.hkex_stocks` in `targets.json`. Currently includes Tencent Holdings, Alibaba, Xiaomi, Kuaishou, JD.com, Meituan, Zijin Mining, SMIC, Hua Hong Semiconductor, Pop Mart, China Shenhua Energy, CATL, Ganfeng Lithium, Kunlun Energy, Sinopec, Guotai Junan International, China Hongqiao, China Merchants Bank, China Construction Bank, Bank of China, HSBC, Innovent Biologics, WuXi Biologics, CNOOC, PetroChina, ICBC, BYD, HKEX, AIA Group, China Life Insurance, Ping An Insurance, China Mobile, NetEase, Baidu, Li Auto, XPeng, ANTA Sports, Horizon Robotics, and more.

### US ETFs

Read from `us_shares.etf` in `targets.json`. Currently includes Nasdaq 100 ETF (QQQ), S\&P 500 ETF (SPY), and Dow Jones Industrial ETF (DIA).

### Hong Kong ETFs

Read from `hk_shares.hkex_etf` in `targets.json`. Currently includes Tracker Fund of Hong Kong, CSOP Hang Seng Tech, and Hang Seng H-Share.

### A-Share & US Stock Instruments

`targets.json` includes pre-defined category structures for A-shares (major indices, sector indices, SSE stocks, SSE ETFs, SZSE stocks, SZSE ETFs) and US stocks (sector indices, stocks, ADRs, ETFs). Users can fill in as needed.

## Data Sources

| Priority | Data Source               | Description                                 |
| -------- | ------------------------- | ------------------------------------------- |
| Primary  | Longport (Longbridge) API | Real-time Hong Kong stock quotes            |
| Fallback | Yahoo Finance API         | US indices and supplementary Hong Kong data |
| Fallback | AKShare / Tushare         | A-shares and partial Hong Kong data         |
| Fallback | Alpha Vantage             | Global stock and index data                 |

## API Configuration

This project requires a [Longport (Longbridge)](https://www.longbridge.com/) API account. Create a `config.py` file in the project root with your credentials:

```python
LONGPORT_APP_KEY = "your_app_key"
LONGPORT_APP_SECRET = "your_app_secret"
LONGPORT_ACCESS_TOKEN = "your_access_token"
```

⚠️ **Important**: `config.py` is excluded from version control via `.gitignore`. Never commit API credentials to the repository.

## Usage

1. Open this project in Trae IDE，then change to the SOLO mode
2. Give the AI Agent Leader (TRAE CN SOLO Coder) the following instruction:

```Markdown
Generate a latest market research report based on the specific requirements in prompt.md in the current directory. After the report is generated, open it directly in the browser.
```

1. The Agent will automatically execute: data fetching → event analysis → index forecast → stock analysis → report generation
2. Reports are output to the `YB_000X/` directory in HTML format (naming: `YB_XXXX_YYYYMMDDHHMMSS.html`)

## Report Features

- **HTML format** with clickable table of contents
- **Real-time data** with accurate timestamps (HK time / US Eastern time)
- **Scenario probability analysis** for future events
- **8-field per-stock analysis** (trend, targets, position advice, logic, etc.)
- **Complete reasoning chain** (macro → index → stock)
- **Reference links** with full URLs and source attribution

## Quality Checks

Each generated report passes 30+ quality validations, including:

- ✅ Correct file naming convention
- ✅ All required fields present for indices and stocks
- ✅ Accurate timestamps (real trading times, not K-line dates)
- ✅ Clickable reference links
- ✅ Probability values for scenario analysis
- ✅ No estimated/simulated data

## License

This project is licensed under the **GNU Affero General Public License v3.0** (AGPL-3.0). See the [LICENSE](LICENSE) file for details.

## Disclaimer

Reports generated by this project are for reference only and do not constitute investment advice. Market investments carry risks; investors should exercise caution.
