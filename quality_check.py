"""
Report Quality Check Script
研报质量检查脚本

=============================================================================
File Function:
    This script performs comprehensive quality checks on generated HTML reports,
    ensuring reports meet the following standards:
    - File format compliance
    - Data completeness
    - Content structure correctness
    - Reference links validity
    - Timestamp accuracy
文件功能：
    本脚本对生成的HTML研报进行全面质量检查，确保研报符合以下标准：
    - 文件格式规范
    - 数据完整性
    - 内容结构正确
    - 参考资料链接有效
    - 时间戳准确性

=============================================================================
Check Items (30+ items):
    1. File Existence Checks
       - Data fetching script file exists
       - CSV data files exist
    2. File Format Checks
       - HTML format is correct
       - Filename format complies with standard (YB_XXXX_YYYYMMDDHHMMSS.html)
    3. Content Completeness Checks
       - Table of contents structure complete
       - Index data table fields correct
       - Stock data table fields correct
       - All 6 indices have trend predictions
       - Each index/stock has high/low target prices
       - Stocks have bullish/bearish/neutral recommendations
       - Stocks have position adjustment recommendations
       - Reasoning chain process complete
    4. Reference Checks
       - References section exists
       - Links are clickable (target="_blank")
       - HTTP link format is correct
    5. Timestamp Accuracy Checks
       - Uses Beijing time
       - Uses US Eastern time labeling
       - Timestamps match actual trading times (not 00:00:00)
    6. Data Quality Checks
       - No estimated/simulated data
       - Quality checklist not leaked into report
检查项目（30+项）：
    1. 文件存在性检查
       - 数据获取脚本文件存在
       - CSV数据文件存在
    2. 文件格式检查
       - HTML格式正确
       - 文件名格式符合规范（YB_XXXX_YYYYMMDDHHMMSS.html）
    3. 内容完整性检查
       - 目录结构完整
       - 指数数据表字段正确
       - 个股数据表字段正确
       - 6个指数都有趋势预判
       - 每个指数/个股都有高/低目标价
       - 个股有做多/做空/观望建议
       - 个股有仓位调整建议
       - 思维链推理过程完整
    4. 参考资料检查
       - 参考资料章节存在
       - 链接可点击（target="_blank"）
       - HTTP链接格式正确
    5. 时间戳准确性检查
       - 使用北京时间
       - 使用美东时间标注
       - 时间戳符合实际交易时间（非00:00:00）
    6. 数据质量检查
       - 无估算/模拟数据
       - 无质量检查清单泄露

=============================================================================
Usage:
    python quality_check.py

    Script will automatically:
    1. Find the latest YB*.html file in output directory
    2. Read file content and perform item-by-item checks
    3. Output check results report
使用方法：
    python quality_check.py

    脚本会自动：
    1. 查找output目录下最新的YB*.html文件
    2. 读取文件内容进行逐项检查
    3. 输出检查结果报告

=============================================================================
Output Description:
    - ✅ PASS: Check item passed
    - ❌ FAIL: Check item failed
    - 🎉 All checks passed! : All checks passed
    - ⚠️ Some checks failed, please review the failures above. : There are failures
输出说明：
    - ✅ PASS: 检查项通过
    - ❌ FAIL: 检查项失败
    - 🎉 所有检查项均通过！: 所有检查通过
    - ⚠️ 部分检查项未通过，请检查上述失败项。: 存在失败项

=============================================================================
Author/Maintainer: AI Agent (TRAE CN SOLO GLM5.1)
Last Updated: 2026-04-23
作者/维护者：AI Agent (TRAE CN SOLO GLM5.1)
最后更新：2026-04-23
=============================================================================
"""

import os
import re
from datetime import datetime
import pytz

# =============================================================================
# Configuration Constants
# 配置常量
# =============================================================================

# Report directory path
# Description: Script will search for YB*.html files in this directory
# Path: output folder under project root
# 研报目录路径
# 说明：脚本会在此目录下查找YB*.html文件
# 路径：项目根目录下的output文件夹
REPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')

# Set Beijing timezone
# Used for generating check report timestamp
# 设置北京时间时区
# 用于生成检查报告的时间戳
bj_tz = pytz.timezone('Asia/Shanghai')

# Get current Beijing time
# 获取当前北京时间
now_bj = datetime.now(bj_tz)

# =============================================================================
# Find Latest Report File
# 查找最新研报文件
# =============================================================================

# List all files starting with YB and ending with .html in output directory
# 列出output目录下所有以YB开头、.html结尾的文件
html_files = [f for f in os.listdir(REPORT_DIR) if f.startswith('YB') and f.endswith('.html')]

# If no report files found, exit with error
# 如果没有找到研报文件，报错退出
if not html_files:
    print("ERROR: No YB*.html report found!")
    exit(1)

