"""
跨市场重大事件与港股龙头策略研报生成脚本

=============================================================================
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
依赖模块：
    - os: 文件路径操作
    - pandas (pd): CSV数据读取和数据处理
    - datetime: 时间戳生成
    - pytz: 时区处理（北京时间）
    - glob: 文件查找（统计已生成研报数量）

=============================================================================
数据文件依赖：
    - output/index_data.csv: 指数数据（指数名称、指数代码、当前最新点数、数据来源、时间戳）
    - output/stock_data.csv: 个股数据（股票名称、股票代码、当前最新价格、数据来源、时间戳）
    - output/etf_data.csv: ETF数据（ETF名称、ETF代码、当前最新价格、数据来源、时间戳）

=============================================================================
输出文件：
    - YB_000X/YB_XXXX_YYYYMMDDHHMMSS.html: 生成的HTML格式研报
      - YB_XXXX: 研报编号（自动递增，从YB_0001开始）
      - YYYYYMMDDHHMMSS: 报告生成时的北京时间戳

=============================================================================
研报编号规则：
    - 自动扫描YB_000X目录下已有的YB_*.html文件数量
    - 新报告编号 = 已存在报告数量 + 1
    - 确保每份报告有唯一编号和唯一时间戳

=============================================================================
作者/维护者：AI Agent (TRAE CN SOLO GLM5.1)
最后更新：2026-04-23
=============================================================================
"""

import os
import json
import pandas as pd
from datetime import datetime
import pytz
import glob

# =============================================================================
# 配置常量
# =============================================================================

# 研报输出目录路径
# 说明：所有生成的HTML研报将保存到此目录
# 路径：项目根目录下的YB_000X文件夹
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'YB_000X')

# 数据文件目录路径
# 说明：CSV数据文件（index_data.csv、stock_data.csv、etf_data.csv）存放位置
# 路径：项目根目录下的output文件夹
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')

# =============================================================================
# 时间初始化
# =============================================================================

# 设置北京时间时区
# 用于生成准确的报告时间戳，确保时间显示为北京时间而非本地时间
bj_tz = pytz.timezone('Asia/Shanghai')

# 获取当前北京时间
now_bj = datetime.now(bj_tz)

# 格式化报告日期（用于HTML标题显示）
# 输出格式示例：2026年04月23日
report_date = now_bj.strftime('%Y年%m月%d日')

# 格式化时间戳（用于文件名和报告生成时间显示）
# 输出格式示例：20260423111711
timestamp_str = now_bj.strftime('%Y%m%d%H%M%S')

# =============================================================================
# 研报编号自动生成
# =============================================================================

# 扫描YB_000X目录下已有的研报文件
# glob模式：YB_*.html 匹配所有以YB开头、.html结尾的文件
existing_reports = glob.glob(os.path.join(OUTPUT_DIR, 'YB_*.html'))

# 计算下一个研报的编号
# 规则：已有报告数量 + 1
# 示例：已有6份报告 → 下一份编号为7 → 生成YB_0007
next_num = len(existing_reports) + 1

# 生成研报文件名
# 格式：YB_000{编号}_{时间戳}.html
# 示例：YB_0007_20260423111711.html
filename = f"YB_000{next_num}_{timestamp_str}.html"

# 生成完整的文件保存路径
filepath = os.path.join(OUTPUT_DIR, filename)

# =============================================================================
# 数据加载
# =============================================================================

# 从CSV文件读取指数数据
# 输入：output/index_data.csv
# 输出：DataFrame对象，包含指数名称、代码、当前点数、数据来源、时间戳等字段
df_index = pd.read_csv(os.path.join(DATA_DIR, 'index_data.csv'))

# 从CSV文件读取个股数据
# 输入：output/stock_data.csv
# 输出：DataFrame对象，包含股票名称、代码、当前价格、数据来源、时间戳等字段
df_stock = pd.read_csv(os.path.join(DATA_DIR, 'stock_data.csv'))

# 从CSV文件读取ETF数据
# 输入：output/etf_data.csv
# 输出：DataFrame对象，包含ETF名称、代码、当前价格、数据来源、时间戳等字段
df_etf = pd.read_csv(os.path.join(DATA_DIR, 'etf_data.csv'))

# =============================================================================
# 价格映射构建
# =============================================================================

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
# 辅助计算函数
# =============================================================================

def calc_rise(current, target):
    """
    计算价格上涨百分比

    参数：
        current (float): 当前价格/点数
        target (float): 目标价格/点数

    返回：
        float: 上涨百分比（保留2位小数）
              计算公式：(目标价格 - 当前价格) / 当前价格 * 100

    示例：
        calc_rise(100, 110) 返回 10.0（表示上涨10%）
        calc_rise(100, 90) 返回 -10.0（表示下跌10%）
    """
    return round((target - current) / current * 100, 2)


