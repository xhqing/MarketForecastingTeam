"""
Market Data Fetching Script
市场数据获取脚本

=============================================================================
File Function:
    This script fetches real-time market data from Longport API, including:
    - HK stock indices (Shanghai Index, Hang Seng Index, Hang Seng Tech Index, HSCEI, etc.)
    - HK stocks (loaded from targets.json configuration file)
    - US stock indices (Nasdaq 100, S&P 500, Dow Jones Industrial Average)
文件功能：
    本脚本从Longport（长桥）API获取实时市场数据，包括：
    - 港股指数（上证指数、恒生指数、恒生科技指数、国企指数等）
    - 港股个股（从targets.json配置文件中读取）
    - 美股指数（纳斯达克100、标普500、道琼斯工业指数）

=============================================================================
Data Output:
    Generates the following CSV files to output directory:
    - index_data.csv: Index data (name, code, current points, timestamp, source)
    - stock_data.csv: Stock data (name, code, current price, timestamp, source)
    - etf_data.csv: ETF data (expandable when needed)
数据输出：
    生成以下CSV文件到output目录：
    - index_data.csv: 指数数据（指数名称、代码、当前点数、时间戳、数据来源）
    - stock_data.csv: 个股数据（股票名称、代码、当前价格、时间戳、数据来源）
    - etf_data.csv: ETF数据（需要时可扩展）

=============================================================================
Configuration Dependencies:
    - targets.json: Target instruments configuration file
      - hk_shares.index_major: HK major indices
      - hk_shares.index_sector: HK sector indices
      - hk_shares.hkex_stocks: HK stocks
      - us_shares.index_major: US major indices
      - us_shares.etf: US ETFs
配置依赖：
    - targets.json: 调研标的配置文件
      - hk_shares.index_major: 港股主要指数
      - hk_shares.index_sector: 港股行业指数
      - hk_shares.hkex_stocks: 港股个股
      - us_shares.index_major: 美股主要指数
      - us_shares.etf: 美股ETF

=============================================================================
API Dependencies:
    - Longport SDK (longbridge.openapi): HK real-time quote data
    - If Longport SDK is not installed, script will output warning but continue
API依赖：
    - Longport SDK (longbridge.openapi): 港股实时行情数据
    - 如未安装Longport SDK，脚本将输出警告但继续运行

=============================================================================
Environment Requirements:
    - Python 3.7+
    - Dependencies: pandas, pytz
    - config.py must have: LONGPORT_APP_KEY, LONGPORT_APP_SECRET, LONGPORT_ACCESS_TOKEN
环境要求：
    - Python 3.7+
    - 依赖库：pandas, pytz
    - config.py中需配置LONGPORT_APP_KEY、LONGPORT_APP_SECRET、LONGPORT_ACCESS_TOKEN

=============================================================================
Author/Maintainer: AI Agent (TRAE CN SOLO GLM5.1)
Last Updated: 2026-04-23
作者/维护者：AI Agent (TRAE CN SOLO GLM5.1)
最后更新：2026-04-23
=============================================================================
"""

import os
import sys
import json
import time
import logging
import pandas as pd
from datetime import datetime
import pytz

# =============================================================================
# Logging Configuration
# 日志配置
# =============================================================================

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# =============================================================================
# Output Directory Configuration
# 输出目录配置
# =============================================================================

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =============================================================================
# Longport SDK Import
# Longport SDK导入
# =============================================================================

try:
    from longport.openapi import QuoteContext, Config, Period, AdjustType
    LONGPORT_AVAILABLE = True
    logger.info("Longport SDK available")
except ImportError:
    LONGPORT_AVAILABLE = False
    logger.warning("Longport SDK not available")

# =============================================================================
# Configuration Import
# 配置导入
# =============================================================================

from config import LONGPORT_APP_KEY, LONGPORT_APP_SECRET, LONGPORT_ACCESS_TOKEN


# =============================================================================
# Configuration File Loading Functions
# 配置文件加载函数
# =============================================================================

