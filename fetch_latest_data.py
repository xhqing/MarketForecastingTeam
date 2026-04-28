"""
最新市场数据获取脚本 - 使用akshare获取港股和美股数据
数据源: stock_hk_daily (新浪财经), index_us_stock_sina (新浪财经)
"""

import akshare as ak
import pandas as pd
import os
import json
from datetime import datetime
import pytz
import time

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

bj_tz = pytz.timezone('Asia/Shanghai')
us_eastern_tz = pytz.timezone('US/Eastern')


def fetch_hk_index_data():
    index_map = {
        "HSI": "恒生指数",
        "HSTECH": "恒生科技指数",
        "HSCEI": "国企指数",
    }
    results = []
    for code, name in index_map.items():
        try:
            df = ak.stock_hk_index_daily_sina(symbol=code)
            if df is not None and not df.empty:
                latest = df.iloc[-1]
                close_price = float(latest['close'])
                date_str = str(latest['date'])
                try:
                    dt = datetime.strptime(date_str, "%Y-%m-%d")
                    dt_bj = bj_tz.localize(dt.replace(hour=16, minute=0, second=0))
                    time_str = dt_bj.strftime('%Y-%m-%d %H:%M:%S') + " (北京时间)"
                except:
                    time_str = date_str + " 16:00:00 (北京时间)"
                source = "https://cn.stockq.org/index/" + code + ".php"
                results.append({
                    "指数名称": name,
                    "指数代码": code,
                    "当前最新点数": close_price,
                    "当前最新点数对应时间戳": time_str,
                    "数据来源": source
                })
                print(f"  ✓ {name}: {close_price} ({date_str})")
            else:
                results.append({"指数名称": name, "指数代码": code, "当前最新点数": "获取失败", "当前最新点数对应时间戳": "获取失败", "数据来源": ""})
                print(f"  ✗ {name}: 获取失败(empty)")
        except Exception as e:
            print(f"  ✗ {name}: {e}")
            results.append({"指数名称": name, "指数代码": code, "当前最新点数": "获取失败", "当前最新点数对应时间戳": "获取失败", "数据来源": ""})
        time.sleep(0.5)
    return results


def fetch_us_index_data():
    us_indices = [
        {"name": "纳斯达克100指数", "code": ".NDX", "sina_code": ".NDX"},
        {"name": "标普500指数", "code": ".SPX", "sina_code": ".INX"},
        {"name": "道琼斯工业指数", "code": ".DJI", "sina_code": ".DJI"},
    ]
    results = []
    for idx in us_indices:
        try:
            df = ak.index_us_stock_sina(symbol=idx["sina_code"])
            if df is not None and not df.empty:
                latest = df.iloc[-1]
                close_price = float(latest['close'])
                date_str = str(latest['date'])
                try:
                    dt = datetime.strptime(date_str, "%Y-%m-%d")
                    dt_us = us_eastern_tz.localize(dt.replace(hour=16, minute=0, second=0))
                    time_str = dt_us.strftime('%Y-%m-%d %H:%M:%S') + " (美东时间)"
                except:
                    time_str = date_str + " 16:00:00 (美东时间)"
                yahoo_code = idx["code"].replace(".", "%5E")
                source = "https://finance.yahoo.com/quote/" + yahoo_code
                results.append({
                    "指数名称": idx["name"],
                    "指数代码": idx["code"],
                    "当前最新点数": close_price,
                    "当前最新点数对应时间戳": time_str,
                    "数据来源": source
                })
                print(f"  ✓ {idx['name']}: {close_price} ({date_str})")
            else:
                results.append({"指数名称": idx["name"], "指数代码": idx["code"], "当前最新点数": "获取失败", "当前最新点数对应时间戳": "获取失败", "数据来源": ""})
        except Exception as e:
            print(f"  ✗ {idx['name']}: {e}")
            results.append({"指数名称": idx["name"], "指数代码": idx["code"], "当前最新点数": "获取失败", "当前最新点数对应时间戳": "获取失败", "数据来源": ""})
        time.sleep(0.5)
    return results


