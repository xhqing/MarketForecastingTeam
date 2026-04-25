"""
Cross-Market Major Events and HK Stock Leading Companies Strategy Report Generation Script
跨市场重大事件与港股龙头策略研报生成脚本

=============================================================================
File Function:
    This script automatically generates cross-market strategy reports, covering A-shares,
    HK stocks, and US stocks, with focus on HK stocks. Report includes:
    - Market data display (indices, stocks, ETFs)
    - Major events analysis (recent events + next week predictions)
    - Index analysis (6 major indices' trend outlook and target levels)
    - Stock analysis (in-depth analysis of HK leading stocks)
    - ETF analysis (HK ETF fund analysis)
    - Complete reasoning chain (macro → index → stocks)
文件功能：
    本脚本自动生成跨市场策略研报，覆盖A股、港股、美股三大市场，以港股为核心焦点。
    研报内容包括：
    - 市场数据展示（指数、个股、ETF）
    - 重大事件分析（近期已发生事件 + 未来一周预测）
    - 指数研判（6大指数的趋势展望和目标点位）
    - 个股分析（港股龙头深度分析）
    - ETF分析（港股ETF基金分析）
    - 完整推理链条（宏观 → 指数 → 个股）

=============================================================================
Dependencies:
    - os: File path operations
    - pandas (pd): CSV data reading and processing
    - datetime: Timestamp generation
    - pytz: Timezone handling (Beijing time)
    - glob: File finding (counting generated reports)
依赖模块：
    - os: 文件路径操作
    - pandas (pd): CSV数据读取和数据处理
    - datetime: 时间戳生成
    - pytz: 时区处理（北京时间）
    - glob: 文件查找（统计已生成研报数量）

=============================================================================
Data File Dependencies:
    - output/index_data.csv: Index data (name, code, current points, source, timestamp)
    - output/stock_data.csv: Stock data (name, code, current price, source, timestamp)
    - output/etf_data.csv: ETF data (name, code, current price, source, timestamp)
数据文件依赖：
    - output/index_data.csv: 指数数据（指数名称、指数代码、当前最新点数、数据来源、时间戳）
    - output/stock_data.csv: 个股数据（股票名称、股票代码、当前最新价格、数据来源、时间戳）
    - output/etf_data.csv: ETF数据（ETF名称、ETF代码、当前最新价格、数据来源、时间戳）

=============================================================================
Output Files:
    - YB_000X/YB_XXXX_YYYYMMDDHHMMSS.html: Generated HTML format report
      - YB_XXXX: Report number (auto-incrementing, starting from YB_0001)
      - YYYYYMMDDHHMMSS: Beijing timestamp when report was generated
输出文件：
    - YB_000X/YB_XXXX_YYYYMMDDHHMMSS.html: 生成的HTML格式研报
      - YB_XXXX: 研报编号（自动递增，从YB_0001开始）
      - YYYYYMMDDHHMMSS: 报告生成时的北京时间戳

=============================================================================
Report Numbering Rules:
    - Automatically scan YB_000X directory for existing YB_*.html files
    - New report number = existing reports count + 1
    - Ensures each report has unique number and timestamp
研报编号规则：
    - 自动扫描YB_000X目录下已有的YB_*.html文件数量
    - 新报告编号 = 已存在报告数量 + 1
    - 确保每份报告有唯一编号和唯一时间戳

=============================================================================
Author/Maintainer: AI Agent (TRAE CN SOLO GLM5.1)
Last Updated: 2026-04-23
作者/维护者：AI Agent (TRAE CN SOLO GLM5.1)
最后更新：2026-04-23
=============================================================================
"""

import os
import pandas as pd
from datetime import datetime
import pytz
import glob

# =============================================================================
# Configuration Constants
# 配置常量
# =============================================================================

# Report output directory path
# Description: All generated HTML reports will be saved to this directory
# Path: YB_000X folder under project root
# 研报输出目录路径
# 说明：所有生成的HTML研报将保存到此目录
# 路径：项目根目录下的YB_000X文件夹
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'YB_000X')

# Data files directory path
# Description: Location of CSV data files (index_data.csv, stock_data.csv, etf_data.csv)
# Path: output folder under project root
# 数据文件目录路径
# 说明：CSV数据文件（index_data.csv、stock_data.csv、etf_data.csv）存放位置
# 路径：项目根目录下的output文件夹
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')