def load_targets_config():
    """
    Load targets.json configuration file
    加载targets.json配置文件

    Returns:
        dict: Configuration dictionary with the following structure:
            - hk_shares: HK stock configuration
                - index_major: Major indices list
                - index_sector: Sector indices list
                - hkex_stocks: HKEX stock list
                - hkex_etf: HKEX ETF list
            - us_shares: US stock configuration
                - index_major: Major indices list
                - etf: ETF list
    返回：
        dict: 配置字典，包含以下结构：
            - hk_shares: 港股配置
                - index_major: 主要指数列表
                - index_sector: 行业指数列表
                - hkex_stocks: 港交所个股列表
                - hkex_etf: 港交所ETF列表
            - us_shares: 美股配置
                - index_major: 主要指数列表
                - etf: ETF列表

    Exception Handling:
        - If targets.json does not exist, returns default empty configuration
        - Uses logger.warning to record warning messages
    异常处理：
        - 如果targets.json文件不存在，返回默认空配置
        - 使用logger.warning记录警告信息

    Example Return:
        {
            "hk_shares": {
                "index_major": [{"name": "恒生指数", "code": "HSI"}],
                "hkex_stocks": [{"name": "腾讯控股", "code": "00700.HK"}]
            }
        }
    示例返回：
        {
            "hk_shares": {
                "index_major": [{"name": "恒生指数", "code": "HSI"}],
                "hkex_stocks": [{"name": "腾讯控股", "code": "00700.HK"}]
            }
        }
    """
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'targets.json')
    if not os.path.exists(config_path):
        logger.warning(f"targets.json not found at {config_path}, using empty config")
        return {"hk_shares": {"index_major": [], "index_sector": [], "hkex_stocks": [], "hkex_etf": []}}

    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    logger.info(f"Loaded targets config from {config_path}")
    return config


def filter_valid_targets(target_list):
    """
    Filter valid target list
    过滤有效标的列表

    Parameters:
        target_list (list): List of target dictionaries, each should contain name and code fields
    参数：
        target_list (list): 标的字典列表，每个字典应包含name和code字段

    Returns:
        list: List containing only targets where both name and code are not empty
    返回：
        list: 只包含name和code都不为空的标的列表

    Description:
        - Used to filter out empty entries in the configuration file
        - Ensures only valid targets are used for data fetching
    说明：
        - 用于过滤配置文件中可能存在的空条目
        - 确保只有有效的标的才会被用于数据获取
    """
    return [t for t in target_list if t.get('name') and t.get('code')]


# =============================================================================
# Configuration Data Extraction Functions
# 配置数据提取函数
# =============================================================================

def get_indices_from_config(config):
    """
    Extract all index information from configuration dictionary
    从配置字典中提取所有指数信息

    Parameters:
        config (dict): Configuration dictionary loaded from targets.json
    参数：
        config (dict): 从targets.json加载的配置字典

    Returns:
        list: List of index information dictionaries, each containing:
            - 指数名称 (str): Index name
            - 指数代码 (str): Index code
            - lp_code (str): Code used by Longport API
    返回：
        list: 指数信息字典列表，每个字典包含：
            - 指数名称 (str)
            - 指数代码 (str)
            - lp_code (str): Longport API使用的代码

    Data Sources:
        - hk_shares.index_major: HK major indices
        - hk_shares.index_sector: HK sector indices
        - us_shares.index_major: US major indices
    数据来源：
        - hk_shares.index_major: 港股主要指数
        - hk_shares.index_sector: 港股行业指数
        - us_shares.index_major: 美股主要指数

    Exception Handling:
        - Skips invalid indices with empty name or code
    异常处理：
        - 跳过name或code为空的无效指数
    """
    indices = []
    hk_shares = config.get('hk_shares', {})

    # Extract HK major indices
    # 提取港股主要指数
    for idx in hk_shares.get('index_major', []):
        if idx.get('name') and idx.get('code'):
            indices.append({
                "指数名称": idx['name'],
                "指数代码": idx['code'],
                "lp_code": idx['code']
            })

    # Extract HK sector indices
    # 提取港股行业指数
    for idx in hk_shares.get('index_sector', []):
        if idx.get('name') and idx.get('code'):
            indices.append({
                "指数名称": idx['name'],
                "指数代码": idx['code'],
                "lp_code": idx['code']
            })

    # Extract US major indices
    # 提取美股主要指数
    us_shares = config.get('us_shares', {})
    for idx in us_shares.get('index_major', []):
        if idx.get('name') and idx.get('code'):
            indices.append({
                "指数名称": idx['name'],
                "指数代码": idx['code'],
                "lp_code": idx['code']
            })

    return indices


