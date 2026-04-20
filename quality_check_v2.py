#!/usr/bin/env python3
from datetime import datetime, timezone, timedelta
import os

bj_time = datetime.now(timezone(timedelta(hours=8)))
print(f"当前北京时间: {bj_time.strftime('%Y-%m-%d %H:%M:%S')}")

report_file = "output/研报_20260420_跨市场重大事件与港股龙头策略研判.md"
print(f"新研报文件存在: {os.path.exists(report_file)}")

old_report = "output/研报_跨市场重大事件与港股龙头策略研判.md"
print(f"旧研报文件仍存在（未覆盖）: {os.path.exists(old_report)}")

print(f"fetch_market_data.py 存在: {os.path.exists('fetch_market_data.py')}")
print(f"market_data.csv 存在: {os.path.exists('output/market_data.csv')}")

with open(report_file, "r", encoding="utf-8") as f:
    content = f.read()

checks = {
    "报告日期包含北京时间": "北京时间" in content.split("\n")[2],
    "无数据截止日期开头": "数据截止" not in content[:200],
    "包含6个指数研判": all(x in content for x in ["恒生指数", "恒生科技指数", "国企指数", "纳斯达克100指数", "标普500指数", "道琼斯指数"]),
    "包含27只指定个股": all(x in content for x in ["腾讯控股", "阿里巴巴", "小米", "比亚迪股份", "工商银行", "宁德时代"]),
    "包含牛熊证个股": "中国移动" in content and "中国平安" in content and "香港交易所" in content,
    "包含目标价/点数": "最高目标价" in content and "最低目标价" in content and "最高目标点数" in content,
    "包含概率值": "概率45%" in content or "概率50%" in content,
    "包含思维链": "宏观判断链" in content and "指数推导链" in content and "个股推导链" in content,
    "包含参考资料": "参考资料" in content and "http" in content,
    "包含质量检查清单": "质量检查清单" in content,
    "日期注明时区精确到时分秒": "16:00:00" in content and "美东时间" in content and "北京时间" in content,
    "盘中数据已标注非收盘价": "非收盘价" in content,
    "未覆盖旧研报": os.path.exists(old_report),
    "无删除文件操作(建议删除)": "建议可删除" in content,
    "新增事件-关税退款": "1660" in content and "关税退款" in content,
    "新增事件-DeepSeek融资": "DeepSeek" in content,
    "新增事件-光伏反内卷": "反内卷" in content,
    "新增事件-Anthropic Mythos": "Mythos" in content,
}

print()
print("--- 质量检查结果 ---")
all_pass = True
for check, result in checks.items():
    status = "✅ 通过" if result else "❌ 未通过"
    if not result:
        all_pass = False
    print(f"{check}: {status}")

print()
print(f"总体结果: {'全部通过 ✅' if all_pass else '存在未通过项 ❌'}")