# =============================================================================
# Time Initialization
# 时间初始化
# =============================================================================

# Set Beijing timezone
# Used to generate accurate report timestamps, ensuring time is displayed in Beijing time not local time
# 设置北京时间时区
# 用于生成准确的报告时间戳，确保时间显示为北京时间而非本地时间
bj_tz = pytz.timezone('Asia/Shanghai')

# Get current Beijing time
# 获取当前北京时间
now_bj = datetime.now(bj_tz)

# Format report date (for HTML title display)
# Output format example: 2026年04月23日
# 格式化报告日期（用于HTML标题显示）
# 输出格式示例：2026年04月23日
report_date = now_bj.strftime('%Y年%m月%d日')

# Format timestamp (for filename and report generation time display)
# Output format example: 20260423111711
# 格式化时间戳（用于文件名和报告生成时间显示）
# 输出格式示例：20260423111711
timestamp_str = now_bj.strftime('%Y%m%d%H%M%S')

# =============================================================================
# Report Number Auto-Generation
# 研报编号自动生成
# =============================================================================

# Scan YB_000X directory for existing report files
# glob pattern: YB_*.html matches all files starting with YB and ending with .html
# 扫描YB_000X目录下已有的研报文件
# glob模式：YB_*.html 匹配所有以YB开头、.html结尾的文件
existing_reports = glob.glob(os.path.join(OUTPUT_DIR, 'YB_*.html'))

# Calculate next report number
# Rule: existing reports count + 1
# Example: 6 existing reports → next number is 7 → generate YB_0007
# 计算下一个研报的编号
# 规则：已有报告数量 + 1
# 示例：已有6份报告 → 下一份编号为7 → 生成YB_0007
next_num = len(existing_reports) + 1

# Generate report filename
# Format: YB_000{number}_{timestamp}.html
# Example: YB_0007_20260423111711.html
# 生成研报文件名
# 格式：YB_000{编号}_{时间戳}.html
# 示例：YB_0007_20260423111711.html
filename = f"YB_000{next_num}_{timestamp_str}.html"

# Generate complete file save path
# 生成完整的文件保存路径
filepath = os.path.join(OUTPUT_DIR, filename)

# =============================================================================
# Data Loading
# 数据加载
# =============================================================================

# Load index data from CSV file
# Input: output/index_data.csv
# Output: DataFrame object containing index name, code, current points, source, timestamp fields
# 从CSV文件读取指数数据
# 输入：output/index_data.csv
# 输出：DataFrame对象，包含指数名称、代码、当前点数、数据来源、时间戳等字段
df_index = pd.read_csv(os.path.join(DATA_DIR, 'index_data.csv'))

# Load stock data from CSV file
# Input: output/stock_data.csv
# Output: DataFrame object containing stock name, code, current price, source, timestamp fields
# 从CSV文件读取个股数据
# 输入：output/stock_data.csv
# 输出：DataFrame对象，包含股票名称、代码、当前价格、数据来源、时间戳等字段
df_stock = pd.read_csv(os.path.join(DATA_DIR, 'stock_data.csv'))

# Load ETF data from CSV file
# Input: output/etf_data.csv
# Output: DataFrame object containing ETF name, code, current price, source, timestamp fields
# 从CSV文件读取ETF数据
# 输入：output/etf_data.csv
# 输出：DataFrame对象，包含ETF名称、代码、当前价格、数据来源、时间戳等字段
df_etf = pd.read_csv(os.path.join(DATA_DIR, 'etf_data.csv'))

# =============================================================================
# Price Mapping Construction
# 价格映射构建
# =============================================================================

# Build index price mapping dictionary
# Purpose: Quick lookup of latest prices by index name for analysis and calculation
# Key: Index name (e.g., "恒生指数")
# Value: Current latest points (float)
# Exception handling: Skip invalid data that cannot be converted to float
# 构建指数价格映射字典
# 用途：根据指数名称快速查询最新价格，用于后续分析和计算
# 键：指数名称（如"恒生指数"）
# 值：当前最新点数（浮点数）
# 异常处理：跳过无法转换为浮点数的无效数据
index_price_map = {}
for _, row in df_index.iterrows():
    try:
        index_price_map[row['指数名称']] = float(row['当前最新点数'])
    except (ValueError, TypeError):
        pass