def fetch_hk_stock_data():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'targets.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    stocks = config.get('hk_shares', {}).get('hkex_stocks', [])
    stocks = [s for s in stocks if s.get('name') and s.get('code')]

    results = []
    for stock in stocks:
        name = stock['name']
        code = stock['code']
        ak_code = code.replace('.HK', '')
        try:
            df = ak.stock_hk_daily(symbol=ak_code, adjust='qfq')
            if df is not None and not df.empty:
                latest = df.iloc[-1]
                close_price = float(latest['close'])
                date_str = str(latest['date'])
                try:
                    dt = datetime.strptime(date_str, "%Y-%m-%d")
                    dt_bj = bj_tz.localize(dt.replace(hour=16, minute=8, second=0))
                    time_str = dt_bj.strftime('%Y-%m-%d %H:%M:%S') + " (北京时间)"
                except:
                    time_str = date_str + " 16:08:00 (北京时间)"
                source = "https://www.aastocks.com/sc/cnhk/quote/quote.aspx?symbol=" + ak_code
                results.append({
                    "股票名称": name,
                    "股票代码": code,
                    "当前最新价格(HKD)": close_price,
                    "当前最新价格对应时间戳": time_str,
                    "数据来源": source
                })
                print(f"  ✓ {name} ({code}): {close_price} ({date_str})")
            else:
                results.append({"股票名称": name, "股票代码": code, "当前最新价格(HKD)": "获取失败", "当前最新价格对应时间戳": "获取失败", "数据来源": ""})
                print(f"  ✗ {name} ({code}): 获取失败(empty)")
        except Exception as e:
            print(f"  ✗ {name} ({code}): {str(e)[:60]}")
            results.append({"股票名称": name, "股票代码": code, "当前最新价格(HKD)": "获取失败", "当前最新价格对应时间戳": "获取失败", "数据来源": ""})
        time.sleep(0.3)
    return results


def fetch_hk_etf_data():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'targets.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    etfs = config.get('hk_shares', {}).get('hkex_etf', [])
    etfs = [e for e in etfs if e.get('name') and e.get('code')]

    results = []
    for etf in etfs:
        name = etf['name']
        code = etf['code']
        ak_code = code.replace('.HK', '')
        try:
            df = ak.stock_hk_daily(symbol=ak_code, adjust='qfq')
            if df is not None and not df.empty:
                latest = df.iloc[-1]
                close_price = float(latest['close'])
                date_str = str(latest['date'])
                try:
                    dt = datetime.strptime(date_str, "%Y-%m-%d")
                    dt_bj = bj_tz.localize(dt.replace(hour=16, minute=8, second=0))
                    time_str = dt_bj.strftime('%Y-%m-%d %H:%M:%S') + " (北京时间)"
                except:
                    time_str = date_str + " 16:08:00 (北京时间)"
                source = "https://www.aastocks.com/sc/cnhk/quote/quote.aspx?symbol=" + ak_code
                results.append({
                    "ETF名称": name,
                    "ETF代码": code,
                    "当前最新价格(HKD)": close_price,
                    "当前最新价格对应时间戳": time_str,
                    "数据来源": source
                })
                print(f"  ✓ {name} ({code}): {close_price} ({date_str})")
            else:
                results.append({"ETF名称": name, "ETF代码": code, "当前最新价格(HKD)": "获取失败", "当前最新价格对应时间戳": "获取失败", "数据来源": ""})
                print(f"  ✗ {name} ({code}): 获取失败(empty)")
        except Exception as e:
            print(f"  ✗ {name} ({code}): {str(e)[:60]}")
            results.append({"ETF名称": name, "ETF代码": code, "当前最新价格(HKD)": "获取失败", "当前最新价格对应时间戳": "获取失败", "数据来源": ""})
        time.sleep(0.3)
    return results


def main():
    print("=" * 60)
    print("开始获取最新市场数据 (akshare - sina数据源)")
    print("=" * 60)

    print("\n--- 获取港股指数数据 ---")
    hk_index_results = fetch_hk_index_data()

    print("\n--- 获取美股指数数据 ---")
    us_index_results = fetch_us_index_data()

    all_index_results = hk_index_results + us_index_results
    df_index = pd.DataFrame(all_index_results)
    index_csv = os.path.join(OUTPUT_DIR, 'index_data.csv')
    df_index.to_csv(index_csv, index=False, encoding='utf-8-sig')
    print(f"\n指数数据已保存到 {index_csv}")

    print("\n--- 获取港股个股数据 ---")
    stock_results = fetch_hk_stock_data()
    df_stock = pd.DataFrame(stock_results)
    stock_csv = os.path.join(OUTPUT_DIR, 'stock_data.csv')
    df_stock.to_csv(stock_csv, index=False, encoding='utf-8-sig')
    print(f"\n个股数据已保存到 {stock_csv}")

    print("\n--- 获取港股ETF数据 ---")
    etf_results = fetch_hk_etf_data()
    df_etf = pd.DataFrame(etf_results)
    etf_csv = os.path.join(OUTPUT_DIR, 'etf_data.csv')
    df_etf.to_csv(etf_csv, index=False, encoding='utf-8-sig')
    print(f"\nETF数据已保存到 {etf_csv}")

    print("\n" + "=" * 60)
    print("数据获取完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
