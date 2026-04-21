import os
import sys
import json
import time
import logging
import pandas as pd
from datetime import datetime
import pytz

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

try:
    from longport.openapi import QuoteContext, Config, Period, AdjustType
    LONGPORT_AVAILABLE = True
    logger.info("Longport SDK available")
except ImportError:
    LONGPORT_AVAILABLE = False
    logger.warning("Longport SDK not available")

APP_KEY = "aa01486322da47b757d479b7d934af5e"
APP_SECRET = "e07e845719888a88f245ee07161ca9d7bccd5c36a550d68dcea479b3cf419da3"
ACCESS_TOKEN = "m_eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ5YWRiMGIxYTdlNzYxNzEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJsb25nYnJpZGdlIiwic3ViIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzg0MjY2MzM0LCJpYXQiOjE3NzY0OTAzMzUsImFrIjoiYWEwMTQ4NjMyMmRhNDdiNzU3ZDQ3OWI3ZDkzNGFmNWUiLCJhYWlkIjoyMDg2MTM4MCwiYWMiOiJsYl9wYXBlcnRyYWRpbmciLCJtaWQiOjE4NDIyMjcyLCJzaWQiOiJ5MENjY1kydXpDeW93b2w2ZTRwcUFBPT0iLCJibCI6MywidWwiOjAsImlrIjoibGJfcGFwZXJ0cmFkaW5nXzIwODYxMzgwIn0.JcuyfiWjzWCFSU--cWM6dv7UBL6iQUBY8qOwxx1VoW8zXY3MWtgxX7EUkA_Cy0R3wWpRrYYIwklX83ed7MZcc6YhcGxL-EmC-Ur_59QCyqu5pJ0ScPAPmke5JppML53nLqChwlqhZVMPHs8wKT9BiwKFIVu5wzOb2LI7v5QbFgzpzW5aLHM7iNXaLFGnhLRYDJ81kuzJ4KJtlK8okD1fsjnDQmrMoNBruWfUlmP2bthU3Xv222PTARdQS6EKqVh2PKe1KzLjC7gcZ93N9bqwOaetNl0_gM50SvlUYTILugOPIgW-RyFtkRkmgeb4Abx9c7rY9UYNmGSSCh7KCVN0jpC84jAjK3VEsJid9HAGP2LGWfCdHcgvX2yix6p5DLkoALDsg_iFgz4TfGeiAtGyVpMT0HKsfgz8UHK4ibbvRXm4B_uOHRRNa2F34BnULg0LewY1Ys-lmGka_5s0YMREcESZI-Zw9dju4stRLhArag1iaky_UbHwOZVzP9X-DcAhO2M-GSYgAwB0lImYe53BGzLAxH_aX8SalGs7y8p63dH8H_Vern1DU1h7fKdfN1iKR9r-OsAEvsOlOcQu1Tp-HbZOHg5t9Lf9lXdlyFSMWMy6cevjcW4KoLXi6agWBxc15TiNBZzyxhLTZlOdkOmSqlc7ICehJAPd0iPNC0d3ec4"

INDICES = [
    {"指数名称": "恒生指数", "指数代码": "HSI", "lp_code": "HSI"},
    {"指数名称": "恒生科技指数", "指数代码": "HSTECH", "lp_code": "HSTECH"},
    {"指数名称": "国企指数", "指数代码": "HSCEI", "lp_code": "HSCEI"},
    {"指数名称": "纳斯达克100指数", "指数代码": ".NDX", "lp_code": ".NDX"},
    {"指数名称": "标普500指数", "指数代码": ".SPX", "lp_code": ".SPX"},
    {"指数名称": "道琼斯指数", "指数代码": ".DJI", "lp_code": ".DJI"},
]