# Build stock price mapping dictionary
# Purpose: Quick lookup of latest prices by stock code for analysis and calculation
# Key: Stock code (e.g., "00700.HK")
# Value: Current latest price (HKD)
# 构建个股价格映射字典
# 用途：根据股票代码快速查询最新价格，用于后续分析和计算
# 键：股票代码（如"00700.HK"）
# 值：当前最新价格（港币HKD）
stock_price_map = {}
for _, row in df_stock.iterrows():
    try:
        stock_price_map[row['股票代码']] = float(row['当前最新价格(HKD)'])
    except (ValueError, TypeError):
        pass

# Build ETF price mapping dictionary
# Purpose: Quick lookup of latest prices by ETF code for analysis and calculation
# Key: ETF code (e.g., "02800.HK")
# Value: Current latest price (HKD)
# 构建ETF价格映射字典
# 用途：根据ETF代码快速查询最新价格，用于后续分析和计算
# 键：ETF代码（如"02800.HK"）
# 值：当前最新价格（港币HKD）
etf_price_map = {}
for _, row in df_etf.iterrows():
    try:
        etf_price_map[row['ETF代码']] = float(row['当前最新价格(HKD)'])
    except (ValueError, TypeError):
        pass

# =============================================================================
# Index Current Price Extraction
# 指数当前价格提取
# =============================================================================

# Extract current prices for each index from price mapping
# If index does not exist in mapping, use default value (from previous trading day's close)
# Default values ensure report can still be generated even if data reading fails
# 从价格映射中提取各指数当前价格
# 如果映射中不存在该指数，则使用默认值（来源于上一交易日收盘价）
# 默认值确保即使数据读取失败，报告仍能正常生成

hsi = index_price_map.get('恒生指数', 26163.24)      # Hang Seng Index
hstech = index_price_map.get('恒生科技指数', 4963.94) # Hang Seng Tech Index
hscei = index_price_map.get('国企指数', 8801.78)     # HSCEI
ndx = index_price_map.get('纳斯达克100指数', 26937.27) # Nasdaq 100 Index
spx = index_price_map.get('标普500指数', 7137.90)     # S&P 500 Index
dji = index_price_map.get('道琼斯工业指数', 49490.03) # Dow Jones Industrial Index

# =============================================================================
# Helper Calculation Functions
# 辅助计算函数
# =============================================================================

def calc_rise(current, target):
    """
    Calculate price increase percentage
    计算价格上涨百分比

    Parameters:
        current (float): Current price/points
        target (float): Target price/points
    参数：
        current (float): 当前价格/点数
        target (float): 目标价格/点数

    Returns:
        float: Increase percentage (rounded to 2 decimal places)
               Formula: (target - current) / current * 100
    返回：
        float: 上涨百分比（保留2位小数）
              计算公式：(目标价格 - 当前价格) / 当前价格 * 100

    Examples:
        calc_rise(100, 110) returns 10.0 (indicating 10% increase)
        calc_rise(100, 90) returns -10.0 (indicating 10% decrease)
    示例：
        calc_rise(100, 110) 返回 10.0（表示上涨10%）
        calc_rise(100, 90) 返回 -10.0（表示下跌10%）
    """
    return round((target - current) / current * 100, 2)


def calc_fall(current, target):
    """
    Calculate price decrease percentage
    计算价格下跌百分比

    Parameters:
        current (float): Current price/points
        target (float): Target price/points
    参数：
        current (float): 当前价格/点数
        target (float): 目标价格/点数

    Returns:
        float: Decrease percentage (rounded to 2 decimal places)
               Formula: (target - current) / current * 100
               Positive means need to rise from current to target, negative means will fall
    返回：
        float: 下跌百分比（保留2位小数）
              计算公式：(目标价格 - 当前价格) / 当前价格 * 100
              正值表示从当前到目标需要上涨，负值表示从当前到目标会下跌

    Examples:
        calc_fall(100, 90) returns -10.0 (indicating falling from 100 to 90 is -10%)
    示例：
        calc_fall(100, 90) 返回 -10.0（表示从100跌到90是-10%）
    """
    return round((target - current) / current * 100, 2)


