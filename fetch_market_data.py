#!/usr/bin/env python3
import requests
import csv
import os
from datetime import datetime, timezone, timedelta

INDICES = [
    ("恒生指数", "HSI", "^HSI", "HK"),
    ("恒生科技指数", "HSTECH", "^HSTECH", "HK"),
    ("国企指数", "HSCEI", "^HSCE", "HK"),
    ("纳斯达克100指数", ".NDX", "^NDX", "US"),
    ("标普500指数", ".SPX", "^GSPC", "US"),
    ("道琼斯指数", ".DJI", "^DJI", "US"),
]

STOCKS = [
    ("腾讯控股", "00700.HK", "0700.HK"),
    ("阿里巴巴", "09988.HK", "9988.HK"),
    ("小米", "01810.HK", "1810.HK"),
    ("快手", "01024.HK", "1024.HK"),
    ("京东", "09618.HK", "9618.HK"),
    ("美团", "03690.HK", "3690.HK"),
    ("紫金矿业", "02899.HK", "2899.HK"),
    ("中芯国际", "00981.HK", "0981.HK"),
    ("华虹半导体", "01347.HK", "1347.HK"),
    ("泡泡玛特", "09992.HK", "9992.HK"),
    ("中国神华", "01088.HK", "1088.HK"),
    ("宁德时代", "03750.HK", "3750.HK"),
    ("赣锋锂业", "01772.HK", "1772.HK"),
    ("昆仑能源", "00135.HK", "0135.HK"),
    ("中国石油化工股份", "00386.HK", "0386.HK"),
    ("国泰君安国际", "01788.HK", "1788.HK"),
    ("中国宏桥", "01378.HK", "1378.HK"),
    ("招商银行", "03968.HK", "3968.HK"),
    ("建设银行", "00939.HK", "0939.HK"),
    ("中国银行", "03988.HK", "3988.HK"),
    ("汇丰控股", "00005.HK", "0005.HK"),
    ("信达生物", "01801.HK", "1801.HK"),
    ("药明生物", "02269.HK", "2269.HK"),
    ("中国海洋石油", "00883.HK", "0883.HK"),
    ("中国石油股份", "00857.HK", "0857.HK"),
    ("工商银行", "01398.HK", "1398.HK"),
    ("比亚迪股份", "01211.HK", "1211.HK"),
]

EXTRA_CBBC = [
    ("中国移动", "00941.HK", "0941.HK"),
    ("中国平安", "02318.HK", "2318.HK"),
    ("网易", "09999.HK", "9999.HK"),
    ("百度集团", "09888.HK", "9888.HK"),
    ("理想汽车", "02015.HK", "2015.HK"),
    ("蔚来", "09866.HK", "9866.HK"),
    ("小鹏汽车", "09868.HK", "9868.HK"),
    ("新鸿基地产", "00016.HK", "0016.HK"),
    ("香港交易所", "00388.HK", "0388.HK"),
    ("长和", "00001.HK", "0001.HK"),
    ("携程集团", "09961.HK", "9961.HK"),
    ("京东健康", "06618.HK", "6618.HK"),
    ("海尔智家", "06690.HK", "6690.HK"),
    ("比亚迪电子", "00285.HK", "0285.HK"),
    ("中远海控", "01919.HK", "1919.HK"),
]

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}


def fetch_yahoo(name, code, yahoo_sym, tz_type="HK"):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{yahoo_sym}?interval=1d&range=5d"
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        result = data["chart"]["result"][0]
        quotes = result["indicators"]["quote"][0]
        closes = quotes.get("close", [])
        timestamps = result["timestamp"]
        last_close = None
        last_ts = None
        for i in range(len(closes) - 1, -1, -1):
            if closes[i] is not None:
                last_close = closes[i]
                last_ts = timestamps[i]
                break
        if last_close:
            tz = timezone(timedelta(hours=-4)) if tz_type == "US" else timezone(timedelta(hours=8))
            tz_label = "美东时间" if tz_type == "US" else "北京时间"
            date_str = datetime.fromtimestamp(last_ts, tz).strftime("%Y-%m-%d")
            return [name, code, f"{last_close:.2f}", f"{date_str}（{tz_label}）"], None
        return None, "无收盘价数据"
    except Exception as e:
        return None, str(e)[:80]


def main():
    print(f"执行时间: {datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S')}（北京时间）")
    print("数据源: Yahoo Finance API（Longport API连接超时，使用备选API）")

    all_results = []
    all_errors = []

    for name, code, yahoo_sym, tz_type in INDICES:
        row, err = fetch_yahoo(name, code, yahoo_sym, tz_type)
        if row:
            all_results.append(row + ["上一交易日收盘点数"])
            print(f"  OK {name}: {row[2]} ({row[3]})")
        else:
            all_errors.append([name, code, err])
            print(f"  FAIL {name}: {err}")

    for name, code, yahoo_sym in STOCKS:
        row, err = fetch_yahoo(name, code, yahoo_sym, "HK")
        if row:
            all_results.append(row + ["上一交易日收盘价"])
            print(f"  OK {name}: {row[2]} ({row[3]})")
        else:
            all_errors.append([name, code, err])
            print(f"  FAIL {name}: {err}")

    for name, code, yahoo_sym in EXTRA_CBBC:
        row, err = fetch_yahoo(name, code, yahoo_sym, "HK")
        if row:
            all_results.append(row + ["上一交易日收盘价"])
            print(f"  OK {name}: {row[2]} ({row[3]})")
        else:
            all_errors.append([name, code, err])
            print(f"  FAIL {name}: {err}")

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, "market_data.csv")

    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["标的名称", "代码", "收盘价/点数", "上一交易日日期", "价格类型"])
        for row in all_results:
            writer.writerow(row)
        if all_errors:
            writer.writerow([])
            writer.writerow(["=== 获取失败的标的 ==="])
            writer.writerow(["标的名称", "代码", "失败原因"])
            for row in all_errors:
                writer.writerow(row)

    print(f"\nOK: {len(all_results)}, FAIL: {len(all_errors)}")
    print(f"Saved: {filepath}")


if __name__ == "__main__":
    main()