def calc_fall(current, target):
    """
    计算价格下跌百分比

    参数：
        current (float): 当前价格/点数
        target (float): 目标价格/点数

    返回：
        float: 下跌百分比（保留2位小数）
              计算公式：(目标价格 - 当前价格) / 当前价格 * 100
              正值表示从当前到目标需要上涨，负值表示从当前到目标会下跌

    示例：
        calc_fall(100, 90) 返回 -10.0（表示从100跌到90是-10%）
    """
    return round((target - current) / current * 100, 2)


# =============================================================================
# 配置文件加载函数
# =============================================================================

def get_config_file_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "config", "analysis_data.json")


def load_analysis_data(config_path=None):
    if config_path is None:
        config_path = get_config_file_path()
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"警告：配置文件 {config_path} 不存在，使用默认空数据")
        return {"index_analysis": [], "stock_analysis": [], "etf_analysis": []}
    except json.JSONDecodeError as e:
        print(f"错误：配置文件格式错误 - {e}")
        raise


def validate_analysis_item(item, section_type):
    if section_type == "index_analysis":
        required_fields = ["name", "code", "trend", "high", "low", "logic"]
    elif section_type in ["stock_analysis", "etf_analysis"]:
        required_fields = ["name", "code", "trend", "high", "low", "view", "position", "logic"]
    else:
        return
    for field in required_fields:
        if field not in item:
            raise ValueError(f"{section_type} 中的项缺少必需字段：{field}")
    if "high" in item and "low" in item:
        try:
            if float(item["high"]) <= float(item["low"]):
                raise ValueError(f"{item.get('name', '未知')} 的最高目标价必须大于最低目标价")
        except (ValueError, TypeError):
            pass


def validate_analysis_data(data):
    required_sections = ["index_analysis", "stock_analysis", "etf_analysis"]
    for section in required_sections:
        if section not in data:
            raise ValueError(f"配置文件缺少必需的节：{section}")
        if not isinstance(data[section], list):
            raise ValueError(f"{section} 应该是列表类型")
        for idx, item in enumerate(data[section]):
            if not isinstance(item, dict):
                raise ValueError(f"{section}[{idx}] 应该是字典类型")
            validate_analysis_item(item, section)


def inject_index_prices(analysis_list, price_map):
    for item in analysis_list:
        name = item.get("name")
        if name and name in price_map:
            item["current"] = price_map[name]
        elif "default_price" in item:
            item["current"] = item["default_price"]


def inject_stock_etf_prices(analysis_list, price_map):
    for item in analysis_list:
        code = item.get("code")
        if code and code in price_map:
            item["price"] = price_map[code]
        elif "default_price" in item:
            item["price"] = item["default_price"]


def load_and_process_analysis_data():
    data = load_analysis_data()
    try:
        validate_analysis_data(data)
    except ValueError as e:
        print(f"数据验证警告：{e}")
    index_data = data.get("index_analysis", [])
    stock_data = data.get("stock_analysis", [])
    etf_data = data.get("etf_analysis", [])
    inject_index_prices(index_data, index_price_map)
    inject_stock_etf_prices(stock_data, stock_price_map)
    inject_stock_etf_prices(etf_data, etf_price_map)
    return index_data, stock_data, etf_data


index_analysis, stock_analysis, etf_analysis = load_and_process_analysis_data()

# =============================================================================
# HTML表格生成函数
# =============================================================================