# [Note: The following data sections contain analysis data with Chinese content for the Chinese market.
# This content should remain in Chinese as it represents market-specific information.
# The analysis data includes: index_analysis, stock_analysis, etf_analysis
# 注意事项：以下数据部分包含中文内容的市场分析数据。
# 这些内容应保持中文，因为它们代表市场特定信息。
# 分析数据包括：index_analysis, stock_analysis, etf_analysis
# ]

# (Index analysis data - keeping original Chinese content)
# 6大指数的详细分析数据
# 每个指数包含：名称、代码、当前点位、趋势判断、高/低目标点位、核心逻辑
# 趋势判断选项：震荡偏弱、震荡偏强、震荡上行
index_analysis = [
    {"name": "恒生指数", "code": "HSI", "current": hsi, "trend": "震荡偏弱", "high": 28500, "low": 24000,
     "logic": "美伊停火协议到期但特朗普宣布无限期延长，地缘风险暂缓但不确定性仍存。科网股全线回调拖累指数，南向资金逆势净买入48.91亿港元提供底部支撑，市场呈现结构性分化格局。"},
    {"name": "恒生科技指数", "code": "HSTECH", "current": hstech, "trend": "震荡偏弱", "high": 5800, "low": 4400,
     "logic": "科网股普遍回调（腾讯跌2.89%、阿里跌3.52%、美团跌2.54%），AI概念高位获利回吐，但光通信板块逆势暴涨（剑桥科技涨21%、长飞光纤涨17%），板块内部分化加剧。"},
    {"name": "国企指数", "code": "HSCEI", "current": hscei, "trend": "震荡偏强", "high": 9800, "low": 8000,
     "logic": "中字头能源板块受益油价高位（布伦特101.90美元/桶），中海油获南向资金净买入4.75亿港元居首，银行板块高股息防御属性突出，估值修复逻辑持续。"},
    {"name": "纳斯达克100指数", "code": ".NDX", "current": ndx, "trend": "震荡偏强", "high": 30000, "low": 24000,
     "logic": "纳指4月22日反弹1.64%，停火延长提振风险偏好，Google Cloud Next大会催化AI算力预期，费半14连涨显示半导体景气度持续，但地缘风险仍压制估值扩张空间。"},
    {"name": "标普500指数", "code": ".SPX", "current": spx, "trend": "震荡偏强", "high": 7800, "low": 6500,
     "logic": "标普500反弹1.05%至7137.90点，停火延长缓解地缘担忧，一季报超预期比例近90%支撑盈利端，能源板块受益油价上涨，但美联储降息推迟至2027年限制估值上行。"},
    {"name": "道琼斯工业指数", "code": ".DJI", "current": dji, "trend": "震荡偏强", "high": 53000, "low": 45000,
     "logic": "道指反弹0.69%至49490.03点，传统行业盈利改善与油价成本压力对冲，GE Vernova等重磅财报超预期，金融和能源板块提供底部支撑，苹果换帅影响有限。"},
]

# (Stock analysis data - keeping original Chinese content)
# 港股龙头个股详细分析数据
# 每个股票包含：名称、代码、当前价格、趋势判断、高/低目标价、观点、仓位建议、核心逻辑
# 价格来源：从stock_price_map中查询，查询不到则使用默认值
stock_analysis = [
    {"name": "腾讯控股", "code": "00700.HK", "price": stock_price_map.get("00700.HK", 504.00), "trend": "震荡偏弱", "high": 600, "low": 430, "view": "看多", "position": "加仓，建议仓位占比：8.00%",
     "logic": "AI赋能核心业务提升变现效率，微信AI搜索功能上线，但科网股整体回调短期承压，南向资金净卖出10.28亿港元，估值仍有修复空间。"},
    # ... (remaining stock data)
]

# (ETF analysis data - keeping original Chinese content)
# 港股主要ETF基金详细分析数据
# 每个ETF包含：名称、代码、当前价格、趋势判断、高/低目标价、观点、仓位建议、核心逻辑
# 价格来源：从etf_price_map中查询，查询不到则使用默认值
etf_analysis = [
    {"name": "盈富基金", "code": "02800.HK", "price": etf_price_map.get("02800.HK", 26.76), "trend": "震荡偏弱", "high": 30, "low": 23, "view": "看多", "position": "加仓，建议仓位占比：10.00%",
     "logic": "跟踪恒生指数，获南向资金5日大幅增持32.89亿元居首，港股通持股比例5.46%且持续上升，高股息+低估值配置价值突出。"},
    # ... (remaining ETF data)
]

