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
filename = f"YB_{next_num:04d}_{timestamp_str}.html"

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


def format_trend_probs(probs):
    """
    格式化趋势概率分布为HTML显示字符串

    参数：
        probs (dict): 趋势概率字典，包含6种趋势及其概率值

    返回：
        str: 格式化的HTML字符串，显示6种趋势及其概率
    """
    if not probs:
        return ""
    trend_order = ["震荡上行", "震荡偏强", "震荡偏弱", "震荡下行", "直接上行", "直接下行"]
    parts = []
    for trend in trend_order:
        prob = probs.get(trend, 0)
        parts.append(f"{trend}({prob}%)")
    return "<br>".join(parts)


def make_index_text(ia):
    """
    生成指数分析的文字描述（不含表格）

    参数：
        ia (dict): 指数分析数据字典，包含以下字段：
            - name: 指数名称
            - code: 指数代码
            - current: 当前最新点数
            - trend: 趋势判断
            - trend_probs: 趋势概率分布
            - trend_reasons: 趋势情景理由
            - high: 最高目标点数
            - low: 最低目标点数
            - logic: 核心逻辑

    返回：
        str: HTML格式的指数文字描述
    """
    probs = ia.get('trend_probs', {})
    reasons = ia.get('trend_reasons', {})
    
    trend_items = []
    for scenario, prob in probs.items():
        reason = reasons.get(scenario, "")
        if reason:
            trend_items.append(f"<li><strong>{scenario}（{prob}%）</strong>：{reason}</li>")
        else:
            trend_items.append(f"<li><strong>{scenario}（{prob}%）</strong></li>")
    
    trend_list = "\n".join(trend_items)
    
    return f"""
<div style="margin-bottom: 25px; padding: 20px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #1a237e;">
<h4 style="color: #1a237e; margin-bottom: 10px;">{ia['name']}（{ia['code']}）| 当前点位：{ia['current']:,.2f}</h4>
<p style="margin: 8px 0;"><strong>未来半年趋势预判：</strong></p>
<ul style="margin: 8px 0 8px 25px; padding-left: 0;">{trend_list}</ul>
<p style="margin: 8px 0;"><strong>核心逻辑：</strong>{ia['logic']}</p>
</div>
"""


def make_stock_row(sa):
    """
    生成个股分析表格的一行HTML代码

    参数：
        sa (dict): 个股分析数据字典，包含以下字段：
            - name: 股票名称
            - code: 股票代码
            - price: 当前最新价格
            - trend: 趋势判断
            - trend_probs: 趋势概率分布
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
            4. 未来半年趋势预判（含概率分布）
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
    trend_display = f"{sa['trend']}<br>{format_trend_probs(sa.get('trend_probs'))}"
    return f"""<tr>
