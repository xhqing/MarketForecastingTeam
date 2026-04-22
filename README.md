# CBBC\_TRAE

跨市场重大事件与港股龙头策略研判 — 基于 AI Agent 的自动化研报生成项目

## 项目简介

本项目利用 AI Agent（TRAE CN SOLO GLM5.1）自动生成跨市场策略研报，覆盖 A股、港股、美股三大市场，以港股为核心焦点。研报内容包括：

- **数据获取**：通过 Longport API 程序化获取最新市场数据
- **重大事件分析**：近期已发生事件 + 未来一周事件预测（含情景概率分析）
- **指数研判**：6大指数的趋势展望和目标点位
- **个股分析**：从 `targets.yaml` 配置文件动态读取的港股个股深度分析
- **推理链条**：完整的宏观 → 指数 → 个股推理过程

## 项目结构

```
CBBC_TRAE/
├── prompt.md              # AI Agent 研报生成 Prompt（核心配置文件）
├── config.py              # API 凭证（不提交到 git）
├── config_example.py      # API 凭证配置模板
├── targets.yaml           # 调研标的配置文件（用户手动维护）
├── fetch_market_data.py   # 市场数据获取脚本
├── generate_report.py     # 研报生成脚本
├── quality_check.py       # 质量校验脚本
├── debug_timestamp.py     # 时间戳调试脚本
├── README.md              # 项目说明文档（中文）
├── README_en.md           # 项目说明文档（英文）
├── .gitignore             # Git 忽略规则
├── LICENSE                # AGPL-3.0 许可证
└── output/                # 输出目录
    ├── index_data.csv     # 指数数据表
    ├── stock_data.csv     # 个股数据表
    └── YB_XXXX_XXXXXXXXXXXX.html  # 生成的研报文件
```

## 标的配置

所有调研标的通过 `targets.yaml` 配置文件管理，支持 A股、港股、美股三大市场。用户可直接编辑该文件添加或删除标的。

### 港股指数（3个）

| 指数     | 代码     |
| ------ | ------ |
| 恒生指数   | HSI    |
| 恒生科技指数 | HSTECH |
| 国企指数   | HSCEI  |

### 美股指数（3个）

| 指数        | 代码   |
| --------- | ---- |
| 标普500指数   | .SPX |
| 纳斯达克100指数 | .NDX |
| 道琼斯工业指数   | .DJI |

### 港股个股

从 `targets.yaml` 的 `hk_shares.hkex_stocks` 中读取，当前包含腾讯控股、阿里巴巴、小米、快手、京东、美团、紫金矿业、中芯国际、华虹半导体、泡泡玛特、中国神华、宁德时代、赣锋锂业、昆仑能源、中国石油化工股份、国泰君安国际、中国宏桥、招商银行、建设银行、中国银行、汇丰控股、信达生物、药明生物、中国海洋石油、中国石油股份、工商银行、比亚迪股份、香港交易所、友邦保险、中国人寿、中国平安、中国移动、网易、百度集团、理想汽车、小鹏汽车、安踏体育、地平线机器人等。

### 港股ETF

从 `targets.yaml` 的 `hk_shares.hkex_etf` 中读取，当前包含盈富基金、南方恒生科技、恒生中国企业。

### A股与美股其他标的

`targets.yaml` 中已预留 A股（大盘指数、行业指数、上交所个股、上交所ETF、深交所个股、深交所ETF）和美股（行业指数、个股、ADR、ETF）的分类结构，用户可按需填写。

## 数据源

| 优先级 | 数据源               | 说明          |
| --- | ----------------- | ----------- |
| 首选  | Longport（长桥）API   | 港股实时行情数据    |
| 备选  | Yahoo Finance API | 美股指数及补充港股数据 |
| 备选  | AKShare / Tushare | A股及部分港股数据   |
| 备选  | Alpha Vantage     | 全球股票及指数数据   |

## API 配置

本项目需要 [Longport（长桥）](https://www.longbridge.com/) API 账号。在项目根目录创建 `config.py` 文件：

```python
LONGPORT_APP_KEY = "your_app_key"
LONGPORT_APP_SECRET = "your_app_secret"
LONGPORT_ACCESS_TOKEN = "your_access_token"
```

⚠️ **重要**：`config.py` 已通过 `.gitignore` 排除版本控制，切勿将 API 凭证提交到仓库。

## 使用方法

1. 在 Trae IDE 中打开本项目
2. 向 AI Agent（TRAE CN SOLO GLM5.1）发送指令：
   > "根据当前目录中的prompt.md中的具体需求生成一份最新的市场研报，该研报生成之后直接使用浏览器打开"
3. Agent 将自动执行：数据获取 → 事件分析 → 指数研判 → 个股分析 → 研报生成
4. 研报输出到 `output/` 目录，HTML 格式（命名规则：`YB_XXXX_YYYYMMDDHHMMSS.html`）

## 研报特性

- **HTML 格式**，带可点击目录
- **实时数据**，精确时间戳（北京时间 / 美东时间）
- **情景概率分析**，对未来事件进行多情景推演
- **8字段个股分析**（趋势预判、目标价、仓位建议、核心逻辑等）
- **完整推理链条**（宏观 → 指数 → 个股）
- **参考链接**，附完整 URL 和来源标注

## 质量校验

每份生成的研报通过 30+ 项质量校验，包括：

- ✅ 文件命名规范
- ✅ 指数和个股字段完整性
- ✅ 时间戳准确性（真实交易时间，非K线日期）
- ✅ 参考链接可点击
- ✅ 情景分析概率值
- ✅ 无估算/模拟数据

## 许可证

本项目基于 **GNU Affero General Public License v3.0**（AGPL-3.0）开源。详见 [LICENSE](LICENSE) 文件。

## 免责声明

本项目生成的研报仅供参考，不构成任何投资建议。市场有风险，投资需谨慎。