# =============================================================================
# HTML Table Generation Functions
# HTML表格生成函数
# =============================================================================

def make_index_data_link(val, source):
    """
    Generate hyperlink for index data source
    生成指数数据来源的超链接

    Parameters:
        val (str): Display text, usually data value or "来源" label
        source (str): Data source URL
    参数：
        val (str): 显示文本，通常是数据值或"来源"标签
        source (str): 数据来源URL

    Returns:
        str: HTML hyperlink tag string
             - If source starts with "http", returns HTML code with hyperlink
             - Otherwise returns original text val
    返回：
        str: HTML超链接标签字符串
            - 如果source以"http"开头，返回带超链接的HTML代码
            - 否则返回原始文本val

    Examples:
        make_index_data_link("来源", "https://example.com")
        returns: '<a href="https://example.com" target="_blank">来源</a>'
    示例：
        make_index_data_link("来源", "https://example.com")
        返回: '<a href="https://example.com" target="_blank">来源</a>'
    """
    try:
        url = str(source)
        if url.startswith('http'):
            return f'<a href="{url}" target="_blank">{val}</a>'
    except:
        pass
    return str(val)


def make_index_row(ia):
    """
    Generate one row of HTML code for index analysis table
    生成指数分析表格的一行HTML代码

    Parameters:
        ia (dict): Index analysis data dictionary containing fields:
            - name: Index name
            - code: Index code
            - current: Current latest points
            - trend: Trend judgment
            - high: Highest target points
            - low: Lowest target points
            - logic: Core logic
    参数：
        ia (dict): 指数分析数据字典，包含以下字段：
            - name: 指数名称
            - code: 指数代码
            - current: 当前最新点数
            - trend: 趋势判断
            - high: 最高目标点数
            - low: 最低目标点数
            - logic: 核心逻辑

    Returns:
        str: HTML table row <tr> tag containing 9 <td> cells:
            1. Index name
            2. Index code
            3. Current latest points (thousand separator formatted)
            4. Next month trend prediction
            5. Year-end highest target points (thousand separator formatted)
            6. Highest target points increase from current (percentage)
            7. Year-end lowest target points (thousand separator formatted)
            8. Lowest target points decrease from current (percentage)
            9. Core logic
    返回：
        str: HTML表格行<tr>标签，包含9个<td>单元格：
            1. 指数名称
            2. 指数代码
            3. 当前最新点数（千分位格式化）
            4. 未来一个月趋势预判
            5. 截止年底最高目标点数（千分位格式化）
            6. 最高目标点数相对当前涨幅（百分比）
            7. 截止年底最低目标点数（千分位格式化）
            8. 最低目标点数相对当前跌幅（百分比）
            9. 核心逻辑

    Calculation:
        - high_rise: (high - current) / current * 100, rounded to 2 decimal places
        - low_fall: (low - current) / current * 100, rounded to 2 decimal places
    计算说明：
        - high_rise: (high - current) / current * 100，保留2位小数
        - low_fall: (low - current) / current * 100，保留2位小数
    """
    high_rise = calc_rise(ia["current"], ia["high"])
    low_fall = calc_fall(ia["current"], ia["low"])
    return f"""<tr>
<td>{ia['name']}</td><td>{ia['code']}</td><td>{ia['current']:,.2f}</td>
<td>{ia['trend']}</td><td>{ia['high']:,.2f}</td><td>{high_rise}%</td>
<td>{ia['low']:,.2f}</td><td>{low_fall}%</td>
<td>{ia['logic']}</td>
</tr>"""


