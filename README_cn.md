# MarketForecastingAgent

AI驱动市场预判系统 — 研究 AI Agent 如何对金融市场进行分析和预判的项目

## 项目简介

本项目利用 AI Agent（TRAE CN SOLO Coder with GLM5.1）进行智能市场分析与预判，覆盖 A股、港股、美股三大市场。AI Agent 执行全面的市场研究，包括：

- **数据获取**：通过 Longport API 程序化获取最新市场数据
- **重大事件分析**：近期已发生事件 + 未来一周事件预测（含情景概率分析）
- **指数研判**：主要指数的趋势展望和目标点位
- **个股分析**：从 `targets.json` 配置文件动态读取的港股个股深度分析
- **推理链条**：完整的宏观 → 指数 → 个股推理过程

## 项目结构

```
MarketForecastingAgent
├── prompt.md              # AI Agent 研报生成 Prompt（核心配置文件）
├── config.py              # API 凭证（不提交到 git）
├── config_example.py      # API 凭证配置模板
├── targets.json          # 调研标的配置文件（用户手动维护）
├── fetch_market_data.py   # 市场数据获取脚本
├── generate_report.py     # 研报生成脚本
├── quality_check.py       # 质量校验脚本
├── debug_timestamp.py     # 时间戳调试脚本
├── README.md              # 项目说明文档（英文）
├── README_cn.md          # 项目说明文档（中文）
├── .gitignore             # Git 忽略规则
├── LICENSE                # AGPL-3.0 许可证
├── output/                # 数据文件目录
│   ├── index_data.csv     # 指数数据表
│   ├── stock_data.csv     # 个股数据表
│   └── etf_data.csv       # ETF数据表
└── YB_000X/               # 研报输出目录
    └── YB_XXXX_YYYYMMDDHHMMSS.html  # 生成的研报文件
```

## 调研标的

所有调研标的通过 `targets.json` 配置文件管理，支持 A股、港股、美股三大市场。用户可直接编辑该文件添加或删除标的。

### 港股指数 (3)

| 指数名称   | 代码     |
| ------ | ------ |
| 恒生指数   | HSI    |
| 恒生科技指数 | HSTECH |
| 国企指数   | HSCEI  |

### 美股指数 (3)

| 指数名称      | 代码   |
| --------- | ---- |
| 标普500指数   | .SPX |
| 纳斯达克100指数 | .NDX |
| 道琼斯工业指数   | .DJI |

### 港股个股

从 `targets.json` 的 `hk_shares.hkex_stocks` 中读取，当前包含腾讯控股、阿里巴巴、小米、快手、京东、美团、紫金矿业、中芯国际、华虹半导体、泡泡玛特、中国神华、宁德时代、赣锋锂业、昆仑能源、中国石油化工股份、国泰君安国际、中国宏桥、招商银行、建设银行、中国银行、汇丰控股、信达生物、药明生物、中国海洋石油、中国石油股份、工商银行、比亚迪股份、香港交易所、友邦保险、中国人寿、中国平安、中国移动、网易、百度集团、理想汽车、小鹏汽车、安踏体育、地平线机器人等。

### 美股ETF

从 `targets.json` 的 `us_shares.etf` 中读取，当前包含纳斯达克100指数ETF（QQQ）、标普500指数ETF（SPY）、道琼斯工业指数ETF（DIA）。

### 港股ETF

从 `targets.json` 的 `hk_shares.hkex_etf` 中读取，当前包含盈富基金、南方恒生科技、恒生中国企业。

### A股与美股其他标的

`targets.json` 中已预留 A股（大盘指数、行业指数、上交所个股、上交所ETF、深交所个股、深交所ETF）和美股（行业指数、个股、ADR、ETF）的分类结构，用户可按需填写。

## 数据来源

| 优先级 | 数据来源              | 说明          |
| --- | ----------------- | ----------- |
| 首选  | Longport（长桥）API   | 港股实时行情      |
| 备选  | Yahoo Finance API | 美股指数及补充港股数据 |
| 备选  | AKShare / Tushare | A股及部分港股数据   |
| 备选  | Alpha Vantage     | 全球股票和指数数据   |

## API 配置

本项目需要 [Longport（长桥）](https://www.longbridge.com/) API 账号。在项目根目录创建 `config.py` 文件，填入您的凭证：

```python
LONGPORT_APP_KEY = "your_app_key"
LONGPORT_APP_SECRET = "your_app_secret"
LONGPORT_ACCESS_TOKEN = "your_access_token"
```

⚠️ **重要**：`config.py` 已通过 `.gitignore` 排除版本控制，切勿将 API 凭证提交到仓库。

## 使用方法

1. 在 Trae IDE 中打开本项目，然后切换到SOLO模式
2. 向 AI Agent（TRAE CN SOLO GLM5.1）发送指令：

```Markdown
根据当前目录中的prompt.md中的具体需求生成一份最新的市场研报，该研报生成之后直接使用浏览器打开
```

1. Agent 将自动执行：数据获取 → 事件分析 → 指数研判 → 个股分析 → 研报生成
2. 研报输出到 `YB_000X/` 目录，HTML 格式（命名规则：`YB_XXXX_YYYYMMDDHHMMSS.html`）

## 研报特性

- **HTML 格式**，带可点击目录
- **实时数据**，精确时间戳（北京时间 / 美东时间）
- **情景概率分析**，对未来事件进行多情景推演
- **个股8字段分析**（趋势、目标价、仓位建议、逻辑等）
- **完整推理链条**（宏观 → 指数 → 个股）
- **参考资料**，包含完整URL和数据来源

## 质量校验

每份生成的研报都会通过 30+ 项质量校验，包括：

- ✅ 文件命名规范正确
- ✅ 指数和个股所有必填字段完整
- ✅ 时间戳准确（真实交易时间，非K线日期）
- ✅ 参考资料链接可点击
- ✅ 情景分析包含概率值
- ✅ 无估算/模拟数据

## 许可证

本项目采用 **GNU Affero General Public License v3.0 (AGPL-3.0)** 许可证。详见 [LICENSE](LICENSE) 文件。

## 免责声明

**本项目主要是一个研究项目。**

本项目旨在研究和评估 AI Agent 对金融市场的分析能力，主要目的是探索 AI 如何通过自动化推理流程完成市场调研、事件分析和趋势预判等工作。

**核心说明：**

- **研究目的**：本项目为学术/研究项目，专注于研究 AI Agent 在金融市场中的分析能力
- **不构成投资建议**：本项目生成的研报仅供研究参考，不构成任何形式的投资建议
- **风险警示**：金融投资具有重大风险，所有投资决策应基于专业建议和个人风险评估
- **免责声明**：项目开发者不对因使用本项目输出进行投资决策而造成的任何损失承担责任

市场有风险，投资需谨慎。