def get_stocks_from_config(config):
    """
    Extract all HK stock information from configuration dictionary
    从配置字典中提取所有港股股票信息

    Parameters:
        config (dict): Configuration dictionary loaded from targets.json
    参数：
        config (dict): 从targets.json加载的配置字典

    Returns:
        list: List of stock information dictionaries, each containing:
            - 股票名称 (str): Stock name
            - 股票代码 (str): Stock code
            - lp_code (str): Code used by Longport API
    返回：
        list: 股票信息字典列表，每个字典包含：
            - 股票名称 (str)
            - 股票代码 (str)
            - lp_code (str): Longport API使用的代码

    Data Sources:
        - hk_shares.hkex_stocks: HKEX stock list
    数据来源：
        - hk_shares.hkex_stocks: 港交所个股列表

    Exception Handling:
        - Skips invalid stocks with empty name or code
    异常处理：
        - 跳过name或code为空的无效股票
    """
    stocks = []
    hk_shares = config.get('hk_shares', {})

    for stock in hk_shares.get('hkex_stocks', []):
        if stock.get('name') and stock.get('code'):
            stocks.append({
                "股票名称": stock['name'],
                "股票代码": stock['code'],
                "lp_code": stock['code']
            })

    return stocks


# =============================================================================
# Longport API Connection Functions
# Longport API连接函数
# =============================================================================

def get_longport_context():
    """
    Create Longport QuoteContext connection object
    创建Longport QuoteContext连接对象

    Returns:
        QuoteContext or None: Returns QuoteContext object on success, None on failure
    返回：
        QuoteContext或None: 成功返回QuoteContext对象，失败返回None

    Configuration Requirements:
        config.py must have:
        - LONGPORT_APP_KEY: Longport App Key
        - LONGPORT_APP_SECRET: Longport App Secret
        - LONGPORT_ACCESS_TOKEN: Longport Access Token
    配置要求：
        config.py中需配置：
        - LONGPORT_APP_KEY: 长桥App Key
        - LONGPORT_APP_SECRET: 长桥App Secret
        - LONGPORT_ACCESS_TOKEN: 长桥Access Token

    Exception Handling:
        - If Longport SDK is not available, returns None
        - If connection creation fails, uses logger.error to log error and returns None
    异常处理：
        - 如果Longport SDK不可用，返回None
        - 如果创建连接失败，使用logger.error记录错误并返回None
    """
    if not LONGPORT_AVAILABLE:
        return None
    try:
        config = Config(
            app_key=LONGPORT_APP_KEY,
            app_secret=LONGPORT_APP_SECRET,
            access_token=LONGPORT_ACCESS_TOKEN,
        )
        ctx = QuoteContext(config)
        logger.info("Longport context created successfully")
        return ctx
    except Exception as e:
        logger.error(f"Failed to create Longport context: {e}")
        return None


# =============================================================================
# Longport Quote Data Fetching Functions
# Longport行情数据获取函数
# =============================================================================