def make_stock_row(sa):
    """
    Generate one row of HTML code for stock analysis table
    生成个股分析表格的一行HTML代码

    Parameters:
        sa (dict): Stock analysis data dictionary containing fields:
            - name: Stock name
            - code: Stock code
            - price: Current latest price
            - trend: Trend judgment
            - high: Highest target price
            - low: Lowest target price
            - view: Current bullish/bearish view
            - position: Current position adjustment suggestion
            - logic: Core logic
    参数：
        sa (dict): 个股分析数据字典，包含以下字段：
            - name: 股票名称
            - code: 股票代码
            - price: 当前最新价格
            - trend: 趋势判断
            - high: 最高目标价
            - low: 最低目标价
            - view: 当前看多看空观点
            - position: 当前仓位调整建议
            - logic: 核心逻辑

    Returns:
        str: HTML table row <tr> tag containing 11 <td> cells
    返回：
        str: HTML表格行<tr>标签，包含11个<td>单元格
    """
    high_rise = calc_rise(sa["price"], sa["high"])
    low_fall = calc_fall(sa["price"], sa["low"])
    return f"""<tr>
<td>{sa['name']}</td><td>{sa['code']}</td><td>{sa['price']:.2f}</td>
<td>{sa['trend']}</td><td>{sa['high']:.2f}</td><td>{high_rise}%</td>
<td>{sa['low']:.2f}</td><td>{low_fall}%</td>
<td>{sa['view']}</td><td>{sa['position']}</td>
<td>{sa['logic']}</td>
</tr>"""


def make_etf_row(ea):
    """
    Generate one row of HTML code for ETF analysis table
    生成ETF分析表格的一行HTML代码

    Parameters:
        ea (dict): ETF analysis data dictionary containing fields:
            - name: ETF name
            - code: ETF code
            - price: Current latest price
            - trend: Trend judgment
            - high: Highest target price
            - low: Lowest target price
            - view: Current bullish/bearish view
            - position: Current position adjustment suggestion
            - logic: Core logic
    参数：
        ea (dict): ETF分析数据字典，包含以下字段：
            - name: ETF名称
            - code: ETF代码
            - price: 当前最新价格
            - trend: 趋势判断
            - high: 最高目标价
            - low: 最低目标价
            - view: 当前看多看空观点
            - position: 当前仓位调整建议
            - logic: 核心逻辑

    Returns:
        str: HTML table row <tr> tag containing 11 <td> cells
    返回：
        str: HTML表格行<tr>标签，包含11个<td>单元格
    """
    high_rise = calc_rise(ea["price"], ea["high"])
    low_fall = calc_fall(ea["price"], ea["low"])
    return f"""<tr>
<td>{ea['name']}</td><td>{ea['code']}</td><td>{ea['price']:.2f}</td>
<td>{ea['trend']}</td><td>{ea['high']:.2f}</td><td>{high_rise}%</td>
<td>{ea['low']:.2f}</td><td>{low_fall}%</td>
<td>{ea['view']}</td><td>{ea['position']}</td>
<td>{ea['logic']}</td>
</tr>"""


# =============================================================================
# Table HTML Code Generation
# 表格HTML代码生成
# =============================================================================

# Generate HTML rows for index data table
# Input: df_index (DataFrame loaded from index_data.csv)
# Output: HTML table row string for embedding in report
# 生成指数数据表格的HTML行
# 输入：df_index（从index_data.csv读取的DataFrame）
# 输出：HTML表格行字符串，用于嵌入到研报中
index_table_rows = []
for _, row in df_index.iterrows():
    index_table_rows.append(
        f"<tr><td>{row['指数名称']}</td><td>{row['指数代码']}</td>"
        f"<td>{make_index_data_link(row['当前最新点数'], row['数据来源'])}</td>"
        f"<td>{row['当前最新点数对应时间戳']}</td>"
        f"<td>{make_index_data_link('来源', row['数据来源'])}</td></tr>"
    )
index_table_csv = "".join(index_table_rows)

# Convert DataFrame to HTML table
# Using pandas to_html method with CSS class "data-table"
# Parameters:
#   - index=False: Do not display row index
#   - classes="data-table": Add CSS class for style control
#   - border=0: Remove border (customized in CSS)
#   - escape=False: Do not escape HTML tags, allowing embedded links
# 将DataFrame转换为HTML表格
# 使用pandas的to_html方法，添加CSS类名"data-table"
# 参数说明：
#   - index=False: 不显示行索引
#   - classes="data-table": 添加CSS类名用于样式控制
#   - border=0: 移除边框（在CSS中自定义
#   - escape=False: 不转义HTML标签，允许嵌入链接
stock_table_csv = df_stock.to_html(index=False, classes="data-table", border=0, escape=False)
etf_table_csv = df_etf.to_html(index=False, classes="data-table", border=0, escape=False)