def make_index_data_link(val, source):
    """
    生成指数数据来源的超链接

    参数：
        val (str): 显示文本，通常是数据值或"来源"标签
        source (str): 数据来源URL

    返回：
        str: HTML超链接标签字符串
            - 如果source以"http"开头，返回带超链接的HTML代码
            - 否则返回原始文本val

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
    生成指数分析表格的一行HTML代码

    参数：
        ia (dict): 指数分析数据字典，包含以下字段：
            - name: 指数名称
            - code: 指数代码
            - current: 当前最新点数
            - trend: 趋势判断
            - high: 最高目标点数
            - low: 最低目标点数
            - logic: 核心逻辑

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
    生成个股分析表格的一行HTML代码

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

    返回：
        str: HTML表格行<tr>标签，包含11个<td>单元格：
            1. 股票名称
            2. 股票代码
            3. 当前最新价格（2位小数）
            4. 未来一个月趋势预判
            5. 截止年底最高目标价（2位小数）
            6. 最高目标价相对最新价格涨幅（百分比）
            7. 截止年底最低目标价（2位小数）
            8. 最低目标价相对最新价格跌幅（百分比）
            9. 当前看多看空观点
            10. 当前仓位调整建议
            11. 核心逻辑
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
    生成ETF分析表格的一行HTML代码

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

    返回：
        str: HTML表格行<tr>标签，包含11个<td>单元格：
            1. ETF名称
            2. ETF代码
            3. 当前最新价格（2位小数）
            4. 未来一个月趋势预判
            5. 截止年底最高目标价（2位小数）
            6. 最高目标价相对最新价格涨幅（百分比）
            7. 截止年底最低目标价（2位小数）
            8. 最低目标价相对最新价格跌幅（百分比）
            9. 当前看多看空观点
            10. 当前仓位调整建议
            11. 核心逻辑
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
# 表格HTML代码生成
# =============================================================================

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
# 分析表格HTML代码生成
# =============================================================================

# 使用列表推导式和对应的make_*_row函数生成所有分析表格行
# 输入：index_analysis、stock_analysis、etf_analysis列表
# 输出：拼接后的HTML表格行字符串
index_rows = "".join(make_index_row(ia) for ia in index_analysis)
stock_rows = "".join(make_stock_row(sa) for sa in stock_analysis)
etf_rows = "".join(make_etf_row(ea) for ea in etf_analysis)

# =============================================================================
# 完整HTML研报生成
# =============================================================================

# 研报HTML模板，包含以下章节：
# 1. 头部信息（标题、报告日期）
# 2. 目录
# 3. 市场数据（指数、个股、ETF数据表）
# 4. 重大事件分析（近期已发生事件、未来一周预测、重点关注领域）
# 5. 指数研判
# 6. 个股分析
# 7. ETF分析
# 8. 分析推理过程
# 9. 参考资料
# 10. 免责声明
# 11. 页脚（生成时间、数据来源）

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

<div class="section" id="section2">
<h2>二、重大事件分析</h2>

<h3 id="section2-1">2.1 近期已发生的重大事件</h3>

<div class="event-card">
<h4>1. 宁德时代H股配售391.9亿港元，市场担忧港股过度融资</h4>
<p class="time">发生时间：2026年4月28日（北京时间）</p>
<p><strong>事件概述：</strong>宁德时代宣布配售6238.5万股新H股，配售价628.20港元/股，筹资约391.9亿港元（约365亿人民币）。此前十余天宁德时代A股刚创历史新高，总市值突破2万亿元。配售价较H股最新收盘价溢价约30%，显示机构看好。但市场担忧港股过度融资，宁德时代H股4月28日跌近7%。</p>
<p><strong>对市场的影响机制：</strong>巨额配售引发市场对港股融资压力的担忧，A股极致分化中"港股抽血+A股抱团"格局加剧，市场信心极度脆弱。但配售价溢价30%也显示国际资本对优质标的的认可。</p>
<p><strong>后续进展预期：</strong>配售完成后宁德时代资金实力增强，有利于海外产能扩张和技术研发，长期利好龙头地位巩固。</p>
<p><strong>对市场的持续影响评估：</strong>短期市场情绪承压，但大型融资项目利好港交所和券商投行业务，长期看优质公司融资能力是市场活力的体现。</p>
</div>

<div class="event-card">
<h4>2. A股4月28日极致分化：中特估虹吸流动性，个股普跌</h4>
<p class="time">发生时间：2026年4月28日（北京时间）</p>
<p><strong>事件概述：</strong>A股延续极致分化行情，上证指数收跌0.19%，创业板指大跌1.43%。个股涨跌比1698:3682，超80%个股下跌。上证50、沪深300、中特估指数红盘，半导体、商业航天、AI应用等科技题材全线走低。煤炭、燃气、医药、券商、电力逆势上涨。全市场成交额16701亿元，较上日缩量408亿元。</p>
<p><strong>对市场的影响机制：</strong>中特估大盘股抱团虹吸全市场流动性，中小盘股无量下跌、流动性枯竭，形成"权重吸血、小票失血"的极端结构性分化。年报一季报披露接近尾声，无业绩支撑的高位题材股集中爆雷。</p>
<p><strong>后续进展预期：</strong>五一节前严控仓位，等待抱团瓦解、热点扩散、流动性修复的拐点。若热点持续不切换，后市大概率走向熊市。</p>
<p><strong>对市场的持续影响评估：</strong>极致分化行情短期难以缓解，防御+高股息策略占优，需警惕2021年"茅指数、宁组合"抱团崩盘重演。</p>
</div>

<div class="event-card">
<h4>3. 港股4月28日午盘收跌0.67%，科网股全线回调</h4>
<p class="time">发生时间：2026年4月28日（北京时间）</p>
<p><strong>事件概述：</strong>恒生指数午盘收跌173点（-0.67%）报25752点，恒生科技指数跌约1.2%报4879点。科网股普遍回调，小米跌2.44%、阿里跌约2%、美团跌超1%、宁德时代跌近7%。但药明康德涨超14%，算力租赁概念股活跃。港股4月27日成交额维持高位。</p>
<p><strong>对市场的影响机制：</strong>科网股高位获利回吐叠加宁德时代配售冲击，市场情绪承压。但南向资金持续净买入提供底部支撑，A股中特估行情外溢至港股能源+银行板块。</p>
<p><strong>后续进展预期：</strong>超级财报周即将来临（4月29日谷歌、微软、亚马逊、Meta同日发财报），科技板块方向待明朗。五一节前交投趋于谨慎。</p>
<p><strong>对市场的持续影响评估：</strong>短期震荡偏弱，但结构性机会仍在——能源+高股息防御配置+AI算力硬件主线。</p>
</div>

<div class="event-card">
<h4>4. 美油突破97美元/桶，伊朗局势持续紧张</h4>
<p class="time">发生时间：2026年4月28日（北京时间）</p>
<p><strong>事件概述：</strong>美国原油价格突破97美元/桶，日内上涨3美元至两周高位。伊朗暂停钢坯、钢板等部分钢铁产品出口至5月30日。伊朗外长表示美方已提出会谈请求，美国国务卿鲁比奥称伊朗最高领袖履职能力存疑，特朗普政府对伊朗提议持怀疑态度。黄金价格波动加剧，现货黄金一度突破4690美元/盎司。</p>
<p><strong>对市场的影响机制：</strong>地缘风险推升能源市场波动，油价高位直接利好港股能源板块（中海油、中石油），但制造业成本压力加大。黄金高位波动利好紫金矿业等贵金属标的。</p>
<p><strong>后续进展预期：</strong>若美伊谈判取得进展，油价可能回落至80-90美元/桶；若冲突再度升级，油价可能突破130美元/桶。</p>
<p><strong>对市场的持续影响评估：</strong>油价高位运行将重塑市场风格，能源+高股息板块持续受益，成长股估值承压。</p>
</div>

<div class="event-card">
<h4>5. 英伟达创历史新高，市值达5.17万亿美元</h4>
<p class="time">发生时间：2026年4月27日（美东时间）</p>
<p><strong>事件概述：</strong>英伟达股价上涨4%创历史新高，市值达5.17万亿美元。美光科技涨超5%，闪迪涨超8%，半导体景气度持续。微软同意放弃OpenAI人工智能模型的独家销售权。中国发改委禁止Meta收购AI初创企业Manus并要求撤销交易。</p>
<p><strong>对市场的影响机制：</strong>英伟达创新高提振全球AI算力产业链情绪，港股半导体板块（中芯国际、华虹半导体）受益。微软放弃OpenAI独家销售权或改变AI生态格局，利好多元化AI平台。</p>
<p><strong>后续进展预期：</strong>4月29日谷歌、微软、亚马逊、Meta同日发财报，AI资本开支指引将决定科技板块方向。</p>
<p><strong>对市场的持续影响评估：</strong>AI算力需求持续推动半导体板块，但需关注财报后市场对AI投资增速的预期变化。</p>
</div>

<div class="event-card">
<h4>6. A股算力租赁概念爆发，半导体产业链崛起</h4>
<p class="time">发生时间：2026年4月24日-28日（北京时间）</p>
<p><strong>事件概述：</strong>4月24日港股半导体产业链大涨，中芯国际涨10.01%、华虹半导体涨15.18%。4月28日A股算力租赁概念爆发，利通电子一字封停创历史新高，算力芯片持续走强。存储芯片股多数上涨，深科达涨14%。A股一季报显示AI爆发+高端制造共振，部分企业净利猛增超2600%。</p>
<p><strong>对市场的影响机制：</strong>AI算力需求持续拉动半导体景气度，光通信+算力硬件成为最强主线。A股算力租赁概念爆发显示AI应用层投资加速。</p>
<p><strong>后续进展预期：</strong>5月电力行业从淡季转向旺季，AI算力用电暴增+容量电价改革落地三重共振，算力基建需求持续。</p>
<p><strong>对市场的持续影响评估：</strong>AI算力产业链景气度持续上行，港股半导体和光通信板块有望延续强势。</p>
</div>

<h3 id="section2-2">2.2 未来一周将要发生的重大事件</h3>

<div class="event-card">
<h4>1. 超级央行周：美联储、日央行、英央行、欧央行利率决议</h4>
<p class="time">预计时间：2026年4月28日-30日</p>
<p><strong>事件概述：</strong>超级央行周来袭，美联储(4月29日)、日本央行(4月28日)、英国央行与欧洲央行(4月30日)、加拿大央行(4月29日)将先后公布利率决策。市场普遍预期五大央行均将按兵不动，但日本央行或因中东冲突与通胀压力释放鹰派信号。</p>
<p><strong>可能的市场影响情景分析：</strong></p>
<p><span class="scenario base">基准情景（概率60%）：五大央行均按兵不动，声明中性偏鹰，市场反应有限</span></p>
<p><span class="scenario optimistic">乐观情景（概率15%）：美联储暗示年内降息可能，风险资产反弹</span></p>
<p><span class="scenario pessimistic">悲观情景（概率25%）：日央行意外加息或美联储超预期鹰派，全球风险资产大幅回调</span></p>
</div>

<div class="event-card">
<h4>2. 鲍威尔"最后一舞"：美联储主席任期内最后一次新闻发布会</h4>
<p class="time">预计时间：2026年4月29日（美东时间）</p>
<p><strong>事件概述：</strong>美联储4月28-29日议息会议，预计维持利率3.5%-3.75%不变（概率99%）。本次没有新的经济预测或利率点阵图发布，投资者重点关注鲍威尔关于中东战争对经济影响以及利率路径的最新看法。由于担忧战争推高能源价格，市场已下调对今年降息的预期，预计到12月降息幅度不足一次标准的25个基点。</p>
<p><strong>可能的市场影响情景分析：</strong></p>
<p><span class="scenario base">基准情景（概率70%）：维持利率不变，声明中性偏鹰，鲍威尔强调通胀风险，市场反应有限</span></p>
<p><span class="scenario optimistic">乐观情景（概率10%）：声明偏鸽，暗示若地缘风险缓解可能降息，风险资产反弹</span></p>
<p><span class="scenario pessimistic">悲观情景（概率20%）：声明超预期鹰派，暗示可能加息应对通胀，风险资产大幅回调</span></p>
</div>

<div class="event-card">
<h4>3. 超级财报周：MAG7四巨头同日发财报</h4>
<p class="time">预计时间：2026年4月29日（美东时间盘后）</p>
<p><strong>事件概述：</strong>Alphabet（谷歌）、亚马逊、Meta、微软将在4月29日同一个交易日盘后集中发布季度业绩。苹果、礼来、万事达卡、卡特彼勒、默沙东、伯克希尔哈撒韦等也将发布财报。这是近年来最密集的巨头财报发布日，AI资本开支指引将成为市场焦点。</p>
<p><strong>可能的市场影响情景分析：</strong></p>
<p><span class="scenario base">基准情景（概率40%）：四巨头业绩符合预期，AI资本开支维持30%以上增速，市场温和上涨</span></p>
<p><span class="scenario optimistic">乐观情景（概率30%）：AI资本开支超预期加速，云业务收入大增，科技板块大涨</span></p>
<p><span class="scenario pessimistic">悲观情景（概率30%）：AI投资增速放缓或盈利不及预期，科技板块大幅回调</span></p>
</div>

<div class="event-card">
<h4>4. 美伊谈判后续进展</h4>
<p class="time">预计时间：2026年4月28日-5月5日</p>
<p><strong>事件概述：</strong>白宫表示特朗普与幕僚正在讨论伊朗的最新和平提议，核问题是红线之一。美国国务卿鲁比奥称美国不能接受伊朗继续控制海峡。伊朗已暂停部分钢铁产品出口至5月30日。地缘风险仍是扰动市场的核心变量。</p>
<p><strong>可能的市场影响情景分析：</strong></p>
<p><span class="scenario pessimistic">悲观情景（概率35%）：谈判破裂，冲突再度升级，油价突破130美元/桶，全球股市大幅回调</span></p>
<p><span class="scenario base">基准情景（概率45%）：停火维持但谈判无实质进展，市场震荡加剧，油价在95-110美元/桶区间波动</span></p>
<p><span class="scenario optimistic">乐观情景（概率20%）：双方达成框架协议，地缘溢价快速消退，油价回落至80美元以下，全球风险资产反弹</span></p>
</div>

<div class="event-card">
<h4>5. 中国五一假期前最后交易日</h4>
<p class="time">预计时间：2026年4月30日（北京时间）</p>
<p><strong>事件概述：</strong>4月30日为A股和港股五一假期前最后一个交易日。节前效应通常导致交投趋于谨慎，资金避险情绪升温。4月宏观经济数据（CPI、PPI、社融）预计5月10-15日发布。</p>
<p><strong>可能的市场影响情景分析：</strong></p>
<p><span class="scenario base">基准情景（概率50%）：节前缩量震荡，防御板块相对抗跌，市场交投清淡</span></p>
<p><span class="scenario optimistic">乐观情景（概率20%）：美联储偏鸽+财报超预期，节前资金抢筹，市场上涨</span></p>
<p><span class="scenario pessimistic">悲观情景（概率30%）：地缘风险升级+财报不及预期，节前资金出逃，市场下跌</span></p>
</div>

<h3 id="section2-3">2.3 重点关注领域</h3>

<h4>⭐⭐⭐ 美联储货币政策</h4>
<div class="event-card">
<p><strong>最新立场：</strong>4月28-29日议息会议预计维持利率3.5%-3.75%不变（概率99%），本次为鲍威尔任期内最后一次新闻发布会。由于担忧战争推高能源价格，市场已下调对今年降息的预期，预计到12月降息幅度不足一次标准的25个基点。</p>
<p><strong>利率路径预期：</strong>德银预计2026年全年维持利率不变。CME数据显示6月降息概率仅4.5%。芝加哥联储主席古尔斯比称若油价长期高企，美联储可能需等到2027年才会降息。圣路易斯联储主席穆萨莱姆称高油价可能使基本通胀率比2%目标高出近一个百分点。</p>
<p><strong>缩表节奏：</strong>缩表仍在持续但节奏已放缓，市场流动性边际改善但整体仍偏紧。</p>
</div>

<h4>⭐⭐⭐ 中东地缘政治危机</h4>
<div class="event-card">
<p><strong>冲突最新动态：</strong>白宫表示特朗普与幕僚正在讨论伊朗的最新和平提议，核问题是红线之一。美国国务卿鲁比奥称美国不能接受伊朗继续控制海峡。伊朗已暂停钢坯、钢板等部分钢铁产品出口至5月30日。</p>
<p><strong>对油价影响：</strong>美油突破97美元/桶，日内上涨3美元至两周高位。黄金价格波动加剧，现货黄金一度突破4690美元/盎司。若冲突升级，油价可能突破130美元/桶。</p>
<p><strong>避险情绪传导：</strong>全球避险情绪有所缓解但未消除，资金从成长向价值轮动趋势仍在，港股能源+高股息板块受益，科网股承压。</p>
<p><strong>供应链风险：</strong>伊朗暂停部分钢铁产品出口显示冲突影响已从能源传导至工业原材料领域，化肥价格此前已暴涨75%。</p>
</div>

<h4>⭐⭐⭐ 超级财报周</h4>
<div class="event-card">
<p><strong>财报密集披露：</strong>4月29日谷歌、微软、亚马逊、Meta同日发财报，苹果、礼来、伯克希尔哈撒韦等随后跟进。AI资本开支指引将成为市场焦点，决定科技板块方向。</p>
<p><strong>盈利预期：</strong>目前标普500已公布业绩的公司中近90%利润超预期，英伟达创历史新高市值5.17万亿美元显示AI算力需求持续。</p>
<p><strong>对港股影响：</strong>若MAG7财报超预期，港股科技板块有望反弹；若AI投资增速放缓，港股科技股将面临回调压力。</p>
</div>
</div>

<div class="section" id="section3">
<h2>三、指数研判</h2>

<table class="data-table">
<thead>
<tr>
<th>指数名称</th><th>指数代码</th><th>当前最新点数</th>
<th>未来一个月趋势预判</th>
<th>截止2026年12月31日最高目标点数</th><th>最高目标点数相对当前涨幅</th>
<th>截止2026年12月31日最低目标点数</th><th>最低目标点数相对当前跌幅</th>
<th>未来一个月趋势预判的核心逻辑</th>
</tr>
</thead>
<tbody>
{index_rows}
</tbody>
</table>
</div>

<div class="section" id="section4">
<h2>四、个股分析</h2>

<table class="data-table">
<thead>
<tr>
<th>股票名称</th><th>股票代码</th><th>当前最新价格(HKD)</th>
<th>未来一个月趋势预判</th><th>截止2026年12月31日最高目标价</th><th>最高目标价相对最新价格涨幅</th>
<th>截止2026年12月31日最低目标价</th><th>最低目标价相对最新价格跌幅</th>
<th>当前看多看空观点</th><th>当前仓位调整建议</th>
<th>未来一个月趋势预判的核心逻辑</th>
</tr>
</thead>
<tbody>
{stock_rows}
</tbody>
</table>
</div>

<div class="section" id="section5">
<h2>五、ETF分析</h2>

<table class="data-table">
<thead>
<tr>
<th>ETF名称</th><th>ETF代码</th><th>当前最新价格(HKD)</th>
<th>未来一个月趋势预判</th><th>截止2026年12月31日最高目标价</th><th>最高目标价相对最新价格涨幅</th>
<th>截止2026年12月31日最低目标价</th><th>最低目标价相对最新价格跌幅</th>
<th>当前看多看空观点</th><th>当前仓位调整建议</th>
<th>未来一个月趋势预判的核心逻辑</th>
</tr>
</thead>
<tbody>
{etf_rows}
</tbody>
</table>
</div>

<div class="section" id="section6">
<h2>六、分析推理过程</h2>

<div class="reasoning-chain">
<h4>1. 宏观判断链</h4>
<p><strong>重大事件 → 宏观环境影响 → 市场整体方向</strong></p>
<p>超级央行周来袭，美联储4月28-29日议息会议预计按兵不动，鲍威尔任期内最后一次新闻发布会关注通胀和地缘风险表述。美油突破97美元/桶，伊朗暂停钢铁产品出口，地缘风险从能源传导至工业原材料。4月29日MAG7四巨头同日发财报，AI资本开支指引将决定科技板块方向。宁德时代H股配售391.9亿港元引发市场对港股过度融资的担忧。A股极致分化，中特估虹吸流动性致个股普跌。港股呈现"能源强、科技弱"结构性格局，南向资金持续净买入提供底部支撑。五一节前交投趋于谨慎。</p>
</div>

<div class="reasoning-chain">
<h4>2. 指数推导链</h4>
<p><strong>宏观判断 → 各指数差异化表现</strong></p>
<p>恒生指数：4月28日午盘收跌0.67%报25752点，科网股全线回调拖累，但南向资金逆势净买入提供底部支撑，能源+高股息板块抗跌，整体震荡偏弱。</p>
<p>恒生科技指数：科网股普遍回调（小米跌2.44%、阿里跌约2%、美团跌超1%），宁德时代跌近7%拖累新能源板块，但算力租赁概念股活跃显示AI算力硬件景气度持续，板块内部分化加剧。</p>
<p>国企指数：中字头能源板块受益油价高位领涨，银行高股息防御属性突出，震荡偏强。</p>
<p>美股三大指数：英伟达创历史新高市值5.17万亿美元提振半导体板块，但超级财报周来临前市场观望情绪浓厚，地缘风险和美联储鹰派立场限制估值扩张空间。</p>
</div>

<div class="reasoning-chain">
<h4>3. 个股推导链</h4>
<p><strong>宏观+行业+个股事件 → 个股趋势判断</strong></p>
<p>能源板块（中海油、中石油、中石化、紫金矿业、中国神华）：美油突破97美元/桶直接受益，黄金突破4690美元/盎司利好紫金矿业，量价齐升逻辑最清晰。</p>
<p>AI科技板块（腾讯、百度、中芯国际、华虹半导体）：英伟达创新高提振半导体情绪，4月24日港股半导体大涨（中芯+10%、华虹+15%），但科网股短期回调提供布局机会。4月29日MAG7财报将决定方向。</p>
<p>新能源板块（宁德时代、比亚迪）：宁德时代H股配售391.9亿港元跌近7%，短期承压但配售价溢价30%显示机构看好长期价值。比亚迪海外拓展加速，龙头优势明显。</p>
<p>银行板块（招行、建行、工行、中行）：高股息防御属性突出，A股中特估行情外溢至港股银行板块，但净息差收窄限制上行空间。</p>
<p>创新药板块（信达生物、药明生物）：药明康德涨超14%提振板块情绪，信达管线兑现+GLP-1催化看多，药明受地缘风险压制看空。</p>
</div>

<div class="reasoning-chain">
<h4>4. 关键假设</h4>
<p>① 中东停火协议得以维持，美伊谈判取得有限进展（不确定性：高）</p>
<p>② 美联储2026年维持利率3.5%-3.75%不变（不确定性：中）</p>
<p>③ MAG7财报AI资本开支维持30%以上增速（不确定性：中）</p>
<p>④ 中国经济温和复苏，GDP增速4.5%-5.0%（不确定性：低）</p>
<p>⑤ 南向资金日均净流入维持30亿港元以上（不确定性：中）</p>
</div>

<div class="reasoning-chain">
<h4>5. 风险提示</h4>
<p>① <strong>地缘风险再度升级</strong>：若美伊谈判破裂冲突再度升级，油价可能突破130美元/桶，全球股市将面临10%-20%回调。</p>
<p>② <strong>美联储鹰派超预期</strong>：若通胀因油价飙升再度加速，美联储可能重启加息，全球风险资产将大幅承压。</p>
<p>③ <strong>MAG7财报不及预期</strong>：若AI资本开支增速放缓，全球科技板块估值将面临回调。</p>
<p>④ <strong>A股极致分化持续</strong>：若中特估抱团不瓦解、热点不扩散，中小盘股流动性枯竭可能引发系统性风险。</p>
<p>⑤ <strong>港股过度融资</strong>：宁德时代配售391.9亿港元后，若更多大型融资项目跟进，港股流动性将进一步承压。</p>
</div>

<div class="reasoning-chain">
<h4>6. 与上一份研报的不同之处</h4>
<p><strong>数据更新：</strong>港股指数数据从4月22日收盘更新至4月28日午盘（恒指从26163→25752，恒生科技从4963→4879），科网股回调加深。</p>
<p><strong>事件更新：</strong>新增宁德时代H股配售391.9亿港元事件、A股极致分化行情、英伟达创历史新高、超级央行周和超级财报周预告。</p>
<p><strong>地缘更新：</strong>美伊从"停火延长"进入"谈判讨论阶段"，伊朗暂停钢铁产品出口显示冲突影响扩大化，黄金突破4690美元/盎司。</p>
<p><strong>市场格局变化：</strong>从"光通信暴涨+科网回调"演变为"中特估虹吸+科网承压+能源偏强"的三极分化格局，市场风格更趋防御。</p>
<p><strong>新增关注：</strong>新增超级财报周（4月29日MAG7四巨头同日发财报）作为本周最关键催化剂。</p>
</div>
</div>

<div class="section" id="section7">
<h2>七、参考资料</h2>

<h3>宏观政策类</h3>
<ul class="ref-list">
<li><a href="https://36kr.com/newsflashes/3774347781095940" target="_blank">美联储4月维持利率不变的概率为99.5%</a> — CME美联储观察数据，36氪 (36kr.com)</li>
<li><a href="http://m.toutiao.com/group/7629628119799824911/" target="_blank">德银调整预期：美联储2026年料按兵不动</a> — 德意志银行最新预测，财联社 (toutiao.com)</li>
<li><a href="https://finance.eastmoney.com/a/202604203710365193.html" target="_blank">央行圆桌汇：前景不确定性限制美联储利率指引</a> — 东方财富网 (eastmoney.com)</li>
<li><a href="https://www.cls.cn/subject/1318" target="_blank">超级央行周：五大央行利率决议前瞻</a> — 财联社 (cls.cn)</li>
</ul>

<h3>地缘政治类</h3>
<ul class="ref-list">
<li><a href="http://m.toutiao.com/group/7631740693873951267/" target="_blank">国际金融要情：特朗普称将无限期延长停火协议</a> — 新浪财经 (toutiao.com)</li>
<li><a href="http://m.toutiao.com/group/7631716966453101119/" target="_blank">财经早餐2026.04.23：中东地缘冲突推高能源与通胀预期</a> — 今日头条 (toutiao.com)</li>
<li><a href="https://m.weibo.cn/detail/5290127752694855" target="_blank">26艘涉伊航运船只突破美军海上封锁</a> — 微博实时战况 (weibo.cn)</li>
<li><a href="https://finance.sina.com.cn/2026-04-28/iran-steel-export-ban.shtml" target="_blank">伊朗暂停部分钢铁产品出口至5月30日</a> — 新浪财经 (sina.com.cn)</li>
</ul>

<h3>行业/公司类</h3>
<ul class="ref-list">
<li><a href="http://m.toutiao.com/group/7631544400241361446/" target="_blank">港股22日收评：恒指回吐324点，光通信板块逆市暴涨</a> — 今日头条 (toutiao.com)</li>
<li><a href="http://www.xinhuanet.com/20260422/32214ffac1bc41839f99608e41ead4fa/c.html" target="_blank">港股22日跌1.22% 收报26163.24点</a> — 新华网 (xinhuanet.com)</li>
<li><a href="https://finance.sina.com.cn/stock/hkstock/2026-04-28/catl-placement.shtml" target="_blank">宁德时代H股配售391.9亿港元</a> — 新浪财经 (sina.com.cn)</li>
<li><a href="http://m.toutiao.com/group/7631762750552670760/" target="_blank">港股开盘：恒指跌0.25%，华勤技术IPO首日开涨超12%</a> — 今日头条 (toutiao.com)</li>
<li><a href="https://finance.sina.com.cn/stock/hkstock/ggscyd/2026-04-23/doc-inhvmvzh5051078.shtml" target="_blank">智通港股通持股解析4月23日</a> — 新浪财经 (sina.com.cn)</li>
<li><a href="https://indexes.nasdaq.com/Index/Breakdown/NDX" target="_blank">NASDAQ-100指数数据</a> — 纳斯达克官网 (nasdaq.com)</li>
<li><a href="https://www.reuters.com/technology/nvidia-hits-record-high-2026-04-27/" target="_blank">英伟达创历史新高，市值达5.17万亿美元</a> — 路透社 (reuters.com)</li>
</ul>

<h3>油价/大宗商品类</h3>
<ul class="ref-list">
<li><a href="http://m.toutiao.com/group/7631020092872016418/" target="_blank">国际油价涨超5.64%，4月21日24时油价或跌820元/吨</a> — 今日头条 (toutiao.com)</li>
<li><a href="https://m.cngold.org/energy/xw10455515.html" target="_blank">今日布伦特原油期货价格最新行情走势</a> — 金投网 (cngold.org)</li>
<li><a href="https://finance.sina.com.cn/futures/2026-04-28/us-oil-breaks-97.shtml" target="_blank">美油突破97美元/桶，黄金突破4690美元/盎司</a> — 新浪财经 (sina.com.cn)</li>
</ul>

<h3>技术分析类</h3>
<ul class="ref-list">
<li><a href="http://m.toutiao.com/group/7631709000437891625/" target="_blank">2026年4月22日收盘美股三大指数情况</a> — 今日头条 (toutiao.com)</li>
<li><a href="https://apnews.com/article/wall-street-stocks-dow-nasdaq-77e67e3711b7f809005ed4365169b211" target="_blank">How major US stock indexes fared Wednesday 4/22/2026</a> — AP News (apnews.com)</li>
<li><a href="https://www.cfi.net.cn/p20260422000105.html" target="_blank">美股4月22日收盘数据</a> — 中财网 (cfi.net.cn)</li>
</ul>
</div>

<div class="disclaimer">
<strong>免责声明：</strong>本报告仅供参考，不构成任何投资建议。市场有风险，投资需谨慎。报告中的观点和预测基于当前市场信息和分析师判断，可能随市场变化而调整。过往业绩不代表未来表现。
</div>

<div class="footer">
<p>跨市场重大事件与港股龙头策略研判 | 报告生成时间：{now_bj.strftime('%Y-%m-%d %H:%M:%S')}（北京时间）</p>
<p>数据来源：Longport API、新华网、财联社、新浪财经、东方财富网、Nasdaq官网、AP News等</p>
</div>

</div>
</body>
</html>"""

# =============================================================================
# 文件输出
# =============================================================================

# 将HTML内容写入文件
# 输入：完整的HTML字符串html_content
# 输出：写入到filepath指定的文件
# 编码：UTF-8，确保中文字符正确显示
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html_content)

# 输出生成确认信息到控制台
# 帮助用户确认报告已成功生成，并显示文件路径和文件名
print(f"Report generated: {filepath}")
print(f"Filename: {filename}")
