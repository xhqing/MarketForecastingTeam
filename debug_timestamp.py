"""
Timestamp Debugging Script
时间戳调试脚本

=============================================================================
File Function:
    This script is used to debug the timestamp format returned by Longport API
    and diagnose timestamp conversion issues. Mainly used to troubleshoot:
    - Timestamp type mismatch (int vs datetime object)
    - Timestamp is 0 or abnormal value
    - Timezone conversion errors
    - HK stock close timestamp showing as 00:00:00
文件功能：
    本脚本用于调试Longport API返回的时间戳格式，诊断时间戳转换问题。
    主要用于排查以下问题：
    - 时间戳类型不匹配（int vs datetime对象）
    - 时间戳为0或异常值
    - 时区转换错误
    - 港股收盘时间戳显示为00:00:00

=============================================================================
Debug Content:
    1. Timestamp format returned by ctx.quote()
       - last_done: Latest trade price
       - timestamp: Trade timestamp
       - timestamp type: may be int, float, or datetime object

    2. Timestamp format returned by ctx.candlesticks()
       - Returns the latest N K-line data
       - Close time and close price for each K-line
       - Used to compare with timestamp returned by quote

    3. datetime timestamp conversion test
       - int/float timestamp to UTC datetime
       - UTC datetime to Beijing time
       - datetime object direct timezone conversion
调试内容：
    1. ctx.quote() 返回的时间戳格式
       - last_done: 最新成交价
       - timestamp: 成交时间戳
       - timestamp类型：可能是int、float或datetime对象

    2. ctx.candlesticks() 返回的时间戳格式
       - 返回最近N条K线数据
       - 每条K线的收盘时间和收盘价
       - 用于对比quote返回的时间戳

    3. datetime时间戳转换测试
       - int/float时间戳转换为UTC datetime
       - UTC datetime转换为北京时间
       - datetime对象直接时区转换

=============================================================================
Test Symbols:
    - 00700.HK: Tencent Holdings
    - 09988.HK: Alibaba
    - 9988.HK: Alibaba (duplicate, possibly US stock code)
测试标的：
    - 00700.HK: 腾讯控股
    - 09988.HK: 阿里巴巴
    - 9988.HK: 阿里巴巴（重复，可能是美股代码）

=============================================================================
Usage Scenarios:
    Use when the following issues appear in reports:
    - Timestamp shows as 00:00:00 (invalid time)
    - Timestamp is 8 hours later or 8 hours earlier than actual trading time (timezone issue)
    - Timestamp type error causing formatting failure
使用场景：
    当研报中出现以下问题时使用：
    - 时间戳显示为 00:00:00（无效时间）
    - 时间戳比实际交易时间晚8小时或早8小时（时区问题）
    - 时间戳类型错误导致格式化失败

=============================================================================
Dependencies:
    - Longport SDK (longbridge.openapi)
    - Python standard library: datetime, pytz, logging
    - API credentials config in config.py
依赖：
    - Longport SDK (longbridge.openapi)
    - Python标准库：datetime, pytz, logging
    - config.py中的API凭证配置

=============================================================================
Output Example:
    Current Beijing time: 2026-04-23 16:30:00+08:00
    Expected market close time (HK): 16:00-16:08 Beijing time
输出示例：
    Current Beijing time: 2026-04-23 16:30:00+08:00
    Expected market close time (HK): 16:00-16:08 Beijing time

=============================================================================
Author/Maintainer: AI Agent (TRAE CN SOLO GLM5.1)
Last Updated: 2026-04-23
作者/维护者：AI Agent (TRAE CN SOLO GLM5.1)
最后更新：2026-04-23
=============================================================================
"""

import os
import sys
import logging
from datetime import datetime
import pytz

# =============================================================================
# Logging Configuration
# 日志配置
# =============================================================================

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# =============================================================================
# Longport SDK Import
# Longport SDK导入
# =============================================================================

try:
    from longbridge.openapi import QuoteContext, Config, Period, AdjustType
    LONGPORT_AVAILABLE = True
except ImportError:
    LONGPORT_AVAILABLE = False
    logger.error("Longport SDK not available")

# =============================================================================
# API Credentials Configuration
# API凭证配置
# =============================================================================

# Default placeholder values (only for debugging, load from config.py in actual use)
# 默认占位符值（仅用于调试，实际使用时从config.py加载）
APP_KEY = "placeholder"
APP_SECRET = "placeholder"
ACCESS_TOKEN = "placeholder"

# Try to load real API credentials from config.py
# 尝试从config.py加载真实的API凭证
try:
    from config import LONGPORT_APP_KEY, LONGPORT_APP_SECRET, LONGPORT_ACCESS_TOKEN
    APP_KEY = LONGPORT_APP_KEY
    APP_SECRET = LONGPORT_APP_SECRET
    ACCESS_TOKEN = LONGPORT_ACCESS_TOKEN
except ImportError:
    # If config.py does not exist, use default placeholder
    # This is normal in debugging environment
    # 如果config.py不存在，使用默认占位符
    # 这种情况在调试环境中是正常的
    pass

# =============================================================================
# Longport Connection Function
# Longport连接函数
# =============================================================================

def get_longport_context():
    """
    Create Longport QuoteContext connection object
    创建Longport QuoteContext连接对象

    Returns:
        QuoteContext or None: Returns QuoteContext object on success, None on failure
    返回：
        QuoteContext或None: 成功返回QuoteContext对象，失败返回None

    Exception Handling:
        - If Longport SDK is not available, returns None
        - If connection creation fails, logs error with logger.error and returns None
    异常处理：
        - 如果Longport SDK不可用，返回None
        - 如果创建连接失败，使用logger.error记录错误并返回None
    """
    if not LONGPORT_AVAILABLE:
        return None
    try:
        config = Config(app_key=APP_KEY, app_secret=APP_SECRET, access_token=ACCESS_TOKEN)
        ctx = QuoteContext(config)
        return ctx
    except Exception as e:
        logger.error(f"Failed to create Longport context: {e}")
        return None