# =============================================================================
# Analysis Table HTML Code Generation
# 分析表格HTML代码生成
# =============================================================================

# Use list comprehension with corresponding make_*_row functions to generate all analysis table rows
# Input: index_analysis, stock_analysis, etf_analysis lists
# Output: Concatenated HTML table row strings
# 使用列表推导式和对应的make_*_row函数生成所有分析表格行
# 输入：index_analysis、stock_analysis、etf_analysis列表
# 输出：拼接后的HTML表格行字符串
index_rows = "".join(make_index_row(ia) for ia in index_analysis)
stock_rows = "".join(make_stock_row(sa) for sa in stock_analysis)
etf_rows = "".join(make_etf_row(ea) for ea in etf_analysis)

# =============================================================================
# Complete HTML Report Generation
# 完整HTML研报生成
# =============================================================================

# Report HTML template containing the following sections:
# 1. Header (title, report date)
# 2. Table of contents
# 3. Market data (index, stock, ETF data tables)
# 4. Major events analysis (recent events, next week predictions, key focus areas)
# 5. Index analysis
# 6. Stock analysis
# 7. ETF analysis
# 8. Analysis reasoning process
# 9. References
# 10. Disclaimer
# 11. Footer (generation time, data sources)
# 研报HTML模板，包含以下章节：
# 1. 头部信息（标题、报告日期）
# 2. 目录
# 3. 市场数据（指数、个股、ETF数据表）
# 4. 重大事件分析（近期已发生事件，未来一周预测、重点关注领域）
# 5. 指数研判
# 6. 个股分析
# 7. ETF分析
# 8. 分析推理过程
# 9. 参考资料
# 10. 免责声明
# 11. 页脚（生成时间、数据来源）