def fetch_longport_quote(ctx, symbols):
    """
    Batch fetch real-time quotes for multiple symbols
    批量获取多个标的的实时报价

    Parameters:
        ctx (QuoteContext): Longport connection object
        symbols (list): List of symbol codes, e.g., ["00700.HK", "09988.HK"]
    参数：
        ctx (QuoteContext): Longport连接对象
        symbols (list): 标的代码列表，如["00700.HK", "09988.HK"]

    Returns:
        dict: Quote results dictionary with symbol as key and dict containing:
            - price (float): Latest trade price
            - timestamp (datetime): Trade timestamp
    返回：
        dict: 报价结果字典，键为标的代码，值为包含以下字段的字典：
            - price (float): 最新成交价
            - timestamp (datetime): 成交时间戳

    Exception Handling:
        - If ctx is None, returns empty dictionary
        - If API call fails, tries batch fetching (5 symbols per batch)
        - 0.5 second delay between batch fetches to avoid too fast requests
    异常处理：
        - 如果ctx为None，返回空字典
        - 如果API调用失败，尝试分批获取（每批5个标的）
        - 分批获取之间有0.5秒延迟，避免请求过快
    """
    if ctx is None:
        return {}
    results = {}
    try:
        quotes = ctx.quote(symbols)
        for q in quotes:
            results[q.symbol] = {
                "price": float(q.last_done),
                "timestamp": q.timestamp,
            }
        logger.info(f"Longport: Got quotes for {len(results)} symbols")
    except Exception as e:
        logger.warning(f"Longport quote failed: {e}")
        # Batch fetching, 5 symbols per batch
        # 分批获取，每批5个标的
        for i in range(0, len(symbols), 5):
            batch = symbols[i:i+5]
            try:
                quotes = ctx.quote(batch)
                for q in quotes:
                    results[q.symbol] = {
                        "price": float(q.last_done),
                        "timestamp": q.timestamp,
                    }
                time.sleep(0.5)
            except Exception as e2:
                logger.warning(f"Longport batch quote failed for {batch}: {e2}")
    return results


def fetch_longport_stock_data(ctx, symbol):
    """
    Fetch quote data for a single stock/index
    获取单个股票/指数的行情数据

    Parameters:
        ctx (QuoteContext): Longport connection object
        symbol (str): Symbol code, e.g., "00700.HK", "HSI"
    参数：
        ctx (QuoteContext): Longport连接对象
        symbol (str): 标的代码，如"00700.HK"、"HSI"

    Returns:
        tuple: (price, timestamp, source)
            - price (float or None): Latest price, rounded to 2 decimal places
            - ts (datetime or None): Trade timestamp
            - source (str): Data source, fixed as "Longport API"
    返回：
        tuple: (价格, 时间戳, 数据来源)
            - price (float或None): 最新价格，保留2位小数
            - ts (datetime或None): 成交时间戳
            - source (str): 数据来源，固定为"Longport API"

    Fetch Strategy:
        1. First try real-time quote (ctx.quote)
        2. If quote fails, try to get daily K-line data (ctx.candlesticks)
        3. If timestamp shows 0:00 (invalid time), ignore the timestamp
    获取策略：
        1. 首先尝试实时报价(ctx.quote)
        2. 如果报价失败，尝试获取日K线数据(ctx.candlesticks)
        3. 如果时间戳显示为0点（无效时间），忽略该时间戳

    Exception Handling:
        - If ctx is None, returns (None, None, "Longport API")
        - All exceptions are caught and logged, returning None values
    异常处理：
        - 如果ctx为None，返回(None, None, "Longport API")
        - 所有异常都被捕获并记录，返回None值
    """
    if ctx is None:
        return None, None, "Longport API"
    price = None
    ts = None
    source = "Longport API"
    try:
        quotes = ctx.quote([symbol])
        if quotes:
            q = quotes[0]
            price = round(float(q.last_done), 2)
            ts = q.timestamp
            # Filter invalid timestamp (0:00)
            # 过滤无效时间戳（0点整）
            if ts is not None and hasattr(ts, 'hour') and ts.hour == 0 and ts.minute == 0 and ts.second == 0:
                ts = None
        if price is None:
            try:
                candles = ctx.candlesticks(symbol, Period.Day, 1, AdjustType.NoAdjust)
                if candles:
                    latest = candles[-1]
                    price = round(float(latest.close), 2)
                    ts = latest.timestamp
            except Exception as e:
                logger.warning(f"Longport candlestick also failed for {symbol}: {e}")
    except Exception as e:
        logger.warning(f"Longport quote failed for {symbol}: {e}")
        try:
            candles = ctx.candlesticks(symbol, Period.Day, 1, AdjustType.NoAdjust)
            if candles:
                latest = candles[-1]
                price = round(float(latest.close), 2)
                ts = latest.timestamp
        except Exception as e2:
            logger.warning(f"Longport candlestick failed for {symbol}: {e2}")
    return price, ts, source