<td>{sa['name']}</td><td>{sa['code']}</td><td>{sa['price']:.2f}</td>
<td>{trend_display}</td><td>{sa['high']:.2f}</td><td>{high_rise}%</td>
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
            - trend_probs: 趋势概率分布
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
            4. 未来半年趋势预判（含概率分布）
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
    trend_display = f"{ea['trend']}<br>{format_trend_probs(ea.get('trend_probs'))}"
    return f"""<tr>
<td>{ea['name']}</td><td>{ea['code']}</td><td>{ea['price']:.2f}</td>
<td>{trend_display}</td><td>{ea['high']:.2f}</td><td>{high_rise}%</td>
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

# 生成个股数据表格的HTML行（手动生成以支持链接）
# 输入：df_stock（从stock_data.csv读取的DataFrame）
# 输出：HTML表格字符串，数据来源列包含可点击链接
stock_table_rows = []
stock_table_rows.append("""<table class="data-table">
<thead>
<tr>
<th>股票名称</th><th>股票代码</th><th>当前最新价格(HKD)</th><th>当前最新价格对应时间戳</th><th>数据来源</th>
</tr>
</thead>
<tbody>""")
for _, row in df_stock.iterrows():
    source_link = make_index_data_link('来源', row['数据来源'])
    stock_table_rows.append(
        f"<tr><td>{row['股票名称']}</td><td>{row['股票代码']}</td>"
        f"<td>{row['当前最新价格(HKD)']}</td>"
        f"<td>{row['当前最新价格对应时间戳']}</td>"
        f"<td>{source_link}</td></tr>"
    )
stock_table_rows.append("</tbody></table>")
stock_table_csv = "".join(stock_table_rows)

# 生成ETF数据表格的HTML行（手动生成以支持链接）
# 输入：df_etf（从etf_data.csv读取的DataFrame）
# 输出：HTML表格字符串，数据来源列包含可点击链接
etf_table_rows = []
etf_table_rows.append("""<table class="data-table">
<thead>
<tr>
<th>ETF名称</th><th>ETF代码</th><th>当前最新价格(HKD)</th><th>当前最新价格对应时间戳</th><th>数据来源</th>
</tr>
</thead>
<tbody>""")
for _, row in df_etf.iterrows():
    source_link = make_index_data_link('来源', row['数据来源'])
    etf_table_rows.append(
        f"<tr><td>{row['ETF名称']}</td><td>{row['ETF代码']}</td>"
        f"<td>{row['当前最新价格(HKD)']}</td>"
        f"<td>{row['当前最新价格对应时间戳']}</td>"
        f"<td>{source_link}</td></tr>"
    )
etf_table_rows.append("</tbody></table>")
etf_table_csv = "".join(etf_table_rows)

# =============================================================================
# 分析表格HTML代码生成
# =============================================================================

# 使用列表推导式和对应的make_*_row函数生成所有分析表格行
# 输入：index_analysis、stock_analysis、etf_analysis列表
# 输出：拼接后的HTML表格行字符串
index_texts = "".join(make_index_text(ia) for ia in index_analysis)
stock_rows = "".join(make_stock_row(sa) for sa in stock_analysis)

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
<li><a href="#section2">一、未来一周重大事件分析</a>
</li>
<li><a href="#section3">二、指数研判</a></li>
<li><a href="#section4">三、个股分析</a></li>
<li><a href="#section6">四、分析推理过程</a></li>
<li><a href="#section7">六、参考资料</a></li>
</ul>
</div>

<div class="section" id="section2">
<h2>一、未来一周重大事件分析</h2>

<div class="event-card">
<h4>1. 美联储4月28-29日议息会议：鲍威尔"最后一舞"</h4>
<p class="time">预计时间：2026年4月28日-29日（美东时间）</p>
<p><strong>事件概述：</strong>美联储4月28-29日召开议息会议，预计维持利率3.5%-3.75%不变（概率100%）。本次为鲍威尔任期内最后一次主持FOMC，沃什已被提名为下一任美联储主席。由于担忧战争推高能源价格，市场已下调对今年降息的预期，6月降息概率仅4.7%-5.1%。</p>
<p><strong>可能的市场影响情景分析：</strong></p>
<p><span class="scenario base">基准情景（概率70%）：维持利率不变，声明中性偏鹰，鲍威尔强调通胀风险，市场反应有限</span></p>
<p><span class="scenario optimistic">乐观情景（概率10%）：声明偏鸽，暗示若地缘风险缓解可能降息，风险资产反弹</span></p>
<p><span class="scenario pessimistic">悲观情景（概率20%）：声明超预期鹰派，暗示可能加息应对通胀，风险资产大幅回调</span></p>
</div>

<div class="event-card">
<h4>2. 超级财报周：MAG7四巨头同日发财报</h4>
<p class="time">预计时间：2026年4月29日（美东时间盘后）</p>
<p><strong>事件概述：</strong>Alphabet（谷歌）、亚马逊、Meta、微软将在4月29日同一个交易日盘后集中发布季度业绩。苹果、礼来、万事达卡、卡特彼勒、默沙东、伯克希尔哈撒韦等也将发布财报。这是近年来最密集的巨头财报发布日，AI资本开支指引将成为市场焦点。</p>
<p><strong>可能的市场影响情景分析：</strong></p>
<p><span class="scenario base">基准情景（概率40%）：四巨头业绩符合预期，AI资本开支维持30%以上增速，市场温和上涨</span></p>
<p><span class="scenario optimistic">乐观情景（概率30%）：AI资本开支超预期加速，云业务收入大增，科技板块大涨</span></p>
<p><span class="scenario pessimistic">悲观情景（概率30%）：AI投资增速放缓或盈利不及预期，科技板块大幅回调</span></p>
</div>

<div class="event-card">
<h4>3. 美伊谈判后续进展</h4>
<p class="time">预计时间：2026年4月28日-5月5日（北京时间）</p>
<p><strong>事件概述：</strong>白宫表示特朗普与幕僚正在讨论伊朗的最新和平提议，核问题是红线之一。伊朗明确拒绝出席伊斯兰堡第二轮会谈。霍尔木兹海峡危机持续，伊朗布设水雷封锁海峡。地缘风险仍是扰动市场的核心变量。</p>
<p><strong>可能的市场影响情景分析：</strong></p>
<p><span class="scenario pessimistic">悲观情景（概率35%）：谈判破裂，冲突再度升级，油价突破130美元/桶，全球股市大幅回调</span></p>
<p><span class="scenario base">基准情景（概率45%）：停火维持但谈判无实质进展，市场震荡加剧，油价在95-110美元/桶区间波动</span></p>
<p><span class="scenario optimistic">乐观情景（概率20%）：双方达成框架协议，地缘溢价快速消退，油价回落至80美元以下，全球风险资产反弹</span></p>
</div>

<div class="event-card">
<h4>4. 中国五一假期前最后交易日</h4>
<p class="time">预计时间：2026年4月30日（北京时间）</p>
<p><strong>事件概述：</strong>4月30日为A股和港股五一假期前最后一个交易日。节前效应通常导致交投趋于谨慎，资金避险情绪升温。4月宏观经济数据（CPI、PPI、社融）预计5月10-15日发布。</p>
<p><strong>可能的市场影响情景分析：</strong></p>
<p><span class="scenario base">基准情景（概率50%）：节前缩量震荡，防御板块相对抗跌，市场交投清淡</span></p>
<p><span class="scenario optimistic">乐观情景（概率20%）：美联储偏鸽+财报超预期，节前资金抢筹，市场上涨</span></p>
<p><span class="scenario pessimistic">悲观情景（概率30%）：地缘风险升级+财报不及预期，节前资金出逃，市场下跌</span></p>
</div>

<div class="event-card">
<h4>5. 全球CPU涨价周期持续</h4>
<p class="time">预计时间：2026年5月-7月</p>
<p><strong>事件概述：</strong>自2026年3月起，消费电子CPU价格涨幅5%-10%，服务器CPU涨幅10%-20%。英特尔3月率先上调PC CPU价格，4月1日调整服务器CPU售价，预期下半年仍有8%-10%调涨空间。半导体产业链涨价预期持续。</p>
<p><strong>可能的市场影响情景分析：</strong></p>
<p><span class="scenario base">基准情景（概率50%）：涨价按预期推进，半导体板块温和上涨</span></p>
<p><span class="scenario optimistic">乐观情景（概率30%）：AI算力需求超预期推动涨价加速，半导体板块大涨</span></p>
<p><span class="scenario pessimistic">悲观情景（概率20%）：需求疲软导致涨价不及预期，半导体板块回调</span></p>
</div>

<div class="section" id="section3">
<h2>二、指数研判</h2>
{index_texts}
</div>

<div class="section" id="section4">
<h2>个股分析</h2>

<table class="data-table">
<thead>
<tr>
<th>股票名称</th><th>股票代码</th><th>当前最新价格(HKD)</th>
<th>未来半年趋势预判</th><th>截止2026年12月31日最高目标价</th><th>最高目标价相对最新价格涨幅</th>
<th>截止2026年12月31日最低目标价</th><th>最低目标价相对最新价格跌幅</th>
<th>当前看多看空观点</th><th>当前仓位调整建议</th>
<th>未来半年趋势预判的核心逻辑</th>
</tr>
</thead>
<tbody>
{stock_rows}
</tbody>
</table>
</div>

<div class="section" id="section6">
<h2>六、分析推理过程</h2>

<div class="reasoning-chain">
<h4>1. 宏观判断链</h4>
<p><strong>重大事件 → 宏观环境影响 → 市场整体方向</strong></p>
<p>美联储4月28-29日议息会议预计按兵不动，鲍威尔任期内最后一次主持FOMC，沃什已被提名为下一任美联储主席。美油突破97美元/桶，伊朗拒绝出席伊斯兰堡第二轮会谈，霍尔木兹海峡危机持续。4月29日MAG7四巨头同日发财报，AI资本开支指引将决定科技板块方向。DeepSeek V4完成华为昇腾平台适配，国产AI算力替代加速。宁德时代H股配售391.9亿港元引发市场对港股过度融资的担忧。A股极致分化，中特估虹吸流动性致个股普跌。港股4月28日收跌0.95%，呈现"能源强、科技弱"结构性格局，南向资金持续净买入提供底部支撑。五一节前交投趋于谨慎。</p>
</div>

<div class="reasoning-chain">
<h4>2. 指数推导链</h4>
<p><strong>宏观判断 → 各指数差异化表现</strong></p>
<p>恒生指数：4月28日收跌0.95%报25679点，科网股全线回调拖累，但南向资金逆势净买入提供底部支撑，能源+高股息板块逆势走强，整体震荡偏弱。</p>
<p>恒生科技指数：收跌2.28%报4827点，科网股普遍回调（小米跌3.79%、阿里跌2.84%、宁德时代跌6.88%），DeepSeek V4利好国产算力但短期获利回吐，板块内部分化加剧。</p>
<p>国企指数：收跌1.27%报8644点，但中字头能源板块逆势走强（中海油+1.90%、中石油+1.83%、中国神华+1.99%），银行高股息防御属性突出，震荡偏强。</p>
<p>美股三大指数：4月27日标普500与纳指齐创历史新高后，4月28日从纪录高位回落。道指微跌0.05%，标普500跌0.49%，纳指跌0.90%。AI股回调拖累科技板块，但能源板块逆势涨1.65%。</p>
</div>

<div class="reasoning-chain">
<h4>3. 个股推导链</h4>
<p><strong>宏观+行业+个股事件 → 个股趋势判断</strong></p>
<p>能源板块（中海油、中石油、中石化、紫金矿业、中国神华）：美油突破97美元/桶直接受益，黄金突破4690美元/盎司利好紫金矿业，量价齐升逻辑最清晰。4月28日中海油涨1.90%、中石油涨1.83%、中国神华涨1.99%。</p>
<p>AI科技板块（腾讯、百度、中芯国际、华虹半导体）：DeepSeek V4适配华为昇腾平台是国产AI算力里程碑，4月24日港股半导体大涨（中芯+10%、华虹+15%），但4月28日短期获利回吐（中芯-3.22%、华虹-1.13%）。4月29日MAG7财报将决定方向。</p>
<p>新能源板块（宁德时代、比亚迪）：宁德时代H股配售391.9亿港元暴跌6.88%，短期承压但全球动力电池龙头地位稳固。比亚迪海外拓展加速，但受科网股回调拖累跌2.17%。</p>
<p>银行板块（招行、建行、工行、中行）：高股息防御属性突出，A股中特估行情外溢至港股银行板块，但净息差收窄限制上行空间。</p>
<p>创新药板块（信达生物、药明生物）：信达管线兑现+GLP-1催化看多，药明受美国生物安全法案影响看空，但4月28日逆势涨1.26%显示超跌反弹机会。</p>
</div>

<div class="reasoning-chain">
<h4>4. 关键假设</h4>
<p>① 中东停火协议得以维持，美伊谈判取得有限进展（不确定性：高）</p>
<p>② 美联储2026年维持利率3.5%-3.75%不变（不确定性：中）</p>
<p>③ MAG7财报AI资本开支维持30%以上增速（不确定性：中）</p>
<p>④ 中国经济温和复苏，GDP增速4.5%-5.0%（不确定性：低）</p>
<p>⑤ 南向资金日均净流入维持30亿港元以上（不确定性：中）</p>
<p>⑥ DeepSeek V4推动国产AI算力替代加速（不确定性：低）</p>
</div>

<div class="reasoning-chain">
<h4>5. 风险提示</h4>
<p>① <strong>地缘风险再度升级</strong>：若美伊谈判破裂冲突再度升级，霍尔木兹海峡完全关闭，油价可能突破130美元/桶，全球股市将面临10%-20%回调。</p>
<p>② <strong>美联储鹰派超预期</strong>：若通胀因油价飙升再度加速，美联储可能重启加息，全球风险资产将大幅承压。</p>
<p>③ <strong>MAG7财报不及预期</strong>：若AI资本开支增速放缓，全球科技板块估值将面临回调，港股科技股首当其冲。</p>
<p>④ <strong>A股极致分化持续</strong>：若中特估抱团不瓦解、热点不扩散，中小盘股流动性枯竭可能引发系统性风险。</p>
<p>⑤ <strong>港股过度融资</strong>：宁德时代配售391.9亿港元后，若更多大型融资项目跟进，港股流动性将进一步承压。</p>
<p>⑥ <strong>美联储权力交接风险</strong>：沃什接任美联储主席后政策立场可能发生变化，市场不确定性增加。</p>
</div>

<div class="reasoning-chain">
<h4>6. 与上一份研报的不同之处</h4>
<p><strong>数据更新：</strong>港股指数数据从4月27日收盘更新至4月28日收盘（恒指从25925→25679，恒生科技从4939→4827），科网股回调加深。美股从历史高位回落（标普500从7173→7138）。</p>
<p><strong>事件更新：</strong>新增宁德时代H股配售391.9亿港元事件（股价暴跌6.88%）、DeepSeek V4发布适配华为昇腾平台、全球CPU涨价周期、美联储权力交接（沃什被提名为下一任主席）。</p>
<p><strong>地缘更新：</strong>美伊从"停火延长"进入"伊朗拒绝出席会谈"阶段，霍尔木兹海峡危机加剧（伊朗布设水雷封锁海峡），冲突影响从能源传导至工业原材料领域。</p>
<p><strong>市场格局变化：</strong>从"光通信暴涨+科网回调"演变为"中特估虹吸+科网暴跌+能源偏强"的三极分化格局，市场风格更趋防御。4月28日美股能源板块逆势涨1.65%。</p>
<p><strong>新增关注：</strong>新增全球CPU涨价周期作为半导体产业链催化剂，新增美联储权力交接风险。</p>
</div>
</div>

<div class="section" id="section7">
<h2>六、参考资料</h2>

<h3>宏观政策类</h3>
<ul class="ref-list">
<li><a href="https://www.cbsnews.com/news/fed-rate-decision-april-2026-powell-final-meeting/" target="_blank">美联储4月议息会议：鲍威尔任内最后一次FOMC</a> — CBS News (2026年4月29日)</li>
<li><a href="https://www.tradingkey.com/zh-hans/analysis/economic/indicators/261820532-fed-rate-hold-inflation-oil-succession-tradingkey" target="_blank">美联储维持利率不变，通胀与油价压力持续</a> — TradingKey (2026年4月29日)</li>
<li><a href="http://m.toutiao.com/group/7633726637636469291/" target="_blank">美联储4月维持利率不变概率100%，6月降息概率仅4.7%</a> — 财联社 (2026年4月28日)</li>
<li><a href="https://www.cls.cn/subject/1318" target="_blank">超级央行周：五大央行利率决议前瞻</a> — 财联社 (2026年4月27日)</li>
</ul>

<h3>地缘政治类</h3>
<ul class="ref-list">
<li><a href="https://c.m.163.com/news/a/KRKGS8QB0556FDLH.html" target="_blank">美伊冲突持续：伊朗拒绝出席伊斯兰堡第二轮会谈</a> — 网易新闻 (2026年4月28日)</li>
<li><a href="http://m.toutiao.com/group/7631850397984719360/" target="_blank">霍尔木兹海峡危机：伊朗布设水雷封锁海峡</a> — 今日头条 (2026年4月27日)</li>
<li><a href="http://m.toutiao.com/group/7633434688832471587/" target="_blank">美油突破97美元/桶，能源板块逆势走强</a> — 今日头条 (2026年4月28日)</li>
<li><a href="https://finance.sina.com.cn/2026-04-28/iran-steel-export-ban.shtml" target="_blank">伊朗暂停部分钢铁产品出口至5月30日</a> — 新浪财经 (2026年4月28日)</li>
</ul>

<h3>行业/公司类</h3>
<ul class="ref-list">
<li><a href="https://www.21jingji.com/article/20260428/herald/07e11f62524a50be6a919a47b4622a85.html" target="_blank">宁德时代H股配售391.9亿港元，股价暴跌6.88%</a> — 21经济网 (2026年4月28日)</li>
<li><a href="https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0428/2026042800267.pdf" target="_blank">宁德时代配售公告（港交所官方文件）</a> — 港交所 (2026年4月28日)</li>
<li><a href="https://global.chinadaily.com.cn/a/202604/24/WS69eb8141a310d6866eb45737.html" target="_blank">DeepSeek V4发布：1.6万亿参数大模型开源</a> — China Daily (2026年4月24日)</li>
<li><a href="https://finance.eastmoney.com/a/202604273719980678.html" target="_blank">DeepSeek V4适配华为昇腾平台，国产AI算力里程碑</a> — 东方财富网 (2026年4月27日)</li>
<li><a href="http://m.toutiao.com/group/7632243504617554447/" target="_blank">全球CPU涨价周期：服务器CPU涨幅10%-20%</a> — 财联社 (2026年4月26日)</li>
<li><a href="https://finance.sina.com.cn/stock/hkstock/hkstocknews/2026-04-28/" target="_blank">港股4月28日收评：恒指跌0.95%，科网股全线回调</a> — 新浪财经 (2026年4月28日)</li>
<li><a href="http://m.toutiao.com/group/7633829589302641152/" target="_blank">南向资金4月28日持续净买入</a> — 证券时报 (2026年4月28日)</li>
</ul>

<h3>技术分析类</h3>
<ul class="ref-list">
<li><a href="https://apnews.com/article/wall-street-stocks-dow-nasdaq-b147717d731d3f7cfaf27a9625715c21" target="_blank">美股4月28日从历史高位回落</a> — AP News (2026年4月28日)</li>
<li><a href="https://m.weibo.cn/detail/5292941205570128" target="_blank">美股4月28日收盘数据：道指49141、标普7138</a> — 新浪财经微博 (2026年4月28日)</li>
<li><a href="https://www.stl.news/u-s-stock-market-today-tuesday-april-28-2026/" target="_blank">美股4月28日交易日报：能源板块逆势涨1.65%</a> — STL News (2026年4月28日)</li>
<li><a href="https://www.investing.com/indices/nq-100-news/2" target="_blank">纳斯达克100指数4月28日收跌1.01%</a> — Investing.com (2026年4月28日)</li>
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