# =============================================================================
# Timestamp Debugging Function
# 时间戳调试函数
# =============================================================================

def debug_timestamp():
    """
    Debug timestamp format returned by Longport API
    调试Longport API返回的时间戳格式

    Debug Flow:
        1. Create Longport connection
        2. Iterate through test symbol list
        3. Perform three tests for each symbol:
           - ctx.quote(): Get real-time quote and timestamp
           - ctx.candlesticks(): Get K-line data and timestamp
           - datetime conversion: Test conversion of different format timestamps
        4. Print detailed debugging information
    调试流程：
        1. 创建Longport连接
        2. 遍历测试标的列表
        3. 对每个标的执行三种测试：
           - ctx.quote(): 获取实时报价和时间戳
           - ctx.candlesticks(): 获取K线数据和时间戳
           - datetime转换: 测试不同格式时间戳的转换
        4. 打印详细的调试信息

    Test Symbols:
        - 00700.HK: Tencent Holdings (HK stock)
        - 09988.HK: Alibaba (HK stock)
        - 9988.HK: Alibaba (alternate code)
    测试标的：
        - 00700.HK: 腾讯控股（港股）
        - 09988.HK: 阿里巴巴（港股）
        - 9988.HK: 阿里巴巴（备用代码）

    Diagnostic Issues:
        - Timestamp type mismatch: print type().__name__
        - Timestamp value abnormal: print repr() to show raw value
        - Timezone conversion error: show UTC and Beijing time comparison
    诊断问题：
        - 时间戳类型不匹配：打印type().__name__
        - 时间戳值异常：打印repr()显示原始值
        - 时区转换错误：显示UTC和北京时间对比
    """
    ctx = get_longport_context()
    if ctx is None:
        logger.error("Cannot create Longport context")
        return

    # Test symbol list
    # 测试标的列表
    symbols = ["00700.HK", "09988.HK", "9988.HK"]

    for symbol in symbols:
        logger.info(f"\n=== Debugging symbol: {symbol} ===")

        # -------------------------------------------------------------------------
        # Test 1: ctx.quote() Get real-time quote
        # 测试1: ctx.quote() 获取实时报价
        # -------------------------------------------------------------------------
        logger.info("1. Testing ctx.quote()")
        try:
            quotes = ctx.quote([symbol])
            if quotes:
                q = quotes[0]
                print(f"  quote.last_done: {q.last_done}")
                print(f"  quote.timestamp: {q.timestamp} (type: {type(q.timestamp).__name__})")
                print(f"  quote.timestamp type value: {repr(q.timestamp)}")
        except Exception as e:
            print(f"  quote failed: {e}")

        # -------------------------------------------------------------------------
        # Test 2: ctx.candlesticks() Get K-line data
        # 测试2: ctx.candlesticks() 获取K线数据
        # -------------------------------------------------------------------------
        logger.info("2. Testing ctx.candlesticks()")
        try:
            # Get latest 5 daily K-lines
            # 获取最近5条日K线
            candles = ctx.candlesticks(symbol, Period.Day, 5, AdjustType.NoAdjust)
            if candles:
                print(f"  Number of candles: {len(candles)}")
                for i, c in enumerate(candles):
                    print(f"  Candle {i}: close={c.close}, timestamp={c.timestamp} (type: {type(c.timestamp).__name__})")
                    print(f"    timestamp repr: {repr(c.timestamp)}")
            else:
                print("  No candles returned")
        except Exception as e:
            print(f"  candlesticks failed: {e}")

        # -------------------------------------------------------------------------
        # Test 3: datetime timestamp conversion
        # 测试3: datetime时间戳转换
        # -------------------------------------------------------------------------
        logger.info("3. Testing datetime conversion")
        try:
            candles = ctx.candlesticks(symbol, Period.Day, 1, AdjustType.NoAdjust)
            if candles:
                c = candles[-1]
                ts = c.timestamp
                print(f"  Original timestamp: {repr(ts)}")

                # Handle int/float timestamp types
                # 处理int/float类型时间戳
                if isinstance(ts, (int, float)):
                    from datetime import timezone
                    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
                    print(f"  As int/float -> UTC datetime: {dt}")
                elif hasattr(ts, 'year'):
                    # Handle datetime objects
                    # 处理datetime对象
                    print(f"  Has year attribute -> {ts}")

                # Convert to Beijing time
                # 转换为北京时间
                bj_tz = pytz.timezone('Asia/Shanghai')
                if isinstance(ts, (int, float)):
                    dt_local = datetime.fromtimestamp(ts, tz=timezone.utc).astimezone(bj_tz)
                else:
                    dt_local = ts.astimezone(bj_tz) if hasattr(ts, 'astimezone') else str(ts)
                print(f"  Converted to Beijing time: {dt_local}")
        except Exception as e:
            print(f"  datetime conversion failed: {e}")

        print()

    # -------------------------------------------------------------------------
    # Print current time and HK stock close time reference
    # 打印当前时间和港股收盘时间参考
    # -------------------------------------------------------------------------
    bj_tz = pytz.timezone('Asia/Shanghai')
    now_bj = datetime.now(bj_tz)
    print(f"\nCurrent Beijing time: {now_bj}")
    print(f"Expected market close time (HK): 16:00-16:08 Beijing time")


if __name__ == "__main__":
    debug_timestamp()