# =============================================================================
# Timestamp Formatting Functions
# 时间戳格式化函数
# =============================================================================

def format_timestamp(ts, is_us_index=False):
    """
    Format timestamp into readable string
    格式化时间戳为可读字符串

    Parameters:
        ts: Timestamp, can be:
            - int/float: Unix timestamp (seconds)
            - datetime: datetime object
            - other: converted via str()
        is_us_index (bool): Whether it's a US index
            - True: Use US Eastern time (US/Eastern)
            - False: Use Beijing time (Asia/Shanghai)
    参数：
        ts: 时间戳，可以是：
            - int/float: Unix时间戳（秒）
            - datetime: datetime对象
            - 其他: 调用str()转换
        is_us_index (bool): 是否为美股指数
            - True: 使用美东时间（US/Eastern）
            - False: 使用北京时间（Asia/Shanghai）

    Returns:
        str: Formatted time string
            - Format: "YYYY-MM-DD HH:MM:SS (timezone)"
            - Example: "2026-04-23 09:30:00 (北京时间)"
            - Example: "2026-04-22 21:30:00 (美东时间)"
    返回：
        str: 格式化后的时间字符串
            - 格式: "YYYY-MM-DD HH:MM:SS (时区)"
            - 示例: "2026-04-23 09:30:00 (北京时间)"
            - 示例: "2026-04-22 21:30:00 (美东时间)"

    Exception Handling:
        - All exceptions are caught, returns str(ts) as fallback
    异常处理：
        - 所有异常都被捕获，返回str(ts)的兜底值
    """
    try:
        if isinstance(ts, (int, float)):
            from datetime import timezone
            dt = datetime.fromtimestamp(ts, tz=timezone.utc)
            if is_us_index:
                local_tz = pytz.timezone('US/Eastern')
                dt_local = dt.astimezone(local_tz)
                return dt_local.strftime('%Y-%m-%d %H:%M:%S') + " (美东时间)"
            else:
                local_tz = pytz.timezone('Asia/Shanghai')
                dt_local = dt.astimezone(local_tz)
                return dt_local.strftime('%Y-%m-%d %H:%M:%S') + " (北京时间)"
        elif hasattr(ts, 'year'):
            dt = ts
            if is_us_index:
                if dt.tzinfo is None:
                    dt = pytz.timezone('US/Eastern').localize(dt)
                return dt.strftime('%Y-%m-%d %H:%M:%S') + " (美东时间)"
            else:
                if dt.tzinfo is None:
                    bj_tz = pytz.timezone('Asia/Shanghai')
                    dt = bj_tz.localize(dt)
                return dt.strftime('%Y-%m-%d %H:%M:%S') + " (北京时间)"
        else:
            return str(ts)
    except Exception as e:
        return str(ts)


# =============================================================================
# Main Function
# 主函数
# =============================================================================