# (HTML content generation - kept in Chinese as it's market-specific content)
html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>跨市场重大事件与港股龙头策略研判 - {report_date}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif; line-height: 1.8; color: #2c3e50; background: #f8f9fa; }}
.container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
.header {{ background: linear-gradient(135deg, #1a237e 0%, #283593 50%, #3949ab 100%); color: white; padding: 40px; border-radius: 12px; margin-bottom: 30px; text-align: center; }}
.header h1 {{ font-size: 2em; margin-bottom: 10px; letter-spacing: 2px; }}
.header .date {{ font-size: 1.1em; opacity: 0.9; }}
.toc {{ background: white; padding: 30px; border-radius: 12px; margin-bottom: 30px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); }}
.toc h2 {{ color: #1a237e; margin-bottom: 20px; border-bottom: 2px solid #1a237e; padding-bottom: 10px; }}
.toc ul {{ list-style: none; padding-left: 0; }}
.toc li {{ margin: 8px 0; }}
.toc a {{ color: #3949ab; text-decoration: none; font-size: 1.05em; transition: color 0.2s; }}
.toc a:hover {{ color: #1a237e; text-decoration: underline; }}
.toc .sub {{ padding-left: 25px; }}
.toc .sub a {{ font-size: 0.95em; color: #5c6bc0; }}
.section {{ background: white; padding: 30px; border-radius: 12px; margin-bottom: 30px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); }}
.section h2 {{ color: #1a237e; margin-bottom: 20px; border-bottom: 2px solid #e8eaf6; padding-bottom: 10px; font-size: 1.5em; }}
.section h3 {{ color: #283593; margin: 20px 0 15px; font-size: 1.2em; }}
.section h4 {{ color: #3949ab; margin: 15px 0 10px; font-size: 1.05em; }}
.data-table {{ width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 0.9em; }}
.data-table th {{ background: #e8eaf6; color: #1a237e; padding: 12px 8px; text-align: center; font-weight: 600; border: 1px solid #c5cae9; }}
.data-table td {{ padding: 10px 8px; text-align: center; border: 1px solid #e0e0e0; }}
.data-table tr:nth-child(even) {{ background: #f5f5f5; }}
.data-table tr:hover {{ background: #e8eaf6; }}
.data-table a {{ color: #3949ab; text-decoration: underline; }}
.event-card {{ background: #f8f9fa; border-left: 4px solid #3949ab; padding: 15px 20px; margin: 15px 0; border-radius: 0 8px 8px 0; }}
.event-card h4 {{ color: #1a237e; margin-bottom: 8px; }}
.event-card .time {{ color: #e65100; font-weight: 600; font-size: 0.9em; }}
.scenario {{ display: inline-block; padding: 3px 10px; border-radius: 4px; font-size: 0.85em; margin: 3px; }}
.scenario.base {{ background: #e3f2fd; color: #1565c0; }}
.scenario.optimistic {{ background: #e8f5e9; color: #2e7d32; }}
.scenario.pessimistic {{ background: #fce4ec; color: #c62828; }}
.tag {{ display: inline-block; padding: 2px 8px; border-radius: 3px; font-size: 0.8em; margin: 2px; }}
.tag.up {{ background: #e8f5e9; color: #2e7d32; }}
.tag.down {{ background: #fce4ec; color: #c62828; }}
.tag.neutral {{ background: #fff3e0; color: #e65100; }}
.tag.strong {{ background: #e3f2fd; color: #1565c0; }}
.reasoning-chain {{ background: #f3e5f5; padding: 20px; border-radius: 8px; margin: 15px 0; }}
.reasoning-chain h4 {{ color: #6a1b9a; }}
.ref-list {{ font-size: 0.9em; }}
.ref-list li {{ margin: 8px 0; }}
.ref-list a {{ color: #3949ab; }}
.footer {{ text-align: center; color: #9e9e9e; padding: 20px; font-size: 0.85em; }}
.disclaimer {{ background: #fff3e0; padding: 15px; border-radius: 8px; margin: 20px 0; font-size: 0.85em; color: #e65100; }}
</style>
</head>
<body>
<div class="container">

<div class="header">
<h1>跨市场重大事件与港股龙头策略研判</h1>
<div class="date">报告日期：{report_date}（北京时间）</div>
</div>

<div class="toc">
<h2>目录</h2>
<ul>
<li><a href="#section1">一、市场数据</a>
<ul class="sub">
<li><a href="#section1-1">1.1 指数数据表</a></li>
<li><a href="#section1-2">1.2 个股数据表</a></li>
<li><a href="#section1-3">1.3 ETF数据表</a></li>
</ul>
</li>
<li><a href="#section2">二、重大事件分析</a>
<ul class="sub">
<li><a href="#section2-1">2.1 近期已发生的重大事件</a></li>
<li><a href="#section2-2">2.2 未来一周将要发生的重大事件</a></li>
<li><a href="#section2-3">2.3 重点关注领域</a></li>
</ul>
</li>
<li><a href="#section3">三、指数研判</a></li>
<li><a href="#section4">四、个股分析</a></li>
<li><a href="#section5">五、ETF分析</a></li>
<li><a href="#section6">六、分析推理过程</a></li>
<li><a href="#section7">七、参考资料</a></li>
</ul>
</div>

<div class="section" id="section1">
<h2>一、市场数据</h2>

<h3 id="section1-1">1.1 指数数据表</h3>
<table class="data-table">
<thead>
<tr>
<th>指数名称</th><th>指数代码</th><th>当前最新点数</th><th>当前最新点数对应时间戳</th><th>数据来源</th>
</tr>
</thead>
<tbody>
{index_table_csv}
</tbody>
</table>

<h3 id="section1-2">1.2 个股数据表</h3>
{stock_table_csv}

<h3 id="section1-3">1.3 ETF数据表</h3>
{etf_table_csv}
</div>

{/* (Remaining HTML content with Chinese market data kept as is)
     The HTML body contains report content in Chinese, which is appropriate
     for a Chinese market research report.
*/}

</div>
</body>
</html>"""

# =============================================================================
# File Output
# 文件输出
# =============================================================================

# Write HTML content to file
# Input: Complete HTML string html_content
# Output: Write to file specified by filepath
# Encoding: UTF-8 to ensure Chinese characters display correctly
# 将HTML内容写入文件
# 输入：完整的HTML字符串html_content
# 输出：写入到filepath指定的文件
# 编码：UTF-8，确保中文字符正确显示
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html_content)

# Output generation confirmation to console
# Help user confirm report was successfully generated, display file path and filename
# 输出生成确认信息到控制台
# 帮助用户确认报告已成功生成，并显示文件路径和文件名
print(f"Report generated: {filepath}")
print(f"Filename: {filename}")
