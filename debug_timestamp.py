import os
import sys
import logging
from datetime import datetime
import pytz

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from longport.openapi import QuoteContext, Config, Period, AdjustType
    LONGPORT_AVAILABLE = True
except ImportError:
    LONGPORT_AVAILABLE = False
    logger.error("Longport SDK not available")

APP_KEY = "placeholder"
APP_SECRET = "placeholder"
ACCESS_TOKEN = "placeholder"

try:
    from config import LONGPORT_APP_KEY, LONGPORT_APP_SECRET, LONGPORT_ACCESS_TOKEN
    APP_KEY = LONGPORT_APP_KEY
    APP_SECRET = LONGPORT_APP_SECRET
    ACCESS_TOKEN = LONGPORT_ACCESS_TOKEN
except ImportError:
    pass

def get_longport_context():
    if not LONGPORT_AVAILABLE:
        return None
    try:
        config = Config(app_key=APP_KEY, app_secret=APP_SECRET, access_token=ACCESS_TOKEN)
        ctx = QuoteContext(config)
        return ctx
    except Exception as e:
        logger.error(f"Failed to create Longport context: {e}")
        return None

def debug_timestamp():
    ctx = get_longport_context()
    if ctx is None:
        logger.error("Cannot create Longport context")
        return

    symbols = ["00700.HK", "09988.HK", "9988.HK"]

    for symbol in symbols:
        logger.info(f"\n=== Debugging symbol: {symbol} ===")

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

        logger.info("2. Testing ctx.candlesticks()")
        try:
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

        logger.info("3. Testing datetime conversion")
        try:
            candles = ctx.candlesticks(symbol, Period.Day, 1, AdjustType.NoAdjust)
            if candles:
                c = candles[-1]
                ts = c.timestamp
                print(f"  Original timestamp: {repr(ts)}")

                if isinstance(ts, (int, float)):
                    from datetime import timezone
                    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
                    print(f"  As int/float -> UTC datetime: {dt}")
                elif hasattr(ts, 'year'):
                    print(f"  Has year attribute -> {ts}")

                bj_tz = pytz.timezone('Asia/Shanghai')
                if isinstance(ts, (int, float)):
                    dt_local = datetime.fromtimestamp(ts, tz=timezone.utc).astimezone(bj_tz)
                else:
                    dt_local = ts.astimezone(bj_tz) if hasattr(ts, 'astimezone') else str(ts)
                print(f"  Converted to Beijing time: {dt_local}")
        except Exception as e:
            print(f"  datetime conversion failed: {e}")

        print()

    bj_tz = pytz.timezone('Asia/Shanghai')
    now_bj = datetime.now(bj_tz)
    print(f"\nCurrent Beijing time: {now_bj}")
    print(f"Expected market close time (HK): 16:00-16:08 Beijing time")

if __name__ == "__main__":
    debug_timestamp()