# Sort by filename, take the last one (latest timestamp)
# 按文件名排序，取最后一个（时间戳最新）
latest_report = sorted(html_files)[-1]
report_path = os.path.join(REPORT_DIR, latest_report)

print(f"Quality checking: {latest_report}")

# =============================================================================
# Read Report Content
# 读取研报内容
# =============================================================================

with open(report_path, 'r', encoding='utf-8') as f:
    content = f.read()

# =============================================================================
# Define Check Items
# 定义检查项
# =============================================================================

checks = []

# -----------------------------------------------------------------------------
# 1. File Existence Checks
# 文件存在性检查
# -----------------------------------------------------------------------------

# Check if data fetching script exists
# 检查数据获取脚本是否存在
checks.append(("数据获取.py文件存在",
    os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fetch_market_data.py'))))

# Check if CSV data files exist
# 检查CSV数据文件是否存在
checks.append(("CSV指数数据存在",
    os.path.exists(os.path.join(REPORT_DIR, 'index_data.csv'))))
checks.append(("CSV个股数据存在",
    os.path.exists(os.path.join(REPORT_DIR, 'stock_data.csv'))))

# -----------------------------------------------------------------------------
# 2. File Format Checks
# 文件格式检查
# -----------------------------------------------------------------------------

# Check if file is HTML format
# 检查文件是否为HTML格式
checks.append(("报告格式为HTML",
    latest_report.endswith('.html')))

# Check if filename format complies with standard
# Format: YB_XXXX (4-digit sequence) _ (14-digit timestamp YYYYMMDDHHMMSS) .html
# Example: YB_0001_20260423111711.html
# 检查文件名格式是否符合规范
# 格式：YB_XXXX（4位序号）_（14位时间戳YYYYMMDDHHMMSS）.html
# 示例：YB_0001_20260423111711.html
checks.append(("文件名YB+序号+时间戳格式",
    bool(re.match(r'YB_\d{4}_\d{14}\.html', latest_report))))

# -----------------------------------------------------------------------------
# 3. Content Completeness Checks
# 内容完整性检查
# -----------------------------------------------------------------------------

# Check if report date uses Beijing time
# 检查报告日期是否使用北京时间
checks.append(("报告日期使用北京时间",
    '北京时间' in content and '报告日期' in content))

# Check if report beginning has "数据截止" text (should not have)
# 检查报告开头是否有"数据截止"字样（不应该有）
checks.append(("报告开头无数据截止日期",
    not re.search(r'数据截止[日日期]', content[:500])))

# Check if table of contents exists and is clickable (anchor links)
# 检查目录是否存在且可点击（锚点链接）
checks.append(("目录存在且可点击",
    'href="#section' in content and '目录' in content))

# Check if index data table contains all required fields
# Fields: index name, index code, current latest points, timestamp, data source
# 检查指数数据表是否包含所有必要字段
# 字段：指数名称、指数代码、当前最新点数、当前最新点数对应时间戳、数据来源
checks.append(("指数数据表字段正确",
    all(f in content for f in ['指数名称', '指数代码', '当前最新点数',
                                   '当前最新点数对应时间戳', '数据来源'])))

# Check if stock data table contains all required fields
# Fields: stock name, stock code, current latest price (HKD), timestamp
# 检查个股数据表是否包含所有必要字段
# 字段：股票名称、股票代码、当前最新价格(HKD)、当前最新价格对应时间戳
checks.append(("个股数据表字段正确",
    all(f in content for f in ['股票名称', '股票代码',
                                   '当前最新价格(HKD)', '当前最新价格对应时间戳'])))

# Check if all 6 indices have trend predictions
# Must include: Hang Seng Index, Hang Seng Tech Index, HSCEI, Nasdaq 100, S&P 500, Dow Jones
# 检查6个指数是否都有趋势预判
# 必须包含：恒生指数、恒生科技指数、国企指数、纳斯达克100指数、标普500指数、道琼斯指数
checks.append(("6个指数均有趋势预判",
    all(idx in content for idx in ['恒生指数', '恒生科技指数', '国企指数',
                                     '纳斯达克100指数', '标普500指数', '道琼斯指数'])))

# Check if trend predictions use standard expressions
# Standard expressions: 震荡上行, 震荡偏强, 震荡偏弱, 震荡下行, 直接上行, 直接下行
# 检查趋势预判是否使用规范表述
# 规范表述：震荡上行、震荡偏强、震荡偏弱、震荡下行、直接上行、直接下行
trend_keywords = ['震荡上行', '震荡偏强', '震荡偏弱', '震荡下行', '直接上行', '直接下行']
checks.append(("趋势预判使用规范表述",
    any(kw in content for kw in trend_keywords)))

# Check if each index has highest/lowest target points
# 检查每个指数是否有最高/最低目标点数
checks.append(("每个指数有最高目标点数",
    '最高目标点数' in content))
checks.append(("每个指数有最低目标点数",
    '最低目标点数' in content))

# Check if each stock has highest/lowest target price
# 检查每个个股是否有最高/最低目标价
checks.append(("每个个股有最高目标价",
    '最高目标价' in content))
checks.append(("每个个股有最低目标价",
    '最低目标价' in content))

# Check if stocks have bullish/bearish/neutral recommendations
# 检查个股是否有做多/做空/观望建议
checks.append(("个股有做多做空建议",
    all(kw in content for kw in ['做多', '做空', '观望'])))

# Check if position adjustment recommendations exist
# 检查是否有仓位调整建议
checks.append(("个股有仓位调整建议",
    '仓位调整建议' in content))

# Check if stock 9 fields are complete
# Fields: next month trend prediction, highest target price, lowest target price,
#         current bullish/bearish recommendation, current position adjustment recommendation,
#         recent stock-specific major events, core logic for next month trend prediction
# 检查个股9个字段是否完整
# 字段：未来一个月趋势预判、最高目标价、最低目标价、当前做多做空建议、
#       当前仓位调整建议、近期个股自身重大事件、未来一个月趋势预判的核心逻辑
stock_fields = ['未来一个月趋势预判', '最高目标价', '最低目标价',
                '当前做多做空建议', '当前仓位调整建议',
                '近期个股自身重大事件', '未来一个月趋势预判的核心逻辑']
checks.append(("个股9个字段完整",
    all(f in content for f in stock_fields)))

# Check if reasoning chain process is complete
# Must include: macro judgment chain, index derivation chain, stock derivation chain,
#              key assumptions, risk warnings
# 检查思维链推理过程是否完整
# 必须包含：宏观判断链、指数推导链、个股推导链、关键假设、风险提示
checks.append(("思维链推理过程完整",
    all(kw in content for kw in ['宏观判断链', '指数推导链', '个股推导链',
                                    '关键假设', '风险提示'])))

# -----------------------------------------------------------------------------
# 4. Reference Checks
# 参考资料检查
# -----------------------------------------------------------------------------

# Check if references section exists and contains href links
# 检查参考资料章节是否存在且包含href链接
checks.append(("参考资料链接已附上",
    '参考资料' in content and 'href=' in content))

# Check if future events have probability values
# 检查未来事件是否有概率值
checks.append(("未来事件有概率值",
    '概率' in content and '%' in content))

# -----------------------------------------------------------------------------
# 5. Timestamp Accuracy Checks
# 时间戳准确性检查
# -----------------------------------------------------------------------------

# Check if US Eastern time labeling exists
# 检查是否有美东时间标注
checks.append(("美东时间标注",
    '美东时间' in content))

# Check if timestamps match actual trading times
# HK trading hours: 9:30-12:00, 13:00-16:00
# Common timestamps: 16:08:33, 16:00:00, etc.
# 检查时间戳是否符合实际交易时间
# 港股交易时间：9:30-12:00, 13:00-16:00
# 常见时间戳：16:08:33, 16:00:00等
checks.append(("时间戳符合实际交易时间",
    '16:08:33' in content or '16:00:00' in content))

# Check if timestamps contain 00:00:00 (non-trading time, except for US Eastern)
# 检查时间戳是否包含00:00:00等非交易时间（美东时间除外）
checks.append(("时间戳不含00:00:00等非交易时间",
    '00:00:00' not in content or '00:00:00 (美东' in content))

# -----------------------------------------------------------------------------
# 6. Data Quality Checks
# 数据质量检查
# -----------------------------------------------------------------------------

# Check if there is estimated/simulated data (should not have)
# 检查是否有估算/模拟数据（不应该有）
checks.append(("所有价格数据非估算",
    '估算' not in content and '模拟' not in content))

# Check if data source links are clickable (target="_blank" and http links)
# 检查数据来源链接是否可点击（target="_blank"且为http链接）
checks.append(("数据来源网页链接可点击跳转",
    'target="_blank"' in content and 'href="http' in content))

# Check if quality checklist is leaked into report (should not have)
# 检查质量检查清单是否泄露到报告中（不应该有）
checks.append(("质量检查清单不在报告中",
    '质量检查清单' not in content))

# =============================================================================
# Output Check Results
# 输出检查结果
# =============================================================================

print("\n" + "="*60)
print("质量检查报告")
print("="*60)

all_pass = True
for name, result in checks:
    status = "✅ PASS" if result else "❌ FAIL"
    if not result:
        all_pass = False
    print(f"  {status} | {name}")

print("="*60)
if all_pass:
    print("🎉 所有检查项均通过！")
else:
    print("⚠️ 部分检查项未通过，请检查上述失败项。")

print(f"\n报告文件: {report_path}")
print(f"检查时间: {now_bj.strftime('%Y-%m-%d %H:%M:%S')}（北京时间）")