STOCKS = [
    {"股票名称": "腾讯控股", "股票代码": "00700.HK", "lp_code": "00700.HK"},
    {"股票名称": "阿里巴巴", "股票代码": "09988.HK", "lp_code": "09988.HK"},
    {"股票名称": "小米", "股票代码": "01810.HK", "lp_code": "01810.HK"},
    {"股票名称": "快手", "股票代码": "01024.HK", "lp_code": "01024.HK"},
    {"股票名称": "京东", "股票代码": "09618.HK", "lp_code": "09618.HK"},
    {"股票名称": "美团", "股票代码": "03690.HK", "lp_code": "03690.HK"},
    {"股票名称": "紫金矿业", "股票代码": "02899.HK", "lp_code": "02899.HK"},
    {"股票名称": "中芯国际", "股票代码": "00981.HK", "lp_code": "00981.HK"},
    {"股票名称": "华虹半导体", "股票代码": "01347.HK", "lp_code": "01347.HK"},
    {"股票名称": "泡泡玛特", "股票代码": "09992.HK", "lp_code": "09992.HK"},
    {"股票名称": "中国神华", "股票代码": "01088.HK", "lp_code": "01088.HK"},
    {"股票名称": "宁德时代", "股票代码": "03750.HK", "lp_code": "03750.HK"},
    {"股票名称": "赣锋锂业", "股票代码": "01772.HK", "lp_code": "01772.HK"},
    {"股票名称": "昆仑能源", "股票代码": "00135.HK", "lp_code": "00135.HK"},
    {"股票名称": "中国石油化工股份", "股票代码": "00386.HK", "lp_code": "00386.HK"},
    {"股票名称": "国泰君安国际", "股票代码": "01788.HK", "lp_code": "01788.HK"},
    {"股票名称": "中国宏桥", "股票代码": "01378.HK", "lp_code": "01378.HK"},
    {"股票名称": "招商银行", "股票代码": "03968.HK", "lp_code": "03968.HK"},
    {"股票名称": "建设银行", "股票代码": "00939.HK", "lp_code": "00939.HK"},
    {"股票名称": "中国银行", "股票代码": "03988.HK", "lp_code": "03988.HK"},
    {"股票名称": "汇丰控股", "股票代码": "00005.HK", "lp_code": "00005.HK"},
    {"股票名称": "信达生物", "股票代码": "01801.HK", "lp_code": "01801.HK"},
    {"股票名称": "药明生物", "股票代码": "02269.HK", "lp_code": "02269.HK"},
    {"股票名称": "中国海洋石油", "股票代码": "00883.HK", "lp_code": "00883.HK"},
    {"股票名称": "中国石油股份", "股票代码": "00857.HK", "lp_code": "00857.HK"},
    {"股票名称": "工商银行", "股票代码": "01398.HK", "lp_code": "01398.HK"},
    {"股票名称": "比亚迪股份", "股票代码": "01211.HK", "lp_code": "01211.HK"},
]

CBBC_STOCKS = [
    {"股票名称": "新鸿基地产", "股票代码": "00016.HK", "lp_code": "00016.HK"},
    {"股票名称": "恒基地产", "股票代码": "00012.HK", "lp_code": "00012.HK"},
    {"股票名称": "新世界发展", "股票代码": "00017.HK", "lp_code": "00017.HK"},
    {"股票名称": "长实集团", "股票代码": "01113.HK", "lp_code": "01113.HK"},
    {"股票名称": "香港交易所", "股票代码": "00388.HK", "lp_code": "00388.HK"},
    {"股票名称": "友邦保险", "股票代码": "01299.HK", "lp_code": "01299.HK"},
    {"股票名称": "中国人寿", "股票代码": "02628.HK", "lp_code": "02628.HK"},
    {"股票名称": "中国平安", "股票代码": "02318.HK", "lp_code": "02318.HK"},
    {"股票名称": "中国移动", "股票代码": "00941.HK", "lp_code": "00941.HK"},
    {"股票名称": "中国联通", "股票代码": "00762.HK", "lp_code": "00762.HK"},
    {"股票名称": "中国电信", "股票代码": "00728.HK", "lp_code": "00728.HK"},
    {"股票名称": "网易", "股票代码": "09999.HK", "lp_code": "09999.HK"},
    {"股票名称": "百度集团", "股票代码": "09888.HK", "lp_code": "09888.HK"},
    {"股票名称": "哔哩哔哩", "股票代码": "09626.HK", "lp_code": "09626.HK"},
    {"股票名称": "蔚来", "股票代码": "09866.HK", "lp_code": "09866.HK"},
    {"股票名称": "理想汽车", "股票代码": "02015.HK", "lp_code": "02015.HK"},
    {"股票名称": "小鹏汽车", "股票代码": "09868.HK", "lp_code": "09868.HK"},
    {"股票名称": "海尔智家", "股票代码": "06690.HK", "lp_code": "06690.HK"},
    {"股票名称": "李宁", "股票代码": "02331.HK", "lp_code": "02331.HK"},
    {"股票名称": "安踏体育", "股票代码": "02020.HK", "lp_code": "02020.HK"},
]