def main():
    """
    Main function: Execute complete market data fetching process
    主函数：执行完整的市场数据获取流程

    Execution Steps:
        1. Load targets.json configuration file
        2. Extract index and stock lists
        3. Create Longport connection
        4. Iterate to fetch all index data
        5. Iterate to fetch all stock data
        6. Save data to CSV files
        7. Print data to console
    执行步骤：
        1. 加载targets.json配置文件
        2. 提取指数和股票列表
        3. 创建Longport连接
        4. 遍历获取所有指数数据
        5. 遍历获取所有股票数据
        6. 保存数据到CSV文件
        7. 打印数据到控制台

    Output Files:
        - output/index_data.csv: Index data
        - output/stock_data.csv: Stock data
    输出文件：
        - output/index_data.csv: 指数数据
        - output/stock_data.csv: 个股数据

    Exit Codes:
        - 0: Normal completion
        - 1: Longport connection creation failed
    退出码：
        - 0: 正常完成
        - 1: Longport连接创建失败

    Timezone Notes:
        - HK stock data uses Beijing time
        - US stock data uses US Eastern time
    时区说明：
        - 港股数据使用北京时间
        - 美股数据使用美东时间
    """
    logger.info("=== Starting market data fetch via Longport SDK ===")

    # Load configuration file
    # 加载配置文件
    targets_config = load_targets_config()
    INDICES = get_indices_from_config(targets_config)
    STOCKS = get_stocks_from_config(targets_config)

    logger.info(f"Loaded {len(INDICES)} indices and {len(STOCKS)} stocks from config")

    # Create Longport connection
    # 创建Longport连接
    ctx = get_longport_context()

    if ctx is None:
        logger.error("Cannot create Longport context, exiting")
        sys.exit(1)

    # Fetch index data
    # 获取指数数据
    logger.info("--- Fetching Index Data ---")
    index_results = []
    for idx in INDICES:
        logger.info(f"Fetching index: {idx['指数名称']} ({idx['lp_code']})")
        # Check if it's a US index
        # 判断是否为美股指数
        is_us = idx['指数名称'] in ["纳斯达克100指数", "标普500指数", "道琼斯指数"]
        price, ts, source = fetch_longport_stock_data(ctx, idx['lp_code'])

        time_str = format_timestamp(ts, is_us) if ts else "获取失败"
        index_results.append({
            "指数名称": idx['指数名称'],
            "指数代码": idx['指数代码'],
            "当前最新点数": price if price else "获取失败",
            "当前最新点数对应时间戳": time_str,
            "数据来源": source
        })
        time.sleep(0.3)  # Avoid too fast requests
        # 避免请求过快

    # Save index data to CSV
    # 保存指数数据到CSV
    df_index = pd.DataFrame(index_results)
    index_csv = os.path.join(OUTPUT_DIR, 'index_data.csv')
    df_index.to_csv(index_csv, index=False, encoding='utf-8-sig')
    logger.info(f"Index data saved to {index_csv}")

    # Fetch stock data
    # 获取个股数据
    logger.info("--- Fetching Stock Data ---")
    stock_results = []
    for i, stock in enumerate(STOCKS):
        logger.info(f"Fetching stock: {stock['股票名称']} ({stock['lp_code']})")
        price, ts, source = fetch_longport_stock_data(ctx, stock['lp_code'])
        time_str = format_timestamp(ts, False) if ts else "获取失败"
        stock_results.append({
            "股票名称": stock['股票名称'],
            "股票代码": stock['股票代码'],
            "当前最新价格(HKD)": price if price else "获取失败",
            "当前最新价格对应时间戳": time_str,
            "数据来源": source
        })
        time.sleep(0.3)  # Avoid too fast requests
        # 避免请求过快

    # Save stock data to CSV
    # 保存个股数据到CSV
    df_stock = pd.DataFrame(stock_results)
    stock_csv = os.path.join(OUTPUT_DIR, 'stock_data.csv')
    df_stock.to_csv(stock_csv, index=False, encoding='utf-8-sig')
    logger.info(f"Stock data saved to {stock_csv}")

    logger.info("=== Data fetch completed ===")

    # Print data to console
    # 打印数据到控制台
    print("\n=== 指数数据 ===")
    print(df_index.to_string(index=False))
    print("\n=== 个股数据 ===")
    print(df_stock.to_string(index=False))


if __name__ == "__main__":
    main()