def get_longport_context():
    if not LONGPORT_AVAILABLE:
        return None
    try:
        config = Config(
            app_key=APP_KEY,
            app_secret=APP_SECRET,
            access_token=ACCESS_TOKEN,
        )
        ctx = QuoteContext(config)
        logger.info("Longport context created successfully")
        return ctx
    except Exception as e:
        logger.error(f"Failed to create Longport context: {e}")
        return None


def fetch_longport_quote(ctx, symbols):
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
    if ctx is None:
        return None, None, None
    price = None
    ts = None
    source = "Longport API"
    try:
        quotes = ctx.quote([symbol])
        if quotes:
            q = quotes[0]
            price = round(float(q.last_done), 2)
            ts = q.timestamp
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


def format_timestamp(ts, is_us_index=False):
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


def main():
    logger.info("=== Starting market data fetch via Longport SDK ===")

    ctx = get_longport_context()

    if ctx is None:
        logger.error("Cannot create Longport context, exiting")
        sys.exit(1)

    logger.info("--- Fetching Index Data ---")
    index_results = []
    for idx in INDICES:
        logger.info(f"Fetching index: {idx['指数名称']} ({idx['lp_code']})")
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
        time.sleep(0.3)

    df_index = pd.DataFrame(index_results)
    index_csv = os.path.join(OUTPUT_DIR, 'index_data.csv')
    df_index.to_csv(index_csv, index=False, encoding='utf-8-sig')
    logger.info(f"Index data saved to {index_csv}")

    logger.info("--- Fetching Stock Data ---")
    all_stocks = STOCKS + CBBC_STOCKS
    stock_symbols = [s['lp_code'] for s in STOCKS]
    cbbc_symbols = [s['lp_code'] for s in CBBC_STOCKS]

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
        time.sleep(0.3)

    df_stock = pd.DataFrame(stock_results)
    stock_csv = os.path.join(OUTPUT_DIR, 'stock_data.csv')
    df_stock.to_csv(stock_csv, index=False, encoding='utf-8-sig')
    logger.info(f"Stock data saved to {stock_csv}")

    logger.info("--- Fetching CBBC Stock Data ---")
    cbbc_results = []
    for stock in CBBC_STOCKS:
        logger.info(f"Fetching CBBC stock: {stock['股票名称']} ({stock['lp_code']})")
        price, ts, source = fetch_longport_stock_data(ctx, stock['lp_code'])
        time_str = format_timestamp(ts, False) if ts else "获取失败"
        cbbc_results.append({
            "股票名称": stock['股票名称'],
            "股票代码": stock['股票代码'],
            "当前最新价格(HKD)": price if price else "获取失败",
            "当前最新价格对应时间戳": time_str,
            "数据来源": source
        })
        time.sleep(0.3)

    df_cbbc = pd.DataFrame(cbbc_results)
    cbbc_csv = os.path.join(OUTPUT_DIR, 'cbbc_stock_data.csv')
    df_cbbc.to_csv(cbbc_csv, index=False, encoding='utf-8-sig')
    logger.info(f"CBBC stock data saved to {cbbc_csv}")

    logger.info("=== Data fetch completed ===")

    print("\n=== 指数数据 ===")
    print(df_index.to_string(index=False))
    print("\n=== 指定个股数据 ===")
    print(df_stock.to_string(index=False))
    print("\n=== 牛熊证个股数据 ===")
    print(df_cbbc.to_string(index=False))


if __name__ == "__main__":
    main()
